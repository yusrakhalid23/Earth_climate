import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pickle

def load_and_train_model(file_path='data/climate_data.csv'):
    # Load the dataset
    data = pd.read_csv(file_path)

    # Features and target (temperature is predicted using other variables)
    features = data[['humidity', 'co2_levels', 'wind_speed', 'rainfall', 'pressure']]
    target = data['temperature']

    # Split for training/testing if needed (optional for full training)
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    # Train the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Save model using pickle
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)

    print("Model trained and saved as model.pkl")

    return model

# Call this function only if you're running this file directly
if __name__ == "__main__":
    load_and_train_model()
