import pandas as pd
from radgraph import RadGraph, get_radgraph_processed_annotations

# Load extracted report text
# RadGraph usual input is just raw radiology report
df = pd.read_csv(r"C:\Users\Dell\Desktop\chexbert_input_map685.csv")

# Remove empty reports and make sure everything is text
df["label_text"] = df["label_text"].fillna("").astype(str).str.strip()
df = df[df["label_text"] != ""].copy()

# Load RadGraph model
radgraph = RadGraph(model_type="modern-radgraph-xl")

results = []

# Loop through each report one by one
for i, row in df.iterrows():
    report = row["label_text"]

    # Radgraph reads the report and extract raw info
    annotations = radgraph([report])
    # Converts raw output into structured format
    # Annotations includes observation, tags to show present or absent, and located at where
    processed = get_radgraph_processed_annotations(annotations)

    findings = []
    
    # Extract useful fields for each finding
    for item in processed["processed_annotations"]:
        observation = item["observation"]     # Which condition is found
        tags = item["tags"]                   # Definitely present / absent, uncertain  
        located_at = item["located_at"]       # Where is it located
        suggestive_of = item["suggestive_of"] # Diagnosis relationship
        
        # 
        findings.append({
            "observation": observation,
            "tags": tags,
            "located_at": located_at,
            "suggestive_of": suggestive_of
        })
    
    # Store full report result    
    results.append({
        "study_id": row["study_id"],
        "text": report,
        "radgraph_findings": findings
    })
    

# Output contains study id, text, and radgraph findings
out_df = pd.DataFrame(results)
out_df.to_csv(r"C:\Users\Dell\Desktop\radgraph_output_685.csv", index=False)

print("The output is saved to radgraph_output_685.csv")