import streamlit as st
import pickle
import os

st.set_page_config(page_title="SMS Spam Detector", page_icon="📱")

st.title("📱 SMS Spam Detector")
st.write("Enter an SMS message below.")

@st.cache_resource
def load_model():
if os.path.exists("model.pkl"):
with open("model.pkl", "rb") as f:
return pickle.load(f)

```
if os.path.exists("model (1).pkl"):
    with open("model (1).pkl", "rb") as f:
        return pickle.load(f)

return None
```

model = load_model()

if model is None:
st.error("Model file not found.")
st.write("Please upload model.pkl or model (1).pkl to your GitHub repository.")
else:
message = st.text_area(
"Enter SMS message",
placeholder="Congratulations! You won a free prize!"
)

```
if st.button("Predict"):
    if message.strip() == "":
        st.warning("Please enter a message.")
    else:
        try:
            prediction = model.predict([message])
            result = str(prediction[0]).lower().strip()

            if result in ["spam", "1", "true", "yes"]:
                st.error("🚨 SPAM MESSAGE")
            else:
                st.success("✅ NOT SPAM")

        except Exception as e:
            st.error("Prediction error:")
            st.code(str(e))
```
