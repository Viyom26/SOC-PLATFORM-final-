from sklearn.cluster import KMeans
import numpy as np

def cluster_attacks(data):
    model = KMeans(n_clusters=3)
    model.fit(np.array(data))
    return model.labels_.tolist()
