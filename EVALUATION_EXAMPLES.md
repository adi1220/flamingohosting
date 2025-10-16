# Evaluation Examples

This document shows practical examples of both evaluation modes.

## Mode 1: Separate Ground Truth Files

### Use Case: Audio Captioning Evaluation

You have audio files and detailed ground truth descriptions in separate text files.

**Directory Structure:**
```
my_dataset/
  audio/
    ├── recording001.wav
    ├── recording002.mp3
    └── recording003.flac
  
  labels/
    ├── recording001.txt
    ├── recording002.txt
    └── recording003.txt
```

**Example Files:**

`audio/recording001.wav` - Contains a conversation  
`labels/recording001.txt` - "Two people discussing vacation plans in a restaurant"

`audio/recording002.mp3` - Contains music  
`labels/recording002.txt` - "Classical piano music with slow tempo and melancholic mood"

**Run Evaluation:**

```bash
# CLI
python cli.py evaluate \
  --audio-dir my_dataset/audio \
  --gt-dir my_dataset/labels \
  --prompt "Please describe the audio in detail." \
  --match-mode exact

# Python API
import audio_flamingo_runner as runner

model = runner.load_model()

result = runner.evaluate_folder(
    audio_dir="my_dataset/audio",
    gt_dir="my_dataset/labels",
    model_bundle=model,
    prompt="Please describe the audio in detail.",
    match_mode="exact"
)

print(f"Accuracy: {result['summary']['f1']:.2%}")
```

**Output:**
```json
{
  "summary": {
    "count": 3,
    "tp": 2,
    "fp": 1,
    "fn": 1,
    "precision": 0.6667,
    "recall": 0.6667,
    "f1": 0.6667
  },
  "details": [
    {
      "file": "recording001.wav",
      "pred": "two people discussing vacation plans in a restaurant",
      "gt": "Two people discussing vacation plans in a restaurant",
      "match": 1
    }
  ]
}
```

---

## Mode 2: Folder Names as Labels

### Use Case 1: Instrument Classification

You have audio files organized by instrument type.

**Directory Structure:**
```
instruments/
  ├── piano/
  │   ├── bach_prelude.mp3
  │   ├── chopin_nocturne.wav
  │   └── beethoven_sonata.flac
  ├── guitar/
  │   ├── spanish_romance.mp3
  │   ├── classical_gas.wav
  │   └── flamenco.mp3
  ├── violin/
  │   ├── paganini.wav
  │   └── vivaldi.mp3
  └── drums/
      ├── rock_beat.wav
      └── jazz_groove.mp3
```

**Run Evaluation:**

```bash
# CLI with "contains" matching
python cli.py evaluate \
  --audio-dir instruments \
  --use-folder-as-label \
  --prompt "What instrument is playing in this audio?" \
  --match-mode contains

# Python API
result = runner.evaluate_folder(
    audio_dir="instruments",
    gt_dir=None,  # Not needed
    model_bundle=model,
    prompt="What instrument is playing in this audio?",
    match_mode="contains",
    use_folder_as_label=True
)
```

**Why "contains" mode?**

With `contains` mode:
- GT: `piano`
- Prediction: "This is a beautiful piano performance with classical style"
- Result: ✅ Match (because "piano" is in the prediction)

With `exact` mode, the above would NOT match because the prediction is longer than just "piano".

**Output Example:**
```json
{
  "summary": {
    "count": 9,
    "tp": 8,
    "fp": 1,
    "fn": 1,
    "precision": 0.8889,
    "recall": 0.8889,
    "f1": 0.8889
  },
  "details": [
    {
      "file": "piano/bach_prelude.mp3",
      "pred": "This is a piano playing a classical piece",
      "gt": "piano",
      "match": 1
    },
    {
      "file": "guitar/spanish_romance.mp3",
      "pred": "Acoustic guitar performing a romantic melody",
      "gt": "guitar",
      "match": 1
    },
    {
      "file": "drums/rock_beat.wav",
      "pred": "Electric guitar with distortion",
      "gt": "drums",
      "match": 0
    }
  ]
}
```

---

### Use Case 2: Sound Scene Classification

