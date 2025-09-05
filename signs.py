import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# -----------------------------
# 1. Dataset Preparation
# -----------------------------
# Folder structure should be like:
# dataset/
#   train/
#       A/
#       B/
#       ...
#   test/
#       A/
#       B/
#       ...

train_dir = "dataset/train"
test_dir = "dataset/test"

img_size = 64  # Resize all images to 64x64
batch_size = 32

# Data augmentation for training
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    zoom_range=0.2,
    shear_range=0.2,
    horizontal_flip=True
)

test_datagen = ImageDataGenerator(rescale=1./255)

train_data = train_datagen.flow_from_directory(
    train_dir,
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode="categorical"
)

test_data = test_datagen.flow_from_directory(
    test_dir,
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode="categorical"
)

# -----------------------------
# 2. Model Architecture (CNN)
# -----------------------------
model = Sequential([
    Conv2D(32, (3,3), activation="relu", input_shape=(img_size, img_size, 3)),
    MaxPooling2D(pool_size=(2,2)),

    Conv2D(64, (3,3), activation="relu"),
    MaxPooling2D(pool_size=(2,2)),

    Conv2D(128, (3,3), activation="relu"),
    MaxPooling2D(pool_size=(2,2)),

    Flatten(),
    Dense(256, activation="relu"),
    Dropout(0.5),
    Dense(train_data.num_classes, activation="softmax")  # Output layer
])

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# -----------------------------
# 3. Training
# -----------------------------
history = model.fit(
    train_data,
    validation_data=test_data,
    epochs=10
)

# -----------------------------
# 4. Save Model
# -----------------------------
model.save("sign_language_model.h5")
print("Model trained and saved as sign_language_model.h5")