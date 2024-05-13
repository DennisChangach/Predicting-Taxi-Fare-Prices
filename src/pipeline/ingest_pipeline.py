import os
import sys
from src.components.data_ingestion import DataIngestion
from src.components.data_preperation import DataPreparation
from src.exception import CustomException

class IngestPipeline:
    def __init__(self):
        pass

    def ingest_data(self):
        try:
            ingest = DataIngestion()
            ingest.initiate_data_ingestion()
        except Exception as e:
            raise CustomException(e,sys)

    def prep_data(self):
        try:
            prep = DataPreparation()
            prep.initiate_data_preparation()
        except Exception as e:
            raise CustomException(e,sys)