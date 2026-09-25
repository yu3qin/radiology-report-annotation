# 685 reports in an excel file
# Extract the section [impression/findings/final section] that CheXpert should read
# Saves CheXpert input

import pandas as pd
import re
import os

# Load report dataset
df = pd.read_excel(r"C:\Users\Dell\Desktop\mimic_feather_685.xlsx")

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
    
def extract_sections(text):
    text = str(text)

    # Match section headers like IMPRESSION:, FINDINGS:, etc.
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

    # Impression
    if "impression" in sections and sections["impression"]:
        return sections["impression"], "impression"

    # Findings
    if "findings" in sections and sections["findings"]:
        return sections["findings"], "findings"

    # final section of report
    if len(sections) > 0:
        last_key = list(sections.keys())[-1]
        return sections[last_key], f"final_section:{last_key}"

    # fallback: whole report if no headers found
    return str(report_text).strip(), "full_report_fallback"

# Apply extraction to create label_text exactly for CheXpert input
df[["label_text", "section_used"]] = df["report_text"].apply(
    lambda x: pd.Series(choose_label_text(x))
)

# Clean text
df["label_text"] = df["label_text"].fillna("").astype(str).str.strip()
df = df[df["label_text"] != ""].copy()

# Save map file to reconnect with CheXpert output
map_df = df[["study_id", "report_path", "section_used", "label_text"]].copy()
map_df.to_csv(r"C:\Users\Dell\Desktop\chexpert_input_map685.csv", index=False)

# Save CheXpert input file
chex_input = df[["label_text"]].copy()
chex_input.to_csv(r"C:\Users\Dell\Desktop\chexpert_input685.csv", index=False, header=False)

print("Saved chexpert_input_map685.csv")
print("Saved chexpert_input685.csv")
print("Rows prepared for CheXpert:", len(df))
# After that run CheXpert in Ubuntu using chexpert input and chexpert output
