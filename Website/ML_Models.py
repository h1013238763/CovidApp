import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer  # Import the SimpleImputer
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the Assets directory
assets_directory = os.path.join(current_directory, 'Assets/Model')

# Now specify the complete path to the file where you want to store the imputer
imputer_file_path = os.path.join(assets_directory, 'imputer.pkl')
model_file_path = os.path.join(assets_directory, 'model.pkl')

# # Load data and handle missing values
# data = pd.read_csv(data_set);
# data.replace({97: np.nan, 99: np.nan}, inplace=True)

# # Encode categorical features
# data['SEX'] = (data['SEX'] == 2).astype(int)
# data['DIABETES'] = (data['DIABETES'] == 1).astype(int)
# data['OBESITY'] = (data['OBESITY'] == 1).astype(int)
# data['ASTHMA'] = (data['ASTHMA'] == 1).astype(int)
# data['TOBACCO'] = (data['TOBACCO'] == 1).astype(int)

# data['PATIENT_TYPE']= (data['PATIENT_TYPE'] == 1).astype(int)
# # Select features and target variable
# selected_columns = ['SEX', 'AGE', 'DIABETES', 'OBESITY', 'ASTHMA', 'TOBACCO','PATIENT_TYPE']
# X = data[selected_columns]
# y = (data['CLASIFFICATION_FINAL'] <= 3).astype(int)

# # Handle missing values using imputation
# imputer = SimpleImputer(strategy='mean')  # You can change the strategy as needed
# X = imputer.fit_transform(X)

# # Split the data into train and test sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Initialize and train the logistic regression model
# model = LogisticRegression()
# model.fit(X_train, y_train)

# # Make predictions
# # y_pred = model.predict(X_test)

# # Serialize the model to a file
# with open(model_file_path, "wb") as model_file:
#     pickle.dump(model, model_file)

# # Serialize the imputer to a file
# with open(imputer_file_path, "wb") as imputer_file:
#     pickle.dump(imputer, imputer_file)

# Calculate and print accuracy
# accuracy = accuracy_score(y_test, y_pred)
# print(f"Accuracy: {accuracy * 100:.2f}%")

# Print the classification report
# print(classification_report(y_test, y_pred))

#model 2 ##############################################################################

# covid_data_set = os.path.join(assets_directory, 'Covid Data UPDATED.csv')
# symptom_data_set = os.path.join(assets_directory, 'Covid 19 symptoms data UPDATED.csv')

# # Load and Explore Data
# symptom_data = pd.read_csv(symptom_data_set)
# covid_data = pd.read_csv(covid_data_set)

# # Randomize the data
# symptom_data_randomized = symptom_data.sample(frac=1, random_state=20)
# covid_data_randomized = covid_data.sample(frac=1, random_state=20)

# # Reduce the size to 100 rows each
# symptom_data_sampled = symptom_data_randomized.head(100)
# covid_data_sampled = covid_data_randomized.head(100)

# # Merge datasets using common identifiers
# merged_data = pd.merge(symptom_data_sampled, covid_data_sampled, on=['Age_0-9', 'Age_10-19', 'Age_20-24', 'Age_25-59', 'Age_60+', 'SEX'])

# # Feature Selection
# X = merged_data[['Fever', 'Tiredness', 'Dry-Cough', 'Difficulty-in-Breathing', 'Sore-Throat',
#                  'None_Sympton', 'Age_0-9', 'Age_10-19', 'Age_20-24', 'Age_25-59', 'Age_60+',
#                  'Severity_None', 'Severity_Mild', 'Severity_Moderate', 'Severity_Severe',
#                  'SEX', 'DIABETES', 'OBESITY', 'ASTHMA', 'TOBACCO']]
# y = merged_data['HAS_COVID']

# # Train-Test Split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Define an extended search space (can be adjusted based on your specific requirements)
# param_dist = {
#     'n_estimators': [50, 100, 150, 200],
#     'max_depth': [3, 5, 7, 10],
#     'learning_rate': [0.01, 0.05, 0.1, 0.2],
#     'subsample': [0.8, 0.9, 1.0],
#     'min_samples_split': [2, 5, 10],
#     'min_samples_leaf': [1, 2, 4]
# }

# # Use only the Gradient Boosting Classifier
# model = GradientBoostingClassifier(random_state=42)

# # Use RandomizedSearchCV with parallel processing
# random_search = RandomizedSearchCV(model, param_dist, n_iter=10, cv=5, n_jobs=-1)
# random_search.fit(X_train, y_train)

# # Build and Train the Model with the best parameters
# best_model_random = random_search.best_estimator_
# best_model_random.fit(X_train, y_train)

# # Handle missing values using imputation
# imputer = SimpleImputer(strategy='mean')  # You can change the strategy as needed
# X = imputer.fit_transform(X)

#model 3##############################################################################
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


# Load the data
file_path = os.path.join(assets_directory, 'Covid_19_symptoms_data_UPDATED.csv')
df = pd.read_csv(file_path)

# Define features and target variable
features = ['Fever', 'Tiredness', 'Dry-Cough', 'Difficulty-in-Breathing', 'Sore-Throat',
            'None_Sympton', 'Age_0-9', 'Age_10-19', 'Age_20-24', 'Age_25-59', 'Age_60+',
            'Severity_Mild', 'Severity_Moderate', 'Severity_None', 'Severity_Severe']

print(df.columns)
X = df[features]
y = df['HAS_COVID']

imputer = SimpleImputer(strategy='mean')  # or another strategy like 'median', 'most_frequent'
X_imputed = imputer.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42)

# Create a Random Forest classifier model
model = RandomForestClassifier(random_state=42)

# Train the model
model.fit(X_train, y_train)

# Predictions on the test set
# y_pred = model.predict(X_test)

with open(model_file_path, "wb") as model_file:
    pickle.dump(model, model_file)

# Serialize the imputer to a file
with open(imputer_file_path, "wb") as imputer_file:
    pickle.dump(imputer, imputer_file)

# Evaluate the Model
# y_pred_random = best_model_random.predict(X_test)

