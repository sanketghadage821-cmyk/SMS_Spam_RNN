import streamlit as st
import pickle
import os

st.set_page_config(
page_title="SMS Spam Detector",
page_icon="📱",
layout="centered"
)

st.title("📱 SMS Spam Detector")
st.write("Enter an SMS message to check whether it is Spam or Not Spam.")

st.markdown("---")

@st.cache_resource
def load_model():

```
file_names = [
    "model.pkl",
    "model (1).pkl"
]

for file_name in file_names:

    if os.path.exists(file_name):

        try:

            with open(file_name, "rb") as file:
                model = pickle.load(file)

            return model

        except Exception as error:

            st.error("Unable to load the model.")
            st.code(str(error))
            return None

return None
```

model = load_model()

if model is None:

```
st.error("❌ Model file not found.")

st.write("Make sure your GitHub repository contains:")

st.code("model.pkl")

st.write("or")

st.code("model (1).pkl")
```

else:

```
message = st.text_area(
    "Enter SMS message:",
    placeholder="Example: Congratulations! You won a free prize!",
    height=150
)

predict_button = st.button(
    "🔍 Predict",
    use_container_width=True
)

if predict_button:

    if message.strip() == "":

        st.warning("⚠️ Please enter an SMS message.")

    else:

        try:

            prediction = model.predict([message])

            result = prediction[0]

            result = str(result).strip().lower()

            if result == "spam" or result == "1" or result == "true" or result == "yes":

                st.error("🚨 SPAM MESSAGE")

            else:

                st.success("✅ NOT SPAM")

        except Exception as error:

            st.error("❌ Prediction failed.")

            st.code(str(error))
```
