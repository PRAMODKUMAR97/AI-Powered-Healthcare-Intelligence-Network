import pandas as pd
import streamlit as st
import numpy as np
import pickle
import joblib
from PIL import Image

st.sidebar.markdown("<h2 style='color: #ffffff;'>📌  Description</h2>", unsafe_allow_html=True)
st.sidebar.image("utils/ph4.png", use_container_width=True)
st.sidebar.markdown("<p class='sidebar-text'>Our AI-powered Drug Recommendation System uses NLP and cosine similarity to analyze medicines and recommend the most relevant alternatives, ensuring accurate, data-driven, and personalized treatment options.</p>", unsafe_allow_html=True)


# Cache loading of models and data for faster execution
@st.cache_resource()
def load_models():
    with open('models/second_feature_models/medicine_dict.pkl', 'rb') as file:
        medicine_dict = pickle.load(file)
    similarity = joblib.load('models/second_feature_models/similarity.joblib')

    return pd.DataFrame(medicine_dict), similarity

@st.cache_resource()
def load_description_data():
    return pd.read_csv('data/Drug reccomendation/medicine.csv')

# Load models and data
medicines, similarity = load_models()
description_data = load_description_data()

# Recommendation function
@st.cache_data()
def recommend(medicine):
    try:
        medicine_index = medicines[medicines['Drug_Name'] == medicine].index[0]
    except IndexError:
        return []
    distances = similarity[medicine_index]
    medicines_list = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[1:6]
    return [medicines.iloc[i[0]].Drug_Name for i in medicines_list]

# Title
st.markdown("""
    <h1 style='text-align: center; color: #004085; font-size: 36px;'>💊 Drug Recommendation System</h1>
""", unsafe_allow_html=True)

# Image Display
image = Image.open('utils/medss.png')
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(image, width=350)

# Searchbox
st.markdown("""
    <h3 style='color: #2c3e50;'>🔍 Find Similar Drugs:</h3>
""", unsafe_allow_html=True)

col1, col2 = st.columns([4, 1])
with col1:
    selected_medicine_name = st.selectbox('Select a medicine:', sorted(medicines['Drug_Name'].values))
with col2:
    recommend_btn = st.button('🔍 Recommend Drug')

# CSS styling
st.markdown("""
    <style>
        div[data-testid="stButton"] > button {
            width: 100%;
            background-color: #007bff;
            color: white;
            border-radius: 10px;
            padding: 8px;
            font-size: 16px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Display Description
desc = description_data.loc[description_data['Drug_Name'] == selected_medicine_name, 'Description']
if not desc.empty:
    st.markdown(f"""
        <p style='background-color: #2c3e50; color: #ffffff; padding: 12px; border-radius: 10px; font-size: 16px;'>
        <strong>Description:</strong> {desc.values[0]}</p>
    """, unsafe_allow_html=True)

# Display Recommendations
if recommend_btn:
    recommendations = recommend(selected_medicine_name)
    if recommendations:
        st.markdown("""
            <h3 style='color: #34495e;'>📌 Recommended Drugs:</h3>
        """, unsafe_allow_html=True)
        
        for drug in recommendations:
            buy_link = f"https://pharmeasy.in/search/all?name={drug}"
            st.markdown(f"""
                <p style='font-size:18px; border:2px solid #34495e; padding: 10px; border-radius:10px; display: flex; justify-content: space-between;'>
                    <a href='{buy_link}' style='text-decoration:none; color:#007bff; font-weight:bold;'>
                    {drug}</a>
                    <a href='{buy_link}' style='background-color: #28a745; color: white; padding: 5px 10px; border-radius: 5px; text-decoration: none;'>
                    🛒 Buy Now</a>
                </p>
            """, unsafe_allow_html=True)
    else:
        st.error("No recommendations found. Please select another drug.")

# Footer
st.markdown("""
    <hr>
    <p style='text-align: center; color: #7f8c8d;'>Made by <span style='color: orange'>Abhay</span> | 
    <a href='' style='text-decoration:none'>Github</a> © 2025</p>
""", unsafe_allow_html=True)
