import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt

# -----------------------------
# Load MNIST Dataset
# -----------------------------

(train_images, train_labels), (test_images, test_labels) = datasets.mnist.load_data()

# Normalize pixel values (0 to 1)
train_images = train_images / 255.0
test_images = test_images / 255.0

# Reshape for CNN
train_images = train_images.reshape((60000, 28, 28, 1))
test_images = test_images.reshape((10000, 28, 28, 1))

# -----------------------------
# Build CNN Model
# -----------------------------

model = models.Sequential()

# Convolution Layer
model.add(layers.Conv2D(
    32,                 # Number of filters
    (3, 3),             # Kernel size
    activation='relu',
    input_shape=(28, 28, 1)
))

# Pooling Layer
model.add(layers.MaxPooling2D((2, 2)))

# Second Convolution Layer
model.add(layers.Conv2D(64, (3, 3), activation='relu'))

# Second Pooling Layer
model.add(layers.MaxPooling2D((2, 2)))

# Flatten Layer
model.add(layers.Flatten())

# Fully Connected Layer
model.add(layers.Dense(64, activation='relu'))

# Output Layer
model.add(layers.Dense(10, activation='softmax'))

# -----------------------------
# Compile Model
# -----------------------------

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# -----------------------------
# Train Model
# -----------------------------

history = model.fit(
    train_images,
    train_labels,
    epochs=5,
    validation_data=(test_images, test_labels)
)

# -----------------------------
# Evaluate Model
# -----------------------------

test_loss, test_acc = model.evaluate(test_images, test_labels)

print("\nTest Accuracy:", test_acc)

# -----------------------------
# Predict Example
# -----------------------------

prediction = model.predict(test_images)

print("\nPredicted Digit:", prediction[0].argmax())
print("Actual Digit:", test_labels[0])

# -----------------------------
# Display Image
# -----------------------------

plt.imshow(test_images[0].reshape(28, 28), cmap='gray')
plt.title("Test Image")
plt.show()
