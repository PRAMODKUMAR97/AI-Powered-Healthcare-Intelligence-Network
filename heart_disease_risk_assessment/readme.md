
# ❤️ AI-Powered Heart Disease Risk Assessment App

This interactive web application uses machine learning models to evaluate heart disease risk based on user input about demographics, medical history, and lifestyle factors. The system provides a personalized risk score and targeted recommendations using SHAP interpretability and LightGBM-based predictions.

---

## 📌 Description

The app analyzes user health data and lifestyle patterns with AI to:
- Predict the risk of heart disease.
- Highlight contributing risk factors.
- Recommend evidence-based actions for health improvement.

It provides a transparent, user-friendly experience and includes interpretability tools to explain predictions.

---

## 🚀 Features

- 🧑‍⚕️ Input user data: age, gender, health history, lifestyle habits.
- 📈 ML-based prediction using an ensemble of LightGBM classifiers.
- 🔍 Explainability with SHAP values and feature importance pie charts.
- ✅ Actionable and personalized health advice.
- 📊 Visual analytics to interpret contributing risk factors.
- 🌐 Deployable as a Streamlit web app.

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit, Plotly
- **Backend:** Python (pandas, numpy, shap)
- **Modeling:** LightGBM via `EasyEnsembleClassifier`, SHAP, Category Encoders
- **Data:** CDC BRFSS dataset (`brfss2022_data_wrangling_output.zip`)
