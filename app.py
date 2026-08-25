from flask import Flask, request, render_template_string
import pickle
import numpy as np

app = Flask(__name__)

# ============================================================
# LOAD MODEL
# ============================================================

MODEL_PATH = "model.pkl"

try:
    with open(MODEL_PATH, "rb") as file:
        model = pickle.load(file)
    print("Model loaded successfully.")
except Exception as e:
    model = None
    print("ERROR loading model:", e)


# ============================================================
# HTML + CSS
# ============================================================

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SMS Spam Detector</title>

    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea, #764ba2);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .container {
            width: 90%;
            max-width: 600px;
            background: white;
            padding: 35px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        }

        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 10px;
        }

        .subtitle {
            text-align: center;
            color: #777;
            margin-bottom: 25px;
        }

        textarea {
            width: 100%;
            height: 150px;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 16px;
            resize: none;
            outline: none;
        }

        textarea:focus {
            border-color: #667eea;
        }

        button {
            width: 100%;
            margin-top: 20px;
            padding: 14px;
            border: none;
            border-radius: 10px;
            background: #667eea;
            color: white;
            font-size: 18px;
            cursor: pointer;
        }

        button:hover {
            background: #5568d8;
        }

        .result {
            margin-top: 25px;
            padding: 18px;
            border-radius: 10px;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            background: #f1f1f1;
        }

        .footer {
            text-align: center;
            margin-top: 20px;
            color: #999;
            font-size: 13px;
        }
    </style>
</head>

<body>

<div class="container">

    <h1>📱 SMS Spam Detector</h1>

    <div class="subtitle">
        Enter an SMS message to check whether it is Spam or Not Spam.
    </div>

    <form method="POST">

        <textarea
            name="message"
            placeholder="Enter your SMS message here..."
            required
        >{{ message }}</textarea>

        <button type="submit">
            Check Message
        </button>

    </form>

    {% if prediction %}
        <div class="result">
            {{ prediction }}
        </div>
    {% endif %}

    <div class="footer">
        SMS Spam Detection using RNN
    </div>

</div>

</body>
</html>
"""


# ============================================================
# PREDICTION FUNCTION
# ============================================================

def predict_message(message):

    if model is None:
        return "❌ Model could not be loaded."

    try:

        # Try prediction directly
        prediction = model.predict([message])

        value = prediction[0]

        # Handle numpy arrays
        if isinstance(value, (list, tuple, np.ndarray)):
            value = np.array(value).flatten()[0]

        value = float(value)

        if value >= 0.5:
            return "🚨 SPAM MESSAGE"

        else:
            return "✅ NOT SPAM"

    except Exception as e:

        print("Prediction error:", e)

        return "❌ Prediction error. Check your model and preprocessing."


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    message = ""

    if request.method == "POST":

        message = request.form.get("message", "").strip()

        if message:

            prediction = predict_message(message)

        else:

            prediction = "⚠️ Please enter a message."

    return render_template_string(
        HTML,
        prediction=prediction,
        message=message
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    return "SMS Spam Detection App is running successfully!"


# ============================================================
# RUN APP
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
