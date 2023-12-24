import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

class CarPricePredictor:
    def __init__(self):
        self.model = None

    def preprocess_data(self, data):
        # Convert 'Year' column to numeric
        data['Year'] = pd.to_numeric(data['Year'], errors='coerce')

        # Convert 'Kms_Driven' column to numeric
        data['Kms_Driven'] = pd.to_numeric(data['Kms_Driven'], errors='coerce')

        # Convert 'Selling_Price' column to numeric
        data['Selling_Price'] = pd.to_numeric(data['Selling_Price'], errors='coerce')

        # Drop rows with missing values
        data = data.dropna()

        return data

    def train(self, dataset_file):
        # Load the dataset
        data = pd.read_csv(dataset_file)

        # Preprocess the data
        data = self.preprocess_data(data)

        # Calculate car's age
        current_year = 2023
        data['Age'] = current_year - data['Year']

        data.columns = data.columns.str.strip()

        
        # Check if 'Fuel_Type' and 'Transmission' columns are present
        if 'Fuel_Type' in data.columns and 'Transmission' in data.columns:
            # Split the data into input features (X) and target variable (y)
            X = data[['Year', 'Age', 'Present_Price', 'Kms_Driven']]
            y = data['Selling_Price']

            # Convert categorical variables to numerical using one-hot encoding
            X = pd.get_dummies(X, columns=['Fuel_Type', 'Transmission'], drop_first=True)

            # Split the dataset into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Train a Random Forest Regressor model
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.model.fit(X_train, y_train)

            # Evaluate the model
            score = self.model.score(X_test, y_test)
            print("Model Accuracy:", score)
        else:
            print("Missing 'Fuel_Type' or 'Transmission' columns in the dataset.")

    def predict(self, car_details):
        # Create a DataFrame with the given car details
        car_data = pd.DataFrame([car_details])

        # Preprocess the data
        car_data = self.preprocess_data(car_data)

        # Calculate car's age
        current_year = 2023
        car_data['Age'] = current_year - car_data['Year']

        # Check if 'Fuel_Type' and 'Transmission' columns are present
        if 'Fuel_Type' in car_data.columns and 'Transmission' in car_data.columns:
            # Convert categorical variables to numerical using one-hot encoding
            car_data = pd.get_dummies(car_data, columns=['Fuel_Type', 'Transmission'], drop_first=True)

            # Make a prediction using the trained model
            selling_price = self.model.predict(car_data[['Year', 'Age', 'Present_Price', 'Kms_Driven']])

            return selling_price[0]
        else:
            print("Missing 'Fuel_Type' or 'Transmission' columns in the car details.")

    def save_model(self, filename):
        # Save the trained model using pickle
        with open(filename, 'wb') as file:
            pickle.dump(self.model, file)

    def load_model(self, filename):
        # Load a trained model from a file
        with open(filename, 'rb') as file:
            self.model = pickle.load(file)




def carprice_tester():
    # Create an instance of the CarPricePredictor class
    car_predictor = CarPricePredictor()

    # Train the model using the dataset
    car_predictor.train('car_price_data2.csv')

    # Save the trained model to a file
    car_predictor.save_model('car_price_model.pkl')

    # Load the saved model from a file
    car_predictor.load_model('car_price_model.pkl')

    # Make predictions using the loaded model
    car_details = {
        'Year': 2018,
        'Present_Price': 9.99,
        'Kms_Driven': 40000,
        'Fuel_Type': 'Petrol',
        'Transmission': 'Manual'
    }
    selling_price = car_predictor.predict(car_details)
    print("Predicted Selling Price:", selling_price)


carprice_tester()