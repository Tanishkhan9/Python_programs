# data_mining.py

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# 1. Load dataset
# Replace 'your_file.csv' with your dataset
df = pd.read_csv("your_file.csv")

print("✅ Data loaded successfully!")
print("First 5 rows:\n", df.head())

# 2. Handle missing values (basic cleanup)
df = df.dropna()  # remove rows with missing values
# Alternatively: df = df.fillna(df.mean())  # fill with mean

# 3. Exploratory Data Analysis
print("\n📊 Summary Statistics:\n", df.describe())
print("\n🔗 Correlation Matrix:\n", df.corr())

# 4. Select numeric features for clustering
numeric_data = df.select_dtypes(include=['int64', 'float64'])

# Standardize data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(numeric_data)

# 5. Apply KMeans Clustering
kmeans = KMeans(n_clusters=3, random_state=42)  # 3 clusters
df['Cluster'] = kmeans.fit_predict(scaled_data)

print("\n✅ Clustering completed. Cluster counts:")
print(df['Cluster'].value_counts())

# 6. Visualization (first two features)
plt.scatter(scaled_data[:, 0], scaled_data[:, 1], c=df['Cluster'], cmap='viridis')
plt.title("KMeans Clustering (First 2 Features)")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.show()

# 7. Save processed data
df.to_csv("processed_data.csv", index=False)
print("\n💾 Processed data saved to processed_data.csv")
