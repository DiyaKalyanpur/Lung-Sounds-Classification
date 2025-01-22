import os
import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pandas as pd

data_file = '/Users/diyakalyanpur/Desktop/output_folder1/updated_mapping.csv'
df = pd.read_csv(data_file)


def load_npy_file(file_path, target_shape=(128, 118)):
    try:
        data = np.load(file_path)
        if data.shape != target_shape:
            print(f"Resizing {file_path} from {data.shape} to {target_shape}")
          
            data = tf.image.resize(data, target_shape).numpy()
        return data
    except Exception as e:
        print(f"Error loading file {file_path}: {e}")
        return None


target_shape = (128, 118)
X = []
y = []

for file, label in zip(df['file'], df['label']):
    data = load_npy_file(file, target_shape=target_shape)
    if data is not None:
        X.append(data)
        y.append(label)

X = np.array(X)
y = np.array(y)
print("Min value in X:", X.min())
print("Maxi value in X:", X.max())

X = X / 255.0


label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)


from tensorflow.keras.regularizers import l2

model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(128, 118, 1)),
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_regularizer=l2(0.001)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_regularizer=l2(0.001)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(128, activation='relu', kernel_regularizer=l2(0.001)),
    #tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(len(label_encoder.classes_), activation='softmax')
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics=['accuracy']
)

#early_stopping = tf.keras.callbacks.EarlyStopping(
#    monitor='val_loss', 
#    patience=10, 
#    restore_best_weights=True
#)

#model.fit(X_train, y_train, validation_data=(X_val, y_val), 
          #epochs=100, batch_size=32) 
          #callbacks=[early_stopping])
print("Number of samples per class after balancing:")
print(class_counts)
