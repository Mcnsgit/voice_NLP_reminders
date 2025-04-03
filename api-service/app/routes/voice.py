from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.voice_processor_file import process_voice

router = APIRouter(prefix="/voice", tags=["voice"])

@router.post("/process")
async def process_voice_command(file: UploadFile) -> dict:
    """
    Process a voice command file and extract task information.
    This is a wrapper around the process_voice function.
    """
    return await process_voice(file)