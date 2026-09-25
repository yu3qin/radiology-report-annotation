# About the project
Manual annotation of radiology reports is often labor intensive, costly and time-consuming in healthcare settings. This project aims to transform unstructured chest radiology report narratives into structured binary condition labels
using a combination of transformer models, graph parsers, and rule based methods. 

A total of six clinically relevant thoracic conditions were targeted and five automated annotation approaches were evaluated. The performance of these methods was benchmarked against radiologist reviewed ground truth on 685 chest radiology reports,
and providing a comprehensive assessment of automated radiology report labeling.


## Target Conditions

* Pneumothorax
* Pleural Effusion
* Pneumonia
* Atelectasis
* Pulmonary Edema
* Lung Metastasis


## Models Evaluated
1. **CheXpert Labeler**
Rule-based labeler using dependency parsing and predefined labeling rules
 
3. **CheXbert**
BERT-based transformer model designed specifically for radiology report classification
 
4. **RadBERT + Logistic Regression**
Embedding based deep learning model that generates specific radiology text embeddings using RadBERT
and logistic regression classifier for condition prediction
 
6. **RadGraph**
Deep learning model that extracts clinical entities and relations from radiology reports
 
7. **Regex Cascade**
Rule-based detector that uses a series of regex matching steps to detect Lung Metastasis, a condition not covered by standard labeling schemas
 
 
## Technical Workflow
1. **Extraction & Normalization**
Extract the `IMPRESSION` section from each report. If unavailable, use `FINDINGS` section instead
 
2. **Automated Annotation**
- Process report text through the selected annotation models
 
3. **Label Binarization**
Standardize outputs into binary labels with (`1 = Positive`, `0 = Negative / Uncertain / Blank`).
 
4. **Performance Evaluation**
Compare predictions against radiologist-reviewed ground truth using accuracy, precision, recall, and F1-score.


## Benchmark Results (n = 685)
| Model | Macro-Accuracy | Macro-Precision | Macro-Recall | Macro-F1 Score |
| :--- | :--:| :---: | :---: | :---: |
| **CheXbert (M2)**                    | **0.992** | **0.972** | **0.975** | **0.973** |
| **CheXpert (M1)**                    | 0.947 | 0.763 | 0.861 | 0.801 |
| **RadGraph (M4)**                    | 0.941 | 0.841 | 0.751 | 0.791 |
| **RadBERT + LR (M3)**                | 0.932 | 0.741 | 0.802 | 0.766 |
| **Metastasis Detector (M5, n = 40)** | 1.000 | 1.000 | 1.000 | 1.000 |


## F1-Score by Clinical Condition
| Condition | CheXpert | CheXbert | RadBERT+LR | RadGraph |
| :--- | :---: | :---: | :---: | :---: |
| **Pneumothorax** | 0.708 | **0.961** | 0.719 | 0.845 |
| **Pleural Effusion** | 0.925 | **0.985** | 0.897 | 0.880 |
| **Pneumonia** | 0.536 | **0.954** | 0.477 | 0.443 |
| **Atelectasis** | 0.947 | **0.985** | 0.883 | 0.908 |
| **Pulmonary Edema** | 0.890 | **0.982** | 0.853 | 0.881 |
 
 
## Key Findings

1. CheXbert performed the best overall, achieving a **Macro-F1 score of 0.973** across the evaluated conditions and demonstrated its strong contextual understanding of radiology-specific language and uncertainty expressions
2. Automated annotation pipelines can reduce the need for manual report labeling, making it easier to build larger datasets for clinical AI research
3. The regex cascade was able to identify rare findings such as **lung metastasis** which are not covered by the other annotation methods
4. Rule-based methods could have a lower performance when interpreting ambiguous statements such as *"cannot exclude pneumonia"* hence impacting pneumonia detection.

## Note
- The evaluation was conducted on limited numbers of radiologist-reviewed chest radiology reports. Access to a larger annotated datasets would allow more robust benchmarking,
evaluation, and validation of the models, while also enabling the prediction and assessment of a wider range of clinical conditions

- Each folder contains the input data, model outputs and evaluation results of its respective model
