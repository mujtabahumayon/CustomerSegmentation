# -*- coding: utf-8 -*-
"""DM_Project_CustomerSegmentation x.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1u-wA0DkiL2JXaQ8Uvtx0QWoigkXM0nul

<h1 align="center">Customer Segmentation using RFM and K-Means</h1>
<h2 align="center">Fundamentals of Data Mining CS663</h2>
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from sklearn.metrics.pairwise import euclidean_distances
warnings.filterwarnings('ignore')

df = pd.read_csv('data.csv',encoding='unicode_escape')

df.head()

df.describe(include='all')

"""----
## Data Pre-Processing
----

**Removing Null Values**
"""

null_df = df.isnull().sum().to_frame().T
null_df= (null_df/df.shape[0])*100
null_df

#remove null values
df=df.dropna()

df.isnull().sum()

"""**Removing duplicate rows**"""

dupliacte_rows = df[df.duplicated()]
dupliacte_rows.head()
dupliacte_rows.shape[0]

df= df.drop_duplicates()
df.head()

mask= df['InvoiceNo'].to_numpy().astype(str)

"""**Dealing with cancelled transactions**"""

mask=np.char.isdigit(mask)

df['Status']=np.where(mask, 'Complete', 'Cancelled')

df['Status'].value_counts()

"""**Analyzing and cleaning Description attribute**"""

df['Description'].value_counts().head(10)

unqiue_descriptions = df['Description'].unique().astype(str)
mask_1=np.char.isupper(unqiue_descriptions)

pd.DataFrame(unqiue_descriptions[~mask_1])

description_filter = ['Discount','Manual','Bank Charges','Next Day Carriage','High Resolution Image','CRUK Commission']
df = df[~df['Description'].isin(description_filter)]

df['Description']= df['Description'].str.upper()

df.shape

"""**Removing zero price values**"""

df = df[df['UnitPrice']>0]

df.shape

# Reset Index
df.reset_index(inplace=True, drop=True)

"""**Cleaned DataFrame**"""

df.head()

df.describe()

"""----
## RFM Analysis
----

