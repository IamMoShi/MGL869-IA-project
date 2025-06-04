# pip install numpy==1.26.4
# pip install pandas
# pip install opencv-python
# pip install scikit-learn
# pip install matplotlib    
# pip install pillow        
# pip install tensorflow-datasets 
# pip install tensorflow
# pip install tensorflow-serving-api
# pip install tensorboard

base_path = "C:/Data/archive"

import numpy as np
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tensorflow.keras.layers import Dense, Flatten ,Dropout,MaxPooling2D,Conv2D,BatchNormalization
from tensorflow.keras.models import Sequential
from sklearn.metrics import f1_score
import os
import glob as gb
import optuna

import tensorflow as tf
from tensorflow.keras import layers, models, regularizers
from tensorflow.keras.preprocessing.image import load_img, img_to_array

tf.random.set_seed(42)

# fonction pour l'augmentation des données
def load_intel_dataset():
    """
    Charge et prépare les ensembles de données Intel Image Classification avec augmentation de données.
    Cette fonction configure trois générateurs d'images pour l'entraînement, la validation et la prédiction à partir des dossiers spécifiés. 
    Pour l'entraînement, elle applique une augmentation de données avancée (rotation, translation, zoom, cisaillement, ajustement de la luminosité, etc.) afin d'améliorer la robustesse du modèle. 
    Les ensembles de validation et de prédiction sont simplement redimensionnés et normalisés.
    Retourne :
        tuple : (train_generator, val_generator, pred_generator)
            - train_generator : générateur d'images pour l'entraînement avec augmentation.
            - val_generator : générateur d'images pour la validation sans augmentation.
            - pred_generator : générateur d'images pour la prédiction (sans étiquettes, sans augmentation).
    """
    train_dir = base_path + '/seg_train/seg_train'
    val_dir = base_path + '/seg_test/seg_test'
    pred_dir = base_path + '/seg_pred'

    # Augmentation de données améliorée pour l'entraînement
    train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,
        rotation_range=30,          # Plage de rotation augmentée
        width_shift_range=0.3,      # Décalage horizontal augmenté
        height_shift_range=0.3,     # Décalage vertical augmenté
        horizontal_flip=True,
        zoom_range=0.3,             # Plage de zoom augmentée
        shear_range=0.2,            # Cisaillement ajouté
        brightness_range=[0.8, 1.2],# Ajustement de la luminosité ajouté
        fill_mode='nearest'
    )

    val_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
    pred_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)

    # Chargement des données d'entraînement et de validation
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(150, 150),
        batch_size=32,
        class_mode='categorical'
    )

    val_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=(150, 150),
        batch_size=32,
        class_mode='categorical'
    )

    # Chargement des données de prédiction (seg_pred)
    pred_generator = pred_datagen.flow_from_directory(
        pred_dir,
        target_size=(150, 150),
        batch_size=32,
        class_mode=None,  # Pas d'étiquettes pour seg_pred
        shuffle=False
    )

    return train_generator, val_generator, pred_generator


from tensorflow.keras.optimizers import Adam, SGD

# Fonction pour créer le modèle VGG16 avec Optuna
def create_model_VGG16(trial):
    
    # Suggest hyperparameters
    optimizer_name = trial.suggest_categorical('optimizer', ['Adam', 'SGD'])
    init = trial.suggest_categorical('init', ['glorot_uniform', 'normal'])
    units = trial.suggest_int('units', 1024, 4096)

    model = Sequential([

        Conv2D(64, (3, 3), padding='same', activation='relu', input_shape=(150, 150, 3)),
        BatchNormalization(),
        Conv2D(64, (3, 3), padding='same', activation='relu'),
        BatchNormalization(),
        MaxPooling2D(pool_size=(2, 2)),
        
        Conv2D(128, (3, 3), padding='same', activation='relu'),
        BatchNormalization(),
        Conv2D(128, (3, 3), padding='same', activation='relu'),
        BatchNormalization(),
        MaxPooling2D(pool_size=(2, 2)),
        
        Conv2D(256, (3, 3), padding='same', activation='relu'),
        BatchNormalization(),
        Conv2D(256, (3, 3), padding='same', activation='relu'),
        BatchNormalization(),
        MaxPooling2D(pool_size=(2, 2)),
        
        Conv2D(512, (3, 3), padding='same', activation='relu'),
        BatchNormalization(),
        Conv2D(512, (3, 3), padding='same', activation='relu'),
        BatchNormalization(),
        Conv2D(512, (3, 3), padding='same', activation='relu'),
        BatchNormalization(),
        Conv2D(512, (3, 3), padding='same', activation='relu'),
        BatchNormalization(),
        MaxPooling2D(pool_size=(2, 2)),

        Conv2D(512, (3, 3), padding='same', activation='relu'),
        BatchNormalization(),
        Conv2D(512, (3, 3), padding='same', activation='relu'),
        BatchNormalization(),
        Conv2D(512, (3, 3), padding='same', activation='relu'),
        BatchNormalization(),
        Conv2D(512, (3, 3), padding='same', activation='relu'),
        BatchNormalization(),
        MaxPooling2D(pool_size=(2, 2)),
        
        
        # Classification part
        Flatten(),
        Dense(units, activation='relu', kernel_initializer=init),
        Dropout(0.2),
        Dense(units, activation='relu', kernel_initializer=init),
        Dropout(0.2),

        Dense(1024, activation='relu', kernel_initializer=init),
        Dropout(0.2),

        # Final output layer
        Dense(6, activation='softmax')
    ])

    optimizer = optimizer_name == 'Adam' and Adam() or SGD()

    # model.compile(loss='sparse_categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

    return model

import numpy as np
from sklearn.metrics import accuracy_score

def predict_and_compute_performances(generator, model):
    num_images = generator.samples if hasattr(generator, 'samples') else len(generator)
    images = []
    true_labels = []

    for i in range(num_images):
        image, label = next(generator)
        images.append(image[0])  
        true_labels.append(np.argmax(label[0]))
        
    true_labels = [int(label) for label in true_labels]
    predictions = model.predict(np.array(images))
    predicted_labels = np.argmax(predictions, axis=1)   # takes the max value in each colomn since the prediction is the probability of each class
    true_labels = np.array(true_labels)
    accuracy = accuracy_score(true_labels, predicted_labels)
    
    return accuracy


# Define the objective function
def objective(trial):
    # Create model
    model = create_model_VGG19(trial)

    # Train the model
    batch_size = trial.suggest_int('batch_size', 32, 256, step=32)
    epochs = trial.suggest_int('epochs', 5, 20, step=5)

    # model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.2, verbose=0)
    with tf.device("/GPU:0"):
        history = model.fit(
            train_generator,
            epochs=epochs,
            validation_data=val_generator,
            callbacks=[
                tf.keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True),
                tf.keras.callbacks.ReduceLROnPlateau(factor=0.3, patience=3)]
            )   

    # Evaluate the model
    # score = model.evaluate(val_generator)
    return predict_and_compute_performances(val_generator, model)

# Run the optimization
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=10)