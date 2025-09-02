import unittest
import pandas as pd
from app.models import load_and_train_model

class TestModels(unittest.TestCase):

    def test_model_training(self):
        data = pd.DataFrame({
            'temperature': [25.3, 26.7, 28.1],
            'humidity': [78, 75, 80],
            'co2_levels': [412.5, 413.2, 414.0]
        })
        
        # Assuming that load_and_train_model function takes a DataFrame as an input
        model = load_and_train_model(data)
        self.assertIsNotNone(model)  # Check if the model is successfully trained

if __name__ == '__main__':
    unittest.main()
