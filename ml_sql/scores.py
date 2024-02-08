import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def print_scores(title, pred, test):
    data = np.array([accuracy_score(pred, test), precision_score(pred, test), recall_score(pred, test), f1_score(pred, test)])
    df = pd.DataFrame(data)
    df.to_csv("./data.csv", index = False, mode = 'a')