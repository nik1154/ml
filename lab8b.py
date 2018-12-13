import matplotlib.pyplot as plt  
import numpy as np  
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans 
from scipy.spatial.distance import cdist


#Size of k
k=2
# Generate dataset (BEFORE)
X, y = make_blobs(centers=k, n_samples=500, center_box=(4,20))
# Visualize
#fig, ax = plt.subplots(figsize=(4,4))
plt.title("Before K mean- Random Dataset")
plt.scatter(X[:,0], X[:,1], alpha=0.5)
plt.show()

#K mean and visualize the clusters(AFTER)
kmeans = KMeans(n_clusters=k)  
kmeans.fit(X)  

plt.title("After K mean")
plt.scatter(X[:,0],X[:,1], c=kmeans.labels_, cmap='rainbow')  
plt.scatter(kmeans.cluster_centers_[:,0] ,kmeans.cluster_centers_[:,1], color='black')  
plt.show()

#Elbow curve
distortions = []
K = range(1,10)
for k in K:
    kmeanModel = KMeans(n_clusters=k).fit(X)
    kmeanModel.fit(X)
    distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / X.shape[0])
# Plot the elbow 
plt.plot(K, distortions, 'bx-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('The Elbow Method showing the optimal k')
plt.show()