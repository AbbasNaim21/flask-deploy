import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

class Translation:
    def __init__(self, model_path):
        self.model = self._load_model(model_path)
        self.english_tokenizer, self.french_tokenizer = self._load_tokenizers(model_path)
        self.max_length_eng = 14  # Replace with your actual max_length_eng
        self.max_length_fr = 16   # Replace with your actual max_length_fr

    def _load_model(self, model_path):
        try:
            model = load_model(model_path)
            logging.info('Model loaded successfully')
            return model
        except Exception as e:
            logging.error(f'Error loading model: {str(e)}')
            return None

    def _load_tokenizers(self, model_path):
        try:
            base_path = os.path.dirname(model_path)
            with open(os.path.join(base_path, 'english_tokenizer.pkl'), 'rb') as handle:
                english_tokenizer = pickle.load(handle)
            with open(os.path.join(base_path, 'french_tokenizer.pkl'), 'rb') as handle:
                french_tokenizer = pickle.load(handle)
            logging.info('Tokenizers loaded successfully')
            return english_tokenizer, french_tokenizer
        except Exception as e:
            logging.error(f'Error loading tokenizers: {str(e)}')
            return None, None

    def predict(self, input_sentence):
        if not self.model or not self.english_tokenizer or not self.french_tokenizer:
            logging.error('Model or tokenizers are not loaded')
            return None

        try:
            input_sequence = self.english_tokenizer.texts_to_sequences([input_sentence])
            logging.info(f'Tokenized input sequence: {input_sequence}')
            input_sequence = pad_sequences(input_sequence, maxlen=self.max_length_eng, padding='post')
            logging.info(f'Padded input sequence: {input_sequence}')

            input_tensor = tf.convert_to_tensor(input_sequence)
            logging.info(f'Input tensor: {input_tensor}')

            predictions = self.model.predict(input_tensor)
            logging.info(f'Raw predictions: {predictions}')

            predicted_sequence = np.argmax(predictions, axis=-1).flatten()
            logging.info(f'Predicted sequence (indices): {predicted_sequence}')

            output_sentence = self.french_tokenizer.sequences_to_texts([predicted_sequence])[0]
            logging.info(f'Output sentence: {output_sentence}')

            return output_sentence
        except Exception as e:
            logging.error(f'Error during prediction: {str(e)}')
            return None
