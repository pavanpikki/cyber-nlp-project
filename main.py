from fastapi import FastAPI, Request
import analysis
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Cyber Threat Intelligence API",
    description="An API for extracting CTI from text using NLP.",
    version="0.1.0",
)

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup complete.")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Request received: {request.method} {request.url.path}")
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000  # in milliseconds
    logger.info(
        f"Response sent: {response.status_code} | Processing time: {process_time:.2f}ms"
    )
    return response

@app.get("/")
def read_root():
    return {"message": "Cyber Threat Intelligence API is running"}

app.include_router(analysis.router, prefix="/api/v1", tags=["analysis"])
