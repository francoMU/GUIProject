from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from guiproject.mnist import load_test_images, load_test_labels, \
    load_training_labels, load_training_images
from keras.layers import Conv2D, MaxPooling2D, Dense, \
    Flatten  # convolution layers; core layers
from keras.layers.normalization import BatchNormalization
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator
from keras.utils.np_utils import to_categorical
from sklearn.model_selection import train_test_split

# https://www.kaggle.com/elcaiseri/mnist-simple-cnn-keras-accuracy-0-99-top-1


test_images = load_test_images().astype('float32').reshape(-1, 28, 28, 1)
training_images = load_training_images(10000).astype('float32').reshape(-1, 28,
                                                                        28, 1)

test_images = test_images / 255.0
training_images = training_images / 255.0

test_labels = to_categorical(load_test_labels())
training_labels = to_categorical(load_training_labels(10000))

print(training_labels.shape)
print(test_images.shape)

X_train, X_test, y_train, y_test = train_test_split(training_images,
                                                    training_labels,
                                                    test_size=0.1,
                                                    random_state=0)

print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

X_train__ = X_train.reshape(X_train.shape[0], 28, 28)

fig, axis = plt.subplots(1, 4, figsize=(20, 10))
for i, ax in enumerate(axis.flat):
    ax.imshow(X_train__[i], cmap='binary')
    digit = y_train[i].argmax()
    ax.set(title=f"Real Number is {digit}")

plt.show()

mean = np.mean(X_train)
std = np.std(X_train)


def standardize(x):
    return (x - mean) / std


# epochs = 50

epochs = 20
batch_size = 64

model = Sequential()

# model.add(Lambda(standardize,input_shape=(28,28,1)))
model.add(Conv2D(filters=64, kernel_size=(3, 3), activation="relu",
                 input_shape=(28, 28, 1)))
model.add(Conv2D(filters=64, kernel_size=(3, 3), activation="relu"))

model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(BatchNormalization())
model.add(Conv2D(filters=128, kernel_size=(3, 3), activation="relu"))
model.add(Conv2D(filters=128, kernel_size=(3, 3), activation="relu"))

model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(BatchNormalization())
model.add(Conv2D(filters=256, kernel_size=(3, 3), activation="relu"))

model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(BatchNormalization())
model.add(Dense(512, activation="relu"))

model.add(Dense(10, activation="softmax"))

model.compile(loss="categorical_crossentropy", optimizer="adam",
              metrics=["accuracy"])

datagen = ImageDataGenerator(
    featurewise_center=False,  # set input mean to 0 over the dataset
    samplewise_center=False,  # set each sample mean to 0
    featurewise_std_normalization=False,  # divide inputs by std of the dataset
    samplewise_std_normalization=False,  # divide each input by its std
    zca_whitening=False,  # apply ZCA whitening
    rotation_range=10,
    # randomly rotate images in the range (degrees, 0 to 180)
    zoom_range=0.1,  # Randomly zoom image
    width_shift_range=0.1,
    # randomly shift images horizontally (fraction of total width)
    height_shift_range=0.1,
    # randomly shift images vertically (fraction of total height)
    horizontal_flip=False,  # randomly flip images
    vertical_flip=False)  # randomly flip images

# datagen.fit(X_train)
train_gen = datagen.flow(X_train, y_train, batch_size=batch_size)
test_gen = datagen.flow(X_test, y_test, batch_size=batch_size)

history = model.fit(train_gen,
                    epochs=epochs,
                    steps_per_epoch=X_train.shape[0] // batch_size,
                    validation_data=test_gen,
                    validation_steps=X_test.shape[0] // batch_size)

PATH = Path(__file__).parent

model.save(PATH / 'fast_model.h5', save_format='h5')

#
# Test the whole model
#

y_pred = model.predict(X_test)
X_test__ = X_test.reshape(X_test.shape[0], 28, 28)

fig, axis = plt.subplots(4, 4, figsize=(12, 14))
for i, ax in enumerate(axis.flat):
    ax.imshow(X_test__[i], cmap='binary')
    ax.set(
        title=f"Real Number is {y_test[i].argmax()}\nPredict Number is "
              f"{y_pred[i].argmax()}")

plt.show()
