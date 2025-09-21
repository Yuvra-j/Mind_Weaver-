MindWeaver Saga - AI Therapeutic Fantasy:
Uses AI to generate therapeutic fantasy narratives based on user emotions.

Features:
- Dynamic Narrative Generation**: Enter emotions to get personalized fantasy stories.
- User-Driven Interaction: Continue stories with your choices.
- Metaphorical Quest Translation: Real-world tasks embedded in fantasy narratives.
- Dark Fantasy Theme: Beautiful UI with Tailwind CSS.

Setup:
 Backend Setup-
1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Get a Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

3. Create a `.env` file in the project root:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

4. Run the Flask backend:
```bash
python app.py
```

The backend will run on `http://127.0.0.1:5000`

 Frontend Setup-
1. Open `index.html` in your web browser.
2. The frontend will automatically connect to the backend.


Usage:
1. Open the web application.
2. Enter your emotions or story choices in the textarea.
3. Click "Ask" to generate a therapeutic fantasy story.
4. Continue the conversation by entering new choices or emotions.

API Endpoints:
- `POST /generate-story` - Generate therapeutic fantasy stories
- `GET /health` - Health check
- `GET /` - API information

Project Structure:
```
MindWeaver/
├── app.py              # Flask backend
├── index.html          # Main frontend
├── script.js           # Frontend JavaScript
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

Tech:
- Frontend: HTML5, Tailwind CSS, Vanilla JavaScript.
- Backend: Flask, Google Gemini AI.

