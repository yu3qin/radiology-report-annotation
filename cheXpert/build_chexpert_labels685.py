# Run after Ubuntu
# Produce final chexpert labels for 685 reports
import pandas as pd

# Load files
map_df = pd.read_csv(r"C:\Users\Dell\Desktop\chexpert_input_map685.csv")
chex = pd.read_csv(r"C:\Users\Dell\Desktop\chexpert_output685.csv")

# Check row counts
print("Rows in chex_input_map:", len(map_df))
print("Rows in chexpert_output:", len(chex))

# Check alignment
if len(map_df) != len(chex):
    raise ValueError("Row counts do not match")

# Combine row by row
merged = pd.concat(
    [map_df.reset_index(drop=True), chex.reset_index(drop=True)],
    axis=1
)

# Remove duplicate columns if any
merged = merged.loc[:, ~merged.columns.duplicated()].copy()

# Build label file
final_df = pd.DataFrame()
final_df["study_id"] = merged["study_id"]
final_df["report_path"] = merged["report_path"]

final_df["Pneumothorax"] = merged["Pneumothorax"]
final_df["Pleural Effusion"] = merged["Pleural Effusion"]
final_df["Pneumonia"] = merged["Pneumonia"]
final_df["Atelectasis"] = merged["Atelectasis"]
final_df["Pulmonary Edema"] = merged["Edema"]

# Leave blank because CheXpert does not label this
final_df["Lung Metastasis"] = ""

# Save original CheXpert labels
final_df.to_excel(r"C:\Users\Dell\Desktop\chexpert_labels685_original.xlsx", index=False)
print("Original CheXpert labels saved as chexpert_labels685_.xlsx")

# Create binary labels 
label_cols = ["Pneumothorax", "Pleural Effusion", "Pneumonia", "Atelectasis", "Pulmonary Edema"]
final_df_binary = final_df.copy()
for col in label_cols:
    final_df_binary[col] = final_df_binary[col].fillna(0)
    final_df_binary[col] = final_df_binary[col].replace(-1, 0)
    final_df_binary[col] = final_df_binary[col].astype(int)

# Save binary labels
final_df_binary.to_excel(r"C:\Users\Dell\Desktop\chexpert_labels685_binary.xlsx", index=False)
print("Binary CheXpert labels saved as chexpert_labels685_binary.xlsx")
