# Run after Command prompt
# Command prompt produce the overall detected conditions
# Produce final chexbert labels for 685 reports with 6 conditions
import pandas as pd

# Load files
map_df = pd.read_csv(r"C:\Users\Dell\Desktop\chexbert_input_map685.csv")
chexbert = pd.read_csv(r"C:\Users\Dell\Desktop\chexbert_output685\labeled_reports.csv")

print("Map rows:", len(map_df))
print("CheXbert rows:", len(chexbert))

# Check alignment
if len(map_df) != len(chexbert):
    raise ValueError("Row mismatch!")

# Combine row by row and merge by index 
merged = pd.concat(
    [map_df.reset_index(drop=True), chexbert.reset_index(drop=True)],
    axis=1
)

# Build label file with necessary columns
final_df = pd.DataFrame()

final_df["study_id"] = merged["study_id"]
final_df["report_path"] = merged["report_path"]

# Include the 6 conditions
final_df["Pneumothorax"] = merged["Pneumothorax"]
final_df["Pleural Effusion"] = merged["Pleural Effusion"]
final_df["Pneumonia"] = merged["Pneumonia"]
final_df["Atelectasis"] = merged["Atelectasis"]
final_df["Pulmonary Edema"] = merged["Edema"]

# CheXbert does NOT label this
final_df["Lung Metastasis"] = ""

# Save
final_df.to_excel(r"C:\Users\Dell\Desktop\chexBERT_labels685.xlsx", index=False)
print("chexBERT_labels685.xlsx is saved")

# Convert CheXpert output to binary labels
label_cols = [
   "Pneumothorax",
   "Pleural Effusion",
   "Pneumonia",
   "Atelectasis",
   "Pulmonary Edema"
]

final_df_binary = final_df.copy()
for col in label_cols:
    final_df_binary[col] = final_df_binary[col].fillna(0)
    final_df_binary[col] = final_df_binary[col].replace(-1, 0)
    final_df_binary[col] = final_df_binary[col].astype(int)

# Save binary labels
final_df_binary.to_excel(r"C:\Users\Dell\Desktop\chexBERT_labels685_binary.xlsx", index=False)
print("Binary labels saved as chexBERT_labels685_binary.xlsx")
