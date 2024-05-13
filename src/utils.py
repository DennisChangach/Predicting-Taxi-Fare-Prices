#The common functions that are utlised by components in the project
import os
import sys
import pickle
import numpy as np
import pandas as pd
import dill  #helps in creating the pickle file
from src.exception import CustomException
from src.logger import logging

from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV


#Function for saving objects
def save_object(file_path,obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)

    except Exception as e:
        raise CustomException(e,sys)

#Function to create objects
def create_features(dataset):
    logging.info("Converting the date columns to datetime format")
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
    
    return dataset
#Function for evaluating models
def evaluate_models(X_train, y_train,X_test,y_test,models,params):
    try:
        report = {}
        logging.info("Runing training and evaluation of the models")
        for i in range(len(list(models))):
            logging.info(f"Running {list(models.keys())[i]} model: Run {i+1} of {len(list(models))}")
            model = list(models.values())[i]
            para=params[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            #Setting the best params
            model.set_params(**gs.best_params_)
            #Training the model
            model.fit(X_train,y_train)

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e, sys)
    
#Function to Load the models/pickle files
def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)