### Recency    
Calculating recency of transaction for each customer
"""

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
rfm = df.groupby('CustomerID')['InvoiceDate'].max().reset_index()
rfm['InvoiceDate']=pd.to_datetime(rfm['InvoiceDate'])

recency = pd.to_datetime(df['InvoiceDate'].max())
rfm['Recency'] = (recency - rfm['InvoiceDate']).dt.days
rfm.drop(columns=['InvoiceDate'], inplace=True)

rfm.shape

rfm.head()

"""### Frequency    
Computing frequency of purchase for each customer
"""

freq = df.groupby('CustomerID')['InvoiceDate'].nunique()
freq = pd.DataFrame(freq).reset_index()
rfm['Frequency']= freq['InvoiceDate']

quantity = df.groupby('CustomerID')['Quantity'].sum()
quantity = pd.DataFrame(quantity).reset_index()
rfm['TotalQuantity'] = quantity['Quantity']
rfm.head()

"""### Monetary    
Computing total spending values of each customer and the average purchase values for each transaction
"""

df['Price'] = df['Quantity']*df['UnitPrice']
monetary = df.groupby('CustomerID')['Price'].sum()
monetary = pd.DataFrame(monetary).reset_index()
rfm['Spending'] = monetary['Price']
rfm.head()

total = df.groupby('CustomerID')['InvoiceNo'].nunique().reset_index()
total.rename(columns={'InvoiceNo': 'No of Transactions'}, inplace=True)
Avg_value = monetary.merge(total, on='CustomerID')
Avg_value['Avg_value'] = Avg_value['Price'] / Avg_value['No of Transactions']
rfm = pd.merge(rfm, Avg_value[['CustomerID', 'Avg_value']], on='CustomerID')
rfm.head()

"""### Geography    
Analyzing country of most numbers of transactions for each customer.
"""

plt.figure(figsize=(6, 3))
country=pd.DataFrame(df['Country'].value_counts()).reset_index()
country = country.rename(columns={'Country': 'Count', 'index': 'Country'})
sns.barplot(country.head(10),x='Count', y='Country',orient='h')
plt.show()

"""Assigning Customers with maximum transactions from UK as 1, 0 otherwise"""

country = df.groupby(['CustomerID', 'Country']).size().reset_index(name='Count')
most_trans_coun= country.sort_values('Count', ascending=False).drop_duplicates('CustomerID')
most_trans_coun['UK'] = most_trans_coun['Country'].apply(lambda x: 1 if x == 'United Kingdom' else 0)

rfm = pd.merge(rfm, most_trans_coun[['CustomerID', 'UK']], on='CustomerID')
rfm.head()

rfm['UK'].value_counts()

"""### Cancellation Rate    
Computing cancellation rate for each customer
"""

purchases = df.groupby('CustomerID')['InvoiceNo'].nunique().reset_index()
purchases.rename(columns={'InvoiceNo':'Transactions_Count'}, inplace=True)

cancelled_rate = df[df['Status']=='Cancelled']
cancelled_rate= cancelled_rate.groupby('CustomerID')['InvoiceNo'].nunique().reset_index()
cancelled_rate.rename(columns={'InvoiceNo':'Cancellation_Count'}, inplace=True)

rfm = pd.merge(rfm, cancelled_rate, on='CustomerID', how='left')
rfm['Cancellation_Count'].fillna(0, inplace=True)
rfm['Cancellation_Rate'] = rfm['Cancellation_Count'] / purchases['Transactions_Count']
rfm.drop(columns=['Cancellation_Count'], inplace=True)

"""### RFM Processed DataFrame     
The RFM analysis is complete here. The final dataframe is as below:
"""

rfm.shape

rfm.head()

"""---
## Outlier Detection using LOF
----
"""

from sklearn.neighbors import LocalOutlierFactor

clf = LocalOutlierFactor(n_neighbors=436) # setting n_neighbors as 10% of the data
outlier = clf.fit_predict(rfm.iloc[:, 1:])

outlier= pd.DataFrame(outlier)
outlier.value_counts()

"""**Labelling each row as Outlier 1 or 0**"""

rfm['Outlier'] = [1 if O==-1 else 0 for O in outlier[0]]
rfm.head()

rfm['Outlier'].value_counts(normalize=True)

"""---
## Processed Data
---

**Now we remove all the outliers from the RFM DataFrame. The Data is now cleaned**
"""

processed_data = rfm[rfm['Outlier'] == 0]
outiler_data = rfm[rfm['Outlier']==1]

processed_data= processed_data.drop(columns=['Outlier']).reset_index(drop=True)
outiler_data= outiler_data.drop(columns=['Outlier']).reset_index(drop=True)

processed_data.head()

processed_data.describe()

"""---
## Correlation
---

After plotting correlation matrix for the attibutes in the RFM. We see some correlation among the attributes.
"""

plt.figure(figsize=(7, 4))
correlation = processed_data.iloc[:,1:]
sns.heatmap(correlation.corr(), annot=True)
plt.show()

"""---
## Standardization and PCA
---

**Standardizing the data using StandardSclaer from SK-learn**
"""

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
to_scale = ['Recency', 'Frequency', 'TotalQuantity','Avg_value','Spending']
scaled_data = processed_data.copy()
scaled_data[to_scale]=sc.fit_transform(scaled_data[to_scale])
scaled_data.head()

"""**As seen form the correlation matrix, some attributes are highly correlated. We will now use PCA to reduce the number of attributes**"""

from sklearn.decomposition import PCA
X=scaled_data.iloc[:,1:]
X
pca = PCA()
pca.fit(X)
cumsum = np.cumsum(pca.explained_variance_ratio_)
plt.plot(cumsum, marker='o')
for i in range(len(cumsum)):
    plt.text(i+0.1, cumsum[i]-0.02, round(cumsum[i], 2))
plt.show()

"""From the plot above, 3 PCA components can explain 97% of the data and there is no major improvement in increasing the attributes to 4. We therefore select Number of components as 3."""

pca=PCA(n_components=3)
X_pca=pca.fit_transform(X)

X_pca = pd.DataFrame(X_pca, columns=['PC'+str(i+1) for i in range(pca.n_components_)])
X_pca.head()

"""**We are now ready to apply K-means clustering on the reduced dataset**

