import tensorflow as tf
from tensorflow.python.keras import layers  # Import layers module for building network layers

# Load and preprocess the MNIST dataset
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0  # Normalize pixel values

# Define a minimal single-layer neural network with 10 output units
model = tf.keras.Sequential(
    [
        # Flatten input images
        layers.Flatten(input_shape=(28, 28)),
        # Modify this section to add hidden layers
        # You can add more hidden layers here with desired number of neurons and activation functions
        # hidden layer with 512 neurons and Rectified Linear Unit (ReLU) activation
        layers.Dense(512, activation="relu"),
        # Output layer with 10 units for 10 classes (digits 0 to 9)
        layers.Dense(10, activation="softmax"),
    ]
)

# Compile the model with appropriate optimizer and loss function
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

# Train the model on the training set
model.fit(x_train, y_train, epochs=10)  # Adjust epochs for more training

# Evaluate performance on a subset of the test set
test_loss, test_acc = model.evaluate(x_test[:1000], y_test[:1000])
print("Test accuracy:", test_acc)
