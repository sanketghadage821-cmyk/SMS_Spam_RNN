import os
import pickle
import numpy as np
from flask import Flask, request, render_template

app = Flask(__name__)

# Load the saved Keras model pickle file
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Input parameters from config: input sequence length = 50, vocab size = 5000
MAX_LEN = 50
VOCAB_SIZE = 5000

def preprocess_text(text):
    """
    Simple word-to-index encoding and padding to match model input shape [null, 50].
    Replace this with your original Tokenizer logic if applicable.
    """
    words = text.lower().split()
    # Simple hashing trick into vocab space [1, VOCAB_SIZE - 1]
    sequence = [hash(w) % (VOCAB_SIZE - 1) + 1 for w in words]
    
    # Pad or truncate sequence to MAX_LEN (50)
    if len(sequence) < MAX_LEN:
        padded = [0] * (MAX_LEN - len(sequence)) + sequence
    else:
        padded = sequence[:MAX_LEN]
        
    return np.array([padded], dtype=np.float32)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    text_input = request.form.get('text_input', '')
    if not text_input.strip():
        return render_template('index.html', error="Please enter valid text for prediction.")
    
    # Preprocess text and run model prediction
    processed_input = preprocess_text(text_input)
    prediction = model.predict(processed_input)[0][0]
    
    # Determine class label and confidence score
    confidence = float(prediction if prediction > 0.5 else 1 - prediction) * 100
    label = "Positive" if prediction > 0.5 else "Negative"
    
    return render_template(
        'index.html', 
        result=label, 
        confidence=f"{confidence:.2f}%", 
        user_input=text_input
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
