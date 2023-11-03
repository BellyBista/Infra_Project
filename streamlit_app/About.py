from pathlib import Path
import PIL
import streamlit as st
import streamlit.components.v1 as components
import settings
import helper
import pandas as pd
import numpy as np
import joblib
from PIL import Image
import xgboost as xgb
import itertools
import dill
import pickle
import json
import os
import streamlit_option_menu as option_menu

# Create an empty list to store saved data
# Use st.cache to store data persistently
@st.cache(allow_output_mutation=True)
def init_saved_data():
    return []

saved_data = init_saved_data()

def main():
    # Using custom css
    helper.local_css(settings.CSS)

    # Using custom js
    helper.local_js(settings.JS)

    selected = option_menu.option_menu(
        menu_title = None,
        options = ["Home", "Estimate Total Charges"],
        icons = ["house", "book"],
        menu_icon = "cast",
        default_index = 0,
        orientation = "horizontal"
    )

    if selected == "Home":
        # Center-align the header and subheader using HTML
        center_style = "display: flex; flex-direction: column; align-items: center; text-align: center;"

        st.markdown("<h1 style='{}'>Navigating Cancer Care</h1>".format(center_style), unsafe_allow_html=True)
        st.markdown("<h3 style='{}'>Your Financial Guide, Powered by Iryss</h3>".format(center_style), unsafe_allow_html=True)

        col1, col2, col3 = st.columns([0.35,0.4,0.3])
        with col1:
            st.write("")
        with col2:
            # Load and display an image from a local file
            image = Image.open('images/logo.png')
            st.image(image, width=250)
        with col3:
            st.write("")

        st.markdown("<span style='{}'>Cancer's challenges are profound, but financial worries should not overshadow the journey to recovery. Iryss's vision transcends the norm, aiming for a world where patients can approach their treatment with tranquillity, armed with the insights to anticipate and strategically plan for their medical expenses.</span>".format(center_style), unsafe_allow_html=True)
        
    if selected == 'Estimate Total Charges':
        # Define CSS styles for the form
        st.markdown(
            """
            <style>
            .stButton button {
                background-color: #808080 !important;
                color: #fff !important;
                border-radius: 4px !important;
                padding: 0.5rem 1rem !important;
            }
            .stTextInput input,
            .stSelectbox select,
            .stCheckbox input {
                border-color: #ccc !important;
                border-radius: 4px !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        user_data = helper.user_inputs()
        # st.write(user_data)

        if user_data['data'][6] == 'No':
            pipe = helper.load_model()

            # Validate the form input
            if st.button('Estimate Total Charges'):
                    df = pd.DataFrame([user_data["data"]], columns=user_data["columns"])
                    df = df.drop("ccsr_procedure_desc", axis=1)

                    prediction = pipe.predict(df)

                    # Modify predictions less than 0 to 0
                    prediction = np.where(prediction < 0, 0, prediction)

                    # Display the predictions
                    st.subheader('Estimation: ')
                    st.text('Estimated total charges: $' + str(prediction[0]))
                    # Append the input and result to the saved_data list
                    saved_data.append(user_data["data"] + [prediction[0]])

                    # Display the saved data table
                    st.subheader('Saved Data')
                    if saved_data:
                        saved_data_df = pd.DataFrame(saved_data, columns=user_data["columns"] + ['Estimated Total Charges'])
                        st.table(saved_data_df)

        else:
            
            def load_json(file_path):
                with open(file_path,'r') as json_file:
                    data = json.load(json_file)
                return data
            def load_obj(file_path):
                with open(file_path, 'rb') as obj:
                    model=dill.load(obj)
                return model

            #load mapping json files
            facility_ordinal_mapping=load_json(settings.FACILITY_ORDINAL_MAPPING)
            county_ordinal_mapping=load_json(settings.COUNTY_ORDINAL_MAPPING)
            ccsr_ordinal_mapping=load_json(settings.CCSR_ORDINAL_MAPPING)
            pipeline_obj = helper.load_ccsr_model()


            if st.button('Estimate Total Charges'):
                df = pd.DataFrame([user_data["data"]], columns=user_data["columns"])
                df.rename(columns={'year': 'discharge_year'}, inplace=True)
                        
                #map the features and make a prediction
                def make_prediction(user_input):
                    #perfoming ordinal encoding on specific columns
                    user_input['facility_name'] = user_input['facility_name'].map(facility_ordinal_mapping)
                    user_input['county'] = user_input['county'].map(county_ordinal_mapping)
                    user_input['ccsr_procedure_desc'] = user_input['ccsr_procedure_desc'].map(ccsr_ordinal_mapping)
                    #make prediction
                    prediction=pipeline_obj.predict(user_input)
                    return prediction
                        
                prediction=make_prediction(user_input=df) #excluding target column

                st.subheader('Estimation: ')
                st.text('Estimated total charges: $'+ str(prediction[0]))


                # Append the input and result to the saved_data list
                saved_data.append(user_data["data"] + [prediction[0]])

                # Display the saved data table
                st.subheader('Saved Data')
                if saved_data:
                    saved_data_df = pd.DataFrame(saved_data, columns=user_data["columns"] + ['Estimated Total Charges'])
                    st.table(saved_data_df)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass