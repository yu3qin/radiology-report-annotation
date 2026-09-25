# scan all .txt report files
# extract each study ID safely
# stores the full report path
# cleans study_id
# keep only rows that have a matching report
# generate file with labels as ground truth and file without labels

import os
from pathlib import Path
import pandas as pd

reports = Path(r"C:\Users\Dell\Desktop\to_amanda\mimic-cxr-reports\files")
ground_truth = Path(r"C:\Users\Dell\Desktop\mimic_labeled_groundtruth.xlsx")

# Scan all report files in MIMIC
report_files = []

for root, dirs, files in os.walk(reports):
    for file in files:
        # Extract study_id correctly (example: s58054149.txt into 58054149)
        if file.endswith(".txt"):  # Select only reports text files
            study_id = file[1: -4] # Extract study id from file name
            report_path = os.path.join(root, file)
            
            # Get full file path of the report
            report_files.append({
                "study_id": study_id,
                "mimic_report_path" : report_path
            })

report_df = pd.DataFrame(report_files)

# Showing how many reports are found
print("Total reports found in MIMIC:", len(report_df))

# Load ground truth
gt = pd.read_excel(ground_truth)

# Clean study_id in both tables
gt["study_id"] = (
    gt["study_id"]
    .astype(str)
    .str.replace(".0", "", regex=False)
    .str.strip()
)

report_df["study_id"] = report_df["study_id"].astype(str).str.strip()

# Match the only reports that exist in both
matched = gt.merge(report_df, on="study_id", how="inner")

# Keep the necessary columns
matched = matched[
    [
        "mimic_report_path",
        "study_id",
        "Pneumothorax",
        "Pleural Effusion",
        "Pneumonia",
        "Atelectasis",
        "Edema",
        "Lung Metastasis"
    ]
]

# Rename the path column
matched = matched.rename(columns={"mimic_report_path": "report_path"})

print("Total matched reports:", len(matched))

# Save results
matched.to_excel(r"C:\Users\Dell\Desktop\mimic_feather_groundtruth685.xlsx", index=False)

no_labels = matched.copy()

label_columns = [
    "Pneumothorax",
    "Pleural Effusion",
    "Pneumonia",
    "Atelectasis",
    "Edema",
    "Lung Metastasis"
]

no_labels[label_columns] =""

no_labels.to_excel(r"C:\Users\Dell\Desktop\mimic_feather_685.xlsx", index=False)
print("File is saved successfully")