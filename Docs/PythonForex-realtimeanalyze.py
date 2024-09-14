import zmq
import tensorflow as tf
import numpy as np

# Load the trained model
model = tf.keras.models.load_model('forex_model.h5')

# ZeroMQ server setup
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    message = socket.recv()
    data = np.frombuffer(message, dtype=np.float32).reshape(1, -1)
    prediction = model.predict(data)
    socket.send(prediction.tobytes())