# Predicting Taxi Fare Prices
This repository implements a machine learning pipeline for predicting taxi fares using a modular approach. The project is divided into well-defined components focusing on specific tasks, promoting reusability, maintainability, and scalability.

## Key Features:

- Modular Design: The code is organized into modules for data ingestion, preparation, transformation, model training, and utilities.
- Data Pipelines: Components are chained together using pipelines for efficient data processing workflows.
- Taxi Fare Prediction: Predicts taxi fares based on historical data.

![Streamlit App](/src/artifacts/images/streamlit_app.jpg)

## Getting Started

- Prerequisites: Python (version 3.10 or above), libraries from requirements.txt
- Clone this repository.
- Run ```pip install -r requirements.txt``` to install dependencies.

## Running the Project:

- Prepare your data: Download the data from the website and upload to the data folder.
- Run the pipeline: Execute the script main.py to run the entire data processing and model training pipeline.

## Project Structure:

data: Contains sample taxi fare data (replace with your data if applicable).
src:
components: Python modules for each processing step.
data_ingestion.py
data_preparation.py
data_transformation.py
model_training.py
utils.py (utility functions)
main.py: Script to run the data processing pipeline and model training.
requirements.txt: Lists required Python libraries.
Further Exploration:

Modify the existing modules or create new ones to customize the pipeline for different tasks.
Experiment with different machine learning models for taxi fare prediction.

Resources:
- [Medium Article]()
