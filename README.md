# Audio to Text App

This project converts audio files into text using a frontend interface and a backend transcription service. The frontend is built with Vue.js, and the backend processes audio files for speech-to-text conversion.

## Prerequisites

### Docker Environment
- **Docker**
- **Docker Compose**

### Local Development
**Frontend:**
- **Node.js** (LTS version recommended)
- **Vite** (for Vue.js project setup)

**Backend:**
- **Python 3.8+**
- **pip**

## Installation

### Using Docker (Recommended)

1. Build and start containers:

    ```bash
    docker-compose up --build
    ```

2. Access the application:

    ```bash
    http://localhost:5173
    ```

### Local Development

#### Frontend Setup

1. Navigate to the frontend directory and install dependencies:

    ```bash
    cd frontend
    npm install
    ```

2. Start the Vue.js development server:

    ```bash
    npm run dev
    ```

3. Access the application at:

    ```bash
    http://localhost:5173
    ```

#### Backend Setup

1. Navigate to the backend directory and set up a virtual environment:

    ```bash
    cd backend
    python -m venv venv
    ```

2. For **Linux/Mac**, activate the virtual environment:

    ```bash
    source venv/bin/activate
    ```

   For **Windows**, use:

    ```bash
    .\venv\Scripts\activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Start the backend server:

    ```bash
    python app.py
    ```

   Or if using Flask:

    ```bash
    flask run
    ```
