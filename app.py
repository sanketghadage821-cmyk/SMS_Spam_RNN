```python
import streamlit as st
import pickle
import os

st.set_page_config(
    page_title="SMS Spam Detector",
    page_icon="📱",
    layout="centered"
)

# ---------- CSS ----------
st.markdown("""
<style>
.main {
    background-color: #0f172a;
}

.title {
    text-align: center;
    font-size: 38px;
    font-weight: bold;
    color: #ffffff;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 30px;
}

.card {
    background-color: #1e293b;
    padding: 30px;
    border-radius: 15px;
    border: 1px solid #334155;
}

.spam {
    background-color: #7f1d1d;
    color: #fecaca;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
}

.notspam {
    background-color: #064e3b;
    color: #a7f3d0;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
}

.error {
    color: #fca5a5;
}
</style>
""", unsafe_allow_html=True)


# ---------- Load Model ----------
@st.cache_resource
def load_model():

    possible_files = [
        "model.pkl",
        "model (1).pkl"
    ]

    for file_name in possible_files:
        if os.path.exists(file_name):
            with open(file_name, "rb") as file:
                return pickle.load(file)

    return None


model = load_model()


# ---------- Header ----------
st.markdown(
    '<div class="title">📱 SMS Spam Detector</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Enter an SMS message and check whether it is Spam or Not Spam</div>',
    unsafe_allow_html=True
)


# ---------- Model Check ----------
if model is None:

    st.error(
        "Model file not found. Please upload model.pkl "
        "or model (1).pkl to the GitHub repository."
    )

else:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    message = st.text_area(
        "Enter SMS Message",
        placeholder="Example: Congratulations! You won a free prize. Call now!",
        height=150
    )

    predict_button = st.button(
        "🔍 Check Message",
        use_container_width=True
    )

    st.markdown('</div>', unsafe_allow_html=True)


    # ---------- Prediction ----------
    if predict_button:

        if not message.strip():

            st.warning("Please enter an SMS message.")

        else:

            try:

                prediction = model.predict([message])

                value = prediction[0]

                # Handle numeric prediction
                try:
                    numeric_value = float(value)

                    if numeric_value >= 0.5:
                        is_spam = True
                    else:
                        is_spam = False

                except (ValueError, TypeError):

                    # Handle text prediction
                    text_value = str(value).lower()

                    is_spam = text_value in [
                        "spam",
                        "1",
                        "true",
                        "yes"
                    ]


                st.markdown("---")

                if is_spam:

                    st.markdown(
                        '<div class="spam">🚨 SPAM MESSAGE</div>',
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        '<div class="notspam">✅ NOT SPAM</div>',
                        unsafe_allow_html=True
                    )


            except Exception as e:

                st.error(
                    f"Prediction failed: {str(e)}"
                )
```
