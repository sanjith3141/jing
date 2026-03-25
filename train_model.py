import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib

# -------------------------
# LOAD DATA
# -------------------------

df = pd.read_csv("purchase_regret_dataset_15000.csv")

# -------------------------
# FEATURE ENGINEERING (🔥 MOST IMPORTANT)
# -------------------------

# Price to Income Ratio (CORE FIX)
df["Price_Income_Ratio"] = df["Price"] / df["Monthly_Income"]

# Log scaling (handles huge ranges)
df["Log_Price"] = np.log1p(df["Price"])
df["Log_Income"] = np.log1p(df["Monthly_Income"])

# -------------------------
# ENCODE CATEGORICALS (FIXED PROPERLY)
# -------------------------

label_encoders = {}

categorical_cols = [
    "Mood",
    "Urgency_Level",
    "Brand_Familiarity",
    "Purchase_Category",
    "Peer_Influence"
]

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le  # store for later use

# -------------------------
# FEATURES & TARGET
# -------------------------

X = df.drop("Regret", axis=1)
y = df["Regret"]

# -------------------------
# SCALING (IMPORTANT)
# -------------------------

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# -------------------------
# TRAIN TEST SPLIT
# -------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# -------------------------
# MODEL
# -------------------------

model = RandomForestClassifier(
    n_estimators=150,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)

# -------------------------
# SAVE EVERYTHING
# -------------------------

joblib.dump(model, "regret_model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(label_encoders, "encoders.pkl")

# -------------------------
# EVALUATION (BONUS)
# -------------------------

accuracy = model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy*100:.2f}%")
print("Model trained and saved successfully.")
