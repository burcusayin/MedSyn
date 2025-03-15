from sklearn.metrics import precision_score, recall_score, f1_score, hamming_loss
from evaluate import load
import numpy as np
import evaluate

bertscore = load("bertscore")
rouge = evaluate.load('rouge')
# modelname = "allenai/scibert_scivocab_uncased"
modelname = "roberta-large"

def compute_icd10_metrics(ground_truth, predictions):
    """
    Computes various metrics for multi-label classification.
    :param ground_truth: List of sets of ground truth codes.
    :param predictions: List of sets of predicted codes.
    :return: Metrics as a dictionary.
    """
    iou_scores = []
    precisions = []
    recalls = []
    f1_scores = []

    for gt, pred in zip(ground_truth, predictions):
        # Compute Intersection and Union for IoU
        intersection = len(gt & pred)
        union = len(gt | pred)
        iou = intersection / union if union > 0 else 0
        iou_scores.append(iou)

        # Precision, Recall, F1
        precision = intersection / len(pred) if len(pred) > 0 else 0
        recall = intersection / len(gt) if len(gt) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

        precisions.append(precision)
        recalls.append(recall)
        f1_scores.append(f1)

    # Average metrics over all samples
    scores = {
    "Jaccard": round(np.mean(iou_scores).item(), 3),
    "Precision": round(np.mean(precisions).item(), 3),
    "Recall": round(np.mean(recalls).item(), 3),
    "F1-Score": round(np.mean(f1_scores).item(), 3),
}
    return scores


def compute_diagnosis_metrics(ground_truth, predictions):
    results_bertscore = bertscore.compute(predictions=predictions, references=ground_truth, lang="en", model_type=modelname)
    results_rouge = rouge.compute(predictions=predictions, references=ground_truth, use_aggregator=True)
    scores = {
        "Precision": round(np.asarray(results_bertscore['precision']).mean(), 3),
        "Recall": round(np.asarray(results_bertscore['recall']).mean(), 3),
        "F1-Score": round(np.asarray(results_bertscore['f1']).mean(), 3),
        "Rouge1": round(np.asarray(results_rouge['rouge1']).mean(), 3),
        "Rouge2": round(np.asarray(results_rouge['rouge2']).mean(), 3),
        "RougeL": round(np.asarray(results_rouge['rougeL']).mean(), 3),
        "RougeLsum": round(np.asarray(results_rouge['rougeLsum']).mean(), 3),
    }

    return scores