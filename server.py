import os
import sys
import logging
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import audio_flamingo_runner as runner

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Audio Flamingo API", version="1.0.0")

# Global model bundle
MODEL_BUNDLE = None
MODEL_DIR = os.getenv("MODEL_DIR", "{{MODEL_DIR}}")


class TranscribeRequest(BaseModel):
    paths: list[str]
    prompt: Optional[str] = None
    max_new_tokens: int = 128


class EvaluateRequest(BaseModel):
    audio_dir: str
    gt_dir: str
    prompt: Optional[str] = None
    max_new_tokens: int = 128
    match_mode: str = "exact"


@app.on_event("startup")
async def startup_event():
    """Load model on startup."""
    global MODEL_BUNDLE
    try:
        logger.info(f"Loading model from {MODEL_DIR}...")
        MODEL_BUNDLE = runner.load_model(model_dir=MODEL_DIR)
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise


@app.get("/healthz")
async def health_check():
    """Health check endpoint."""
    if MODEL_BUNDLE is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "status": "ok",
        "device": MODEL_BUNDLE["device"],
        "model": "nvidia/audio-flamingo-3"
    }


@app.post("/transcribe")
async def transcribe(request: TranscribeRequest):
    """Transcribe audio files."""
    if MODEL_BUNDLE is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Validate paths exist
    for path in request.paths:
        if not Path(path).exists():
            raise HTTPException(
                status_code=400,
                detail=f"File not found: {path}"
            )
    
    try:
        logger.info(f"Processing {len(request.paths)} file(s)")
        start_time = __import__('time').time()
        
        if len(request.paths) == 1:
            # Single file
            result = runner.transcribe_file(
                request.paths[0],
                MODEL_BUNDLE,
                request.prompt,
                request.max_new_tokens
            )
            results = [result]
        else:
            # Multiple files
            results = runner.transcribe_files(
                request.paths,
                MODEL_BUNDLE,
                request.prompt,
                request.max_new_tokens
            )
        
        elapsed = __import__('time').time() - start_time
        logger.info(f"Processed {len(results)} file(s) in {elapsed:.2f}s")
        
        return {"results": results}
    
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/evaluate")
async def evaluate(request: EvaluateRequest):
    """Evaluate model on a folder of audio files."""
    if MODEL_BUNDLE is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Validate directories exist
    if not Path(request.audio_dir).exists():
        raise HTTPException(
            status_code=400,
            detail=f"Audio directory not found: {request.audio_dir}"
        )
    if not Path(request.gt_dir).exists():
        raise HTTPException(
            status_code=400,
            detail=f"Ground truth directory not found: {request.gt_dir}"
        )
    
    try:
        logger.info(f"Evaluating folder: {request.audio_dir}")
        start_time = __import__('time').time()
        
        result = runner.evaluate_folder(
            request.audio_dir,
            request.gt_dir,
            MODEL_BUNDLE,
            request.prompt,
            request.max_new_tokens,
            request.match_mode
        )
        
        elapsed = __import__('time').time() - start_time
        logger.info(f"Evaluation completed in {elapsed:.2f}s")
        logger.info(f"Results: {result['summary']}")
        
        return result
    
    except Exception as e:
        logger.error(f"Evaluation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def main():
    """Run the server."""
    import argparse
    parser = argparse.ArgumentParser(description="Audio Flamingo REST API Server")
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host to bind to"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind to"
    )
    parser.add_argument(
        "--model-dir",
        type=str,
        default=MODEL_DIR,
        help="Path to model directory"
    )
    
    args = parser.parse_args()
    
    # Set model directory
    global MODEL_DIR
    MODEL_DIR = args.model_dir
    
    logger.info(f"Starting server on {args.host}:{args.port}")
    logger.info(f"Model directory: {MODEL_DIR}")
    
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        log_level="info"
    )


if __name__ == "__main__":
    main()
