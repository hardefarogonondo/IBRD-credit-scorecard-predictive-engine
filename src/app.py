# Import Libraries
import json
import requests
import streamlit as st

# Initialization
API_URL = 'http://localhost:8000/score'
with open('inputs.json', 'r') as file:
    inputs = json.load(file)

# Main UI
st.title("IBRD Credit Scorecard Predictive Engine")

# Service Inputs
region = st.selectbox("Region", inputs["regions"])
country = st.selectbox("Country", inputs["countries"])
guarantor = st.selectbox("Guarantor", inputs["guarantors"])
loan_type = st.selectbox("Loan Type", inputs["loan_types"])
principal_amount = st.number_input("Principal Amount", min_value = 0)

# Predict Score Button
if st.button("Predict Score"):
    data = {"region": region,
            "country": country,
            "guarantor": guarantor,
            "loan_ype": loan_type,
            "principal_amount": principal_amount}
    response = requests.post(API_URL, json = {"data": data})
    prediction = response.json()["score"]
    st.write(f"Predicted Score: {prediction}")