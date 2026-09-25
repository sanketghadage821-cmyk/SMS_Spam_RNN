```python
import streamlit as st
import numpy as np
import pickle
import os

# TensorFlow
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="SMS Spam Detector",
    page_icon="📱",
    layout="centered"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #0f172a;
}

.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: white;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 17px;
    margin-bottom: 30px;
}

.box {
    background-color: #1e293b;
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #334155;
}

.spam {
    background-color: #7f1d1d;
    border: 1px solid #ef4444;
    color: #fecaca;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    font-size: 25px;
    font-weight: bold;
}

.ham {
    background-color: #064e3b;
    border: 1px solid #10b981;
    color: #a7f3d0;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    font-size: 25px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="title">📱 SMS Spam Detector</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Machine Learning / RNN based SMS classification</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

@st.cache_resource
def load_prediction_model():

    # Try Keras model files
    keras_files = [
        "model.keras",
        "model.h5",
        "sms_spam_model.h5"
    ]

    for filename in keras_files:

        if os.path.exists(filename):

            try:
                return load_model(filename), "keras"

            except Exception:
                pass


    # Try pickle model
    pickle_files = [
        "model.pkl",
        "model (1).pkl"
    ]

    for filename in pickle_files:

        if os.path.exists(filename):

            try:

                with open(filename
```
