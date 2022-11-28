import os
import sys
import json
import pandas as pd
import numpy as np
from glob import glob


def get_features(input_feature_group_name = "", input_created_date = ""):
    ##feature schemas
    ## Read the feature schema for the feature store
    try:
        all_features_path = glob(os.path.join(os.path.dirname(__file__), "eks_feature_store", "*.json"))
        #print(all_features_path)

        for count,file_name in enumerate(all_features_path):
            with open(file_name) as f:
                feature_data = json.load(f)
                print(feature_data)
                if count == 0 :
                    features_df = pd.json_normalize(data=feature_data, record_path='features_list', 
                                meta=['feature_group_name', 'feature_group_description', 'model_type', 'problem_type', 'created_by', 'created_date', 'model_parameters'])
                else:
                    features_df =  features_df.append(pd.json_normalize(data=feature_data, record_path='features_list', 
                                meta=['feature_group_name', 'feature_group_description', 'model_type', 'problem_type',  'created_by', 'created_date', 'model_parameters']))

        # pd.set_option('display.max_columns', None)
        # print(features_df)

        if input_feature_group_name != "" and input_created_date != "":
            features_df = features_df[(features_df['feature_group_name'] == input_feature_group_name) & (features_df['created_date'] == input_created_date)]

    except Exception as e:
        error_type = type(e)
        print("Error reading the features json -" + str(error_type))
        features_df = pd.DataFrame()

    return features_df
