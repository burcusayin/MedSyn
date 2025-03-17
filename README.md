# MedSyn

## 1. Set Up Your Environment. Make sure you have python >= 3.11 

### Create virtual environment
```
python3 -m venv venv
source venv/bin/activate
```
### Install dependencies
```
pip install -r requirements.txt
```

## 2. Download MIMIC-IV and MIMIC-IV-Note datasets and prepare your test set.

Use ```src/preprocess_mimicIV.py``` to prepare your test set and put it under dataset/ directory.

## 3. Run the baseline experiments.

Use the script below. Please make sure you give the correct path for the dataset.
```
scripts/baseline.sh
```
## 4. Run the two-agent experiments.
Use the script below. Please make sure you give the correct path for the dataset.
```
scripts/dialogue.sh
```

## 5. Evaluate results.

You can use ```scripts/eval_icd_codes.sh``` and ```scripts/multi_turn_analysis.sh``` to analyze the results.
