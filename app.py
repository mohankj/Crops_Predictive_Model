import streamlit as st
import numpy as np
import pandas as pd
import pickle
import time

video_file = open('myvideo.mp4', 'rb')
video_bytes = video_file.read()

st.subheader('Predict the Production of Crops at any Particular Season')
# mapping_dict = pickle.load(open("mapping_dict.pkl"),'rb')
# model = pickle.load(open("model.pkl"),'rb')
# data = pickle.load(open("original_data.pkl",'rb'))

with open('mapping_dict.pkl', 'rb') as f:
    mapping_dict = pickle.load(f)

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('original_data.pkl', 'rb') as f:
    data = pickle.load(f)


def predict(State,District,Crop,Season,Area):
    ## Predicting the Production Of Crops.
    state = mapping_dict['State'][State]
    district = mapping_dict['District'][District]
    crop = mapping_dict['Crop'][Crop]
    season = mapping_dict['Season'][Season]
    
    

    prediction = model.predict(pd.DataFrame(np.array([state,district,crop,season,Area]).reshape(1,5),columns=['State','District','Crop','Season','Area']))
    return prediction

# Input
state_list = data['State'].unique()
selected_state = st.selectbox(
    "Type or select a State from the dropdown",
    options = state_list
)

district_list = data['District'].unique()
selected_district = st.selectbox(
    "Type or select a District from the dropdown",
    district_list
)

crop_list = data['Crop'].unique()
selected_crop = st.selectbox(
    "Type or select a Crops from the dropdown",
    crop_list
)

season_list = data['Season'].unique()
selected_season = st.selectbox(
    "Type or select a Season from the dropdown",
    season_list
)

area = st.number_input('Areas of Plot in (Hectares):', min_value=0.00001, max_value=100000000.0, value=1.0)


if st.button('Predict Production'):
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
        if percent_complete==98:
            my_bar.progress(percent_complete+1,text="Sucessfully Completed")
        

    st.video(video_bytes,start_time=0)
    col1,col2,col3 =st.columns(3)
    col1.subheader(predict(selected_state,selected_district,selected_crop,selected_season,area))
    col2.subheader('Tonnes')




