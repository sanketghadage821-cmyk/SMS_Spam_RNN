import os
import pickle
import numpy as np
from flask import Flask, request, render_template

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Load Saved Assets
# ---------------------------------------------------------------------------
MODEL_PATH = 'model.pkl'
TOKENIZER_PATH = 'tokenizer.pkl'  # If you saved your Tokenizer separately

# Load trained RNN model
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

# Load Tokenizer if available; fallback to word hashing if not present
tokenizer = None
if os.path.exists(TOKENIZER_PATH):
    with open(TOKENIZER_PATH, 'rb') as f:
        tokenizer = pickle.load(f)

# Model configuration constants
MAX_LEN = 50        # Input sequence length matching model requirements
VOCAB_SIZE = 5000   # Vocabulary size threshold


def preprocess_text(text):
    """
    Preprocesses raw text input to match the sequence format required by the RNN.
    """
    text = text.strip().lower()
    
    if tokenizer is not None:
        # Standard Keras Tokenizer sequence transformation
        sequences = tokenizer.texts_to_sequences([text])
        sequence = sequences[0]
    else:
        # Fallback sequence encoding via modulo hashing
        words = text.split()
        sequence = [(abs(hash(w)) % (VOCAB_SIZE - 1)) + 1 for w in words]

    # Apply padding to match input shape [1, 50]
    if len(sequence) < MAX_LEN:
        padded = [0] * (MAX_LEN - len(sequence)) + sequence
    else:
        padded = sequence[:MAX_LEN]

    return np.array([padded], dtype=np.float32)


# ---------------------------------------------------------------------------
# Flask Routes
# ---------------------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    sms_input = request.form.get('text_input', '')
    
    if not sms_input.strip():
        return render_template('index.html', error="Please enter a valid message.")

    # 1. Preprocess the input SMS
    processed_input = preprocess_text(sms_input)

    # 2. Generate prediction score from the RNN model
    raw_prediction = model.predict(processed_input)[0][0]
    
    # 3. Process threshold (Binary classification: > 0.5 is Spam)
    is_spam = raw_prediction > 0.5
    label = "Spam" if is_spam else "Ham (Legitimate)"
    confidence = float(raw_prediction if is_spam else 1.0 - raw_prediction) * 100

    return render_template(
        'index.html',
        result=label,
        confidence=f"{confidence:.2f}%",
        user_input=sms_input,
        is_spam=is_spam
    )


if __name__ == '__main__':
    # Render binds dynamic port via PORT environment variable
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
