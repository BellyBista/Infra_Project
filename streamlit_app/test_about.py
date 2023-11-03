import streamlit as st
from About import init_saved_data

def test_init_saved_data():
    saved_data = init_saved_data()
    assert isinstance(saved_data, list)

if __name__ == '__main__':
    test_init_saved_data()
