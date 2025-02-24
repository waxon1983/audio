from fastapi import FastAPI, UploadFile, File
from pydub import AudioSegment
import io

app = FastAPI()

@app.post("/get-duration")
async def get_audio_duration(file: UploadFile = File(...)):
    try:
        # Read file into memory
        content = await file.read()
        audio = AudioSegment.from_file(io.BytesIO(content))

        # Get duration in seconds
        duration = len(audio) / 1000  # Convert ms to sec

        return {"filename": file.filename, "duration_seconds": duration}
    
    except Exception as e:
        return {"error": str(e)}

