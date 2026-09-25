import pandas as pd
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score

# Load CheXpert binary labels dataset
# Selected CheXpert labels because their labels are validated against expert radiologists
df_labels = pd.read_excel("chexpert_labels685.xlsx")                   # CheXpert labels for 5 conditions
df_input = pd.read_csv("chexpert_input_map685.csv")                    # Report text from CheXpert input
df_groundtruth = pd.read_excel("mimic_feather_groundtruth685.xlsx")    # Ground truth evaluation file for 5 conditions
df_lung = pd.read_csv("lung_metastasis40.csv")                         # Lung metastasis ground truth (40 reports)

# Prepare report text
# Use 'label_text' as the report text for RadBERT
df_input["report_text"] = df_input["label_text"].fillna("").astype(str).str.strip()
df_input['index'] = df_input.index

# Load RadBERT
model_name = "StanfordAIMI/RadBERT"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)
model.eval()

# Function to generate embeddings
def get_embedding(text):

    inputs = tokenizer(text, return_tensors="pt",
        truncation=True,
        padding="max_length",
        max_length=128
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
    embedding = outputs.last_hidden_state[:, 0, :]
    return embedding.squeeze().cpu().numpy()

# Generate embeddings
embeddings = []

for text in df_input["report_text"]:
    emb = get_embedding(text)
    embeddings.append(emb)

X = np.vstack(embeddings)

print(f"Embeddings shape: {X.shape}")

# RadBERT + LogisticRegression only outputs binary labels (0 and 1).
# Ground truth will be converted to binary (−1 → 0) for fair evaluation.
# One prediction output file is produced
results = df_input[["study_id", "report_path"]].copy()
 
# Evaluation results
eval_results = []
 
# CONDITIONS
chexpert_conditions = [
    "Pneumothorax",
    "Pleural Effusion",
    "Pneumonia",
    "Atelectasis",
    "Pulmonary Edema"
]
 
# Map condition names to ground truth column names where they differ
groundtruth_col_map = {
    "Pulmonary Edema": "Edema"
}
 
# TRAIN CLASSIFIERS
for condition in chexpert_conditions:
 
    print(f"\nTraining RadBERT classifier for {condition}...")
 
    # Training labels from CheXpert (−1, 0, 1) → convert −1 to 0 for binary training
    y_original = df_labels[condition].fillna(0).astype(int).values
    y_binary   = np.where(y_original == -1, 0, y_original)
 
    # Train / test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_binary, test_size=0.2, random_state=42, stratify=y_binary
    )
 
    # Train classifier
    classifier = LogisticRegression(max_iter=1000)
    classifier.fit(X_train, y_train)
 
    # Predict on all data (binary output: 0 or 1)
    y_pred = classifier.predict(X)
 
    # Save predictions to single output dataframe
    results[condition] = y_pred
 
    # EVALUATION: ground truth converted to binary (−1 to 0)
    gt_col        = groundtruth_col_map.get(condition, condition)
    y_true        = df_groundtruth[gt_col].fillna(0).astype(int).values
    y_true_binary = np.where(y_true == -1, 0, y_true)
 
    # Compute all metrics
    acc       = accuracy_score(y_true_binary, y_pred)
    precision = precision_score(y_true_binary, y_pred, zero_division=0)
    recall    = recall_score(y_true_binary, y_pred, zero_division=0)
    f1        = f1_score(y_true_binary, y_pred, zero_division=0)
 
    eval_results.append({
        "Condition": condition,
        "Accuracy":  round(acc, 4),
        "Precision": round(precision, 4),
        "Recall":    round(recall, 4),
        "F1 Score":  round(f1, 4),
    })
 
    print(f"Accuracy for {condition}: {acc:.4f}")
    print(classification_report(y_true_binary, y_pred, zero_division=0))
 
# LUNG METASTASIS
print("\nTraining RadBERT classifier for Lung Metastasis...")
 
lung_map = dict(zip(df_lung["study_id"], df_lung["lung_metastasis"]))
y_lung   = df_input["study_id"].map(lung_map).fillna(0).astype(int).values
 
X_train, X_test, y_train, y_test = train_test_split(
    X, y_lung, test_size=0.2, random_state=42, stratify=y_lung
)
 
classifier = LogisticRegression(max_iter=1000)
classifier.fit(X_train, y_train)

y_pred_all = classifier.predict(X)
 
results["Lung_Metastasis"] = y_pred_all
 
y_true_lung = y_lung
acc         = accuracy_score(y_true_lung, y_pred_all)
precision   = precision_score(y_true_lung, y_pred_all, zero_division=0)
recall      = recall_score(y_true_lung, y_pred_all, zero_division=0)
f1          = f1_score(y_true_lung, y_pred_all, zero_division=0)
 
eval_results.append({
    "Condition": "Lung Metastasis",
    "Accuracy":  round(acc, 4),
    "Precision": round(precision, 4),
    "Recall":    round(recall, 4),
    "F1 Score":  round(f1, 4),
})
 
print(f"\nAccuracy for Lung Metastasis: {acc:.4f}")
print(classification_report(y_true_lung, y_pred_all, zero_division=0))
 
# SAVE OUTPUT FILES
# Single prediction output
results.to_csv("radbert_predictions.csv", index=False)
 
# Full evaluation results with all metrics
eval_df = pd.DataFrame(eval_results)
eval_df.to_excel("radbert_evaluation_results.xlsx", index=False)
 
print("\nRadBERT has completed predictions and evaluation.")