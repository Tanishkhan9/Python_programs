import numpy as np

# Sigmoid activation function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Derivative of sigmoid
def sigmoid_derivative(x):
    return x * (1 - x)

# Input dataset (XOR)
X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

# Target output
y = np.array([
    [0],
    [1],
    [1],
    [0]
])

# Random seed for reproducibility
np.random.seed(1)

# Initialize weights randomly
input_neurons = 2
hidden_neurons = 2
output_neurons = 1

# Weights between input and hidden layer
weights_input_hidden = np.random.uniform(size=(input_neurons, hidden_neurons))

# Weights between hidden and output layer
weights_hidden_output = np.random.uniform(size=(hidden_neurons, output_neurons))

# Biases
bias_hidden = np.random.uniform(size=(1, hidden_neurons))
bias_output = np.random.uniform(size=(1, output_neurons))

# Learning rate
learning_rate = 0.5

# Training loop
epochs = 10000

for epoch in range(epochs):

    # --------------------
    # Forward Propagation
    # --------------------

    # Hidden layer
    hidden_input = np.dot(X, weights_input_hidden) + bias_hidden
    hidden_output = sigmoid(hidden_input)

    # Output layer
    final_input = np.dot(hidden_output, weights_hidden_output) + bias_output
    predicted_output = sigmoid(final_input)

    # --------------------
    # Error Calculation
    # --------------------

    error = y - predicted_output

    # --------------------
    # Backpropagation
    # --------------------

    # Output layer delta
    d_predicted_output = error * sigmoid_derivative(predicted_output)

    # Hidden layer error
    hidden_error = d_predicted_output.dot(weights_hidden_output.T)

    # Hidden layer delta
    d_hidden_layer = hidden_error * sigmoid_derivative(hidden_output)

    # --------------------
    # Update Weights
    # --------------------

    weights_hidden_output += hidden_output.T.dot(d_predicted_output) * learning_rate

    weights_input_hidden += X.T.dot(d_hidden_layer) * learning_rate

    bias_output += np.sum(d_predicted_output, axis=0, keepdims=True) * learning_rate

    bias_hidden += np.sum(d_hidden_layer, axis=0, keepdims=True) * learning_rate

# --------------------
# Final Output
# --------------------

print("Final Predicted Output:")
print(predicted_output)
