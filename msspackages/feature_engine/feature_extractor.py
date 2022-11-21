import os
import sys
import json
import pandas as pd
import numpy as np


def get_features(feature_group_name = "node_autoencoder_ad_features", created_date = "11-21-2022"):
    ##feature schemas
    ## Read the feature schema for the feature store
    try:
        feature_schema_path = os.path.join(os.path.dirname(__file__), "eks_feature_store", feature_group_name + ".json")
        ##print(feature_schema_path)

        with open(feature_schema_path) as feature_schema:
            feature_data = json.load(feature_schema)

        feature_list_data = pd.json_normalize(data=feature_data, record_path='features_list', 
                                meta=['feature_group_name', 'feature_group_description', 'created_by', 'created_date'])
    except Exception as e:
        print("Error reading the features json -" + type(e))
        feature_list_data = pd.DataFrame()

    return feature_list_data

