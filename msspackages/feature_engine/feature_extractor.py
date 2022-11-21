import os
import sys
import json
import pandas as pd
import numpy as np


def get_features(feature_file_name="node_autoencoder_ad_features", feature_group = "node_autoencoder_ad_features", created_date = "11-21-2022"):
    ##feature schemas
    ## Read the feature schema for the feature store
    try:
        feature_schema_path = os.path.join(os.path.dirname(__file__), "eks_feature_store", feature_file_name + ".json")
        ##print(feature_schema_path)

        with open(feature_schema_path) as feature_schema:
            feature_data = json.load(feature_schema)

        feature_list_data = pd.json_normalize(data=feature_data, record_path='features_list', 
                                meta=['feature_group_name', 'feature_group_description', 'created_by', 'created_date'])
    except Exception:
        print("Error reading the features json")
        feature_list_data = pd.DataFrame()

    return feature_list_data

