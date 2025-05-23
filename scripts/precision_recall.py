import numpy as np

def calculate_classification_metrics(confusion_matrix):
    """
    Calculate precision, recall, F1 score, balanced accuracy, weighted accuracy, 
    Matthews Correlation Coefficient, and overall accuracy.
    
    Parameters:
    confusion_matrix (numpy.ndarray): A 2D array representing the confusion matrix
                                      Rows represent actual classes
                                      Columns represent predicted classes
    
    Returns:
    dict: A dictionary containing per-class and overall metrics
    """
    # Ensure input is a numpy array
    cm = np.array(confusion_matrix)
    
    # Number of classes
    num_classes = cm.shape[0]
    
    # Initialize results dictionary
    metrics = {
        'per_class': {
            'precision': [],
            'recall': [],
            'f1_score': [],
            'balanced_accuracy': [],
            'weighted_accuracy': [],
            'mcc': []
        },
        'overall': {
            'accuracy': 0,
            'macro_precision': 0,
            'macro_recall': 0,
            'macro_f1_score': 0,
            'macro_balanced_accuracy': 0,
            'macro_weighted_accuracy': 0,
            'macro_mcc': 0,
            'weighted_precision': 0,
            'weighted_recall': 0,
            'weighted_f1_score': 0,
            'weighted_balanced_accuracy': 0,
            'weighted_weighted_accuracy': 0,
            'weighted_mcc': 0
        }
    }
    
    # Total samples per class and overall
    total_samples = np.sum(cm)
    class_samples = np.sum(cm, axis=1)
    
    # Calculate overall accuracy
    correct_predictions = np.trace(cm)
    metrics['overall']['accuracy'] = correct_predictions / total_samples
    
    # Define class labels
    CLASS_LABELS = [
        'N (Noun)', 
        'V (Verb)', 
        'NM (Noun Modifier)', 
        'D (Determiner)', 
        'P (Preposition)', 
        'VM (Verb Modifier)', 
        'PRE (Prefix)', 
        'DT (Determiner Type)', 
        'NPL (Noun Plural)', 
        'CJ (Conjunction)'
    ]
    
    # Calculate metrics for each class
    for class_idx in range(num_classes):
        # True Positives (TP)
        tp = cm[class_idx, class_idx]
        
        # False Positives (FP) - sum of column minus true positive
        fp = np.sum(cm[:, class_idx]) - tp
        
        # False Negatives (FN) - sum of row minus true positive
        fn = np.sum(cm[class_idx, :]) - tp
        
        # True Negatives (TN) - sum of all samples minus TP, FP, FN
        tn = total_samples - (tp + fp + fn)
        
        # Precision = TP / (TP + FP)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        
        # Recall = TP / (TP + FN)
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        
        # F1 Score = 2 * (Precision * Recall) / (Precision + Recall)
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        # Balanced Accuracy = (Sensitivity + Specificity) / 2
        sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        balanced_accuracy = (sensitivity + specificity) / 2
        
        # Weighted Accuracy (accuracy of this class weighted by its samples)
        weighted_accuracy = (tp + tn) / (tp + tn + fp + fn)
        
        # Matthews Correlation Coefficient (MCC)
        # MCC = ((TP * TN) - (FP * FN)) / sqrt((TP+FP)(TP+FN)(TN+FP)(TN+FN))
        mcc_denominator = np.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))
        mcc = ((tp * tn) - (fp * fn)) / mcc_denominator if mcc_denominator != 0 else 0
        
        # Store per-class results
        metrics['per_class']['precision'].append(precision)
        metrics['per_class']['recall'].append(recall)
        metrics['per_class']['f1_score'].append(f1)
        metrics['per_class']['balanced_accuracy'].append(balanced_accuracy)
        metrics['per_class']['weighted_accuracy'].append(weighted_accuracy)
        metrics['per_class']['mcc'].append(mcc)
    
    # Convert lists to numpy arrays for easier calculation
    precisions = np.array(metrics['per_class']['precision'])
    recalls = np.array(metrics['per_class']['recall'])
    f1_scores = np.array(metrics['per_class']['f1_score'])
    balanced_accuracies = np.array(metrics['per_class']['balanced_accuracy'])
    weighted_accuracies = np.array(metrics['per_class']['weighted_accuracy'])
    mccs = np.array(metrics['per_class']['mcc'])
    
    # Macro averaging (simple average of all classes)
    metrics['overall']['macro_precision'] = np.mean(precisions)
    metrics['overall']['macro_recall'] = np.mean(recalls)
    metrics['overall']['macro_f1_score'] = np.mean(f1_scores)
    metrics['overall']['macro_balanced_accuracy'] = np.mean(balanced_accuracies)
    metrics['overall']['macro_weighted_accuracy'] = np.mean(weighted_accuracies)
    metrics['overall']['macro_mcc'] = np.mean(mccs)
    
    # Weighted averaging (weighted by number of samples in each class)
    metrics['overall']['weighted_precision'] = np.average(precisions, weights=class_samples)
    metrics['overall']['weighted_recall'] = np.average(recalls, weights=class_samples)
    metrics['overall']['weighted_f1_score'] = np.average(f1_scores, weights=class_samples)
    metrics['overall']['weighted_balanced_accuracy'] = np.average(balanced_accuracies, weights=class_samples)
    metrics['overall']['weighted_weighted_accuracy'] = np.average(weighted_accuracies, weights=class_samples)
    metrics['overall']['weighted_mcc'] = np.average(mccs, weights=class_samples)
    
    return metrics

