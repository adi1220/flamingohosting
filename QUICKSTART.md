# Quick Start Guide

## What You Need to Know

**Audio Flamingo 3 is an audio understanding model, NOT a transcription model.**

### ❌ Wrong Expectation
"It will convert speech to text like Whisper"

### ✅ Correct Understanding  
"It answers questions about audio - any audio (speech, music, sounds)"

## Example Interactions

### Music Analysis
```python
# Ask: "What instruments are playing?"
# Response: "This piece features a piano, violin, and cello in a classical arrangement."
```

### Sound Recognition
```python
# Ask: "What sounds can you hear in this audio?"
# Response: "I can hear birds chirping, wind blowing, and distant traffic noise."
```

### Speech Understanding
```python
# Ask: "Summarize what the speaker is talking about."
# Response: "The speaker is discussing climate change solutions and renewable energy."
```

### Audio Description
```python
# Ask: "Please describe the audio in detail."
# Response: "This is a conversation between two people in what sounds like a cafe setting..."
```

## 5-Minute Setup

### 1. Download Model (One Time)

```bash
pip install huggingface_hub

python -c "
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id='nvidia/audio-flamingo-3',
    local_dir='./audio-flamingo-3-model',
    local_dir_use_symlinks=False
)
"
```

### 2. Install Dependencies

```bash
pip install torch torchaudio transformers fastapi uvicorn pydantic
```

### 3. Set Model Path

```bash
export MODEL_DIR=/absolute/path/to/audio-flamingo-3-model
```

### 4. Test It!

**Python:**
```python
import audio_flamingo_runner as runner

# Load model
model = runner.load_model()

# Ask a question about audio
result = runner.transcribe_file(
    path="your_audio.mp3",
    model_bundle=model,
    prompt="What instruments are playing in this song?"
)

print(result["text"])
```

**CLI:**
```bash
python cli.py transcribe \
  --path your_audio.mp3 \
  --prompt "What sounds can you hear?"
```

**REST API:**
```bash
# Start server
python server.py

# In another terminal
curl -X POST http://127.0.0.1:8000/transcribe \
  -H "Content-Type: application/json" \
  -d '{
    "paths": ["/absolute/path/to/your_audio.mp3"],
    "prompt": "Please describe this audio."
  }'
```

## Common Prompts

### For Music
- "What instruments are playing in this audio?"
- "Describe the genre and mood of this music."
- "What is the tempo and rhythm?"

### For Sounds
- "What sounds can you hear?"
- "Is this indoors or outdoors?"
- "Describe the acoustic environment."

### For Speech
- "Summarize what the speaker is saying."
- "What is the speaker's tone or mood?"
- "Please transcribe and explain this audio."

### General
- "Please describe the audio in detail."
- "What happens in this audio?"
- "Analyze this audio and tell me what's happening."

## Evaluation Mode

If you want to test the model's accuracy:

**1. Create your test set:**
```
audio/
  ├── song1.mp3
  └── talk1.wav

labels/
  ├── song1.txt  ("Piano and guitar playing jazz music")
  └── talk1.txt  ("Two people discussing business plans")
```

**2. Run evaluation:**
```bash
python cli.py evaluate \
  --audio-dir ./audio \
  --gt-dir ./labels \
  --prompt "Please describe the audio in detail."
```

**3. Get metrics:**
- Precision: How accurate are the matches?
- Recall: How many did it get right?
- F1 Score: Overall performance

## Tips

1. **Be specific in your prompts** - "What instruments?" vs "Describe the audio"
2. **Adjust max_new_tokens** - Longer responses need more tokens (default: 128)
3. **Use GPU** - Much faster inference (automatically detected)
4. **Default prompt** - If you don't provide a prompt, it uses "Please describe the audio in detail."

## Need Speech Transcription?

If you specifically need to convert speech to text (like subtitles), use:
- OpenAI Whisper
- wav2vec2
- Other ASR (Automatic Speech Recognition) models

Audio Flamingo is for **understanding and reasoning** about audio, not just transcription.

## Troubleshooting

**"Model not found"**
- Make sure MODEL_DIR points to the correct directory
- Verify the directory contains `config.json` and model weights

**"Out of memory"**
- Reduce `max_new_tokens`
- Use CPU instead of GPU (slower but uses less memory)
- Process one file at a time

**"Unexpected output"**
- Check your prompt - it should be a question or instruction
- The model needs context about what you want to know
- Try different phrasings of your question

## What's Next?

- Check `README.md` for complete documentation
- See `test_smoke.py` for example code
- Read the paper: https://arxiv.org/abs/2507.08128
- Try the Hugging Face demo: https://huggingface.co/spaces/manoskary/audio-flamingo-3
