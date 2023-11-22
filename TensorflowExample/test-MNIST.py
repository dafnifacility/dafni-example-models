# Run a simple machine learning classifier. Taken from the Tensorflow (KERAS) examples.
# https://www.tensorflow.org/tutorials/keras/classification

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow.python.client import device_lib

# Helper libraries
import os
import numpy as np
import matplotlib.pyplot as plt

gPATHI = ""
gPATHO = ""
# Pre-amble to setup folders
isDAFNI = os.environ.get("ISDAFNI")
print("ISDAFNI Environment variable = ", isDAFNI, type(isDAFNI))
if isDAFNI == "True":
    if os.name == "nt":
        pren = os.environ.get("HOMEDRIVE")
    else:
        pren = "/"
    gPATHI = os.path.join(pren, "data", "inputs")
    gPATHO = os.path.join(pren, "data", "outputs")
    print("Running within DAFNI: ", gPATHO)
else:
    print("Not running within DAFNI, using run directory")

print(tf.__version__)
local_dev_ps = device_lib.list_local_devices()
for dev in local_dev_ps:
    print(dev.name)

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

fashion_mnist = tf.keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

train_images = train_images/255.0
test_images = test_images/255.0

plt.figure(figsize=(10, 10))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[train_labels[i]])
plt.savefig(os.path.join(gPATHO, 'clothes.png'))

model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

history = model.fit(train_images, train_labels, epochs=10)
print(history.history.keys())

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(history.history['loss'], label='Loss fn')
ax.plot(history.history['accuracy'], label='Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Loss fn/Accuracy')
plt.legend()
plt.savefig(os.path.join(gPATHO, 'training.png'))

test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
print('\nTest accuracy:', test_acc)

probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
predictions = probability_model.predict(test_images)

def plot_image(i, predictions_array, true_label, img):
    true_label, img = true_label[i], img[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(img, cmap=plt.cm.binary)
    predicted_label = np.argmax(predictions_array)
    if predicted_label == true_label:
        color = 'blue'
    else:
        color = 'red'

    plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                            100*np.max(predictions_array),
                                            class_names[true_label]),
                                            color=color)

def plot_value_array(i, predictions_array, true_label):
    true_label = true_label[i]
    plt.grid(False)
    plt.xticks(range(10))
    plt.yticks([])
    thisplot = plt.bar(range(10), predictions_array, color="#777777")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array)
    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('blue')

# Plot the first X test images, their predicted labels, and the true labels.
# Color correct predictions in blue and incorrect predictions in red.
num_rows = 5
num_cols = 3
num_images = num_rows*num_cols
plt.figure(figsize=(2*2*num_cols, 2*num_rows))
for i in range(num_images):
  plt.subplot(num_rows, 2*num_cols, 2*i+1)
  plot_image(i, predictions[i], test_labels, test_images)
  plt.subplot(num_rows, 2*num_cols, 2*i+2)
  plot_value_array(i, predictions[i], test_labels)
plt.tight_layout()
plt.savefig(os.path.join(gPATHO, 'predictions.png'))