**Directory Structure:**
```
soundscapes/
  ├── indoor/
  │   ├── office_chatter.wav
  │   ├── kitchen_sounds.mp3
  │   └── living_room.wav
  ├── outdoor/
  │   ├── street_traffic.mp3
  │   ├── park_birds.wav
  │   └── beach_waves.mp3
  ├── nature/
  │   ├── forest_birds.wav
  │   ├── rain.mp3
  │   └── thunder.wav
  └── urban/
      ├── subway.wav
      ├── construction.mp3
      └── crowd.wav
```

**Run Evaluation:**

```bash
python cli.py evaluate \
  --audio-dir soundscapes \
  --use-folder-as-label \
  --prompt "Is this audio recorded indoors, outdoors, in nature, or in an urban setting?" \
  --match-mode contains
```

---

### Use Case 3: Genre Classification

**Directory Structure:**
```
music/
  ├── jazz/
  │   ├── miles_davis_style.mp3
  │   ├── bebop.wav
  │   └── smooth_jazz.mp3
  ├── classical/
  │   ├── mozart.wav
  │   ├── bach.mp3
  │   └── beethoven.flac
  ├── rock/
  │   ├── classic_rock.mp3
  │   ├── hard_rock.wav
  │   └── indie_rock.mp3
  └── electronic/
      ├── techno.wav
      ├── house.mp3
      └── ambient.wav
```

**Run Evaluation:**

```bash
python cli.py evaluate \
  --audio-dir music \
  --use-folder-as-label \
  --prompt "What genre is this music?" \
  --match-mode contains \
  --max-new-tokens 64
```

---

## REST API Examples

### Mode 1: With Separate GT Files

```bash
curl -X POST http://127.0.0.1:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "audio_dir": "/home/user/my_dataset/audio",
    "gt_dir": "/home/user/my_dataset/labels",
    "prompt": "Please describe the audio in detail.",
    "max_new_tokens": 128,
    "match_mode": "exact"
  }'
```

### Mode 2: Folder Names as Labels

```bash
curl -X POST http://127.0.0.1:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "audio_dir": "/home/user/instruments",
    "use_folder_as_label": true,
    "prompt": "What instrument is playing?",
    "max_new_tokens": 64,
    "match_mode": "contains"
  }'
```

**Response:**
```json
{
  "summary": {
    "count": 9,
    "tp": 8,
    "fp": 1,
    "fn": 1,
    "precision": 0.8889,
    "recall": 0.8889,
    "f1": 0.8889
  },
  "details": [...]
}
```

---

## Python API Complete Example

```python
import audio_flamingo_runner as runner
from pathlib import Path

# Load model once
print("Loading model...")
model = runner.load_model(model_dir="/path/to/audio-flamingo-3")

# Example 1: Evaluate with separate GT files
print("\n=== Evaluation Mode 1: Separate GT Files ===")
result1 = runner.evaluate_folder(
    audio_dir="datasets/audio_captions/audio",
    gt_dir="datasets/audio_captions/labels",
    model_bundle=model,
    prompt="Please describe the audio in detail.",
    match_mode="exact"
)

print(f"Total files: {result1['summary']['count']}")
print(f"F1 Score: {result1['summary']['f1']:.2%}")

# Example 2: Evaluate with folder names as labels (instrument classification)
print("\n=== Evaluation Mode 2: Folder Names as Labels ===")
result2 = runner.evaluate_folder(
    audio_dir="datasets/instruments",
    gt_dir=None,  # Not needed
    model_bundle=model,
    prompt="What instrument is playing in this audio?",
    match_mode="contains",  # Use contains since GT is just "piano" but pred might be "piano playing classical music"
    use_folder_as_label=True
)

print(f"Total files: {result2['summary']['count']}")
print(f"Precision: {result2['summary']['precision']:.2%}")
print(f"Recall: {result2['summary']['recall']:.2%}")
print(f"F1 Score: {result2['summary']['f1']:.2%}")

# Show some examples
print("\nSample predictions:")
for detail in result2['details'][:3]:
    print(f"\nFile: {detail['file']}")
    print(f"GT: {detail['gt']}")
    print(f"Prediction: {detail['pred']}")
    print(f"Match: {'✓' if detail['match'] else '✗'}")
```

---

## Tips for Best Results

### 1. Choose the Right Match Mode

**Use `exact` when:**
- Ground truth is a full sentence/description
- You want strict matching
- Example: GT = "A piano playing classical music" should match exactly

**Use `contains` when:**
- Ground truth is a keyword or category
- Model output is typically longer than GT
- Example: GT = "piano" should match "This is a piano performance"

