from flask import Flask, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai
import requests
import uuid
from datetime import datetime
from database_config import DatabaseOperations, create_tables, get_db
from functools import wraps

load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Configure Google Gemini API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-pro')

# Initialize database
create_tables()
db_ops = DatabaseOperations()

# Google OAuth configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI = 'http://127.0.0.1:5000/auth/google/callback'

# Authentication decorator
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Authentication Routes
@app.route('/auth/google', methods=['GET'])
def google_auth():
    """Initiate Google OAuth flow"""
    auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20email%20profile&response_type=code"
    return redirect(auth_url)

@app.route('/auth/google/callback', methods=['GET'])
def google_callback():
    """Handle Google OAuth callback"""
    code = request.args.get('code')
    if not code:
        return jsonify({'error': 'Authorization code not provided'}), 400
    
    token_url = 'https://oauth2.googleapis.com/token'
    token_data = {
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': GOOGLE_REDIRECT_URI
    }
    
    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()
    
    if 'access_token' not in token_json:
        return jsonify({'error': 'Failed to get access token'}), 400
    
    
    user_info_url = f"https://www.googleapis.com/oauth2/v2/userinfo?access_token={token_json['access_token']}"
    user_response = requests.get(user_info_url)
    user_info = user_response.json()
    
    user = db_ops.get_user_by_google_id(user_info['id'])
    if not user:
        user = db_ops.create_user(
            google_id=user_info['id'],
            email=user_info['email'],
            name=user_info['name'],
            picture_url=user_info.get('picture')
        )
    
    # Store user in session
    session['user_id'] = user.id
    session['user_email'] = user.email
    session['user_name'] = user.name
    session['user_picture'] = user.picture_url
    
    # Redirect back to frontend
    return redirect('http://127.0.0.1:5500/index.html')  # Adjust port as needed

@app.route('/auth/status', methods=['GET'])
def auth_status():
    """Check authentication status"""
    if 'user_id' in session:
        return jsonify({
            'authenticated': True,
            'user': {
                'id': session['user_id'],
                'email': session['user_email'],
                'name': session['user_name'],
                'picture': session['user_picture']
            }
        })
    return jsonify({'authenticated': False}), 401

@app.route('/auth/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({'message': 'Logged out successfully'})

# Main Application Routes
@app.route('/generate-story', methods=['POST'])
@require_auth
def generate_story():
    try:
        data = request.get_json()
        user_input = data.get('user_input', '').strip()
        chat_id = data.get('chat_id')
        
        if not user_input:
            return jsonify({'error': 'No input provided'}), 400
        
        if not chat_id:
            chat = db_ops.create_chat(session['user_id'], title=user_input[:50] + "..." if len(user_input) > 50 else user_input)
            chat_id = chat.id
        else:
            chat = db_ops.get_chat_by_id(chat_id)
            if not chat or chat.user_id != session['user_id']:
                return jsonify({'error': 'Chat not found'}), 404
        
        # Save user message
        db_ops.add_message(chat_id, 'user', user_input)
        
        # Create a therapeutic fantasy prompt
        prompt = f"""
        You are a therapeutic AI that creates personalized fantasy narratives to help users process their emotions. 
        The user has shared: "{user_input}"
        
        Create a therapeutic fantasy story that:
        1. Acknowledges their emotion/input
        2. Transforms it into a metaphorical fantasy adventure
        3. Provides gentle guidance and hope
        4. Includes a real-world actionable step if appropriate
        5. Uses rich, immersive fantasy language
        6. Is 2-4 paragraphs long but meaningful
        7. Where user can be main character or part of story but not narrator
        8. Give user some options to choose from to continue the story
        
        
        Make it feel personal, magical, and therapeutic. Use fantasy elements like magical creatures, enchanted places, or quests that metaphorically represent their emotional journey.
        """

        response = model.generate_content(prompt)
        story = response.text.strip()
        
        # Save assistant message
        db_ops.add_message(chat_id, 'assistant', story)
        
        return jsonify({
            'story': story,
            'chat_id': chat_id
        })
        
    except Exception as e:
        print(f"Error generating story: {str(e)}")
        return jsonify({'error': 'Failed to generate story. Please try again.'}), 500

# Additional Routes
@app.route('/chats', methods=['GET'])
@require_auth
def get_chats():
    """Get user's chat history"""
    try:
        chats = db_ops.get_user_chats(session['user_id'])
        return jsonify([{
            'id': chat.id,
            'title': chat.title,
            'created_at': chat.created_at.isoformat(),
            'updated_at': chat.updated_at.isoformat()
        } for chat in chats])
    except Exception as e:
        return jsonify({'error': 'Failed to fetch chats'}), 500

@app.route('/chats/<int:chat_id>/messages', methods=['GET'])
@require_auth
def get_chat_messages(chat_id):
    """Get messages for a specific chat"""
    try:
        # Verify chat belongs to user
        chat = db_ops.get_chat_by_id(chat_id)
        if not chat or chat.user_id != session['user_id']:
            return jsonify({'error': 'Chat not found'}), 404
        
        messages = db_ops.get_chat_messages(chat_id)
        return jsonify([{
            'id': msg.id,
            'role': msg.role,
            'content': msg.content,
            'created_at': msg.created_at.isoformat()
        } for msg in messages])
    except Exception as e:
        return jsonify({'error': 'Failed to fetch messages'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'MindWeaver Saga API is running'})

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'MindWeaver Saga API',
        'endpoints': {
            'POST /generate-story': 'Generate therapeutic fantasy stories',
            'GET /auth/google': 'Google OAuth login',
            'GET /auth/status': 'Check authentication status',
            'POST /auth/logout': 'Logout user',
            'GET /chats': 'Get user chats',
            'GET /chats/<id>/messages': 'Get chat messages',
            'GET /health': 'Health check'
        }
    })

if __name__ == '__main__':
    required_vars = ['GOOGLE_API_KEY', 'GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET', 'DATABASE_URL']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        print(f"Warning: Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these in your .env file or environment variables.")
    app.run(debug=True, host='127.0.0.1', port=5000)
