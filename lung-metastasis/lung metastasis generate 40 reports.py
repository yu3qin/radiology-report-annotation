# Create 40 reports for lung metastasis (ground truth)
# with 7 LM reports and 33 additional reports that dont have LM
import pandas as pd

# Load MIMIC-Feather 685 dataset
df_mimic = pd.read_excel(r"C:\Users\Dell\Desktop\mimic_feather_685.xlsx")

# Load identified lung metastasis reports
df_positive = pd.read_excel(r"C:\Users\Dell\Desktop\lung_metastasis_reports.xlsx")

# Extract the study_ids for the 7 positive reports
positive_ids = df_positive['study_id'].tolist()

# Create lung_metastasis column: 1 if in positive_ids, else 0
df_mimic['lung_metastasis'] = df_mimic['study_id'].apply(lambda x: 1 if x in positive_ids else 0)

# Keep only necessary columns
df_mimic = df_mimic[['study_id', 'report_path', 'lung_metastasis']]

# Filter positive and negative reports
lm_positive = df_mimic[df_mimic['lung_metastasis'] == 1]
lm_negative = df_mimic[df_mimic['lung_metastasis'] == 0]

# Randomly sample 33 negatives to combine with the 7 positives
lm_negative_sample = lm_negative.sample(n=33, random_state=42)

# Combine positives + sampled negatives
lm_40 = pd.concat([lm_positive, lm_negative_sample])

# Shuffle and reset index
lm_40 = lm_40.sample(frac=1, random_state=42).reset_index(drop=True)

# Save the final 40-report dataset
lm_40.to_csv(r"C:\Users\Dell\Desktop\lung_metastasis40.csv", index=False)

print("Dataset saved to lung_metastasis40.csv")
