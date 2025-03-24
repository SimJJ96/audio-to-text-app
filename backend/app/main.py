from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
from contextlib import asynccontextmanager
from app.routes import transcribe, search
from app.database import create_tables, SessionLocal
from sqlalchemy import text
from logging.handlers import RotatingFileHandler
import logging
import os


# Create a logs directory if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log format
    handlers=[
        RotatingFileHandler(
            os.path.join(LOG_DIR, "app.log"),  # Log file path
            maxBytes=1024 * 1024,  # 1 MB per log file
            backupCount=5,  # Keep up to 5 backup log files
        ),
        logging.StreamHandler(),  # Also log to the console
    ]
)

logger = logging.getLogger(__name__)

# Define lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()  # Ensure tables exist on startup
    yield  # Continue app execution

app = FastAPI(lifespan=lifespan)
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from your frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(transcribe.router)
app.include_router(search.router)

@app.get("/health")
def health_check():
    try:
        logger.info("Health check endpoint called")

        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        logger.info("Database connection check passed")

        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}", exc_info=True)
        return {"status": "error", "detail": str(e)}