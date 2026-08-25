from flask import Flask, request
import pickle
import os

app = Flask(__name__)

# Load model
with open("model.pkl", "rb") as file:
    model = pickle.load(file)


@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        message = request.form["message"]

        try:
            prediction = model.predict([message])

            if float(prediction[0]) >= 0.5:
                result = "🚨 Spam Message"
            else:
                result = "✅ Not Spam"

        except Exception as e:
            result = "Prediction Error: " + str(e)

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>SMS Spam Detector</title>

        <style>
            body {{
                font-family: Arial;
                background: #f2f2f2;
                text-align: center;
                padding-top: 100px;
            }}

            .box {{
                background: white;
                width: 400px;
                margin: auto;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 0 10px #ccc;
            }}

            textarea {{
                width: 100%;
                height: 100px;
                padding: 10px;
                margin: 15px 0;
            }}

            button {{
                background: #4CAF50;
                color: white;
                border: none;
                padding: 12px 25px;
                cursor: pointer;
                border-radius: 5px;
            }}

            h2 {{
                color: #333;
            }}

            .result {{
                margin-top: 20px;
                font-size: 20px;
                font-weight: bold;
            }}
        </style>

    </head>

    <body>

        <div class="box">

            <h2>📱 SMS Spam Detector</h2>

            <form method="POST">

                <textarea
                    name="message"
                    placeholder="Enter SMS message"
                    required
                ></textarea>

                <br>

                <button type="submit">
                    Check SMS
                </button>

            </form>

            <div class="result">
                {result}
            </div>

        </div>

    </body>
    </html>
    """


@app.route("/health")
def health():
    return "App is running!"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
