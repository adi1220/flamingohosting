# Audio Flamingo 3 - Complete Offline Solution Summary

## 📦 What's Included

### Core Files
1. **audio_flamingo_runner.py** - Python API with all core functionality
2. **server.py** - FastAPI REST server (localhost:8000)
3. **cli.py** - Command-line interface
4. **requirements.txt** - All dependencies

### Documentation
5. **README.md** - Complete documentation and API reference
6. **QUICKSTART.md** - 5-minute getting started guide
7. **EVALUATION_EXAMPLES.md** - Comprehensive evaluation examples
8. **SUMMARY.md** - This file

### Testing
9. **test_smoke.py** - Automated smoke tests

---

## 🎯 Key Features Delivered

### ✅ Two Evaluation Modes

**Mode 1: Separate Ground Truth Files**
```
audio/file1.wav → labels/file1.txt
```
Best for: Detailed descriptions, captions, complex GT

**Mode 2: Folder Names as Labels** ⭐ NEW
```
audio/piano/song1.wav → GT = "piano"
```
Best for: Classification tasks, simple labels

### ✅ Two Matching Strategies

- **exact**: Full string must match (after normalization)
- **contains**: GT keyword must appear in prediction

### ✅ Three Usage Interfaces

1. **Python API** - Direct function calls
2. **REST API** - HTTP server for integration
3. **CLI** - Command-line tool

---

## 🚀 Quick Start

### 1. Install
```bash
pip install -r requirements.txt
export MODEL_DIR=/path/to/audio-flamingo-3-model
```

### 2. Use It

**Python:**
```python
import audio_flamingo_runner as runner
model = runner.load_model()

# Ask a question about audio
result = runner.transcribe_file(
    "audio.mp3", 
    model, 
    prompt="What instruments are playing?"
)
print(result["text"])
```

**CLI:**
```bash
python cli.py transcribe --path audio.mp3 --prompt "What sounds can you hear?"
```

**REST API:**
```bash
python server.py  # Start server
curl -X POST http://127.0.0.1:8000/transcribe -H "Content-Type: application/json" \
  -d '{"paths": ["/path/audio.mp3"], "prompt": "Describe this audio"}'
```

---

## 📊 Evaluation Examples

### Example 1: Instrument Classification (Folder Mode)

**Structure:**
```
instruments/
  ├── piano/song1.mp3, song2.wav
  ├── guitar/track1.mp3
  └── drums/beat1.wav
```

**Run:**
```bash
python cli.py evaluate \
  --audio-dir instruments \
  --use-folder-as-label \
  --prompt "What instrument is playing?" \
  --match-mode contains
```

**Why this works:**
- Folder name = Ground truth label
- `contains` mode lets model say "piano playing classical music" and still match GT "piano"

### Example 2: Audio Captioning (File Mode)

**Structure:**
```
dataset/
  audio/clip1.wav, clip2.mp3
  labels/clip1.txt, clip2.txt
```

**Run:**
```bash
python cli.py evaluate \
  --audio-dir dataset/audio \
  --gt-dir dataset/labels \
  --prompt "Please describe the audio in detail." \
  --match-mode exact
```

---

## 🔑 Key Design Decisions

### Why "transcribe_file" name?

The spec required these function names. While Audio Flamingo doesn't transcribe, we kept the interface consistent with requirements while documenting the actual behavior (audio understanding/QA).

### Why support folder-as-label mode?

Common ML pattern for classification:
```
dataset/
  class1/samples...
  class2/samples...
```

This makes it trivial to evaluate on standard classification datasets.

### Why two match modes?

**exact**: For detailed evaluations
- GT: "A piano playing Chopin's nocturne"
- Works when you have full descriptions

**contains**: For classification tasks
- GT: "piano"
- Pred: "This is a beautiful piano performance"
- Result: Match! (flexible, practical)

---

## 📋 Complete API Reference

### Python Functions

```python
# Load model (once)
model_bundle = runner.load_model(model_dir, device)

# Single file
result = runner.transcribe_file(path, model_bundle, prompt, max_new_tokens)

# Multiple files
results = runner.transcribe_files(paths, model_bundle, prompt, max_new_tokens)

# Evaluate - Mode 1
result = runner.evaluate_folder(
    audio_dir, gt_dir, model_bundle, 
    prompt, max_new_tokens, match_mode="exact"
)

# Evaluate - Mode 2 (folder as label)
result = runner.evaluate_folder(
    audio_dir, None, model_bundle,
    prompt, max_new_tokens, match_mode="contains",
    use_folder_as_label=True
)
```

### REST Endpoints

```
POST /transcribe
  Body: {paths, prompt, max_new_tokens}
  
POST /evaluate
  Body: {audio_dir, gt_dir, prompt, max_new_tokens, match_mode, use_folder_as_label}
  
GET /healthz
  Returns: {status, device, model}
```

