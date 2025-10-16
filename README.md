# Audio Flamingo Offline Runner

Complete offline solution for running nvidia/audio-flamingo-3 locally with Python API, REST server, CLI, and evaluation capabilities.

## Prerequisites

- Python 3.8+
- PyTorch with CUDA (recommended) or CPU
- Model files downloaded locally via `snapshot_download`

## Installation

```bash
pip install torch torchaudio transformers fastapi uvicorn pydantic
```

## Environment Setup

Set the model directory path:

```bash
export MODEL_DIR=/path/to/your/audio-flamingo-3-model
```

Or use the default `{{MODEL_DIR}}` in the code and replace it with your actual path.

## Usage

### 1. Python API (Local Function Calls)

```python
import audio_flamingo_runner as runner

# Load model once
model_bundle = runner.load_model(model_dir="/path/to/model")

# Transcribe single file
result = runner.transcribe_file(
    path="/data/audio.wav",
    model_bundle=model_bundle,
    prompt=None,
    max_new_tokens=128
)
print(result)
# Output: {"file": "...", "text": "...", "tokens_generated": 45, "elapsed_sec": 0.57}

# Transcribe multiple files
results = runner.transcribe_files(
    paths=["/data/audio1.wav", "/data/audio2.mp3"],
    model_bundle=model_bundle,
    max_new_tokens=128
)

# Evaluate on folder
eval_results = runner.evaluate_folder(
    audio_dir="/data/audio",
    gt_dir="/data/labels",
    model_bundle=model_bundle,
    match_mode="exact"
)
print(eval_results["summary"])
# Output: {"count": 10, "tp": 8, "fp": 2, "fn": 2, "precision": 0.8, "recall": 0.8, "f1": 0.8}
```

### 2. REST API Server

Start the server:

```bash
# Using default settings (127.0.0.1:8000)
python server.py

# With custom settings
python server.py --host 127.0.0.1 --port 8000 --model-dir /path/to/model
```

#### Health Check

```bash
curl http://127.0.0.1:8000/healthz
```

Response:
```json
{
  "status": "ok",
  "device": "cuda",
  "model": "nvidia/audio-flamingo-3"
}
```

#### Transcribe Single File

```bash
curl -X POST http://127.0.0.1:8000/transcribe \
  -H "Content-Type: application/json" \
  -d '{
    "paths": ["/absolute/path/to/audio.wav"],
    "prompt": null,
    "max_new_tokens": 128
  }'
```

#### Transcribe Multiple Files

```bash
curl -X POST http://127.0.0.1:8000/transcribe \
  -H "Content-Type: application/json" \
  -d '{
    "paths": [
      "/absolute/path/to/audio1.wav",
      "/absolute/path/to/audio2.mp3"
    ],
    "max_new_tokens": 128
  }'
```

Response:
```json
{
  "results": [
    {
      "file": "/absolute/path/to/audio1.wav",
      "text": "transcribed text here",
      "tokens_generated": 45,
      "elapsed_sec": 0.57
    }
  ]
}
```

#### Evaluate Folder

```bash
curl -X POST http://127.0.0.1:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "audio_dir": "/absolute/path/to/audio",
    "gt_dir": "/absolute/path/to/labels",
    "max_new_tokens": 128,
    "match_mode": "exact"
  }'
```

Response:
```json
{
  "summary": {
    "count": 10,
    "tp": 8,
    "fp": 2,
    "fn": 2,
    "precision": 0.8,
    "recall": 0.8,
    "f1": 0.8
  },
  "details": [
    {
      "file": "sample001.wav",
      "pred": "hello world",
      "gt": "hello world",
      "match": 1
    }
  ]
}
```

### 3. CLI Interface

#### Transcribe Single File

```bash
python cli.py transcribe \
  --path /data/audio.wav \
  --prompt "Transcribe this audio:" \
  --max-new-tokens 128 \
  --output results.json
```

#### Transcribe Multiple Files

```bash
python cli.py transcribe \
  --paths /data/audio1.wav /data/audio2.mp3 /data/audio3.flac \
  --max-new-tokens 128
```

Output written to `transcribe_results.json` by default.

#### Evaluate Folder

```bash
python cli.py evaluate \
  --audio-dir /data/audio \
  --gt-dir /data/labels \
  --max-new-tokens 128 \
  --match-mode exact \
  --output eval_results.json
```

Output written to `evaluation_results.json` by default.

#### With Custom Model Directory

```bash
python cli.py --model-dir /custom/path/to/model transcribe --path /data/audio.wav
```

## Evaluation Mode

### Folder Structure

```
audio/
  ├── sample001.wav
  ├── clip02.mp3
  └── test_03.flac

labels/
  ├── sample001.txt
  ├── clip02.txt
  └── test_03.txt
```

### Ground Truth Files

Each `.txt` file should contain the expected transcription (can be single or multi-line).

### Normalization

