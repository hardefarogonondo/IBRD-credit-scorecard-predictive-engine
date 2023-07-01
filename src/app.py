import streamlit as st
import requests
import json

# Defining the server URL
API_URL = "http://localhost:8000/score"

# UI building
st.title("IBRD Credit Scorecard Predictive Engine")

# Input fields
region = st.selectbox('Region', ['Region 1', 'Region 2', 'Region 3'])
country = st.selectbox('Country', ['Country 1', 'Country 2', 'Country 3'])
guarantor = st.selectbox('Guarantor', ['Guarantor 1', 'Guarantor 2', 'Guarantor 3'])
loan_type = st.selectbox('Loan Type', ['Loan Type 1', 'Loan Type 2', 'Loan Type 3'])
principal_amount = st.number_input('Principal Amount', min_value=0)

# Submit button
if st.button('Predict Score'):
    # Creating the data dictionary
    data = {'Region': region, 'Country': country, 'Guarantor': guarantor, 'Loan Type': loan_type, 'Principal Amount': principal_amount}
    
    # Sending a post request to our API and saving the response
    response = requests.post(API_URL, json={'data': data})
    
    # Extracting the prediction from the response
    prediction = response.json()['score']
    
    st.write(f"Predicted Score: {prediction}")
