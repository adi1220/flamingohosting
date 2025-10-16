# Evaluation Mode Selection Guide

## Quick Decision Tree

```
Do you have detailed text descriptions for each audio file?
├─ YES → Use Mode 1 (Separate GT Files) + exact match
└─ NO
    └─ Are your audio files organized into category folders?
        ├─ YES → Use Mode 2 (Folder as Label) + contains match
        └─ NO → Organize them first, then use Mode 2
```

---

## Mode Comparison Table

| Feature | Mode 1: Separate Files | Mode 2: Folder as Label |
|---------|------------------------|-------------------------|
| **GT Location** | Separate .txt files | Subfolder names |
| **Best For** | Detailed descriptions, captions | Classification tasks |
| **GT Complexity** | Full sentences | Single words/short phrases |
| **Typical Match Mode** | `exact` | `contains` |
| **Setup Effort** | Higher (need to create txt files) | Lower (just organize folders) |
| **Flexibility** | High (different GT per file) | Lower (same prompt for all files in folder) |
| **Dataset Type** | Captioning, QA, description | Classification, tagging |

---

## When to Use Mode 1 (Separate GT Files)

### ✅ Use When:
- Each audio file has a unique, detailed ground truth
- You're evaluating captions or descriptions
- GT is more than 2-3 words
- You need different GT for every file

### Example Datasets:
- Audio captioning (AudioCaps, Clotho)
- Conversation summarization
- Detailed sound descriptions
- Question-answering tasks

### Structure:
```
dataset/
  audio/
    ├── clip001.wav
    ├── clip002.mp3
    └── clip003.flac
  labels/
    ├── clip001.txt  → "Two people having a casual conversation in a coffee shop"
    ├── clip002.txt  → "Classical piano music with slow tempo and melancholic mood"
    └── clip003.txt  → "Birds chirping in a forest with wind rustling through leaves"
```

### Command:
```bash
python cli.py evaluate \
  --audio-dir dataset/audio \
  --gt-dir dataset/labels \
  --prompt "Please describe the audio in detail." \
  --match-mode exact
```

---

## When to Use Mode 2 (Folder as Label)

### ✅ Use When:
- Doing classification (instrument, genre, scene, etc.)
- GT is a single word or short phrase
- Files naturally group into categories
- You already have organized folders

### Example Datasets:
- Instrument recognition (NSynth, IRMAS)
- Genre classification (GTZAN)
- Sound event classification (ESC-50, UrbanSound8K)
- Scene recognition (DCASE)

### Structure:
```
dataset/
  ├── piano/
  │   ├── sample001.wav
  │   ├── sample002.mp3
  │   └── sample003.wav
  ├── guitar/
  │   ├── track001.wav
  │   └── track002.mp3
  └── drums/
      ├── beat001.wav
      └── beat002.wav
```

### Command:
```bash
python cli.py evaluate \
  --audio-dir dataset \
  --use-folder-as-label \
  --prompt "What instrument is playing in this audio?" \
  --match-mode contains
```

---

## Match Mode Selection

### exact Match

**When to use:**
- GT is a complete sentence/description
- You want strict evaluation
- GT and prediction should be nearly identical

**Example:**
```python
GT: "piano playing classical music"
Prediction: "piano playing classical music"
Result: ✅ Match

GT: "piano playing classical music"
Prediction: "piano performance"
Result: ❌ No match
```

**Command:**
```bash
--match-mode exact
```

---

### contains Match

**When to use:**
- GT is a keyword or category name
- Prediction is typically longer than GT
- You want flexible matching

**Example:**
```python
GT: "piano"
Prediction: "This is a beautiful piano performance with classical elements"
Result: ✅ Match (because "piano" is in prediction)

GT: "piano"
Prediction: "Keyboard instrument playing"
Result: ❌ No match (word "piano" not present)
```

**Command:**
```bash
--match-mode contains
```

---

## Real-World Examples

### Example 1: ESC-50 Dataset (Sound Classification)

**Original Dataset Structure:**
```
ESC-50/
  audio/
    1-100032-A-0.wav    (dog bark)
    1-110389-A-0.wav    (rain)
    ...
  meta/
    esc50.csv           (contains labels)
```

**Convert to Mode 2:**
```
ESC-50/
  dog/
    1-100032-A-0.wav
    2-100032-A-0.wav
  rain/
    1-110389-A-0.wav
  chainsaw/
    ...
```

**Evaluate:**
```bash
python cli.py evaluate \
  --audio-dir ESC-50 \
  --use-folder-as-label \
  --prompt "What sound is this?" \
  --match-mode contains
```

---

### Example 2: AudioCaps (Audio Captioning)

**Original Structure:**
```
audiocaps/
  train/
    Y-08bBDa8j2f0.wav
    Y-08fgUC0kYg.wav
    ...
  captions.csv
```

**Convert to Mode 1:**
```
audiocaps/
  audio/
    clip001.wav
    clip002.wav
  labels/
    clip001.txt  → "A man speaks followed by laughter"
    clip002.txt  → "
