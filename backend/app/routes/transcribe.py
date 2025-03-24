from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from datetime import datetime
from app.database import SessionLocal, get_db
from app.models import Transcription
from sqlalchemy.orm import Session
from app.whisper_service import transcribe
from typing import List
import shutil
import os
import logging

router = APIRouter()

logger = logging.getLogger(__name__)

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "../data/uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
logger.info(f"Using upload directory: {UPLOAD_DIR}")

SUPPORTED_EXTENSIONS = {".wav", ".mp3", ".mp4", ".m4a", ".webm"}

def validate_file_extension(filename: str):
    """
    Validates that the file has a supported extension.
    """
    _, ext = os.path.splitext(filename)
    if ext.lower() not in SUPPORTED_EXTENSIONS:
        logger.warning(f"Unsupported file type: {filename}")
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Supported types are: {', '.join(SUPPORTED_EXTENSIONS)}"
        )


def generate_unique_filename(filename: str, db: Session) -> str:
    """
    Generates a unique filename by appending a timestamp and ensuring it doesn't exist in the database.
    """
    name, ext = os.path.splitext(filename)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_filename = f"{name}_{timestamp}{ext}"
    
    while db.query(Transcription).filter(Transcription.file_name == unique_filename).first():
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_filename = f"{name}_{timestamp}{ext}"
    
    logger.info(f"Generated unique filename: {unique_filename}")
    return unique_filename

@router.post("/transcribe")
async def transcribe_audio(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    transcriptions = [] 

    try:
        for file in files:
            validate_file_extension(file.filename)
            logger.info(f"File validation successful: {file.filename}")

            filename = generate_unique_filename(file.filename, db)
            file_path = os.path.join(UPLOAD_DIR, filename)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)


            transcription_text = transcribe(file_path)
            logger.info(f"Transcription completed for file: {filename}")
            created_time = datetime.now()

            # Save the transcription to the database
            transcription = Transcription(
                file_name=filename,
                text=transcription_text,
                created_at=created_time
            )
            db.add(transcription)
            db.commit()
            db.refresh(transcription)

            logger.info(f"Transcription saved to database: {filename}")

            # Add the transcription to the response
            transcriptions.append({
                "id": transcription.id,
                "file_name": filename,
                "text": transcription_text,
                "created_at": created_time.strftime("%Y-%m-%d %H:%M:%S") 
            })

        return {
            "message": "Files uploaded and transcribed successfully",
            "transcriptions": transcriptions
        }

    except HTTPException:
        logger.error(f"HTTPException: {e.detail}")
        raise

    except Exception as e:
        db.rollback()
        logger.error(f"An error occurred: {str(e)}", exc_info=True)

        for file_info in transcriptions:
            file_path = os.path.join(UPLOAD_DIR, file_info["file_name"])
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Deleted file due to error: {file_path}")
        
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    finally:
        file.file.close()
        logger.info("File handle closed")