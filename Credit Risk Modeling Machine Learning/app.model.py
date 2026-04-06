import streamlit as st
import pandas as pd
import joblib

# ==============================
# 📦 Cargar modelo
# ==============================
model = joblib.load('model/best_model.pkl')

# Columnas EXACTAS del entrenamiento
model_columns = [
    'Age','Job','Credit amount','Duration',
    'Sex_female','Sex_male',
    'Housing_free','Housing_own','Housing_rent',
    'Saving accounts_little','Saving accounts_moderate',
    'Saving accounts_quite rich','Saving accounts_rich',
    'Checking account_little','Checking account_moderate','Checking account_rich',
    'Purpose_business','Purpose_car','Purpose_domestic appliances',
    'Purpose_education','Purpose_furniture/equipment','Purpose_radio/TV',
    'Purpose_repairs','Purpose_vacation/others',
    'duration_per_year'
]

THRESHOLD = 0.5

# ==============================
# 🖥️ UI
# ==============================
st.title("💳 Credit Risk Prediction")

age = st.number_input("Age", 18, 100, 30)
job = st.number_input("Job (0-3)", 0, 3, 1)

sex = st.selectbox("Sex", ["male", "female"])
housing = st.selectbox("Housing", ["own", "rent", "free"])

saving_accounts = st.selectbox(
    "Saving accounts",
    ["little", "moderate", "quite rich", "rich"]
)

checking_account = st.selectbox(
    "Checking account",
    ["little", "moderate", "rich"]
)

purpose = st.selectbox(
    "Purpose",
    ["business","car","domestic appliances","education",
     "furniture/equipment","radio/TV","repairs","vacation/others"]
)

credit_amount = st.number_input("Credit amount", 0.0, value=1000.0)
duration = st.number_input("Duration (months)", 1, value=12)

# ==============================
# 🔮 Predicción
# ==============================
if st.button("Predict"):

    # Base
    input_data = pd.DataFrame({
        "Age": [age],
        "Job": [job],
        "Credit amount": [credit_amount],
        "Duration": [duration],
    })

    # Feature engineering
    input_data["duration_per_year"] = duration / 12

    # ==============================
    # One Hot manual (igual que entrenamiento)
    # ==============================

    # Sex
    input_data["Sex_male"] = 1 if sex == "male" else 0
    input_data["Sex_female"] = 1 if sex == "female" else 0

    # Housing
    for val in ["free","own","rent"]:
        input_data[f"Housing_{val}"] = 1 if housing == val else 0

    # Saving accounts
    for val in ["little","moderate","quite rich","rich"]:
        input_data[f"Saving accounts_{val}"] = 1 if saving_accounts == val else 0

    # Checking account
    for val in ["little","moderate","rich"]:
        input_data[f"Checking account_{val}"] = 1 if checking_account == val else 0

    # Purpose
    for val in [
        "business","car","domestic appliances","education",
        "furniture/equipment","radio/TV","repairs","vacation/others"
    ]:
        input_data[f"Purpose_{val}"] = 1 if purpose == val else 0

    # ==============================
    # Alinear columnas
    # ==============================
    input_data = input_data.reindex(columns=model_columns, fill_value=0)

    # ==============================
    # Predicción
    # ==============================
    proba = model.predict_proba(input_data)[0][1]
    prediction = 1 if proba >= THRESHOLD else 0

    # ==============================
    # Resultado
    # ==============================
    if prediction == 1:
        st.error("⚠️ Cliente Riesgoso (BAD)")
    else:
        st.success("✅ Cliente Confiable (GOOD)")

    st.write(f"📊 Probabilidad de default: {proba:.2%}")
    st.write(f"🎯 Threshold: {THRESHOLD}")