# Import Libraries
import json
import requests
import streamlit as st

# Initialization
API_URL = 'http://127.0.0.1:8000/score'
with open('../config/input_options.json', 'r') as file:
    input_options = json.load(file)

# Main UI
st.title("IBRD Credit Scorecard Predictive Engine")

# Service Inputs
region = st.selectbox("Region", input_options["regions"])
country = st.selectbox("Country", input_options["countries"])
guarantor = st.selectbox("Guarantor", input_options["guarantors"])
loan_type = st.selectbox("Loan Type", input_options["loan_types"])
principal_amount = st.number_input("Principal Amount", min_value = 0)

# Predict Score Button
if st.button("Predict Score"):
    data = {"region": region,
            "country": country,
            "guarantor": guarantor,
            "loan_type": loan_type,
            "principal_amount": principal_amount}
    response = requests.post(API_URL, json = {"data": data})
    prediction = response.json()["score"]
    st.write(f"Predicted Score: {prediction}")