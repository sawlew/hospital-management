import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
data = pd.read_csv('appointments.csv')

# Preprocess the data
data['appointment_date'] = pd.to_datetime(data['appointment_date'])
data['scheduled_date'] = pd.to_datetime(data['scheduled_date'])
data['waiting_time'] = (data['appointment_date'] - data['scheduled_date']).dt.days

# Features and labels
features = ['age', 'waiting_time']
X = data[features]
y = data['no_show']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save the model
joblib.dump(model, 'no_show_predictor.joblib')
