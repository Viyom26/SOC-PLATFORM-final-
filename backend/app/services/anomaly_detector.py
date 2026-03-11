from sklearn.ensemble import IsolationForest
import numpy as np

def detect_anomalies(data):
    model = IsolationForest()
    preds = model.fit_predict(np.array(data))
    return preds.tolist()
