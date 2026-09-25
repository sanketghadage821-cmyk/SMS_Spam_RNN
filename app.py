import streamlit as st
import pickle
import os

st.set_page_config(page_title="SMS Spam Detector", page_icon="📱")

st.title("SMS Spam Detector")
st.write("Enter an SMS message and click Predict.")

def load_model():
    if os.path.exists("model.pkl"):
        with open("model.pkl", "rb") as f:
            return pickle.load(f)
    if os.path.exists("model (1).pkl"):
        with open("model (1).pkl", "rb") as f:
            return pickle.load(f)
    return None

model = load_model()

if model is None:
    st.error("Model file not found.")
    st.write("Add model.pkl or model (1).pkl to the same GitHub repository.")
else:
    message = st.text_area("SMS Message")

    if st.button("Predict"):
        if not message.strip():
            st.warning("Please enter an SMS message.")
        else:
            try:
                prediction = model.predict([message])[0]
                result = str(prediction).lower().strip()

                if result in ["spam", "1", "true", "yes"]:
                    st.error("SPAM MESSAGE")
                else:
                    st.success("NOT SPAM")

            except Exception as e:
                st.error("Prediction failed.")
                st.code(str(e))
