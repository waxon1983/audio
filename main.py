from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse
from pydub import AudioSegment
import io
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Starting FastAPI app...")

app = FastAPI()

# Middleware to limit upload size (5MB = 5,000,000 bytes)
@app.middleware("http")
async def limit_request_size(request: Request, call_next):
    if request.method == "POST" and request.url.path == "/get-duration":
        body = await request.body()
        if len(body) > 5_000_000:
            logger.warning("File too large — rejecting request.")
            return JSONResponse(
                content={"error": "File too large. Max size is 5MB."},
                status_code=413,
            )
        request._body = body  # store it so FastAPI can read it again
    return await call_next(request)

# Health check route
@app.api_route("/", methods=["GET", "HEAD"])
async def root():
    logger.info("Health check ping received")
    return {"status": "ok"}

# Additional ping route for monitoring
@app.get("/ping")
async def ping():
    logger.info("Ping check received")
    return {"status": "pong"}

# Main file processing route
@app.post("/get-duration")
async def get_audio_duration(file: UploadFile = File(...)):
    try:
        logger.info(f"Received file: {file.filename}")

        content = await file.read()
        logger.info(f"File size: {len(content)} bytes")

        audio = AudioSegment.from_file(io.BytesIO(content))
        duration = len(audio) / 1000  # ms to seconds

        logger.info(f"Duration: {duration:.2f} seconds")

        return {"filename": file.filename, "duration_seconds": duration}
    
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        return {"error": str(e)}
