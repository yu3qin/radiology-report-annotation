# MIMIC Report Matching & Preprocessing

This script (`mimic_report_matching688.py`) links local MIMIC radiology report text files with their corresponding radiologist ground-truth labels.

## How It Works

1. **Scans Local Files**: Iterates through the local MIMIC folder, extracts the `study_id` from each filename (e.g., `s58054149.txt` $\rightarrow$ `58054149`), and records the full file paths.
2. **Cleans & Matches Data**: Loads the ground-truth Excel file, fixes formatting issues in `study_id` (strips `.0` artifacts), and runs an inner join to pair reports with their metadata.
3. **Filters Columns**: Retains only key columns needed for analysis (`study_id`, `report_path`, and the 6 target clinical conditions).

## Matching Results

* **Original test set**: 687 reports
* **Successfully matched**: **685 reports (99.7%)**
* **Excluded**: 2 reports (missing from local storage)

## Outputs

* `mimic_feather_groundtruth685.xlsx` — Full ground-truth data (paths + condition labels).
* `mimic_feather_685.xlsx` — Cleaned input dataset with labels removed, used to feed downstream labellers.

## Usage

```bash
python mimic_report_matching688.py