# Modify print_metrics to use class labels
def print_metrics(metrics):
    """
    Pretty print the calculated metrics
    """
    # Define class labels
    CLASS_LABELS = [
        'N (Noun)', 
        'V (Verb)', 
        'NM (Noun Modifier)', 
        'D (Determiner)', 
        'P (Preposition)', 
        'VM (Verb Modifier)', 
        'PRE (Prefix)', 
        'DT (Determiner Type)', 
        'NPL (Noun Plural)', 
        'CJ (Conjunction)'
    ]

    print("Overall Metrics:")
    print(f"    Accuracy:               {metrics['overall']['accuracy']:.4f}")
    
    print("\nPer-Class Metrics:")
    for i, (p, r, f1, ba, wa, mcc) in enumerate(zip(
        metrics['per_class']['precision'], 
        metrics['per_class']['recall'], 
        metrics['per_class']['f1_score'],
        metrics['per_class']['balanced_accuracy'],
        metrics['per_class']['weighted_accuracy'],
        metrics['per_class']['mcc']
    )):
        print(f"  {CLASS_LABELS[i]}:")
        print(f"    Precision:          {p:.4f}")
        print(f"    Recall:             {r:.4f}")
        print(f"    F1 Score:           {f1:.4f}")
        print(f"    Balanced Accuracy:  {ba:.4f}")
        print(f"    Weighted Accuracy:  {wa:.4f}")
        print(f"    Matthews Corr Coef: {mcc:.4f}")
    
    print("\nOverall Metrics:")
    print("  Macro Averaging:")
    print(f"    Macro Precision:          {metrics['overall']['macro_precision']:.4f}")
    print(f"    Macro Recall:             {metrics['overall']['macro_recall']:.4f}")
    print(f"    Macro F1 Score:           {metrics['overall']['macro_f1_score']:.4f}")
    print(f"    Macro Balanced Accuracy:  {metrics['overall']['macro_balanced_accuracy']:.4f}")
    print(f"    Macro Weighted Accuracy:  {metrics['overall']['macro_weighted_accuracy']:.4f}")
    print(f"    Macro Matthews Corr Coef: {metrics['overall']['macro_mcc']:.4f}")
    
    print("\n  Weighted Averaging:")
    print(f"    Weighted Precision:          {metrics['overall']['weighted_precision']:.4f}")
    print(f"    Weighted Recall:             {metrics['overall']['weighted_recall']:.4f}")
    print(f"    Weighted F1 Score:           {metrics['overall']['weighted_f1_score']:.4f}")
    print(f"    Weighted Balanced Accuracy:  {metrics['overall']['weighted_balanced_accuracy']:.4f}")
    print(f"    Weighted Accuracy:           {metrics['overall']['weighted_weighted_accuracy']:.4f}")
    print(f"    Weighted Matthews Corr Coef: {metrics['overall']['weighted_mcc']:.4f}")
    
# Example confusion matrix
SCALAR_cm = np.array([
    [262,12,23,0,4,3,0,2,0,0],
    [3,77,6,0,0,0,1,0,0,0],
    [58,10,286,2,2,0,12,2,1,1],
    [0,0,0,43,0,0,0,0,0,0],
    [2,0,2,0,71,1,0,0,0,0],
    [1,0,0,0,0,6,0,0,0,1],
    [8,1,11,1,0,0,36,0,0,0],
    [3,0,0,0,0,2,0,45,0,0],
    [4,1,4,0,0,0,0,0,55,0],
    [1,0,3,0,0,0,0,0,0,7],
])
flair_cm = np.array([
    [295,22,219,1,2,2,39,2,0,0],
    [11,61,12,0,0,0,0,0,1,0],
    [9,17,74,0,0,1,1,21,0,0],
    [3,0,3,45,1,0,1,0,0,0],
    [7,0,12,0,71,1,1,0,0,3],
    [6,0,4,0,3,8,0,3,0,1],
    [0,0,0,0,0,0,0,0,0,0],
    [2,0,1,0,0,0,2,23,0,0],
    [5,1,7,0,0,0,3,0,55,0],
    [1,0,2,0,0,0,0,0,0,5],
])

ensemble_cm = np.array([
    [242,7,22,0,4,6,10,0,0,1],
    [8,60,4,0,1,0,7,1,0,0],
    [72,29,297,2,10,3,17,25,4,1],
    [0,0,0,40,1,0,0,0,0,0],
    [6,0,3,4,58,0,0,3,0,2],
    [1,4,0,0,0,3,2,0,0,0],
    [2,1,5,0,0,0,8,0,0,0],
    [4,0,1,0,0,0,3,20,0,0],
    [5,0,2,0,0,0,2,0,52,0],
    [2,0,1,0,3,0,0,0,0,5  ],
])
# Calculate and print metrics
scalar_metrics = calculate_classification_metrics(SCALAR_cm)
flair_metrics = calculate_classification_metrics(flair_cm)
ensemble_metrics = calculate_classification_metrics(ensemble_cm)

print("Scalar: ")
print_metrics(scalar_metrics)

print("Flair")
print_metrics(flair_metrics)

print("ensemble")
print_metrics(ensemble_metrics)