import tensorflow as tf
import numpy as np
import cv2
import os
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten
from keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Initialize image data generator with rescaling
train_data_gen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_generator = tf.keras.utils.image_dataset_from_directory(
    'fer2013/train',
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(48, 48),
    batch_size=64,
    color_mode="grayscale",
    label_mode='categorical'
)

validation_generator = tf.keras.utils.image_dataset_from_directory(
    'fer2013/train',
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(48, 48),
    batch_size=64,
    color_mode="grayscale",
    label_mode='categorical'
)

# Create model structure
emotion_model = Sequential()

emotion_model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)))
emotion_model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
emotion_model.add(Dropout(0.25))

emotion_model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
emotion_model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
emotion_model.add(Dropout(0.25))

emotion_model.add(Flatten())
emotion_model.add(Dense(1024, activation='relu'))
emotion_model.add(Dropout(0.5))
emotion_model.add(Dense(7, activation='softmax'))  # 7 emotion classes

# Compile the model
history = emotion_model.compile(
    loss='categorical_crossentropy',
    optimizer=Adam(learning_rate=0.0001),
    metrics=['accuracy']
)

steps_per_epoch = train_generator.cardinality().numpy()
validation_steps = validation_generator.cardinality().numpy()

# Train the model
emotion_model_info = emotion_model.fit(
    train_generator,
    steps_per_epoch=steps_per_epoch,
    epochs=50,
    validation_data=validation_generator,
    validation_steps=validation_steps
)

emotion_model.save('emotion_model.h5')  # Save the entire model
print("Model trained and saved!")
