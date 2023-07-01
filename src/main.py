from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import pickle
import numpy as np

# load the scorecard
with open('../../models/final_scorecard.pkl', 'rb') as file:
    scorecard = pickle.load(file)

app = FastAPI()

# Define a Pydantic model to handle incoming request body
class Item(BaseModel):
    data: dict

@app.post('/score')
def score_data(item: Item):
    # convert the incoming json to a pandas dataframe
    raw_data = pd.DataFrame(item.data, index=[0])

    # transform the raw data to match the scorecard
    transformed_data = transform_data(raw_data)

    # dot product with scorecard
    score = calculate_score(transformed_data)

    return {'score': score}

def transform_data(raw_data):
    # Include all necessary transformations on your incoming data
    # to match the form of the data used to create the scorecard.

    # Example: one-hot encoding a categorical feature
    raw_data = pd.get_dummies(raw_data, columns=['Region', 'Country', 'Guarantor', 'Loan Type'])

    # If your scorecard expects certain columns that might be missing in the input data,
    # you should add those columns with default values. Example:
    expected_columns = list(scorecard['Feature Name'])
    for column in expected_columns:
        if column not in raw_data.columns:
            raw_data[column] = 0

    # Make sure the column order matches the scorecard
    raw_data = raw_data[expected_columns]

    return raw_data


def calculate_score(transformed_data):
    score = np.dot(transformed_data.values, scorecard['Score - Final'].values)
    return score
