import os
import sys
from src.components.data_ingestion import DataIngestion
from src.components.data_preperation import DataPreparation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
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
def transform_data():
    try:
        train_data = "artifacts\\train.csv"
        test_data = "artifacts\\test.csv"

        data_transformation = DataTransformation()
        train_arr,test_arr= data_transformation.initiate_data_transformation(train_data,test_data)
        return train_arr,test_arr
    
    except Exception as e:
        raise CustomException(e,sys)
def model_train():
    try:
        train_arr,test_arr = transform_data()
        model_trainer = ModelTrainer()
        model_trainer.initiate_model_trainer(train_array=train_arr,test_array=test_arr)
    except Exception as e:
        raise CustomException(e,sys)

if __name__=="__main__":
    model_train()