import os 
import tempfile
import speech_recognition as sr
from fastapi import UploadFile
from app.services.nlp_service import extract_task_details

async def process_voice(file: UploadFile) -> dict:
    """Process a bvoice recording to extract text and task information.
    """
    #save uploaded file to a temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        contents = await file.read()
        temp_file.write(contents)
        temp_path = temp_file.name
        
    try:
        #use speech recognitio to convert audio to text 
        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            
        #extract task details using nlp
        task_details = extract_task_details(text)
        
        return {
            "success": True,
            "text": text,
            "task": task_details
        }
    except sr.UnknownValueError:
        return {
            "success": False,
            "error": "Could not understand audio"
        }
    except sr.RequestError as e:
        return {
            "success": False,
            "error": f"Speech recognition service error: {e}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error processing voice: {str(e)}"
        }
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_path):
            os.unlink(temp_path)
