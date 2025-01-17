# -*- coding: utf-8 -*-
"""NLP - BERT - KMeans

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12R0p2seKNIqyyp4jsd8R0i2lCkTva7t2
"""

pip install sentence-transformers

from transformers import BertModel, BertTokenizer, AdamW, get_linear_schedule_with_warmup
import torch
import numpy as np
from sklearn.model_selection import train_test_split
from torch import nn, optim
from torch.utils.data import Dataset, DataLoader
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score, silhouette_samples

df = pd.read_excel("/content/Node list (6).xlsx")

model = SentenceTransformer('bert-large-uncased')

df_2 = df['Label'].tolist()

embeddings = model.encode(df_2)

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

similarity_matrix = cosine_similarity(embeddings)

distance_matrix = 1 - similarity_matrix

embeddings_2 = pd.DataFrame(embeddings)
similarity_matrix_2 =pd.DataFrame(similarity_matrix)

k_range = range(1, 10)

inertia = []
for k in k_range:
    kmeans = KMeans(n_clusters=k).fit(embeddings)
    inertia.append(kmeans.inertia_)

plt.figure(figsize=(10, 6))
plt.plot(k_range, inertia, 'bx-')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.title('Elbow Method For Optimal k')
plt.show()

model = KMeans(n_clusters=8, init='k-means++')
cluster_labels = model.fit(embeddings)
labels = model.labels_

labels_2 = pd.DataFrame(labels)

sample_silhouette_values = silhouette_samples(embeddings, labels)
for i in range(7):
    cluster_silhouette_values = sample_silhouette_values[labels == i]
    print(f"Cluster {i}:", cluster_silhouette_values.mean())

score = silhouette_score(embeddings, labels)

print(score)

# Resultados a excel

with pd.ExcelWriter('Nodes analysis sept.xlsx') as writer:
  embeddings_2.to_excel(writer,sheet_name= 'embeddings',index=False)
  similarity_matrix_2.to_excel(writer,sheet_name= 'similarity_matrix',index=False)
  labels_2.to_excel(writer,sheet_name= 'kmeans_labels',index=False)