---
## K-Means Clustering
---

### Elbow Method    
The Elbow Method is a simple technique for determining the optimal number of clusters in K-means. It involves running the algorithm for a range of cluster numbers and plotting the within-cluster sum of squares (WCSS) against the number of clusters. The "elbow" point on the plot, where the reduction in WCSS slows down, indicates an optimal balance between model complexity and performance.
"""

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
#scaled_data.drop(columns=['Average_Days_Between_Purchases'], inplace=True, axis=1)

wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters = i, init = 'k-means++', n_init='auto', random_state = 42)
    kmeans.fit(X_pca)
    wcss.append(kmeans.inertia_)
plt.plot(range(1, 11), wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

"""### Silhouette  Score    
The Silhouette Score quantifies the separation and cohesion of clusters. By assessing the average distances within and between clusters, the Silhouette Score helps identify the number of clusters that maximizes clustering quality. A higher Silhouette Score signifies well-defined clusters.
"""

from yellowbrick.cluster import SilhouetteVisualizer

fig, ax = plt.subplots(3, 2, figsize=(15,15))
for i in [2, 3, 4, 5, 6, 7]:
    km = KMeans(n_clusters=i, init='k-means++', n_init='auto', random_state=42)
    q, mod = divmod(i, 2)
    visualizer = SilhouetteVisualizer(km, colors='yellowbrick', ax=ax[q-1][mod])
    visualizer.fit(X_pca)
    ax[q-1][mod].set_title(f'Silhouette Plot for {i} Clusters', fontsize=15)
    cluster_labels=km.predict(X_pca)
    silhouette_avg = silhouette_score(X_pca, cluster_labels)
    ax[q-1][mod].text(0, 0.5, f'Silhouette Score: {silhouette_avg:.2f}', transform=ax[q-1][mod].transAxes)

"""### Cluster Stability    
Cluster Stability involves evaluating the robustness of clusters by using random data subsamples. By calculating the average movement of cluster centroids in each iteration, this method assesses the consistency of cluster assignments. Cluster Stability ensures that identified clusters are not artifacts of random initialization, providing a more reliable representation of the underlying data structure.
"""

def normalize(list1):
    min_value = np.min(list1)
    max_value = np.max(list1)
    normalized_list = [(x - min_value) / (max_value - min_value) for x in list1]
    return normalized_list

def cluster_movement_range(X, n_iterations, cluster_range):
    movement_per_iteration = {k: [] for k in cluster_range}
    for k in cluster_range:
        for i in range(n_iterations):
            sample = X.sample(frac=0.7,random_state=i)

            model = KMeans(n_clusters=k, init='k-means++', n_init='auto', random_state=42)
            model.fit(sample)
            centers = model.cluster_centers_
            if i > 0:
                movement = np.mean(np.linalg.norm(centers - prev_centers, axis=1))
                movement_per_iteration[k].append(movement)

            prev_centers = centers

    mean_movement_per_cluster = {k: np.mean(movements) for k, movements in movement_per_iteration.items()}

    return mean_movement_per_cluster


n_iterations = 20
cluster_range = range(2, 11)
mean_movement_per_cluster = cluster_movement_range(X_pca, n_iterations, cluster_range)

plt.plot(list(mean_movement_per_cluster.keys()), normalize(list(mean_movement_per_cluster.values())), marker='o')
plt.title('Mean Difference in Clusters Centers')
plt.xlabel('Number of Clusters')
plt.ylabel('Noramlized Mean Difference')
plt.xticks(list(mean_movement_per_cluster.keys()))
plt.grid(True)
plt.show()

"""### Training with Optimal No. of Clusters (K=3)