### 2. Craft Effective Prompts

**For Instrument Classification:**
```
"What instrument is playing in this audio?"
"Identify the primary instrument."
```

**For Scene Classification:**
```
"Is this audio recorded indoors or outdoors?"
"What type of environment is this?"
```

**For Genre Classification:**
```
"What genre is this music?"
"Classify the musical style."
```

**For General Description:**
```
"Please describe the audio in detail."
"What can you hear in this audio?"
```

### 3. Normalization is Automatic

Both prediction and ground truth are automatically normalized:
- Converted to lowercase
- Whitespace trimmed
- Multiple spaces collapsed to single space

So these are equivalent:
- GT: `"Piano"` → normalized: `"piano"`
- Prediction: `"  PIANO  "` → normalized: `"piano"`
- Result: ✅ Match

### 4. File Naming

**Mode 1 (Separate GT files):**
- Audio: `sample001.wav` → GT: `sample001.txt` ✅
- Audio: `sample001.mp3` → GT: `sample001.txt` ✅
- Audio: `clip-05.wav` → GT: `clip-05.txt` ✅

**Mode 2 (Folder names):**
- Any filenames work, only folder name matters
- `piano/anything.wav` → GT = "piano"
- `guitar/xyz123.mp3` → GT = "guitar"

---

## Common Pitfalls

### ❌ Wrong: Mismatch between prompt and GT

```bash
# BAD: Asking for genre but GT has instrument names
python cli.py evaluate \
  --audio-dir instruments \
  --use-folder-as-label \
  --prompt "What genre is this?" \
  # Folder names: piano, guitar, drums
```

### ✅ Correct: Prompt matches what GT represents

```bash
# GOOD: Asking for instrument and GT has instrument names
python cli.py evaluate \
  --audio-dir instruments \
  --use-folder-as-label \
  --prompt "What instrument is playing?"
  # Folder names: piano, guitar, drums
```

### ❌ Wrong: Using exact mode with keyword GTs

```bash
# BAD: GT is "piano" but model says "piano playing music"
python cli.py evaluate \
  --audio-dir instruments \
  --use-folder-as-label \
  --prompt "What instrument is playing?" \
  --match-mode exact  # Will fail!
```

### ✅ Correct: Using contains mode with keyword GTs

```bash
# GOOD: GT is "piano", model says "piano playing music" → Match!
python cli.py evaluate \
  --audio-dir instruments \
  --use-folder-as-label \
  --prompt "What instrument is playing?" \
  --match-mode contains  # Will match!
```

---

## Advanced: Mixed Evaluation

You can also manually combine results from multiple evaluations:

```python
import audio_flamingo_runner as runner

model = runner.load_model()

# Evaluate multiple datasets
datasets = [
    ("instruments", "What instrument is playing?", "contains"),
    ("genres", "What genre is this music?", "contains"),
    ("scenes", "What environment is this?", "contains")
]

overall_tp = 0
overall_count = 0

for audio_dir, prompt, mode in datasets:
    result = runner.evaluate_folder(
        audio_dir=audio_dir,
        gt_dir=None,
        model_bundle=model,
        prompt=prompt,
        match_mode=mode,
        use_folder_as_label=True
    )
    
    overall_tp += result['summary']['tp']
    overall_count += result['summary']['count']
    
    print(f"{audio_dir}: F1={result['summary']['f1']:.2%}")

overall_accuracy = overall_tp / overall_count if overall_count > 0 else 0
print(f"\nOverall Accuracy: {overall_accuracy:.2%}")
```

---

## Exporting Results

All evaluation results are automatically saved as JSON. You can then process them:

```python
import json
import pandas as pd

# Load results
with open('evaluation_results.json', 'r') as f:
    results = json.load(f)

# Convert to DataFrame for analysis
df = pd.DataFrame(results['details'])

# Analyze per-category performance
if 'file' in df.columns:
    df['category'] = df['file'].apply(lambda x: x.split('/')[0])
    category_accuracy = df.groupby('category')['match'].mean()
    print(category_accuracy)

# Find all mistakes
mistakes = df[df['match'] == 0]
print(f"\nMistakes ({len(mistakes)}):")
for _, row in mistakes.iterrows():
    print(f"\nFile: {row['file']}")
    print(f"Expected: {row['gt']}")
    print(f"Got: {row['pred']}")
```
