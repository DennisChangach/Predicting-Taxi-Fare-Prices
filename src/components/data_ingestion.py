#Reading the data from the source e.g database
import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from pyspark.sql import SparkSession
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    #path for data ingestion component
    raw_data_path:str=os.path.join('artifacts','data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()

    def initiate_data_ingestion(self):
        '''
        This function loads the raw file and generates a sample csv file to be used for modelling
        '''
        logging.info("Entered the data ingestion component")
        try:
            # Create SparkSession
            logging.info("Started Creating a Spark Session")
            spark = SparkSession.builder.appName("CSV_Sample").getOrCreate()
            logging.info("Spark session created..loading the raw dataset now")
            #Reading the dataset
            raw_data = spark.read.csv("data\\2017_Yellow_Taxi_Trip_Data.csv",header = True,inferSchema=True)
            #logging this in the logfiles
            logging.info("Read the dataset as a spark dataframe...generating sample data next")

            # Sample 5 million rows explicitly (optional)
            df_sample = raw_data.sample(withReplacement=False, fraction=0.001)

            logging.info("Generated smaple...converting to pandas dataframe next")
            #converting to pandas dataframe
            pandas_df = df_sample.toPandas()
            
            logging.info("Created pandas dataframe...saving to a CSV file next")
            #saving the raw data
            pandas_df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

        
            logging.info("Ingestion of the data is completed")

            return(
                self.ingestion_config.raw_data_path
            )

        except Exception as e:
            raise CustomException(e,sys)
        