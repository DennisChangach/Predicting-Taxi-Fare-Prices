import os
import sys
from src.components.data_ingestion import DataIngestion
from src.components.data_preperation import DataPreparation
from src.exception import CustomException

def ingest_data():
    try:
        ingest = DataIngestion()
        ingest.initiate_data_ingestion()
    except Exception as e:
        raise CustomException(e,sys)

def prep_data():
    try:
        prep = DataPreparation()
        prep.initiate_data_preparation()
    except Exception as e:
        raise CustomException(e,sys)

if __name__=="__main__":
    prep_data()