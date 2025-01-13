#Data clusterisation
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from scipy.stats import entropy
import warnings
from sklearn.exceptions import ConvergenceWarning

data = pd.read_csv("C:/Users/egoro/Desktop/Kaggle experience/train.csv", index_col='Id')
useful = data[['SalePrice']].copy()

useful = useful.dropna()
useful = useful.sort_values(by='SalePrice')

# Кластеризация
kmeans = KMeans(n_clusters=100, random_state=42)
kmeans.fit(useful)

# Метки кластеров
labels = kmeans.labels_

sorted_labels = np.sort(labels)
sorted_labels = pd.Series(sorted_labels)
print(sorted_labels)

# Находим переходы между кластерами
split_points = []
for i in range(1, len(sorted_labels)):
    if sorted_labels.iloc[i] != sorted_labels.iloc[i - 1]:
        split_value = (useful.iloc[i]['SalePrice'] + useful.iloc[i - 1]['SalePrice']) / 2
        split_points.append(split_value)

print(split_points)
