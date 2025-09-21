# MindWeaver Setup Guide

This guide will help you set up MindWeaver with Google authentication and database integration.

## Prerequisites

1. **Python 3.8+** installed
2. **PostgreSQL** installed and running
3. **Google Cloud Console** account for OAuth setup

## Step 1: Database Setup

### Install PostgreSQL
- **Windows**: Download from [postgresql.org](https://www.postgresql.org/download/windows/)
- **macOS**: `brew install postgresql`
- **Linux**: `sudo apt-get install postgresql postgresql-contrib`

### Create Database
1. Start PostgreSQL service
2. Open psql or pgAdmin
3. Create a database named `mindweaver`:
   ```sql
   CREATE DATABASE mindweaver;
   ```

## Step 2: Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
5. Set application type to "Web application"
6. Add authorized redirect URIs:
   - `http://127.0.0.1:5000/auth/google/callback`
7. Copy the Client ID and Client Secret

## Step 3: Environment Configuration

Create a `.env` file in the project root:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_NAME=mindweaver
DATABASE_URL=postgresql://postgres:your_postgres_password@localhost:5432/mindweaver

# Google API Configuration
GOOGLE_API_KEY=your_google_gemini_api_key
GOOGLE_CLIENT_ID=your_google_oauth_client_id
GOOGLE_CLIENT_SECRET=your_google_oauth_client_secret

# Flask Configuration
SECRET_KEY=your_secret_key_here
```

## Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 5: Initialize Database

```bash
python setup_database.py
```

## Step 6: Run the Application

```bash
python app.py
```

The application will be available at:
- Frontend: `http://127.0.0.1:5500` (or your Live Server port)
- Backend: `http://127.0.0.1:5000`

## Features Added

### ✅ New Chat Button
- Added a "New Chat" button in the left sidebar
- Clears current conversation and starts fresh
- Preserves user authentication

### ✅ Google Sign-In
- Google OAuth integration
- User profile display with avatar
- Session management
- Secure authentication flow

### ✅ Database Integration
- User accounts storage
- Chat history persistence
- Message storage
- User-specific data isolation

### ✅ Enhanced UI
- Profile picture display
- Sign-in/Sign-out functionality
- Improved header layout
- Responsive design

## API Endpoints

- `GET /auth/google` - Initiate Google OAuth
- `GET /auth/status` - Check authentication status
- `POST /auth/logout` - Logout user
- `POST /generate-story` - Generate story (requires auth)
- `GET /chats` - Get user's chat history
- `GET /chats/<id>/messages` - Get chat messages

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Verify database exists

### Google OAuth Issues
- Check Client ID and Secret
- Verify redirect URI matches exactly
- Ensure Google+ API is enabled

### Frontend Issues
- Check CORS settings
- Verify API endpoints are accessible
- Check browser console for errors

## Security Notes

- Never commit `.env` file to version control
- Use strong secret keys
- Keep OAuth credentials secure
- Regularly update dependencies

## Support

If you encounter issues:
1. Check the console logs
2. Verify all environment variables
3. Ensure all services are running
4. Check database connectivity
