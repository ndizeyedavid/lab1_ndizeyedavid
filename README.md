# Lab 1: Grade Evaluator & Archiver

## Overview

This project contains two scripts that work together to evaluate student grades from a CSV file and archive results for record-keeping.

- **`grade-evaluator.py`**: Reads `grades.csv`, validates scores and weights, computes GPA, determines Pass/Fail status, and identifies resubmission candidates.
- **`organizer.sh`**: Archives the current `grades.csv` with a timestamp into an `archive/` folder, creates a fresh `grades.csv`, and logs the operation.

## Files

| File                 | Description                                       |
| -------------------- | ------------------------------------------------- |
| `grade-evaluator.py` | Python grade evaluation application               |
| `organizer.sh`       | Bash archive and reset script                     |
| `.gitignore`         | Prevents emacs temp files from reaching this repo |

## How to Run

### First clone the repo

```bash
git clone https://github.com/ndizeyedavid/lab1_ndizeyedavid
```

### Run The Python Application

```bash
python3 grade-evaluator.py
```

The script will prompt you to enter a CSV filename (e.g., `grades.csv`). It then validates and processes the data, printing the results to the terminal.

### Run Bash Archive Script

```bash
chmod +x organizer.sh
./organizer.sh
```

The script moves `grades.csv` into `archive/grades_<YYYYMMDD-HHMMSS>.csv`, creates a new empty `grades.csv`, and appends a log entry to `organizer.log`.

## `grade-evaluator.py`: What It Does

1. **File Existence & Empty Check**: Verifies the CSV file exists and is not empty. Exits gracefully with a message if missing or empty.
2. **Data Validation**: Ensures all scores are between 0–100 and that weights sum correctly (Formative = 60, Summative = 40, Total = 100).
3. **Grade Calculations**: Computes weighted scores, category percentages, and GPA (out of 5.0).
4. **Pass/Fail Decision**: Student passes **only if** both Formative ≥ 50% AND Summative ≥ 50%.
5. **Resubmission Logic**: Identifies failed Formative assignments with the highest weight for resubmission.

## `organizer.sh`: What It Does

1. Checks if an `archive/` directory exists; creates one if not.
2. Generates a timestamp in `YYYYMMDD-HHMMSS` format.
3. Moves `grades.csv` → `archive/grades_<timestamp>.csv`.
4. Creates a fresh, empty `grades.csv` with `touch`.
5. Appends a log entry to `organizer.log` with the timestamp, original filename, and archived filename.
