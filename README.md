# Customer Segmentation Using RFM and K-Means

![Project Badge](https://img.shields.io/badge/Status-Completed-green)   
![ML Badge](https://img.shields.io/badge/Machine%20Learning-Python-orange)

## 📌 Overview
This project is part of the **CS663 Term Project: Data Mining** course and focuses on **Customer Segmentation** using **RFM (Recency, Frequency, and Monetary) analysis** and **K-Means clustering**. The goal is to identify customer segments based on their purchasing behavior and derive meaningful insights for business strategies.

## 📂 Dataset
The dataset consists of **transactional data** from a UK-based online retail store. It includes all transactions between **01/12/2010 and 09/12/2011**. The data contains essential attributes such as:
- Invoice Number
- Stock Code
- Description
- Quantity
- Invoice Date
- Unit Price
- Customer ID
- Country

## 🎯 Objectives
- Perform **data preprocessing** to clean and transform the data.
- Apply **feature engineering** techniques to extract useful insights.
- Implement **RFM analysis** to classify customers based on their purchasing behavior.
- Use **K-Means clustering** to segment customers.
- Evaluate clustering performance using the **Elbow Method** and **Silhouette Score**.
- Visualize and interpret the results.

## 🔧 Steps Involved

### 1️⃣ Data Preprocessing
- Handling missing values.
- Removing duplicates and irrelevant data.
- Converting categorical variables into meaningful numerical values.

### 2️⃣ Feature Engineering
- **Geographical Insights:** Classifying transactions based on UK (1) and non-UK (0).
- **Cancellation Rate:** Identifying order cancellations.
- **Outlier Detection:** Using **Local Outlier Factor (LOF)** to detect anomalies.
- **Feature Extraction:** Creating new meaningful variables.
- **Correlation Analysis:** Identifying relationships between features.
- **Standardization & PCA:** Normalizing data and reducing dimensionality.

### 3️⃣ Clustering
- **RFM Analysis:** Grouping customers based on Recency, Frequency, and Monetary values.
- **K-Means Clustering:**
  - Using the **Elbow Method** to determine the optimal number of clusters.
  - Evaluating clusters using the **Silhouette Score**.
  - Ensuring **Cluster Stability**.

### 4️⃣ Results & Insights
- Identified **three distinct customer clusters**:
  - **Cluster 2:** High-value customers with the highest spending average.
  - **Cluster 1:** Moderate spenders.
  - **Cluster 0:** Low-value customers with minimal spending.
- Visualizations and insights extracted from the segmentation process.

## 📊 Results
- 24% of customers belong to **Cluster 0** (low spenders).
- 68% belong to **Cluster 1** (moderate spenders).
- 7% belong to **Cluster 2** (high spenders).
- **Cluster 2** customers are the most valuable to the business.

## 🚀 Future Work
- Explore alternative **clustering techniques** such as **Hierarchical Clustering** and **DBSCAN**.
- Implement **predictive analytics** to forecast customer purchasing behavior.
- Enhance **data visualization** to improve interpretation.
- Apply **deep learning** methods for advanced customer segmentation.

## 📜 Conclusion
This project successfully segmented customers based on their purchasing behavior using **RFM analysis and K-Means clustering**. The insights derived from clustering help businesses tailor their marketing strategies and improve customer retention.

