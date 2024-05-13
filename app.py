import streamlit as st
import pandas as pd
from src.logger import logging

from src.pipeline.predict_pipeline import CustomData,PredictPipeline



def main():
    st.set_page_config(page_title = "Caantin AI",page_icon = "🚖",
                       initial_sidebar_state = 'expanded')
                   
    st.title("NYC Yellow Taxi Trip 🚖")

    data = trip_fare_form()

    if data is not None:
        #st.write(data)

        #Initialise the object for the PredictPipeline class
        predict_pipeline=PredictPipeline()
        #Predicting the results
        results=predict_pipeline.predict(data)

        st.write(f"The predicted fare amount is: {round(results[0],2)} ")

   

#Function to get input info
def trip_fare_form():
    with st.form(key='fare_amount',clear_on_submit=False):
        st.subheader("Predict Taxi Fare 💵")
        VendorID= st.selectbox("VendorID",[1,2],index=1)
        tpep_pickup_datetime = st.text_input("Pickup_datetime",value="2017-07-27 18:31:15")
        tpep_dropoff_datetime = st.text_input("Dropoff_datetime",value="2017-07-27 18:48:44")
        passenger_count = st.number_input("passenger_count",value=1)
        trip_distance = st.number_input("trip_distance",value=2.25)
        RatecodeID= st.selectbox("RatecodeID",[1,2,3,4,5,6],index=0)
        store_and_fwd_flag= st.selectbox("store_and_fwd_flag",["N","Y"],index=0)
        payment_type = st.selectbox("payment_type",[0,1,2,3,4,5,6],index=1)
        PULocationID = st.number_input("PULocationID",value=148)
        DOLocationID = st.number_input("DOLocationID",value=246)
        
        #Get the inputs as a datafdrmae
        if st.form_submit_button("Predict 🔮"):
            data = CustomData(
                VendorID = VendorID,
                tpep_pickup_datetime = tpep_pickup_datetime,
                tpep_dropoff_datetime = tpep_dropoff_datetime,
                passenger_count = passenger_count,
                trip_distance = trip_distance,
                RatecodeID = RatecodeID,
                store_and_fwd_flag = store_and_fwd_flag,
                payment_type = payment_type,
                PULocationID = PULocationID,
                DOLocationID = DOLocationID,

            )
            #Getting the prediction features as a dataframe
            pred_df = data.get_data_as_data_frame()
            return pred_df
    
    
         


if __name__=="__main__":
    main()