import pandas as pd
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

# Load the climate data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Function to train the Random Forest model for temperature prediction
def train_trend_prediction_model(data):
    # Include new features
    features = data[['humidity', 'co2_levels', 'wind_speed', 'rainfall', 'pressure']]
    target = data['temperature']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate accuracy
    accuracy = model.score(X_test, y_test)
    print(f"Random Forest Prediction Model Accuracy: {accuracy * 100:.2f}%")
    
    return model

# Detect anomalies using Isolation Forest
def detect_anomalies(data):
    features = data[['temperature', 'humidity', 'co2_levels', 'wind_speed', 'rainfall', 'pressure']]
    
    iso_forest = IsolationForest(contamination=0.05, random_state=42)
    data['anomaly'] = iso_forest.fit_predict(features)
    
    anomalies = data[data['anomaly'] == -1]
    print(f"Anomalies detected: {len(anomalies)}")
    return anomalies

# Visualize correlations
def visualize_correlations(data):
    plt.figure(figsize=(10, 8))
    correlation_matrix = data[['temperature', 'humidity', 'co2_levels', 'wind_speed', 'rainfall', 'pressure']].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Correlation Matrix - Climate Variables')
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    file_path = 'data/climate_data.csv'
    climate_data = load_data(file_path)
    
    # Train prediction model
    trend_model = train_trend_prediction_model(climate_data)
    
    # Detect anomalies
    anomalies = detect_anomalies(climate_data)
    
    # Visualize correlation matrix
    visualize_correlations(climate_data)
