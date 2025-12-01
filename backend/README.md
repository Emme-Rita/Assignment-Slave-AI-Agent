# Assignment Helper Backend

AI-powered assignment helper API built with FastAPI, Google Gemini, and Tavily Search.

## Features

- 📄 **Assignment Processing**: Upload assignments (PDF, Word, Images) with text or voice instructions
- 🤖 **AI-Powered Analysis**: Uses Google Gemini 1.5 Pro for intelligent assignment help
- 🔍 **Web Research**: Integrated Tavily search for comprehensive research capabilities
- 🔒 **Secure File Handling**: Validates file types and sizes for security
- 📧 **Future Features**: Email and WhatsApp integration (coming soon)

## Setup

### Prerequisites

- Python 3.8+
- Google Gemini API Key
- Tavily API Key

### Installation

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
Edit `.env` file and add your API keys:
```
GEMINI_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### Running the Server

```bash
cd app
python main.py
```

Or using uvicorn directly:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Assignment Analysis

**POST** `/api/v1/assignment/analyze`
- Upload assignment file (PDF, Word, Image)
- Provide text instructions
- Optional: Enable web research

**POST** `/api/v1/assignment/analyze-with-voice`
- Upload assignment file
- Upload voice note (future: will be transcribed)
- Optional: Enable web research

### Research

**POST** `/api/v1/research/research`
- Perform web research on a topic
- Returns sources and summary

**GET** `/api/v1/research/research/{query}`
- Quick research via GET request

## Project Structure

```
backend/
├── app/
│   ├── core/
│   │   ├── config.py          # Configuration
│   │   └── security.py        # CORS setup
│   ├── services/
│   │   ├── ai_service.py      # Gemini integration
│   │   ├── search_service.py  # Tavily integration
│   │   ├── file_service.py    # File validation
│   │   ├── email_service.py   # Email (placeholder)
│   │   └── whatsapp_service.py # WhatsApp (placeholder)
│   ├── api/
│   │   ├── v1/
│   │   │   └── endpoints/
│   │   │       ├── assignment.py
│   │   │       └── research.py
│   │   └── api.py
│   └── main.py
├── requirements.txt
└── .env
```

## Security Features

- File type validation
- File size limits (10MB max)
- CORS configuration
- Secure API key handling via environment variables

## Future Enhancements

- [x] Voice transcription integration (Implemented with Gemini Flash)
- [x] Email service endpoints (Simulated)
- [x] WhatsApp messaging endpoints (Simulated)
- [ ] User authentication
- [ ] Rate limiting
- [ ] Database integration for history
- [ ] Batch processing

## Deployment on Render (Web Service)

1.  Push your code to GitHub.
2.  Log in to [Render](https://render.com/).
3.  Click **New +** and select **Web Service**.
4.  Connect your GitHub repository (`Assignment-Slave-AI-Agent`).
5.  Configure the service:
    *   **Name**: `assignment-helper-backend` (or any name you prefer)
    *   **Runtime**: `Python 3`
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
    *   **Root Directory**: `backend`
6.  **Environment Variables**:
    *   Scroll down to "Environment Variables" and add:
        *   `GEMINI_API_KEY`: Your actual Gemini API key
        *   `TAVILY_API_KEY`: Your actual Tavily API key
        *   `PYTHON_VERSION`: `3.11.0` (Recommended)
7.  Click **Create Web Service**.

## License

MIT
