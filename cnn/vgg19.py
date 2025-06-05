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

# Function to predict and display images with labels


def predict_and_display(pred_generator, model, num_images=5):
    """
    Predicts the classes of a specified number of images from a data generator using a trained model,
    and displays the images along with their predicted class labels.
    Args:
        pred_generator (keras.preprocessing.image.DirectoryIterator): 
            The data generator providing image file paths and class indices.
        model (keras.Model): 
            The trained Keras model used for making predictions.
        num_images (int, optional): 
            The number of images to predict and display. Defaults to 5.
    Returns:
        None. Displays a matplotlib figure with the images and their predicted labels.
    """
    
    class_labels = {v: k for k, v in pred_generator.class_indices.items()}

    pred_generator.reset()
    image_paths = pred_generator.filepaths[:num_images]
    images = []
    for i in range(num_images):
        img = load_img(image_paths[i], target_size=(150, 150))
        img_array = img_to_array(img) / 255.0
        images.append(img_array)
    images = np.array(images)

    predictions = model.predict(images)
    predicted_labels = np.argmax(predictions, axis=1)
    
    plt.figure(figsize=(15, 5))
    for i in range(num_images):
        plt.subplot(1, num_images, i + 1)
        plt.imshow(images[i])
        predicted_class = class_labels[predicted_labels[i]]
        plt.title(f'Predicted: {predicted_class}')
        plt.axis('off')
    plt.close()

# Charger et traiter les données
train_generator, val_generator, pred_generator = load_intel_dataset()

# Définir le modèle VGG19
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
        
        # *** PAS CONFORME à un VRAI VGG-19 ***
        
        Conv2D(256, (3, 3), padding='same', activation='relu'),
        BatchNormalization(),
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
        MaxPooling2D(pool_size=(2, 2)),
        
        Conv2D(1024, (3, 3), padding='same', activation='relu'),
        BatchNormalization(),
        Conv2D(1024, (3, 3), padding='same', activation='relu'),
        BatchNormalization(),
        Conv2D(1024, (3, 3), padding='same', activation='relu'),
        BatchNormalization(),
        MaxPooling2D(pool_size=(2, 2)),

        Conv2D(2048, (3, 3), padding='same', activation='relu'),
        BatchNormalization(),
        Conv2D(2048, (3, 3), padding='same', activation='relu'),
        BatchNormalization(),
        Conv2D(2048, (3, 3), padding='same', activation='relu'),
        BatchNormalization(),
        MaxPooling2D(pool_size=(2, 2)),
        
        # Classification part
        Flatten(),
        Dense(4096, activation='relu'),
        Dropout(0.2),
        Dense(4096, activation='relu'),
        Dropout(0.2),
        Dense(1024, activation='relu'),
        Dropout(0.2),
        Dense(6, activation='softmax')
    ])

model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

model.summary()

# Entraîner le modèle
history = model.fit(
            train_generator,
            epochs=30,
            validation_data=val_generator,
            callbacks=[
                tf.keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True),
                tf.keras.callbacks.ReduceLROnPlateau(factor=0.3, patience=3)]
)

model.save("C:/Data/Models/CNNIntelImagesClassification_VGG19-Extra.keras")

import matplotlib.pyplot as plt
import numpy as np

def predict_and_display(generator, model, num_images=5):
    images = []
    true_labels = []
    
    for i in range(num_images):
        image, label = next(generator)
        images.append(image[0])  
        true_labels.append(np.argmax(label[0]))
    
    predictions = model.predict(np.array(images))
    predicted_labels = np.argmax(predictions, axis=1)
    
    class_names = list(generator.class_indices.keys())
    
    plt.figure(figsize=(15, 8))
    for i in range(num_images):
        plt.subplot(3, 5, i+1)
        plt.imshow(images[i])
        plt.title(f'Pred: {class_names[predicted_labels[i]]}\nTrue: {class_names[true_labels[i]]}')
        plt.axis('off')
    
    plt.tight_layout()
    plt.show()

#Afficher les prédictions de 15 images
predict_and_display(val_generator, model, num_images=15)

def predict_and_time(generator, model, num_images=5):
    images = []
    true_labels = []
    
    for i in range(num_images):
        image, label = next(generator)
        images.append(image[0])  
        true_labels.append(np.argmax(label[0]))
    
    start_time = time.time()
    predictions = model.predict(np.array(images))
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Prediction time for {num_images} images: {elapsed_time:.4f} seconds")
    print(f"Number of items in predictions: {len(predictions)}")
    
# Prédire 100 images et mesurer le temps de prédiction
predict_and_time(val_generator, model, num_images=100)


import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import accuracy_score, recall_score, precision_score

def predict_and_compute_performances(generator, model):
    num_images = generator.samples if hasattr(generator, 'samples') else len(generator)

    images = []
    true_labels = []

    for i in range(num_images):
        image, label = next(generator)
        images.append(image[0])  
        true_labels.append(np.argmax(label[0]))
        
    true_labels = [int(label) for label in true_labels]
    print("True labels for displayed images:", true_labels)

    predictions = model.predict(np.array(images))

    predicted_labels = np.argmax(predictions, axis=1)   # takes the max value in each colomn since the prediction is the probability of each class
    print("Predicted labels for displayed images:", predicted_labels)

    true_labels = np.array(true_labels)
    print("True labels:", true_labels)

    f1 = f1_score(true_labels, predicted_labels, average='macro')
    
    accuracy = accuracy_score(true_labels, predicted_labels)
    recall = recall_score(true_labels, predicted_labels, average='macro')
    precision = precision_score(true_labels, predicted_labels, average='macro')

    print("Accuracy:", accuracy)
    print("Precision (macro):", precision)
    print("Recall (macro):", recall)
    print("F1 Score (macro) for displayed images:", f1)

    n_classes = len(np.unique(true_labels))
    # Binarize the true labels
    true_labels_bin = label_binarize(true_labels, classes=list(range(n_classes)))
    predicted_labels_bin = label_binarize(predicted_labels, classes=list(range(n_classes)))

    # Compute ROC curve and ROC area for each class
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(true_labels_bin[:, i], predicted_labels_bin[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    plt.figure(figsize=(8, 6))
    for i in range(n_classes):
        plt.plot(fpr[i], tpr[i], label=f'Class {i} (AUC = {roc_auc[i]:.2f})')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.title('ROC Curve for Each Class')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend()
    plt.grid(True)
    plt.show()
   
predict_and_compute_performances(val_generator, model)

# Affichier l'historique d'entrainement
df = pd.DataFrame(history.history)
df.plot(figsize=(8, 5))
plt.grid(True)
plt.gca().set_ylim(0, 1)
plt.show()



