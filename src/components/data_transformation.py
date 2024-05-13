#Transforming the data & Pre-Processing the Data
import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts',"preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    #Function for creating the pickle file that will be useful in data transformation
    def get_data_transformer_object(self):
        '''
        This function is responsible for getting the data transformation object
        
        '''
        logging.info("Entered data transformation component")

        try:
            #Numerical & Categorical Features
            numerical_columns = ['VendorID', 'passenger_count', 'trip_distance', 'RatecodeID',
       'PULocationID', 'DOLocationID', 'payment_type',
        'trip_duration', 'pickup_day_no', 'dropoff_day_no',
       'pickup_hour', 'dropoff_hour', 'pickup_month', 'dropoff_month',
       'pickup_year', 'dropoff_year']
            categorical_columns = ['store_and_fwd_flag']

            #Numerical Pipeline
            num_pipeline = Pipeline(
                steps = [
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]
            )
            logging.info(f"Numerical column encoding completed: {numerical_columns}")

            #Categorical Pipeline
            cat_pipeline = Pipeline(
                steps = [
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))

                ]
            )
            logging.info(f"Catergorical column encoding completed: {categorical_columns}")

            #Combining both using ColumnTransformer
            preprocessor = ColumnTransformer(
                [
                   ("num_pipeline",num_pipeline,numerical_columns),
                   ("cat_pipeline",cat_pipeline,categorical_columns) 
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)
        
    #Function to start data transformatiomn
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Reading train and test data completed")

            logging.info("Obtaining preprocessing object")

            #Getting the prerocessing object
            preprocessing_obj = self.get_data_transformer_object()

            target_column_name="fare_amount"
           
            #Defining the input train and target feature
            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            #Applying transformatin to te train & test input features: returns an array
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            #Applying transformation on the test features
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            #stacking the arrays side by side
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            #Calling the save object function to store the pickle file
            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )

            return (
                train_arr,
                test_arr,
            )
        except Exception as e:
            raise CustomException(e,sys)