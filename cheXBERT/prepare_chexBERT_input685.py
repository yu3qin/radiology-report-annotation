# CheXbert pipeline
# Read report text
# Extract impression/findings/final section
# Save them into a new excel sheet with added column 'Report impression'
# Run chexbert then get label reports.csv

import pandas as pd
import re
import os

# Load report dataset with 685 reports
df = pd.read_excel(r"C:\Users\Dell\Desktop\mimic_feather_685.xlsx")

# Read reports
def read_report(path):
    if pd.isna(path) or str(path).strip() == "":
        return ""
    path = str(path).strip()
    if not os.path.exists(path):
        return ""
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read().strip()
    except:
        return ""

df["report_text"] = df["report_path"].apply(read_report)

print("Reports with text:", (df["report_text"].str.len() > 0).sum())
print("Reports without text:", (df["report_text"].str.len() == 0).sum())

def extract_sections(text):
    text = str(text)
    pattern = re.compile(
        r'(?ims)^\s*([A-Z ][A-Z /_-]{1,40})\s*:\s*(.*?)(?=^\s*[A-Z ][A-Z /_-]{1,40}\s*:|\Z)'
    )

    sections = {}
    for header, content in pattern.findall(text):
        key = " ".join(header.strip().lower().split())
        sections[key] = content.strip()

    return sections

def choose_label_text(report_text):
    sections = extract_sections(report_text)

    if "impression" in sections and sections["impression"]:
        return sections["impression"], "impression"

    if "findings" in sections and sections["findings"]:
        return sections["findings"], "findings"

    if len(sections) > 0:
        last_key = list(sections.keys())[-1]
        return sections[last_key], f"final_section:{last_key}"

    return str(report_text).strip(), "full_report_fallback"

df[["label_text", "section_used"]] = df["report_text"].apply(
    lambda x: pd.Series(choose_label_text(x))
)

df["label_text"] = df["label_text"].fillna("").astype(str).str.strip()
df = df[df["label_text"] != ""].copy()

# Save map file for reconnecting later
map_df = df[["study_id", "report_path", "section_used", "label_text"]].copy()
map_df.to_csv(r"C:\Users\Dell\Desktop\chexbert_input_map685.csv", index=False)

# Save CheXbert input with required columns
chexbert_input = df[["label_text"]].copy()
chexbert_input = chexbert_input.rename(columns={"label_text": "Report Impression"})
chexbert_input.to_csv(r"C:\Users\Dell\Desktop\chexbert_input685.csv", index=False)

print("Saved: chexbert_input_map685.csv")
print("Saved: chexbert_input685.csv")
print("Rows prepared for CheXbert:", len(df))