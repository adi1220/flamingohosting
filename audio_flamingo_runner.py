import os
import time
import torch
import torchaudio
import re
from pathlib import Path
from typing import Optional
from transformers import AutoProcessor, AutoModelForVision2Seq
import numpy as np


def load_model(model_dir: str = "{{MODEL_DIR}}", device: Optional[str] = None) -> dict:
    """
    Returns a dict with:
      - 'model': loaded model on device
      - 'processor': processor for audio
      - 'device': 'cuda' or 'cpu'
    """
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    
    print(f"Loading model from {model_dir} on {device}...")
    
    # Load processor and model from local directory
    processor = AutoProcessor.from_pretrained(model_dir, local_files_only=True)
    model = AutoModelForVision2Seq.from_pretrained(
        model_dir,
        local_files_only=True,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32
    )
    model = model.to(device)
    model.eval()
    
    # Set seeds for determinism
    torch.manual_seed(42)
    if device == "cuda":
        torch.cuda.manual_seed_all(42)
    
    print(f"Model loaded successfully on {device}")
    
    return {
        "model": model,
        "processor": processor,
        "device": device
    }


def _load_and_preprocess_audio(path: str, processor, device: str):
    """Load audio file, resample if needed, and preprocess."""
    # Load audio
    waveform, sample_rate = torchaudio.load(path)
    
    # Convert to mono if stereo
    if waveform.shape[0] > 1:
        waveform = torch.mean(waveform, dim=0, keepdim=True)
    
    # Get target sample rate from processor
    target_sr = processor.feature_extractor.sampling_rate
    
    # Resample if needed
    if sample_rate != target_sr:
        resampler = torchaudio.transforms.Resample(sample_rate, target_sr)
        waveform = resampler(waveform)
    
    # Convert to numpy for processor
    audio_array = waveform.squeeze().numpy()
    
    return audio_array, target_sr


def transcribe_file(
    path: str,
    model_bundle: dict,
    prompt: Optional[str] = None,
    max_new_tokens: int = 128,
) -> dict:
    """
    Runs inference on a SINGLE file.
    Note: Audio Flamingo is an audio understanding model, not a transcription model.
    It answers questions about audio (sounds, music, speech).
    
    Returns JSON:
      {
        "file": "<input path>",
        "text": "<final output string>",
        "tokens_generated": <int>,
        "elapsed_sec": <float>
      }
    """
    start_time = time.time()
    
    model = model_bundle["model"]
    processor = model_bundle["processor"]
    device = model_bundle["device"]
    
    # Load and preprocess audio
    audio_array, sample_rate = _load_and_preprocess_audio(path, processor, device)
    
    # Default prompt if none provided - Audio Flamingo expects a question/instruction
    if prompt is None:
        prompt = "Please describe the audio in detail."
    
    # Process audio and text together
    # Audio Flamingo uses a vision-language model architecture adapted for audio
    inputs = processor(
        text=prompt,
        audios=audio_array,
        return_tensors="pt",
        padding=True,
        sampling_rate=sample_rate
    )
    
    # Move inputs to device
    inputs = {k: v.to(device) if isinstance(v, torch.Tensor) else v for k, v in inputs.items()}
    
    # Generate
    with torch.no_grad():
        with torch.cuda.amp.autocast(enabled=(device == "cuda")):
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                num_beams=1,
                temperature=None,
                top_p=None
            )
    
    # Decode output - remove the input prompt from the generated text
    generated_text = processor.batch_decode(outputs, skip_special_tokens=True)[0]
    
    # Remove the prompt from the output if it's included
    if prompt in generated_text:
        generated_text = generated_text.replace(prompt, "").strip()
    
    elapsed_sec = time.time() - start_time
    tokens_generated = outputs.shape[1]
    
    return {
        "file": path,
        "text": generated_text.strip(),
        "tokens_generated": tokens_generated,
        "elapsed_sec": elapsed_sec
    }


def transcribe_files(
    paths: list[str],
    model_bundle: dict,
    prompt: Optional[str] = None,
    max_new_tokens: int = 128,
    num_workers: int = 0
) -> list[dict]:
    """
    Batch inference for MULTIPLE files.
    Returns a list of JSON objects (same schema as transcribe_file).
    """
    results = []
    
    # For simplicity, process sequentially (num_workers not used in this implementation)
    # Could be extended with multiprocessing for CPU or batch processing
    for path in paths:
        result = transcribe_file(path, model_bundle, prompt, max_new_tokens)
        results.append(result)
    
    return results


def _normalize_text(text: str) -> str:
    """Normalize text for comparison."""
    # Lowercase
    text = text.lower()
    # Strip leading/trailing whitespace
    text = text.strip()
    # Collapse multiple whitespace to single space
    text = re.sub(r'\s+', ' ', text)
    return text


def evaluate_folder(
    audio_dir: str,
    gt_dir: str,
    model_bundle: dict,
    prompt: Optional[str] = None,
    max_new_tokens: int = 128,
    match_mode: str = "exact"
) -> dict:
    """
    Evaluation mode. For each audio file in audio_dir, load a ground truth file
    with the SAME stem name from gt_dir and extension .txt, containing the target string.
    """
    audio_path = Path(audio_dir)
    gt_path = Path(gt_dir)
    
    # Find all audio files
    audio_extensions = {'.wav', '.flac', '.mp3', '.m4a'}
    audio_files = [f for f in audio_path.iterdir() 
                   if f.suffix.lower() in audio_extensions]
    
    if not audio_files:
        return {
            "summary": {
                "count": 0,
                "tp": 0,
                "fp": 0,
                "fn": 0,
                "precision": 0.0,
                "recall": 0.0,
                "f1": 0.0
            },
            "details": []
        }
    
    details = []
    tp = 0
    
    for audio_file in audio_files:
        # Find corresponding ground truth file
        gt_file = gt_path / f"{audio_file.stem}.txt"
        
        if not gt_file.exists():
            print(f"Warning: No ground truth found for {audio_file.name}, skipping...")
            continue
        
        # Load ground truth
        with open(gt_file, 'r', encoding='utf-8') as f:
            gt_text = f.read()
        
        # Run inference
        result = transcribe_file(
            str(audio_file),
            model_bundle,
            prompt,
            max_new_tokens
        )
        
        pred_text = result["text"]
        
        # Normalize both texts
        pred_normalized = _normalize_text(pred_text)
        gt_normalized = _normalize_text(gt_text)
        
        # Compare
        if match_mode == "exact":
            match = 1 if pred_normalized == gt_normalized else 0
        else:
            # Extensible for future modes
            match = 1 if pred_normalized == gt_normalized else 0
        
        tp += match
        
        details.append({
            "file": audio_file.name,
            "pred": pred_text,
            "gt": gt_text,
            "match": match
        })
    
    # Calculate metrics
    count = len(details)
    fp = count - tp  # Files where pred != gt
    fn = count - tp  # Same as FP for binary classification per file
    
    # Calculate precision, recall, F1
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return {
        "summary": {
            "count": count,
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "precision": precision,
            "recall": recall,
            "f1": f1
        },
        "details": details
    }