Both predictions and ground truth are normalized before comparison:
- Convert to lowercase
- Strip leading/trailing whitespace
- Collapse multiple spaces to single space

### Metrics

For each file, the comparison is binary (match or no match):

- **TP (True Positive)**: Normalized prediction exactly equals normalized ground truth
- **FP (False Positive)**: Prediction doesn't match ground truth (count = 1)
- **FN (False Negative)**: Same as FP (count = 1)

Computed metrics:
- **Precision** = TP / (TP + FP)
- **Recall** = TP / (TP + FN)
- **F1** = 2 × Precision × Recall / (Precision + Recall)

## Features

✅ **Offline Operation**: No network calls after model download  
✅ **Multiple Audio Formats**: .wav, .flac, .mp3, .m4a  
✅ **Automatic Resampling**: Handles different sample rates  
✅ **Long Audio Support**: Processes files up to 10+ minutes  
✅ **GPU Acceleration**: Uses CUDA when available with mixed precision  
✅ **Deterministic Inference**: Reproducible results with fixed seeds  
✅ **Batch Processing**: Efficient multi-file transcription  
✅ **REST API**: Production-ready FastAPI server  
✅ **CLI Tool**: Easy command-line interface  
✅ **Evaluation Framework**: Automated testing with metrics  

## Supported Audio Types

- WAV (`.wav`)
- FLAC (`.flac`)
- MP3 (`.mp3`)
- M4A (`.m4a`)

Files are automatically:
- Converted to mono if stereo
- Resampled to model's required sample rate
- Normalized by the processor

## Error Handling

The system validates:
- File existence before processing
- Directory existence for evaluation
- Audio format compatibility
- Model loading errors

REST API returns appropriate HTTP status codes:
- `200`: Success
- `400`: Bad request (invalid paths, missing files)
- `500`: Internal server error (model errors)
- `503`: Service unavailable (model not loaded)

## Output Format

### Transcription Result

```json
{
  "file": "/path/to/audio.wav",
  "text": "transcribed text output",
  "tokens_generated": 45,
  "elapsed_sec": 0.573
}
```

### Evaluation Result

```json
{
  "summary": {
    "count": 10,
    "tp": 8,
    "fp": 2,
    "fn": 2,
    "precision": 0.8,
    "recall": 0.8,
    "f1": 0.8
  },
  "details": [
    {
      "file": "sample001.wav",
      "pred": "predicted transcription",
      "gt": "ground truth text",
      "match": 1
    }
  ]
}
```

## Testing

Create a test directory structure:

```bash
mkdir -p test_data/audio test_data/labels

# Add your test audio files to test_data/audio/
# Add corresponding .txt files to test_data/labels/
```

Run smoke test:

```bash
# Test single file transcription
python cli.py transcribe --path test_data/audio/sample.wav

# Test evaluation
python cli.py evaluate \
  --audio-dir test_data/audio \
  --gt-dir test_data/labels
```

## Performance Tips

1. **GPU Usage**: Ensure CUDA is available for faster inference
2. **Batch Processing**: Use `transcribe_files()` for multiple files
3. **Model Loading**: Load model once and reuse for multiple calls
4. **Mixed Precision**: Automatically enabled on GPU for efficiency

## Troubleshooting

### Model Loading Fails

```bash
# Verify model directory contains required files
ls $MODEL_DIR
# Should contain: config.json, model weights, processor files
```

### Audio File Not Found

```bash
# Use absolute paths
python cli.py transcribe --path /absolute/path/to/audio.wav
```

### CUDA Out of Memory

- Reduce `max_new_tokens`
- Process files individually instead of batching
- Use CPU mode: `device="cpu"`

### Import Errors

```bash
# Ensure all dependencies are installed
pip install torch torchaudio transformers fastapi uvicorn pydantic
```

## Architecture

### Components

1. **audio_flamingo_runner.py**: Core inference engine
   - `load_model()`: Model initialization
   - `transcribe_file()`: Single file inference
   - `transcribe_files()`: Batch inference
   - `evaluate_folder()`: Evaluation framework

2. **server.py**: FastAPI REST server
   - `/transcribe`: Transcription endpoint
   - `/evaluate`: Evaluation endpoint
   - `/healthz`: Health check

3. **cli.py**: Command-line interface
   - `transcribe`: CLI transcription
   - `evaluate`: CLI evaluation

### Data Flow

```
Audio File → Load & Resample → Processor → Model → Decode → Text Output
```

### Evaluation Flow

```
Audio Folder + GT Folder → Transcribe Each → Normalize → Compare → Metrics
```

## License

This implementation follows the model's original license. Check the nvidia/audio-flamingo-3 model card for details.

## Notes

- Replace `{{MODEL_DIR}}` with your actual model path
- All processing is done locally without internet access
- Model files must be pre-downloaded using `huggingface_hub.snapshot_download`
- Supports deterministic inference with fixed random seeds
