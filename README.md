# Youtube_Transcript_Summarizer
AI-powered YouTube video summarizer using Gemini and Streamlit


 YouTube Transcript Summarizer
An AI-powered web app that extracts transcripts from any YouTube video and generates concise, point-wise summaries using Google Gemini 2.5 Flash.

✨ Features
🔗 Supports multiple YouTube URL formats (youtube.com/watch?v=, youtu.be/, /shorts/)
📝 Extracts transcript using youtube-transcript-api v1.x
🌐 Auto-fallback to any available language if English transcript is unavailable
🤖 Summarizes transcript into key points using Google Gemini 2.5 Flash
🖼️ Displays video thumbnail preview before generating summary
⚡ Clean, interactive UI built with Streamlit

Tech Stack

LayerTechnology
FrontendStreamlitAI 
ModelGoogle Gemini 2.5 Flash (google-genai)
Transcript APIyoutube-transcript-api v1.2.4
LanguagePython 3.10+
Configpython-dotenv

YTTranscriber/
│
├── app.py               # Main Streamlit application
├── .env                 # API keys (not committed to Git)
├── requirements.txt     # Python dependencies
└── README.md     

How It Works

YouTube URL
    │
    ▼
Extract Video ID
    │
    ▼
Fetch Transcript (youtube-transcript-api)
    │
    ▼
Send to Google Gemini 2.5 Flash
    │
    ▼
Display Point-wise Summary


User pastes a YouTube video URL
App extracts the video ID and fetches the transcript
Transcript is sent to Gemini with a summarization prompt
Summary is displayed as structured bullet points


