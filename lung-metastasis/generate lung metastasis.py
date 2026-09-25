import pandas as pd
import os
import re

# Load the dataset with 685 report paths
df = pd.read_excel(r"C:\Users\Dell\Desktop\mimic_feather_685.xlsx")

# Read the report content from the file paths
def read_report(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except:
        return ""  # If the report cannot be read, return an empty string

# Keep only the reports that exist in the system
df["exists"] = df["report_path"].apply(os.path.exists)
df = df[df["exists"]].copy()

# Read the report text into a new column
df["report_text"] = df["report_path"].apply(read_report)

# Detection function to find lung metastasis
def detect_lung_metastasis(text):
    text = str(text).lower()

    # Define patterns for negative, uncertain, and positive detections
    negative_patterns = [
        r'no evidence of .*metastasis',
        r'no .*metastasis',
        r'without .*metastasis',
        r'negative for .*metastasis',
        r'rule out metastasis',
        r'no pulmonary metastasis',
    ]
    
    uncertain_patterns = [
        r'history of metastasis',
        r'known metastasis',
        r'concern for metastasis',
        r'possible metastasis',
        r'cannot exclude metastasis',
        r'suspicious for metastasis',
        r'evaluate .*metastasis',
    ]
    
    positive_patterns = [
        r'pulmonary metastasis',
        r'lung metastasis',
        r'pulmonary metastases',
        r'lung metastases',
        r'metastases',
        r'metastastic',
        r'known metastatic',
        r'pulmonary nodules .*metastasis',
        r'nodular opacities .*metastasis',
        r'innumerable .*nodules .*metastasis',
    ]

    # Check negative patterns
    for pat in negative_patterns:
        if re.search(pat, text):
            return 0  # No lung metastasis

    # Check uncertain patterns (treat these as no definite metastasis)
    for pat in uncertain_patterns:
        if re.search(pat, text):
            return 0  # Uncertain or history, mark as no metastasis

    # Check for positive lung metastasis patterns
    for pat in positive_patterns:
        if re.search(pat, text):
            return 1  # Lung metastasis found

    return 0  # If no patterns are found, return 0 (no metastasis)

# Apply lung metastasis detection
df["lung_metastasis"] = df["report_text"].apply(detect_lung_metastasis)

# Count how many reports have lung metastasis detected
lung_metastasis_count = df["lung_metastasis"].sum()
print(f"Number of reports detected with lung metastasis: {lung_metastasis_count}")

# Filter for reports with lung metastasis detected
lung_metastasis_reports = df[df["lung_metastasis"] == 1]

# Save the lung metastasis reports
lung_metastasis_reports[["study_id", "report_path", "lung_metastasis"]].to_excel(
    r"C:\Users\Dell\Desktop\lung_metastasis_detected.xlsx", index=False
)

print("Report is saved to lung_metastasis_detected.xlsx")