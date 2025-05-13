from fastapi import FastAPI, UploadFile, File
from pydub import AudioSegment
import io
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Starting FastAPI app...")

app = FastAPI()

# Health check route for UptimeRobot / Render
@app.api_route("/", methods=["GET", "HEAD"])
async def root():
    logger.info("Health check received")
    return {"status": "ok"}

# Additional ping route (optional separate UptimeRobot monitor)
@app.get("/ping")
async def ping():
    logger.info("Ping received")
    return {"status": "pong"}

# Main API route
@app.post("/get-duration")
async def get_audio_duration(file: UploadFile = File(...)):
    try:
        logger.info(f"Received file: {file.filename}")

        # Read file content
        content = await file.read()
        audio = AudioSegment.from_file(io.BytesIO(content))

        duration = len(audio) / 1000  # ms → seconds
        logger.info(f"Duration: {duration}s")

        return {"filename": file.filename, "duration_seconds": duration}
    
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"error": str(e)}
