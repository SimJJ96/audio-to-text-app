# Audio-to-Text Backend

This is a FastAPI-based backend for handling audio file uploads, processing transcriptions, and storing them in a database.

## Installation

1. Clone the repository:
   ```sh
   git clone <repo_url>
   cd audio-to-text-app/backend
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\\Scripts\\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Running the Application

1. Set up the environment variables:
   ```sh
   export UPLOAD_DIR="./data/uploads"
   export DATABASE_URL="sqlite:///./test.db"  # Change as needed
   ```
2. Start the FastAPI server:
   ```sh
   uvicorn app.main:app --reload
   ```

## API Endpoints

### Upload and Transcribe Audio Files
#### `POST /transcribe`
Uploads audio files and transcribes them using the Whisper model.

**Request:**
- `files`: List of audio files (supports `.wav`, `.mp3`, `.mp4`, `.m4a`, `.webm`)

**Example (cURL):**
```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/transcribe' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'files=@sample.mp3'
```

**Response:**
```json
{
  "message": "Files uploaded and transcribed successfully",
  "transcriptions": [
    {
      "id": 1,
      "file_name": "sample_20240321010101.mp3",
      "text": "Transcribed text here",
      "created_at": "2024-03-21 01:01:01"
    }
  ]
}
```

### Retrieve All Transcriptions
#### `GET /transcriptions`
Fetches all transcriptions stored in the database.

**Example:**
```sh
curl -X 'GET' 'http://127.0.0.1:8000/transcriptions' -H 'accept: application/json'
```

**Response:**
```json
[
  {
    "id": 1,
    "file_name": "sample_20240321010101.mp3",
    "text": "Transcribed text here",
    "created_at": "2024-03-21 01:01:01"
  }
]
```

### Search Transcriptions
#### `GET /search`
Searches for transcriptions by filename.

**Request:**
- `file_name`: Filename to search for (query parameter)

**Example:**
```sh
curl -X 'GET' 'http://127.0.0.1:8000/search?file_name=sample.mp3' -H 'accept: application/json'
```

**Response (if found):**
```json
{
  "transcriptions": [
    {
      "id": 1,
      "file_name": "sample_20240321010101.mp3",
      "text": "Transcribed text here",
      "created_at": "2024-03-21 01:01:01"
    }
  ]
}
```

**Response (if not found):**
```json
{
  "message": "No transcriptions found matching the criteria"
}
```

## Running Tests

1. Install test dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run tests using `pytest`:
   ```sh
   pytest
   ```

## Logging
Logs are stored and displayed for debugging. Important logs include file upload success, validation errors, transcription process logs, and error handling logs.

## Notes
- The app will automatically create the `transcriptions` table if it doesn’t exist.
- Uploaded files are stored in the directory specified by `UPLOAD_DIR`.
- Ensure `UPLOAD_DIR` exists and is writable.
