# Evaluation for 685 reports
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load files
pred_df = pd.read_excel(r"C:\Users\Dell\Desktop\chexpert_labels685.xlsx")
gt_df = pd.read_excel(r"C:\Users\Dell\Desktop\mimic_feather_groundtruth685.xlsx")

print("Pred rows:", len(pred_df))
print("Ground truth rows:", len(gt_df))

# Merge by study_id
merged = pred_df.merge(gt_df, on="study_id", suffixes=("_pred", "_gt"))

print("Matched rows:", len(merged))
print("Merged columns:")
print(merged.columns.tolist())

# prediction column -> ground truth column
label_map = {
    "Pneumothorax_pred": "Pneumothorax_gt",
    "Pleural Effusion_pred": "Pleural Effusion_gt",
    "Pneumonia_pred": "Pneumonia_gt",
    "Atelectasis_pred": "Atelectasis_gt",
    "Pulmonary Edema": "Edema"
}

results = []

for pred_col, gt_col in label_map.items():
    y_pred = pd.to_numeric(merged[pred_col], errors="coerce").fillna(0).replace(-1, 0).astype(int)
    y_true = pd.to_numeric(merged[gt_col], errors="coerce").fillna(0).replace(-1, 0).astype(int)

    acc = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    results.append({
        "Label": pred_col,
        "Accuracy": round(acc, 3),
        "Precision": round(precision, 3),
        "Recall": round(recall, 3),
        "F1": round(f1, 3)
    })

    print(f"\n{pred_col}")
    print("Accuracy :", round(acc, 3))
    print("Precision:", round(precision, 3))
    print("Recall   :", round(recall, 3))
    print("F1       :", round(f1, 3))

results_df = pd.DataFrame(results)
results_df.to_excel(r"C:\Users\Dell\Desktop\chexpert_evaluation_results685.xlsx", index=False)
merged.to_excel(r"C:\Users\Dell\Desktop\chexpert_vs_groundtruth_685.xlsx", index=False)

print("\nSaved: chexpert_evaluation_results685.xlsx")
print("Saved: chexpert_vs_groundtruth_685.xlsx")
print("\nSummary:")
print(results_df)