import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataPreparationConfig:
    #path for data preparation component
    raw_data_path:str=os.path.join('artifacts','data.csv')
    train_data_path:str=os.path.join('artifacts','train.csv')
    test_data_path:str=os.path.join('artifacts','test.csv')

class DataPreparation:
    def __init__(self):
        self.preparation_config=DataPreparationConfig()

    def initiate_data_preparation(self):
        logging.info("Entered the data preparation component")
        try:
            #reading the csv file into a dataframe
            df = pd.read_csv(self.preparation_config.raw_data_path)
            #logging this in the logfiles
            logging.info("Read the dataset as a dataframe")

            dataset = df.copy()
            logging.info("Converting the date columns to datatime format")
            #Converting to datetime
            dataset["tpep_pickup_datetime"] = pd.to_datetime(dataset["tpep_pickup_datetime"])
            dataset["tpep_dropoff_datetime"] = pd.to_datetime(dataset["tpep_dropoff_datetime"])

            logging.info("Creating Trip Duration Column")
            #calculating trip duration(in minutes) using pickup & dropoff times
            dataset['trip_duration'] = (dataset["tpep_dropoff_datetime"] - dataset["tpep_pickup_datetime"]).dt.total_seconds() / 60

            logging.info("Creating Time Variables")
            #Creating the time variables
            dataset['pickup_day_no']=dataset['tpep_pickup_datetime'].dt.weekday
            dataset['dropoff_day_no']=dataset['tpep_dropoff_datetime'].dt.weekday
            dataset['pickup_hour']=dataset['tpep_pickup_datetime'].dt.hour
            dataset['dropoff_hour']=dataset['tpep_dropoff_datetime'].dt.hour
            dataset['pickup_month']=dataset['tpep_pickup_datetime'].dt.month
            dataset['dropoff_month']=dataset['tpep_dropoff_datetime'].dt.month
            dataset['pickup_year']=dataset['tpep_pickup_datetime'].dt.year
            dataset['dropoff_year']=dataset['tpep_dropoff_datetime'].dt.year

            logging.info("Filtering dataframe to remove records")
            #removing records where trip duration, trip distance and total fare amount are recorded as 0
            dataset_1 = dataset[(dataset['trip_duration'] !=0) & (dataset['trip_distance']!=0) & (dataset['fare_amount']>0)].reset_index(drop=True)
            
            logging.info("Removing unused columns")
            #Dropping the columns that will NOT be used in the analysis & building the model
            dataset_1.drop(['extra',
                'mta_tax', 'tip_amount', 'tolls_amount', 'improvement_surcharge',
                'total_amount','tpep_pickup_datetime','tpep_dropoff_datetime'],axis=1,inplace=True)
            
            
            #Train test Split
            logging.info("Train Test split initiated")
            train_set,test_set = train_test_split(dataset_1,test_size=0.2,random_state=42)

            #saving the train & test datasets
            train_set.to_csv(self.preparation_config.train_data_path,index=False, header=True)
            test_set.to_csv(self.preparation_config.test_data_path,index=False,header=True)

            logging.info("Preparation of the data is completed")

            return(
                self.preparation_config.train_data_path,
                self.preparation_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e,sys)