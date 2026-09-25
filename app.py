import streamlit as st
import numpy as np
import pickle
import os

from tensorflow.keras.models import load_model

st.set_page_config(
page_title="SMS Spam Detector",
page_icon="📱",
layout="centered"
)

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
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 17px;
    margin-bottom: 30px;
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

st.markdown(
'<div class="title">📱 SMS Spam Detector</div>',
unsafe_allow_html=True
)

st.markdown(
'<div class="subtitle">RNN Based SMS Classification</div>',
unsafe_allow_html=True
)

@st.cache_resource
def load_prediction_model():

```
# Keras model
for filename in ["model.keras", "model.h5", "sms_spam_model.h5"]:

    if os.path.exists(filename):
        try:
            return load_model(filename), "keras"
        except Exception:
            pass

# Pickle model
for filename in ["model.pkl", "model (1).pkl"]:

    if os.path.exists(filename):
        try:
            with open(filename, "rb") as file:
                return pickle.load(file), "pickle"
        except Exception:
            pass

return None, None
```

model, model_type = load_prediction_model()

if model is None:

```
st.error("❌ Model file not found.")

st.write("Make sure your repository contains:")

st.code("""
```

model.pkl
or
model (1).pkl
""")

```
st.stop()
```

message = st.text_area(
"Enter SMS Message",
placeholder="Example: Congratulations! You won a free prize!",
height=150
)

if st.button("🔍 Check Message", use_container_width=True):

```
if not message.strip():

    st.warning("Please enter an SMS message.")

else:

    try:

        if model_type == "pickle":

            prediction = model.predict([message])

            result = str(prediction[0]).lower().strip()

            if result in ["spam", "1", "true", "yes"]:

                st.markdown(
                    '<div class="spam">🚨 SPAM MESSAGE</div>',
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    '<div class="ham">✅ NOT SPAM</div>',
                    unsafe_allow_html=True
                )

        else:

            st.info(
                "Keras model loaded. The original tokenizer is required "
                "to convert SMS text into the correct RNN input format."
            )

    except Exception as e:

        st.error("Prediction failed.")
        st.code(str(e))
```
