# Import Libraries
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pandas as pd
import pickle

# Initialization
with open('../../models/final_scorecard.pkl', 'rb') as file:
    scorecard = pickle.load(file)
app = FastAPI()
class Item(BaseModel):
    data: dict

@app.post('/score')
def score_data(item: Item):
    raw_data = pd.DataFrame(item.data, index = [0])
    transformed_data = transform_data(raw_data)
    score = calculate_score(transformed_data)
    return {"score": score}

def region_binning(df):
    df["region"] = df["region"].replace(regions_bin)
    return df

def country_binning(df, groups):
    for i, group in enumerate(groups):
        for country in group:
            df.loc[df["country"] == country, "country"] = f'group_{chr(97+i)}'
    remaining_countries = set(df["country"]) - set([f'group_{chr(97+i)}' for i in range(len(groups))])
    last_group_name = f'group_{chr(97+len(groups)-1)}'
    for country in remaining_countries:
        df.loc[df["country"] == country, "country"] = last_group_name
    return df

def guarantor_binning(df, groups):
    for i, group in enumerate(groups):
        for guarantor in group:
            df.loc[df["guarantor"] == guarantor, "guarantor"] = f'group_{chr(97+i)}'
    remaining_guarantors = set(df["guarantor"]) - set([f'group_{chr(97+i)}' for i in range(len(groups))])
    last_group_name = f'group_{chr(97+len(groups)-1)}'
    for guarantor in remaining_guarantors:
        df.loc[df["guarantor"] == guarantor, "guarantor"] = last_group_name
    df["guarantor"] = df["guarantor"].fillna(last_group_name)
    return df

def loan_type_binning(df, groups):
    for i, group in enumerate(groups):
        for loan_type in group:
            df.loc[df["loan_type"] == loan_type, "loan_type"] = f'group_{chr(97+i)}'
    remaining_loan_types = set(df["loan_type"]) - set([f'group_{chr(97+i)}' for i in range(len(groups))])
    return df

def principal_amount_binning(df):
    bins = [-np.inf, 1978840.31, 8013587.75, 23240000.00, 40215236.00, 54947816.00, 249441952.00, np.inf]
    bin_labels = ["-inf_to_1978840.31", "1978840.31_to_8013587.75", "8013587.75_to_23240000.00", "23240000.00_to_40215236.00", "40215236.00_to_54947816.00", "54947816.00_to_249441952.00", "249441952.00_to_inf"]
    df["principal_amount"] = pd.cut(df["principal_amount"], bins = bins, labels = bin_labels)
    df["principal_amount"] = df["principal_amount"].astype(str)
    return df

def feature_binning(df):
    df = region_binning(df)
    df = country_binning(df, country_groups)
    df = guarantor_binning(df, guarantor_groups)
    df = loan_type_binning(df, loan_type_groups)
    df = principal_amount_binning(df)
    return df

def transform_data(raw_data):
    binned_data = feature_binning(raw_data)
    raw_data = pd.get_dummies(df,
                                columns = feature_to_encode,
                                prefix = feature_to_encode,
                                prefix_sep = ":")
    encoded_data = raw_data.astype(int)

    # If your scorecard expects certain columns that might be missing in the input data,
    # you should add those columns with default values. Example:
    expected_columns = list(scorecard['Feature Name'])
    for column in expected_columns:
        if column not in raw_data.columns:
            raw_data[column] = 0

    # Make sure the column order matches the scorecard
    raw_data = raw_data[expected_columns]

    return encoded_data


def calculate_score(transformed_data):
    score = np.dot(transformed_data.values, scorecard['Score - Final'].values)
    return score
