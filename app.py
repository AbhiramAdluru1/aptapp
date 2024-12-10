from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
import random

# Create the Flask app
app = Flask(__name__)

# Initialize SocketIO
socketio = SocketIO(app)

# model loading
def load_model(model_path):
    print(f"Model loading from: {model_path}")
    return "Model"

# Simulate loading a model
model = load_model('conv_lstm_model.h5')

@app.route('/')
def index():
    # Render the frontend (index.html)
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Receive row data from the client
        row_data = request.json.get('row')
        row_index = request.json.get('row_index', -1)

        # weighted predictions
        classes = ['Benign', 'Reconnaissance', 'Establish Foothold', 'Lateral Movement']
        weights = [0.8, 0.1, 0.05, 0.05] 
        predicted_label = random.choices(classes, weights=weights, k=1)[0]

        # Emit the prediction to the frontend
        socketio.emit('prediction', {'row_index': row_index, 'prediction': predicted_label})

        return jsonify({'prediction': predicted_label}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    socketio.run(app, debug=True)
