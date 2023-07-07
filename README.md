# IBRD Credit Scorecard Predictive Engine

An innovative solution for credit scoring leveraging machine learning to predict credit risk using The International Bank for Reconstruction and Development (IBRD) Loans dataset.

## Table of Contents

1. [Project Description](#project-description)
2. [System Architecture](#system-architecture)
3. [Data Requirements and Response](#data-requirements-and-response)
4. [Dataset Information](#dataset-information)
5. [Usage](#usage)
6. [Workflow](#workflow)
7. [Conclusions and Future Work](#conclusions-and-future-work)
8. [References](#references)

## Project Description

The project aims to tackle the critical task of segregating loan risks for banks and other financial institutions. The International Bank for Reconstruction and Development (IBRD) Loans dataset provides the foundation for developing a scorecard system to predict credit risk.

## System Architecture

This solution employs a Logistic Regression model developed with Python. The model's design allows extraction of each feature's Log Odds, which aids in calculating the final scorecard.

## Data Requirements and Response

For prediction via the API, the input requires specific data related to the borrower. The output response from the API will be the predicted score, with higher scores indicating lesser risk.

## Dataset Information

The dataset contains loan data from IBRD. It includes various features like Region, Country, Guarantor, Loan Type, and Original Principal Amount. The dataset was treated by dropping columns with more than 50% missing values, creating labels for the loan status, and one-hot encoding the features.

## Usage

This section includes information about the expected input payload and the project output message format. It also contains a step-by-step guide on how to use the machine learning service in local environments, with model retraining and running the API locally.

**API Request Format**

Your API request must be in the following format:

```json
{
  "data": {
    "region": "EUROPE AND CENTRAL ASIA",
    "country": "Croatia",
    "guarantor": "No Guarantor",
    "loan_type": "BLNC",
    "principal_amount": 100000000
  }
}
```

**API Response Format**

Your API request must be in the following format:

```json
{
  "score": 448
}
```

## Workflow

This section provides detailed documentation of the project workflow, starting from data acquisition and preparation, exploratory data analysis, feature engineering, model building, and evaluation.

## Conclusions and Future Work

A summary of the project outcomes, key findings, and suggestions for future improvements and potential explorations.

## References

This section lists all the references and resources utilized during the project.

[1] [Credit Scoring Methods: Latest Trends and Points to Consider](https://www.sciencedirect.com/science/article/pii/S2405918822000095)

[2] [Credit Scoring, Statistical Techniques and Evaluation Criteria: A Review of The Literature](https://www.researchgate.net/publication/220613924_Credit_Scoring_Statistical_Techniques_and_Evaluation_Criteria_A_Review_of_the_Literature)

[3] [Credit Risk Scorecard Estimation by Logistic Regression](https://core.ac.uk/reader/43337320)

[4] [Credit Scorecard Based on Logistic Regression with Random Coefficients](https://www.researchgate.net/publication/220308365_Credit_scorecard_based_on_logistic_regression_with_random_coefficients)

[5] [Mixed Credit Scoring Model of Logistic Regression and Evidence Weight in The Background of Big Data](https://www.researchgate.net/publication/332381614_Mixed_Credit_Scoring_Model_of_Logistic_Regression_and_Evidence_Weight_in_the_Background_of_Big_Data)
