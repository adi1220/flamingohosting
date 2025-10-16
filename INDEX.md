# Audio Flamingo 3 - Complete Documentation Index

## 📖 Documentation Structure

This project includes comprehensive documentation across multiple files. Start here to find what you need.

---

## 🚀 Getting Started (5 minutes)

**Start Here:** [`QUICKSTART.md`](#quickstart)  
Best for: First-time users, quick setup, basic usage examples

**Covers:**
- What Audio Flamingo actually does (not transcription!)
- 5-minute installation
- Simple usage examples (Python, CLI, REST API)
- Common prompts and use cases

---

## 📚 Complete Reference

**Read Next:** [`README.md`](#readme)  
Best for: Comprehensive API reference, all features, deployment

**Covers:**
- Complete API documentation
- All three interfaces (Python, REST, CLI)
- Evaluation framework details
- Performance tips and troubleshooting
- Supported formats and features

---

## 🎯 Evaluation Guide

### Choose Your Mode

**Decision Helper:** [`EVALUATION_MODE_GUIDE.md`](#evaluation-mode-guide)  
Best for: Understanding which evaluation mode to use

**Covers:**
- Mode 1 vs Mode 2 comparison
- Match mode selection (exact vs contains)
- Decision trees and flowcharts
- Common mistakes and solutions
- Quick reference commands

### Practical Examples

**Cookbook:** [`EVALUATION_EXAMPLES.md`](#evaluation-examples)  
Best for: Real-world examples, code templates, specific use cases

**Covers:**
- Complete working examples for both modes
- Instrument classification example
- Genre classification example
- Audio captioning example
- Conversion scripts (CSV to folders)
- Per-category analysis code

---

## 📋 Project Overview

**Summary:** [`SUMMARY.md`](#summary)  
Best for: Understanding the complete solution, feature overview

**Covers:**
- What's included in the project
- Key features and capabilities
- Complete API reference summary
- Use case matrix
- Best practices
- Quick links to all docs

---

## 📄 File Reference

### Core Implementation Files

| File | Purpose | When to Use |
|------|---------|-------------|
| `audio_flamingo_runner.py` | Core Python API | Direct integration, custom workflows |
| `server.py` | REST API server | Production deployment, HTTP integration |
| `cli.py` | Command-line interface | Quick testing, automation scripts |
| `requirements.txt` | Dependencies | Installation |
| `test_smoke.py` | Automated testing | Verify setup, smoke tests |

### Documentation Files

| File | Purpose | Read When |
|------|---------|-----------|
| `INDEX.md` | This file | Finding documentation |
| `QUICKSTART.md` | Fast setup | Getting started (first read) |
| `README.md` | Complete reference | Need detailed API docs |
| `EVALUATION_MODE_GUIDE.md` | Mode selection | Confused about evaluation modes |
| `EVALUATION_EXAMPLES.md` | Practical examples | Need working code examples |
| `SUMMARY.md` | Project overview | Want big picture view |

---

## 🎓 Learning Path

### Beginner Path (30 minutes)

1. **Read:** `QUICKSTART.md` (5 min)
2. **Do:** Install dependencies and set MODEL_DIR (5 min)
3. **Try:** Run a single transcription example (5 min)
4. **Test:** Run `python test_smoke.py` (10 min)
5. **Explore:** Try different prompts on your audio (5 min)

### Evaluation Path (45 minutes)

1. **Read:** `EVALUATION_MODE_GUIDE.md` - Decision section (10 min)
2. **Decide:** Which mode fits your use case (5 min)
3. **Read:** Relevant section in `EVALUATION_EXAMPLES.md` (10 min)
4. **Do:** Organize your data according to chosen mode (10 min)
5. **Run:** Your first evaluation (10 min)

### Advanced Path (60+ minutes)

1. **Read:** `README.md` - Complete API reference (20 min)
2. **Read:** `EVALUATION_EXAMPLES.md` - All examples (20 min)
3. **Study:** `audio_flamingo_runner.py` source code (20 min)
4. **Customize:** Adapt code for your specific needs (variable)

---

## 🔍 Quick Lookup

### "I want to..."

| Goal | Go To | Section |
|------|-------|---------|
| Get started quickly | `QUICKSTART.md` | All |
| Understand what this model does | `QUICKSTART.md` | "What You Need to Know" |
| Install dependencies | `README.md` | "Installation" |
| Use Python API | `README.md` | "Python API" |
| Start REST server | `README.md` | "REST API Server" |
| Use CLI | `README.md` | "CLI Interface" |
| Choose evaluation mode | `EVALUATION_MODE_GUIDE.md` | "Quick Decision Tree" |
| Classify instruments | `EVALUATION_EXAMPLES.md` | "Use Case 1" |
| Caption audio | `EVALUATION_EXAMPLES.md` | "Use Case: Audio Captioning" |
| See all features | `SUMMARY.md` | "Key Features" |
| Troubleshoot errors | `README.md` | "Troubleshooting" |
| Convert my dataset | `EVALUATION_MODE_GUIDE.md` | "Conversion Scripts" |
| Understand metrics | `SUMMARY.md` | "Metrics Explained" |

---

## 💡 Common Questions

### Q: Is this a speech-to-text model?
**A:** No! Read `QUICKSTART.md` - "What is Audio Flamingo?" section.  
It's an audio *understanding* model that answers questions about audio.

### Q: Which evaluation mode should I use?
**A:** Read `EVALUATION_MODE_GUIDE.md` - "Quick Decision Tree" section.  
Short answer: Mode 2 + contains for classification, Mode 1 + exact for descriptions.

### Q: How do I organize my dataset?
**A:** Depends on your use case:
- Classification → `EVALUATION_MODE_GUIDE.md` - "Mode 2" section
- Descriptions → `EVALUATION_MODE_GUIDE.md` - "Mode 1" section

### Q: Can I see a complete working example?
**A:** Yes! `EVALUATION_EXAMPLES.md` has multiple complete examples with code.

### Q: What's the difference between exact and contains matching?
**A:** `EVALUATION_MODE_GUIDE.md` - "Match Mode Selection" section.  
Short answer: exact requires full match, contains allows substring matching.

### Q: How do I deploy to production?
**A:** `README.md` - "REST API Server" section and `SUMMARY.md` - "Workflow Summary".

### Q: Where are example curl commands?
**A:** `README.md` - REST API sections and `EVALUATION_EXAMPLES.md` - REST API section.

---

## 🛠️ Use Case Guides

### Audio Classification Tasks

**Read:**
1. `EVALUATION_MODE_GUIDE.md` - "Mode 2" section
2. `EVALUATION_EXAMPLES.md` - Use Cases 1-3

**Use:** Mode 2 + contains matching

**Examples:**
- Instrument recognition
- Genre classification
- Scene classification
- Sound event detection

### Audio Description/Captioning Tasks

**Read:**
1. `EVALUATION_MODE_GUIDE.md` - "Mode 1" section
2. `EVALUATION_EXAMPLES.md` - "Audio Captioning Evaluation"

**Use:** Mode 1 + exact matching

**Examples:**
- Audio captioning
- Sound description
- Speech summarization

---

## 📊 Code Examples Quick Reference

### Python One-Liner

```python
# See: QUICKSTART.md - "Python" section
import audio_flamingo_runner as runner
model = runner.load_model()
result = runner.transcribe_file("audio.mp3", model, prompt="What sounds can you hear?")
print(result["text"])
```

### CLI One-Liner

```bash
# See: README.md - "CLI Interface" section
python cli.py transcribe --path audio.mp3 --prompt "What instrument is playing?"
```

### Evaluation (Folder Mode)

```bash
# See: EVALUATION_EXAMPLES.md - "Use Case 1"
python cli.py evaluate --audio-dir instruments --use-folder-as-label \
  --prompt "What instrument?" --match-mode contains
```

### Evaluation (File Mode)

```bash
# See: EVALUATION_EXAMPLES.md - "Use Case: Audio Captioning"
python cli.py evaluate --audio-dir audio --gt-dir labels \
  --prompt "Describe the audio." --match-mode exact
```

---

## 🎯 Recommended Reading Order

### First Time User
1. `INDEX.md` (this file) - 2 min
2. `QUICKSTART.md` - 10 min
3. Try the examples - 15 min
4. **Total:** 27 minutes to working system

### Evaluating a Dataset
1. `EVALUATION_MODE_GUIDE.md` - Decision section - 5 min
2. Organize your data - 10 min
3. `EVALUATION_EXAMPLES.md` - Relevant example - 10 min
4. Run evaluation - 5 min
5. **Total:** 30 minutes to first results

### Production Deployment
1. `README.md` - Complete reference - 20 min
2. `SUMMARY.md` - Best practices - 10 min
3. `server.py` source code review - 10 min
4. Deploy and test - 20 min
5. **Total:** 60 minutes to production

---

## 🔗 External Resources

- **Model Card:** https://huggingface.co/nvidia/audio-flamingo-3
- **Research Paper:** https://arxiv.org/abs/2507.08128
- **Demo:** https://huggingface.co/spaces/manoskary/audio-flamingo-3
- **GitHub:** https://github.com/NVIDIA/audio-flamingo

---

## ✅ Checklist: Am I Ready?

Before starting, make sure you have:

- [ ] Downloaded Audio Flamingo 3 model to local directory
- [ ] Set `MODEL_DIR` environment variable
- [ ] Installed dependencies from `requirements.txt`
- [ ] Read `QUICKSTART.md`
- [ ] Understand this is NOT a transcription model

**All checked?** You're ready! Start with `QUICKSTART.md` examples.

---

## 🆘 Getting Help

1. **Setup issues?** → `README.md` - "Troubleshooting" section
2. **Evaluation confusion?** → `EVALUATION_MODE_GUIDE.md` - "Common Mistakes" section
3. **Need examples?** → `EVALUATION_EXAMPLES.md` - Find similar use case
4. **API questions?** → `README.md` - Complete API reference
5. **Model behavior questions?** → Check Hugging Face model card

---

## 📝 Document Summaries

### QUICKSTART.md
**Length:** ~5 pages  
**Read Time:** 10 minutes  
**Purpose:** Get running in 5 minutes  
**Key Sections:**
- What is Audio Flamingo (NOT transcription!)
- 5-minute setup
- Common prompts and use cases
- Quick examples for Python/CLI/REST

**Read this if:** You're new to the project

---

### README.md
**Length:** ~15 pages  
**Read Time:** 20-30 minutes  
**Purpose:** Complete technical reference  
**Key Sections:**
- Installation and setup
- All three APIs (Python, REST, CLI)
- Evaluation modes (both)
- Features and capabilities
- Troubleshooting guide

**Read this if:** You need complete documentation

---

### EVALUATION_MODE_GUIDE.md
**Length:** ~12 pages  
**Read Time:** 15-20 minutes  
**Purpose:** Help you choose the right evaluation approach  
**Key Sections:**
- Mode 1 vs Mode 2 comparison
- Quick decision tree
- Match mode selection (exact vs contains)
- Real-world dataset examples
- Common mistakes and solutions

**Read this if:** You're confused about which evaluation mode to use

---

### EVALUATION_EXAMPLES.md
**Length:** ~15 pages  
**Read Time:** 20-30 minutes  
**Purpose:** Practical, copy-paste ready examples  
**Key Sections:**
- Complete working examples
- Multiple use cases (instruments, genres, scenes, captions)
- Python, CLI, and REST examples
- Dataset conversion scripts
- Per-category analysis code

**Read this if:** You want working code examples

---

### SUMMARY.md
**Length:** ~8 pages  
**Read Time:** 10-15 minutes  
**Purpose:** High-level project overview  
**Key Sections:**
- What's included
- Key features
- Quick start
- API reference summary
- Use case matrix
- Workflow diagrams

**Read this if:** You want the big picture

---

## 🎨 Visual Guide to Evaluation Modes

### Mode 1: Separate Files
```
📁 my_dataset/
  📁 audio/
    🎵 song1.wav ───┐
    🎵 song2.mp3 ───┤
    🎵 song3.flac ──┤
                    │
  📁 labels/        │
    📄 song1.txt ◄──┘  "Piano playing classical music"
    📄 song2.txt ◄───  "Guitar solo with reverb"
    📄 song3.txt ◄───  "Drum kit performing jazz"

✅ Use when: Each file has unique, detailed description
🎯 Match mode: exact
📝 Example: Audio captioning, detailed descriptions
```

### Mode 2: Folder as Label
```
📁 instruments/
  📁 piano/         ◄── Label = "piano"
    🎵 song1.wav
    🎵 song2.mp3
    🎵 song3.wav
    
  📁 guitar/        ◄── Label = "guitar"
    🎵 track1.wav
    🎵 track2.mp3
    
  📁 drums/         ◄── Label = "drums"
    🎵 beat1.wav
    🎵 beat2.wav

✅ Use when: Files grouped by category/class
🎯 Match mode: contains
📝 Example: Classification tasks (instruments, genres, scenes)
```

---

## 🔄 Workflow Diagrams

### Research/Development Workflow
```
1. Download Model
   ↓
2. Read QUICKSTART.md
   ↓
3. Try Basic Examples
   ↓
4. Choose Evaluation Mode
   │
   ├─→ Classification? → Mode 2 (folder labels)
   └─→ Descriptions?   → Mode 1 (text files)
   ↓
5. Run Evaluation
   ↓
6. Analyze Results
   ↓
7. Iterate (adjust prompts, modes)
```

### Production Deployment Workflow
```
1. Develop Locally (Python API)
   ↓
2. Test with CLI
   ↓
3. Deploy REST Server
   ↓
4. Integrate with Application
   ↓
5. Monitor /healthz
   ↓
6. Scale as Needed
```

---

## 🎯 Task-Specific Quick Links

### I want to classify instruments
1. Read: `EVALUATION_MODE_GUIDE.md` → "Mode 2" section
2. See: `EVALUATION_EXAMPLES.md` → "Use Case 1: Instrument Classification"
3. Command: 
   ```bash
   python cli.py evaluate --audio-dir instruments --use-folder-as-label \
     --prompt "What instrument is playing?" --match-mode contains
   ```

### I want to caption audio
1. Read: `EVALUATION_MODE_GUIDE.md` → "Mode 1" section
2. See: `EVALUATION_EXAMPLES.md` → "Use Case: Audio Captioning Evaluation"
3. Command:
   ```bash
   python cli.py evaluate --audio-dir audio --gt-dir labels \
     --prompt "Please describe the audio." --match-mode exact
   ```

### I want to deploy a REST API
1. Read: `README.md` → "REST API Server" section
2. See: `SUMMARY.md` → "Production Deployment" workflow
3. Command:
   ```bash
   python server.py --host 0.0.0.0 --port 8000
   ```

### I want to understand metrics
1. Read: `SUMMARY.md` → "Metrics Explained" section
2. See: `README.md` → "Evaluation Mode" → "Metrics" section

### I want to convert my CSV dataset
1. Read: `EVALUATION_MODE_GUIDE.md` → "Conversion Scripts" section
2. Copy the appropriate script for your needs

---

## 📦 Complete File List

### Must Read
- ✅ `INDEX.md` - This navigation guide
- ✅ `QUICKSTART.md` - Start here!
- ✅ `README.md` - Complete reference

### Evaluation Guides
- 📊 `EVALUATION_MODE_GUIDE.md` - Choose your mode
- 📊 `EVALUATION_EXAMPLES.md` - Working examples

### Reference
- 📚 `SUMMARY.md` - Project overview

### Implementation
- 🐍 `audio_flamingo_runner.py` - Core Python API
- 🌐 `server.py` - REST API server
- 💻 `cli.py` - Command-line interface
- 🧪 `test_smoke.py` - Smoke tests
- 📋 `requirements.txt` - Dependencies

---

## 🚦 Traffic Light System

### 🟢 Green (Ready to Start)
You should feel comfortable if you've read:
- `INDEX.md` (this file)
- `QUICKSTART.md`
- Tried at least one example

### 🟡 Yellow (Learning)
You're here if you're:
- Reading through `README.md`
- Trying different evaluation modes
- Experimenting with prompts

### 🔴 Red (Need Help)
Stop and read documentation if:
- You don't understand what Audio Flamingo does
- You're confused about evaluation modes
- Results don't make sense
- You're getting errors

---

## 💡 Pro Tips

1. **Start Simple**: Use Mode 2 + contains for your first evaluation
2. **Iterate on Prompts**: Try 3-4 different prompts to find what works
3. **Check Examples First**: Someone probably already did something similar
4. **Read Error Messages**: They often tell you exactly what's wrong
5. **Use Test Mode**: Run on 5-10 files first before full dataset

---

## 📈 Success Metrics

After reading the docs, you should be able to:

- [ ] Explain what Audio Flamingo does (vs transcription)
- [ ] Run a single file inference
- [ ] Choose between Mode 1 and Mode 2 for your use case
- [ ] Run an evaluation and interpret the metrics
- [ ] Write effective prompts for your task
- [ ] Choose between exact and contains matching
- [ ] Start the REST API server
- [ ] Find relevant examples in the documentation

**All checked?** Congratulations! You're an Audio Flamingo expert! 🎉

---

## 🎓 Advanced Topics

Once comfortable with basics, explore:

1. **Custom Prompts**: Experiment with different phrasings
2. **Batch Processing**: Optimize for large datasets
3. **Per-Category Analysis**: Dive into the example code
4. **API Integration**: Build your own application
5. **Performance Tuning**: GPU optimization, batch sizes

Find these topics in `README.md` and `EVALUATION_EXAMPLES.md`.

---

## 📚 Glossary

**Audio Flamingo**: Audio understanding model (NOT transcription)  
**Mode 1**: Evaluation with separate ground truth text files  
**Mode 2**: Evaluation using folder names as labels  
**exact match**: Prediction must exactly equal ground truth  
**contains match**: Ground truth must appear in prediction  
**GT**: Ground Truth (expected/correct answer)  
**Prompt**: Question or instruction given to the model  
**Inference**: Running the model on audio to get a response

---

## 🎬 Getting Started Right Now

### Quick Start (10 minutes)
```bash
# 1. Install
pip install -r requirements.txt

# 2. Set model path
export MODEL_DIR=/path/to/audio-flamingo-3-model

# 3. Test single file
python cli.py transcribe --path your_audio.mp3 --prompt "What sounds can you hear?"

# Done! You just used Audio Flamingo!
```

### Next Steps
- Read `QUICKSTART.md` for more examples
- Try different prompts
- Explore evaluation modes when ready

---

## 📞 Support Resources

- **Documentation**: All .md files in this project
- **Model Info**: https://huggingface.co/nvidia/audio-flamingo-3
- **Research Paper**: https://arxiv.org/abs/2507.08128
- **Code Issues**: Check `README.md` troubleshooting section

---

## ✨ Final Checklist

Before you start using Audio Flamingo:

- [ ] I understand this is NOT a transcription model
- [ ] I've read `QUICKSTART.md`
- [ ] I have the model downloaded locally
- [ ] I've set the `MODEL_DIR` environment variable
- [ ] I've installed dependencies
- [ ] I know where to find examples
- [ ] I know which evaluation mode I need

**Ready to go!** 🚀

Start with: `python test_smoke.py` or try your first inference!

---

*Last Updated: Matches Audio Flamingo 3 (nvidia/audio-flamingo-3)*  
*Documentation Version: 1.0*
 `
