from sklearn.ensemble import IsolationForest  # type: ignore
import numpy as np

def detect_anomalies(data):
    try:
        # ✅ handle empty or invalid input
        if not data or len(data) < 2:
            return []

        arr = np.array(data)

        # ✅ reshape if 1D (VERY IMPORTANT)
        if len(arr.shape) == 1:
            arr = arr.reshape(-1, 1)

        # 🔥 improved model config
        model = IsolationForest(
            n_estimators=100,
            contamination=0.1,
            random_state=42
        )

        preds = model.fit_predict(arr)

        # ✅ convert to clean Python list
        return preds.tolist()

    except Exception as e:
        print("Anomaly detection failed:", e)
        return []