# Converts into labels of (-1, 0 and 1) and binary labels (0, 1)
import pandas as pd
import ast

# Load RadGraph output (which only contains text)
df = pd.read_csv(r"C:\Users\Dell\Desktop\radgraph_output_685.csv")

# If report_path is not in Radgraph output, load it from original map file
if "report_path" not in df.columns:
    map_df = pd.read_csv(r"C:\Users\Dell\Desktop\chexbert_input_map685.csv")
    df = df.merge(map_df[["study_id", "report_path"]], on="study_id", how="left")
    
# Target conditions and keywords
condition_keywords = {
    "Pneumothorax":     ["pneumothorax", "air in pleural space", "gas in pleural space", "pneumothoraces"],
    "Pleural Effusion": ["effusion", "pleural effusion", "blunted costophrenix angles", "fluid in pleural space", "pleural fluid"],
    "Pneumonia":        ["pneumonia", "airspace disease", "consolidation", "infiltrate", "obscured vascular markings", "infection", 
                         "infectious process"],
    "Atelectasis":      ["atelectasis", "atelecta", "collapse"],
    "Edema":            ["edema", "pulmonary edema", "heart failure", "chf", "vascular congestion", "pulmonary congestion", 
                         "industinctness", "vascular prominence"],
    "Lung Metastasis":  ["metastasis", "metastases", "metastatic", "pulmonary metastases", "metastatic disease"]
}

# CONVERTS Radgraph certain tags into numeric labels
def convert_tag_to_label(tags):
    tags = str(tags).lower()

    if "definitely present" in tags:   # 1 = present
        return 1
    elif "definitely absent" in tags:  # 0 = absent
        return 0
    elif "uncertain" in tags:          # -1 = uncertain
        return -1
    else:
        return None                    # tag does not match with any category

# CONVERTS RadGraph findings for a single report into a label for a specific condition
def get_condition_label(findings_text, keywords):
    try:
        findings = ast.literal_eval(findings_text)
    except:
        return None     # if parsing fails return None

    final_label = None  # Default label if uncertain or absent

    for item in findings:
        observation = str(item.get("observation", "")).lower()
        tags = item.get("tags", [])

        if any(keyword in observation for keyword in keywords):
            label = convert_tag_to_label(tags) # Convert tag to numeric labels

            # Priority: positive > uncertain > negative
            if label == 1:
                return 1
            elif label == -1:
                final_label = -1  # Keep uncertain labels when no positive found
            elif label == 0 and final_label is None:
                final_label = 0

    return final_label

# Create label columns
for condition, keywords in condition_keywords.items():
    df[condition] = df["radgraph_findings"].apply(get_condition_label, keywords=keywords)
    
# Keep only columns    
label_columns = list(condition_keywords.keys())
output_df = df[["report_path", "study_id"] + label_columns].copy()

# Save labels with -1, 0, 1
output_df.to_csv(r"C:\Users\Dell\Desktop\radgraph_labels_685.csv", index=False)
print("Labels are saved to radgraph_labels_685.csv")

# CONVERT into binary labels
output_df_binary = output_df.copy()
for col in label_columns:
    # Convert -1 or 0 → 0, 1 → 1
    output_df_binary[col] = output_df_binary[col].apply(lambda x: 1 if x == 1 else 0)

output_df_binary.to_csv(r"C:\Users\Dell\Desktop\radgraph_binary_labels685.csv", index=False)
print("Binary labels are saved to radgraph_binary_labels685.csv")