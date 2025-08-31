import json
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import MultiLabelBinarizer

def evaluate_file(predicted_path, reference_path):
    # Load JSON files
    with open(predicted_path, 'r') as f:
        preds = json.load(f)
    with open(reference_path, 'r') as f:
        refs = json.load(f)

    # Extract label lists
    y_true = [item['labels'] for item in refs]
    y_pred = [item['labels'] for item in preds]

    # Binarize labels for multi-label metrics
    mlb = MultiLabelBinarizer()
    y_true_bin = mlb.fit_transform(y_true)
    y_pred_bin = mlb.transform(y_pred)

    # Compute metrics
    acc = accuracy_score(y_true_bin, y_pred_bin)  # exact match
    prec = precision_score(y_true_bin, y_pred_bin, average='micro', zero_division=0)
    rec = recall_score(y_true_bin, y_pred_bin, average='micro', zero_division=0)
    f1 = f1_score(y_true_bin, y_pred_bin, average='micro', zero_division=0)

    return {
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1": f1
    }
