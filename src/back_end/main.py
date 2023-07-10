# Import Libraries
from fastapi import FastAPI
from pydantic import BaseModel
import json
import numpy as np
import pandas as pd
import pickle

# Initialization
with open('/app/models/final_scorecard.pkl', 'rb') as file:
    scorecard = pickle.load(file)
with open('/app/config/binnings.json', 'r') as file:
    binnings = json.load(file)
app = FastAPI()


class Item(BaseModel):
    data: dict


def country_guarantor_status_generator(raw_data):
    raw_data["country_guarantor_status"] = raw_data.apply(lambda row: "same" if row["country"] == row["guarantor"]
                                                          else ("no_guarantor"
                                                                if pd.isnull(row["guarantor"])
                                                                else "differ"), axis=1)
    return raw_data


def region_binning(raw_data):
    raw_data["region"] = raw_data["region"].replace(binnings["regions_bin"])
    return raw_data


def country_binning(raw_data):
    country_bins = binnings["country_bins"]
    for group, countries in country_bins.items():
        raw_data.loc[raw_data["country"].isin(countries), "country"] = group
    return raw_data


def guarantor_binning(raw_data):
    guarantor_bins = binnings["guarantor_bins"]
    for group, guarantors in guarantor_bins.items():
        raw_data.loc[raw_data["guarantor"].isin(
            guarantors), "guarantor"] = group
    return raw_data


def loan_type_binning(raw_data):
    loan_type_bins = binnings["loan_type_bins"]
    for group, loan_types in loan_type_bins.items():
        raw_data.loc[raw_data["loan_type"].isin(
            loan_types), "loan_type"] = group
    return raw_data


def principal_amount_binning(raw_data):
    principal_amount_bins = binnings["principal_amount_bins"]
    raw_data["bins"] = np.nan
    for bin in principal_amount_bins:
        lower, upper, bin_name = bin
        mask = (raw_data["principal_amount"].astype(float) > lower) & (
            raw_data["principal_amount"].astype(float) <= upper)
        raw_data.loc[mask, "bins"] = bin_name
    raw_data["principal_amount"] = raw_data["bins"]
    raw_data = raw_data.drop(columns="bins")
    return raw_data


def feature_engineering(raw_data):
    binned_data = country_guarantor_status_generator(raw_data)
    binned_data = region_binning(binned_data)
    binned_data = country_binning(binned_data)
    binned_data = guarantor_binning(binned_data)
    binned_data = loan_type_binning(binned_data)
    binned_data = principal_amount_binning(binned_data)
    return binned_data


def one_hot_encoding(binned_data):
    category_dict = binnings["categories"]
    for feature, categories in category_dict.items():
        for category in categories:
            binned_data[f"{feature}:{category}"] = (
                binned_data[feature] == category).astype(int)
        binned_data = binned_data.drop(columns=feature)
    return binned_data


def get_score(encoded_data, scorecard):
    encoded_data_copy = encoded_data.copy()
    missing_cols = set(scorecard["Feature Name"]) - set(encoded_data.columns)
    for column in missing_cols:
        encoded_data_copy[column] = 0
    encoded_data_copy["Intercept"] = 1
    encoded_data_copy = encoded_data_copy[scorecard["Feature Name"]]
    scorecard_scores = scorecard["Score - Final"].values.reshape(
        scorecard.shape[0], 1)
    scored_data = encoded_data_copy.dot(scorecard_scores)
    return int(scored_data.values[0][0])


@app.post('/score')
def score_data(item: Item):
    raw_data = pd.DataFrame(item.data, index=[0])
    binned_data = feature_engineering(raw_data)
    encoded_data = one_hot_encoding(binned_data)
    score = get_score(encoded_data, scorecard)
    return {"score": score}