### CLI Commands

```bash
# Single file
python cli.py transcribe --path file.wav --prompt "..."

# Multiple files
python cli.py transcribe --paths file1.wav file2.mp3 --prompt "..."

# Evaluate - Mode 1
python cli.py evaluate --audio-dir ./audio --gt-dir ./labels --prompt "..."

# Evaluate - Mode 2
python cli.py evaluate --audio-dir ./audio --use-folder-as-label --prompt "..." --match-mode contains
```

---

## 💡 Use Case Matrix

| Task | Folder Mode | Match Mode | Example Prompt |
|------|-------------|------------|----------------|
| Instrument Classification | ✅ Yes | `contains` | "What instrument is playing?" |
| Genre Classification | ✅ Yes | `contains` | "What genre is this music?" |
| Scene Classification | ✅ Yes | `contains` | "Is this indoors or outdoors?" |
| Audio Captioning | ❌ No | `exact` | "Describe the audio in detail." |
| Sound Event Detection | ✅ Yes | `contains` | "What sounds can you hear?" |
| Speech Summarization | ❌ No | `exact` | "Summarize this conversation." |

---

## 🎓 Best Practices

### 1. Prompt Engineering

**Good Prompts:**
- "What instrument is playing in this audio?"
- "Describe the acoustic environment."
- "What genre is this music?"

**Avoid:**
- "Tell me" (too vague)
- Empty prompts without default
- Prompts mismatched to GT

### 2. Match Mode Selection

```python
# Classification? Use contains
result = runner.evaluate_folder(
    ...,
    match_mode="contains",
    use_folder_as_label=True
)

# Detailed descriptions? Use exact
result = runner.evaluate_folder(
    ...,
    match_mode="exact",
    use_folder_as_label=False
)
```

### 3. Performance Tips

- Load model once, reuse for all files
- Use GPU (automatic if available)
- Batch files when possible
- Adjust `max_new_tokens` based on expected output length

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Model not found | Check `MODEL_DIR` environment variable |
| Out of memory | Reduce `max_new_tokens` or use CPU |
| Low accuracy | Try `contains` mode, adjust prompt |
| Missing GT files | Check file naming matches (stem must be identical) |
| Server won't start | Check port 8000 not in use |

---

## 📚 Documentation Quick Links

- **Getting Started**: Read `QUICKSTART.md`
- **Full API Details**: Read `README.md`
- **Evaluation Examples**: Read `EVALUATION_EXAMPLES.md`
- **Test Your Setup**: Run `python test_smoke.py`

---

## ✨ What Makes This Special

1. **Fully Offline** - Zero network calls after model download
2. **Dual Evaluation Modes** - Handles both file-based and folder-based GT
3. **Flexible Matching** - Exact or contains modes for different use cases
4. **Production Ready** - REST API, proper error handling, logging
5. **Well Documented** - 4 comprehensive docs + inline code comments
6. **Easy to Use** - Works in 5 minutes with QUICKSTART guide

---

## 🔄 Workflow Summary

### Development/Testing
```
1. Download model → 2. Run test_smoke.py → 3. Try examples
```

### Classification Task
```
1. Organize files by category (folder-as-label)
2. python cli.py evaluate --use-folder-as-label --match-mode contains
3. Review metrics
```

### Captioning/Description Task
```
1. Create audio/ and labels/ directories
2. python cli.py evaluate --gt-dir labels --match-mode exact
3. Analyze results
```

### Production Deployment
```
1. python server.py
2. Integrate with your app via REST API
3. Monitor /healthz endpoint
```

---

## 📊 Metrics Explained

All evaluation modes return:

```json
{
  "summary": {
    "count": 100,          // Total files evaluated
    "tp": 85,              // True Positives (correct matches)
    "fp": 15,              // False Positives (incorrect predictions)
    "fn": 15,              // False Negatives (same as FP for binary)
    "precision": 0.85,     // TP / (TP + FP)
    "recall": 0.85,        // TP / (TP + FN)
    "f1": 0.85            // Harmonic mean of precision & recall
  },
  "details": [...]         // Per-file breakdown
}
```

---

## 🎉 You're Ready!

Everything you need is here:
- ✅ Code that works offline
- ✅ Multiple interfaces (Python, REST, CLI)
- ✅ Two evaluation modes
- ✅ Comprehensive documentation
- ✅ Real-world examples

**Next Steps:**
1. Run `python test_smoke.py` to verify setup
2. Try examples from `EVALUATION_EXAMPLES.md`
3. Adapt to your specific use case

**Questions?** Check the troubleshooting sections in README.md and EVALUATION_EXAMPLES.md.

---

*Built for nvidia/audio-flamingo-3 - An audio understanding model that answers questions about sounds, music, and speech.*
