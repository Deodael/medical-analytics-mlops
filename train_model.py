import os
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression

# 1. Generate standard training feature profiles [Age, BMI, Cholesterol]
X_train = np.array([
    [22, 21.0, 160], [25, 23.4, 175],  # Baseline Low Risk
    [65, 34.2, 260], [58, 31.1, 240],  # Baseline High Risk
    [30, 24.5, 180], [45, 28.2, 210],
    [70, 29.5, 250], [21, 19.2, 150]
])

# Labels: 0 = Low Risk, 1 = High Risk
y_train = np.array([0, 0, 1, 1, 0, 1, 1, 0])

# 2. Train the predictive classifier 
print("⚡ Training medical risk classification model matrix...")
model = LogisticRegression()
model.fit(X_train, y_train)

# 3. Create the destination directory if it doesn't exist and serialize the weights
os.makedirs("src", exist_ok=True)
model_file_path = "src/medical_model.pkl"
joblib.dump(model, model_file_path)

print(f"✅ Model binary successfully serialized to: {model_file_path}")
