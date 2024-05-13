import os
import sys
from src.exception import CustomException
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformationConfig
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer


class TrainPipeline:
    def __init__(self):
        pass

    def train_model(self):
        try:
            train_data = "artifacts\\train.csv"
            test_data = "artifacts\\test.csv"

            data_transformation = DataTransformation()
            train_arr,test_arr= data_transformation.initiate_data_transformation(train_data,test_data)

            model_trainer = ModelTrainer()
            model_trainer.initiate_model_trainer(train_array=train_arr,test_array=test_arr)
        except Exception as e:
            raise CustomException(e,sys)