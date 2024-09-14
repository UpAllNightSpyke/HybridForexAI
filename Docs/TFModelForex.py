import tensorflow as tf
import numpy as np

# Load preprocessed data
data = np.load('preprocessed_data.npy')
X_train = data[:, :-1]
y_train = data[:, -1]

# Define the model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1, activation='linear')
])

# Compile the model
model.compile(optimizer='adam', loss='mse')

# Train the model
model.fit(X_train, y_train, epochs=50, batch_size=32)

# Save the model
model.save('forex_model.h5')