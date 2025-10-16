#!/usr/bin/env python3
"""
Smoke test script for Audio Flamingo offline runner.
Creates synthetic test data and verifies all components work.
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path
import numpy as np
import torchaudio

# Try to import the runner
try:
    import audio_flamingo_runner as runner
except ImportError:
    print("ERROR: Cannot import audio_flamingo_runner.py")
    print("Make sure audio_flamingo_runner.py is in the current directory")
    sys.exit(1)


def create_test_audio(path: str, duration: float = 2.0, sample_rate: int = 16000):
    """Create a simple sine wave audio file for testing."""
    t = np.linspace(0, duration, int(sample_rate * duration))
    # Create a simple tone (440 Hz)
    audio = np.sin(2 * np.pi * 440 * t)
    # Add some variation
    audio = audio * 0.5 + np.sin(2 * np.pi * 880 * t) * 0.3
    
    # Convert to tensor
    waveform = torch.from_numpy(audio).float().unsqueeze(0)
    
    # Save
    torchaudio.save(path, waveform, sample_rate)
    print(f"Created test audio: {path}")


def run_smoke_test():
    """Run complete smoke test of all functionality."""
    print("=" * 60)
    print("Audio Flamingo Offline Runner - Smoke Test")
    print("=" * 60)
    
    # Get model directory
    model_dir = os.getenv("MODEL_DIR", "{{MODEL_DIR}}")
    if model_dir == "{{MODEL_DIR}}":
        print("\nERROR: MODEL_DIR not set!")
        print("Please set MODEL_DIR environment variable:")
        print("  export MODEL_DIR=/path/to/your/audio-flamingo-3-model")
        sys.exit(1)
    
    if not Path(model_dir).exists():
        print(f"\nERROR: Model directory not found: {model_dir}")
        sys.exit(1)
    
    print(f"\nModel directory: {model_dir}")
    
    # Create temporary test directory
    temp_dir = tempfile.mkdtemp(prefix="audio_flamingo_test_")
    print(f"Test directory: {temp_dir}")
    
    try:
        # Create test audio files
        audio_dir = Path(temp_dir) / "audio"
        labels_dir = Path(temp_dir) / "labels"
        audio_dir.mkdir()
        labels_dir.mkdir()
        
        print("\n1. Creating test audio files...")
        test_files = []
        test_prompts = [
            "Please describe the audio in detail.",
            "What sounds can you hear in this audio?",
            "Describe the characteristics of this audio."
        ]
        
        for i in range(3):
            audio_path = audio_dir / f"test_{i:03d}.wav"
            create_test_audio(str(audio_path), duration=1.0 + i * 0.5)
            test_files.append(str(audio_path))
            
            # Create corresponding label with expected answer
            label_path = labels_dir / f"test_{i:03d}.txt"
            with open(label_path, 'w') as f:
                # These are example expected answers
                f.write(f"This audio contains a tone at 440 Hz with some harmonics.")
        
        # Define the prompt to use for evaluation
        eval_prompt = "Please describe the audio in detail."
        
        # Load model
        print("\n2. Loading model...")
        model_bundle = runner.load_model(model_dir=model_dir)
        print(f"   Device: {model_bundle['device']}")
        
        # Test single file transcription
        print("\n3. Testing single file audio understanding...")
        result = runner.transcribe_file(
            test_files[0],
            model_bundle,
            prompt="Please describe the audio in detail.",
            max_new_tokens=64
        )
        print(f"   File: {result['file']}")
        print(f"   Response: {result['text'][:100]}...")
        print(f"   Tokens: {result['tokens_generated']}")
        print(f"   Time: {result['elapsed_sec']:.2f}s")
        
        # Test batch transcription
        print("\n4. Testing batch audio understanding...")
        results = runner.transcribe_files(
            test_files,
            model_bundle,
            prompt="What sounds can you hear?",
            max_new_tokens=64
        )
        print(f"   Processed {len(results)} files")
        for r in results:
            print(f"   - {Path(r['file']).name}: {r['text'][:50]}...")
        
        # Test evaluation
        print("\n5. Testing evaluation...")
        eval_result = runner.evaluate_folder(
            str(audio_dir),
            str(labels_dir),
            model_bundle,
            prompt=eval_prompt,
            max_new_tokens=64
        )
        
        summary = eval_result['summary']
        print(f"   Files evaluated: {summary['count']}")
        print(f"   True Positives: {summary['tp']}")
        print(f"   False Positives: {summary['fp']}")
        print(f"   Precision: {summary['precision']:.2f}")
        print(f"   Recall: {summary['recall']:.2f}")
        print(f"   F1 Score: {summary['f1']:.2f}")
        
        # Save results
        results_file = Path(temp_dir) / "test_results.json"
        with open(results_file, 'w') as f:
            json.dump({
                "transcription": {"results": results},
                "evaluation": eval_result
            }, f, indent=2)
        print(f"\n   Results saved to: {results_file}")
        
        print("\n" + "=" * 60)
        print("✓ All smoke tests passed!")
        print("=" * 60)
        print(f"\nTest files located at: {temp_dir}")
        print("You can manually inspect the results or delete the directory.")
        
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR during testing: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Optionally clean up (commented out to allow inspection)
        # shutil.rmtree(temp_dir)
        pass


if __name__ == "__main__":
    import torch
    success = run_smoke_test()
    sys.exit(0 if success else 1)
