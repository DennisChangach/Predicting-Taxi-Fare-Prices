import os
import sys
import pandas as pd
from src.exception import CustomException
from src.utils import load_object
from src.logger import logging
from src.utils import create_features

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self,features):
        try:
            model_path = 'artifacts\model.pkl'
            preprocessor_path = 'artifacts\preprocessor.pkl'
            model = load_object(file_path = model_path)
            logging.info("Loaded the model")
            preprocessor = load_object(file_path = preprocessor_path)
            logging.info("Loaded the scaler ")

            #scaling the data
            data_scaled = preprocessor.transform(features)
            logging.info("Completed scaling the prediction features")
            preds = model.predict(data_scaled)
            logging.info("Completed doing predictions")
            return preds
        except Exception as e:
            raise CustomException(e,sys)

#Responsible for mapping the input fields from the FE to the backend
class CustomData:
    def __init__(self,
        VendorID: str,
        tpep_pickup_datetime: str,
        tpep_dropoff_datetime:str,
        passenger_count: int,
        trip_distance:float,
        RatecodeID: int,
        payment_type: int,
        PULocationID: int,
        DOLocationID:int,
        store_and_fwd_flag:str
        ):
        

        self.VendorID = VendorID

        self.tpep_pickup_datetime = tpep_pickup_datetime

        self.tpep_dropoff_datetime = tpep_dropoff_datetime

        self.passenger_count = passenger_count

        self.trip_distance = trip_distance

        self.RatecodeID = RatecodeID

        self.payment_type = payment_type

        self.PULocationID = PULocationID

        self.DOLocationID = DOLocationID

        self.store_and_fwd_flag = store_and_fwd_flag
    
    
    #Function to return the input as Dataframe
    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "VendorID": [self.VendorID],
                "tpep_pickup_datetime": [self.tpep_pickup_datetime],
                "tpep_dropoff_datetime": [self.tpep_dropoff_datetime],
                "passenger_count": [self.passenger_count],
                "trip_distance": [self.trip_distance],
                "RatecodeID": [self.RatecodeID],
                "store_and_fwd_flag": [self.store_and_fwd_flag],
                "PULocationID": [self.PULocationID],
                "DOLocationID": [self.DOLocationID],
                "payment_type": [self.payment_type],
                

            }
            logging.info("Loaded the prediction features as a Dataframe")
            df = pd.DataFrame(custom_data_input_dict)
            
            logging.info("Creating new features")
            df1 = create_features(df)

            logging.info("Dropping unused columns/features")
            df1.drop(['tpep_pickup_datetime','tpep_dropoff_datetime'],axis=1,inplace=True)
            return df1

        except Exception as e:
            raise CustomException(e, sys) 