from flask import Flask, request, jsonify
import logging
from model.model import Translation

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Create an instance of Translation
model_path = "./model/my_translation_Model.h5"
translator = Translation(model_path)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/v1/predict', methods=['POST', 'GET'])
def predict():
    try:
        # Handle GET requests
        if request.method == 'GET':
            input_sentence = request.args.get('input')
            if not input_sentence:
                return jsonify({'error': 'Invalid input: Missing "input" query parameter'}), 400

        # Handle POST requests
        elif request.method == 'POST':
            data = request.get_json(force=True)  # Ensure it parses JSON even if Content-Type is not set
            if data is None:
                return jsonify({'error': 'Invalid input: No JSON data received'}), 400

            input_sentence = data.get('input')
            if not input_sentence:
                return jsonify({'error': 'Invalid input: Missing "input" key'}), 400

        logging.info(f'Received input sentence: {input_sentence}')

        # Use the predict method from the Translation class
        output_sentence = translator.predict(input_sentence)
        logging.info(f'Prediction output: {output_sentence}')

        if output_sentence is None:
            return jsonify({'error': 'Prediction failed'}), 500

        return jsonify({'prediction': output_sentence})
    except Exception as e:
        logging.error(f'Error during prediction: {str(e)}')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Ensure Flask is accessible from external IPs
    app.run(debug=True, host='0.0.0.0', port=8000)
