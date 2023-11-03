from unittest.mock import patch
from pathlib import Path
import json
import dill
import streamlit as st
from About import (init_saved_data, main, make_prediction)

def test_init_saved_data():
    saved_data = init_saved_data()
    assert isinstance(saved_data, list)

@patch('streamlit.spinner', return_value=True)
@patch('streamlit.markdown')
def test_main_home(mock_markdown, mock_spinner):
    selected = "Home"  # Mock user's selection
    with st.spinner("Loading..."):  # Mock loading message
        main()
    # Assertions to check if the "Home" section is displayed correctly
    mock_markdown.assert_any_call(r"<h1 style='.*'>Navigating Cancer Care</h1>")
    mock_markdown.assert_any_call(r"<h3 style='.*'>Your Financial Guide, Powered by Iryss</h3>")

@patch('streamlit.spinner', return_value=True)
@patch('streamlit.markdown')
@patch('streamlit.button', return_value=True)
def test_main_estimate_total_charges(mock_button, mock_markdown, mock_spinner):
    selected = "Estimate Total Charges"  # Mock user's selection
    with st.spinner("Loading..."):  # Mock loading message
        main()
    # Assertions to check if the "Estimate Total Charges" section is displayed correctly
    mock_markdown.assert_any_call(r"<style>.*</style>")
    mock_button.assert_called_once()

@patch('streamlit.button', return_value=True)
def test_estimate_total_charges_button(mock_button):
    selected = "Estimate Total Charges"  # Mock user's selection
    with st.spinner("Loading..."):  # Mock loading message
        main()
    # Simulate clicking the "Estimate Total Charges" button
    mock_button.assert_called_once()

def test_load_json():
    # Replace with the directory containing your JSON files
    json_dir = "./streamlit_app/model_A_object"

    # List of JSON file names to test
    json_files = ["ccsr_ordinal_mapping.json", "county_ordinal_mapping.json", "facility_ordinal_mapping.json"]

    for file_name in json_files:
        file_path = Path(json_dir) / file_name
        assert file_path.is_file(), f"File not found: {file_path}"

        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            assert isinstance(data, dict), f"Expected a dictionary in {file_name}"
            assert len(data) > 0, f"Dictionary is empty in {file_name}"

def test_load_obj():
    # Replace with the directory containing your object files
    obj_dir = "./streamlit_app/model"

    # List of object file names to test
    obj_files = ["model_A.pkl", "pipeline_obj_updated.pkl"]

    for file_name in obj_files:
        file_path = Path(obj_dir) / file_name
        assert file_path.is_file(), f"File not found: {file_path}"

        with open(file_path, 'rb') as obj_file:
            model = dill.load(obj_file)
            assert model is not None, f"Failed to load the object from {file_name}"
"""
def test_make_prediction():
    user_input = {}  # Replace with your mock input data
    prediction = make_prediction(user_input)
    assert isinstance(prediction, (int, float))  # Assert that the prediction is a number
"""

if __name__ == '__main__':
    test_init_saved_data()
    test_main_home()
    test_main_estimate_total_charges()
    test_estimate_total_charges_button()
    test_load_json()
    test_load_obj()
