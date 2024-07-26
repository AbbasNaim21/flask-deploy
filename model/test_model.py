import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np

# Load the Keras model
model_path = './model/my_translation_Model.h5'
model = load_model(model_path)

# Load the tokenizers
with open('./model/english_tokenizer.pkl', 'rb') as handle:
    english_tokenizer = pickle.load(handle)

with open('./model/french_tokenizer.pkl', 'rb') as handle:
    french_tokenizer = pickle.load(handle)

# Define max lengths for padding
max_length_eng = 14  # Replace with your actual max_length_eng
max_length_fr = 16  # Replace with your actual max_length_fr

def translate_sentence(input_sentence):
    # Tokenize and pad the input sentence
    input_sequence = english_tokenizer.texts_to_sequences([input_sentence])
    print(f'Tokenized input sequence: {input_sequence}')
    input_sequence = pad_sequences(input_sequence, maxlen=max_length_eng, padding='post')
    print(f'Padded input sequence: {input_sequence}')

    # Convert input data to tensor
    input_tensor = tf.convert_to_tensor(input_sequence)
    print(f'Input tensor: {input_tensor}')

    # Make prediction
    predictions = model.predict(input_tensor)
    print(f'Raw predictions: {predictions}')

    # Decode the prediction
    predicted_sequence = np.argmax(predictions, axis=-1)
    print(f'Predicted sequence (indices): {predicted_sequence}')
    predicted_sequence = predicted_sequence.flatten()
    print(f'Flattened predicted sequence: {predicted_sequence}')
    output_sentence = french_tokenizer.sequences_to_texts([predicted_sequence])[0]
    print(f'Output sentence: {output_sentence}')

    return output_sentence

# Test the function
input_sentence = "Hello, how are you?"
output_sentence = translate_sentence(input_sentence)
print(f'Translated sentence: {output_sentence}')
