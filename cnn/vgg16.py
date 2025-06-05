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

# Juste compter le nombre d'images dans le dossier train
for folder in os.listdir(base_path + "/seg_train/seg_train"):
    files = gb.glob(base_path + "/seg_train/seg_train/" + folder + "/*.jpg")
    print(f"For Training Data , Found {len(files)} images in {folder} folder")  

code = {'buildings': 0 ,'forest':1 ,'glacier':2,'mountain':3 ,'sea':4 ,'street':5}

def getcode(n):
    for x,y in code.items():
        if n==y:
            return x
        
# Load and resize training images to (100, 100) and assign labels
import cv2
X_train = []
y_train = []
new_size = 100
for folder in os.listdir(base_path + "/seg_train/seg_train/"):
    files = gb.glob(base_path + "/seg_train/seg_train/" + folder + "/*.jpg")
    for file in files:
        image = cv2.imread(file)
        image_resize = cv2.resize(image,(new_size,new_size))
        X_train.append(image_resize)
        y_train.append(code[folder])

# Load and resize validation images to (100, 100) and assign labels
X_test = []
y_test = []
for folder in os.listdir(base_path + "/seg_test/seg_test/"):
    files = gb.glob(base_path + "/seg_test/seg_test/" + folder + "/*.jpg")
    for file in files:
        image = cv2.imread(file)
        image_resize = cv2.resize(image,(new_size,new_size))
        X_test.append(image_resize)
        y_test.append(code[folder])

# Charger et redimensionner les images de prédiction à (100, 100)
X_val = []
files = gb.glob(base_path + "/seg_pred/seg_pred/*.jpg")
for file in files:
    image = cv2.imread(file)
    image_resize = cv2.resize(image,(new_size,new_size))
    X_val.append(image_resize)

X_train = np.array(X_train)
y_train = np.array(y_train)
X_test = np.array(X_test)
y_test = np.array(y_test)
X_val = np.array(X_val)

# Normalisation des données
X_train = tf.keras.utils.normalize(X_train, axis=1)
X_test = tf.keras.utils.normalize(X_test, axis=1)

# Définir l'architecture du modèle VGG16
model = Sequential([

        Conv2D(64, (3, 3), padding='same', activation='relu', input_shape=(X_train.shape[1:])),
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
        MaxPooling2D(pool_size=(2, 2)),
        
        Conv2D(512, (3, 3), padding='same', activation='relu'),
        BatchNormalization(),
        Conv2D(512, (3, 3), padding='same', activation='relu'),
        BatchNormalization(),
        Conv2D(512, (3, 3), padding='same', activation='relu'),
        BatchNormalization(),
        MaxPooling2D(pool_size=(2, 2)),
        
        # Partie classification
        Flatten(),
        Dense(4096, activation='relu'),
        Dropout(0.2),
        Dense(4096, activation='relu'),
        Dropout(0.2),
        Dense(1000, activation='relu'),
        Dropout(0.2),
        Dense(6, activation='softmax')
])

# Compiler le modèle
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

history = model.fit(X_train, y_train, epochs = 20, validation_data=(X_test, y_test), batch_size=32, verbose=1)

# Sauvegarder le modèle
model.save("C:/Data/Models/CNNIntelImagesClassification_VGG16.keras")

Loss , Acc = model.evaluate(X_test,y_test)
print("Accuracy: ", Acc)
print("Loss: ", Loss)

# Prédire sur l'ensemble de test
y_test_pred = model.predict(X_test)
y_test_pred_labels = np.argmax(y_test_pred, axis=1)

# Calculer le score F1 (moyenne macro)
f1_test = f1_score(y_test, y_test_pred_labels, average='macro')
print("Test F1 Score (macro):", f1_test)

# Prédire sur l'ensemble d'entraînement
y_train_pred = model.predict(X_train)
y_train_pred_labels = np.argmax(y_train_pred, axis=1)

# Calculer le score F1 (moyenne macro)
f1_train = f1_score(y_train, y_train_pred_labels, average='macro')
print("Train F1 Score (macro):", f1_train)

from sklearn.metrics import precision_score, recall_score

# Precision and recall for test set
precision_test = precision_score(y_test, y_test_pred_labels, average='macro')
recall_test = recall_score(y_test, y_test_pred_labels, average='macro')

# Precision and recall for train set
precision_train = precision_score(y_train, y_train_pred_labels, average='macro')
recall_train = recall_score(y_train, y_train_pred_labels, average='macro')

print("Test Precision (macro):", precision_test)
print("Test Recall (macro):", recall_test)
print("Train Precision (macro):", precision_train)
print("Train Recall (macro):", recall_train)

# Affichier les courbes ROC pour l'ensemble de test et d'entraînement
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize
import matplotlib.pyplot as plt

# Binarize the labels for multi-class ROC
n_classes = 6
y_test_bin = label_binarize(y_test, classes=list(range(n_classes)))
y_train_bin = label_binarize(y_train, classes=list(range(n_classes)))

# ROC curve for test set
fpr_test = dict()
tpr_test = dict()
roc_auc_test = dict()
for i in range(n_classes):
    fpr_test[i], tpr_test[i], _ = roc_curve(y_test_bin[:, i], y_test_pred[:, i])
    roc_auc_test[i] = auc(fpr_test[i], tpr_test[i])

# ROC curve for train set
fpr_train = dict()
tpr_train = dict()
roc_auc_train = dict()
for i in range(n_classes):
    fpr_train[i], tpr_train[i], _ = roc_curve(y_train_bin[:, i], y_train_pred[:, i])
    roc_auc_train[i] = auc(fpr_train[i], tpr_train[i])

# Plot ROC curves
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
for i in range(n_classes):
    plt.plot(fpr_test[i], tpr_test[i], label=f'Class {i} (AUC = {roc_auc_test[i]:.2f})')
plt.plot([0, 1], [0, 1], 'k--')
plt.title('Test ROC Curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend()

plt.subplot(1, 2, 2)
for i in range(n_classes):
    plt.plot(fpr_train[i], tpr_train[i], label=f'Class {i} (AUC = {roc_auc_train[i]:.2f})')
plt.plot([0, 1], [0, 1], 'k--')
plt.title('Train ROC Curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend()

plt.tight_layout()
plt.show()

# Affichier les courbes d'apprentissage
df = pd.DataFrame(history.history)
df.plot(figsize=(8, 5))
plt.grid(True)
plt.gca().set_ylim(0, 1)
plt.show()


# Prédire 40 images et les afficher
num_images = 40
for idx in range(num_images):
    img = X_val[idx].astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)
    pred = model.predict(img)
    predicted_class = np.argmax(pred, axis=1)[0]
    class_name = [k for k, v in code.items() if v == predicted_class][0]
    print(f"Image {idx}: Predicted class index: {predicted_class}, class name: {class_name}")
    plt.imshow(X_val[idx])
    plt.axis('off')
    plt.title(f"Image {idx} from X_val")
    plt.show()