Based on the cluster evaluation, the optimal number of clusters is 3, having a decent Silhouette score of 0.3 and good cluster stability compared to 4 clusters and above.
"""

kmeans = KMeans(n_clusters = 3, init = 'k-means++', n_init='auto', random_state = 42)
kmeans.fit(X_pca)
clusters=kmeans.labels_
labelled_data = processed_data.copy()
labelled_data['Cluster']=clusters

labelled_data['Cluster'].value_counts()

"""**The labelled DataFrame with cluster IDs is below**"""

labelled_data.head()

"""---
## Customer Segmentation
---

**We fisrt plot PCA components of the Labelled DataFrame to see a visual representaion of the clusters**
"""

colors = {0: '#1f77b4', 1: '#ff7f0e', 2: '#2ca02c'}
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(X_pca['PC1'], X_pca['PC2'], X_pca['PC3'], c=labelled_data['Cluster'].map(colors))
legend_labels = {0: 'Cluster 0', 1: 'Cluster 1', 2: 'Cluster 2'}
legend_elements = [plt.Line2D([0], [0], marker='o', color='w', \
                markerfacecolor=colors[label], markersize=10, label=legend_labels[label]) for label in colors]

ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()

"""**In order to analyze the cluster, we can plot bar chart of the average values of attributes of the RFM DataFrame to better understand the customer segmentation**"""

colors = ['#1f77b4','#ff7f0e','#2ca02c']
cluster0=labelled_data[labelled_data['Cluster']==0].drop(columns=['Cluster'])
cluster1=labelled_data[labelled_data['Cluster']==1].drop(columns=['Cluster'])
cluster2=labelled_data[labelled_data['Cluster']==2].drop(columns=['Cluster'])

zero= pd.DataFrame(cluster0.iloc[:,1:].mean()).reset_index().rename(columns={0:'Cluster0'})
one= pd.DataFrame(cluster1.iloc[:,1:].mean()).reset_index().rename(columns={0:'Cluster1'})
two= pd.DataFrame(cluster2.iloc[:,1:].mean()).reset_index().rename(columns={0:'Cluster2'})
plot_df = pd.merge(zero, one, on='index')
plot_df = pd.merge(plot_df, two, on='index')
ax = plot_df.plot(kind='bar', x='index', logy=True, rot=0, color=colors)
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
ax.set_xlabel('Features')
ax.set_ylabel('Average Values')
plt.show()

"""Following chart represents the percenatge of customers assigned to each cluster"""

cluster_pct = (labelled_data['Cluster'].value_counts(normalize=True) * 100).reset_index()
cluster_pct.columns = ['Cluster', 'Percentage']
cluster_pct.sort_values(by='Cluster', inplace=True)

plt.figure(figsize=(8, 3))
sns.barplot(x='Percentage', y='Cluster', data=cluster_pct, orient='h', palette=colors)
for index, value in enumerate(cluster_percentage['Percentage']):
    plt.text(2, index, f'{value:.2f}%', color='white')
plt.show()

"""## Conclusion     
       
In conclusion, the customer segmentation analysis using RFM (Recency, Frequency, Monetary) and K-means clustering has provided valuable insights into distinct customer behaviors. The identified clusters reveal diverse spending patterns and transaction characteristics, allowing for targeted strategies to enhance customer engagement and satisfaction.
     
1. **Cluster 0 (Blue):**
Customers in this cluster demonstrate conservative spending habits, with lower transaction frequency and product volume. While their average transaction value is modest, the low cancellation frequency and rate suggest a stable and loyal customer base.

2. **Cluster 1 (Orange):**
Customers in Cluster 1 display a moderate spending level, characterized by infrequent but substantial transactions. The increasing spending trend indicates potential for future growth. Despite a moderate cancellation frequency, the higher average transaction value suggests a willingness to make significant purchases.

3. **Cluster 2 (Green):**
Cluster 2 represents high-value customers with a substantial total spend and frequent transactions. However, their high cancellation frequency raises concerns about potential dissatisfaction. Although their spending trend is low, indicating a possible decrease over time, strategies can be devised to retain these valuable customers and address their cancellation tendencies.

This segmentation analysis provides a foundation for personalized marketing, customer retention, and loyalty programs tailored to the specific needs and behaviors of each cluster. Continued monitoring and adjustment of strategies based on evolving customer trends will be key to maximizing the effectiveness of these initiatives.
"""