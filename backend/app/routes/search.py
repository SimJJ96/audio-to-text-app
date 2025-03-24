from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import SessionLocal, get_db
from app.models import Transcription
from typing import List
import logging

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/transcriptions")
def get_all_transcriptions(db: Session = Depends(get_db)) -> List[dict]:

    try:
        logger.info("Fetching all transcriptions")
        transcriptions = db.query(Transcription).order_by(desc(Transcription.created_at)).all()
        logger.info(f"Found {len(transcriptions)} transcriptions")
        return [
            {
                "id": t.id,
                "file_name": t.file_name,
                "text": t.text,
                "created_at": t.created_at.strftime("%Y-%m-%d %H:%M:%S") 
            }
            for t in transcriptions
        ]
    except Exception as e:
        logger.error(f"Error fetching transcriptions: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while fetching transcriptions")


@router.get("/search")
def search_transcription(
    file_name: str = Query(..., description="Search for transcriptions by file name (supports partial matching)"), 
    db: Session = Depends(get_db)
    ):

    try:
        logger.info(f"Searching for transcriptions with file name containing: {file_name}")
        transcriptions = db.query(Transcription).filter(Transcription.file_name.ilike(f"%{file_name}%")).order_by(desc(Transcription.created_at)).all()
        
        if not transcriptions:
            logger.warning(f"No transcriptions found matching: {file_name}")
            return {"message": "No transcriptions found matching the criteria"}
        
        logger.info(f"Found {len(transcriptions)} matching transcriptions")

        return [
            {
                "id": t.id,
                "file_name": t.file_name,
                "text": t.text,
                "created_at": t.created_at.strftime("%Y-%m-%d %H:%M:%S") 
            }
            for t in transcriptions
        ]
    except Exception as e:
        logger.error(f"Error searching transcriptions: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while searching transcriptions")