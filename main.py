import random
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import os
import cv2
import pickle

# from tensorflow.keras.models import Sequential
from keras import Sequential
from keras.src.layers import Conv2D, Activation, MaxPooling2D, Flatten, Dense
from tensorflow.keras.models import load_model

class StopAtAccuracy(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if logs.get('accuracy') >= 1.0:
            print("\nReached 100% accuracy, stopping training!")
            self.model.stop_training = True


def create_test_data(X_test, y_test):
    DATADIR = "C:/Users/Ghafo/Desktop/projects/MachineLearningAttempt2nd/images/test"
    CATEGORIES = ["normal", "pneumonia"]
    for category in CATEGORIES:
        path = os.path.join(DATADIR, category)  # path to the images
        class_num = CATEGORIES.index(category)
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
                test_data.append([new_array, class_num])
            except Exception as e:
                pass

    for features, label in test_data:
        X_test.append(features)
        y_test.append(label)

    X_test = np.array(X_test).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    pickle_out = open("X_test.pickle", "wb")
    pickle.dump(X_test, pickle_out)
    pickle_out.close()

    pickle_out = open("y_test.pickle", "wb")
    pickle.dump(y_test, pickle_out)
    pickle_out.close()


def create_training_data(X_train, y_train):
    DATADIR = "C:/Users/Ghafo/Desktop/projects/MachineLearningAttempt2nd/images/train"
    CATEGORIES = ["normal", "pneumonia"]
    for category in CATEGORIES:
        path = os.path.join(DATADIR, category)  # path to the images
        class_num = CATEGORIES.index(category)
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
                training_data.append([new_array, class_num])
            except Exception as e:
                pass

            # plt.imshow(img_array, cmap="gray")
            # plt.show()

    random.shuffle(training_data)

    for features, label in training_data:
        X_train.append(features)
        y_train.append(label)

    X_train = np.array(X_train).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    pickle_out = open("X.pickle", "wb")
    pickle.dump(X_train, pickle_out)
    pickle_out.close()

    pickle_out = open("y.pickle", "wb")
    pickle.dump(y_train, pickle_out)
    pickle_out.close()


def create_val_data(X_val, y_val):
    DATADIR = "C:/Users/Ghafo/Desktop/projects/MachineLearningAttempt2nd/images/val"
    CATEGORIES = ["normal", "pneumonia"]
    for category in CATEGORIES:
        path = os.path.join(DATADIR, category)  # path to the images
        class_num = CATEGORIES.index(category)
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
                val_data.append([new_array, class_num])
            except Exception as e:
                pass

            # plt.imshow(img_array, cmap="gray")
            # plt.show()

    random.shuffle(val_data)

    for features, label in val_data:
        X_val.append(features)
        y_val.append(label)

    X_val = np.array(X_val).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    pickle_out = open("X_val.pickle", "wb")
    pickle.dump(X_val, pickle_out)
    pickle_out.close()

    pickle_out = open("y_val.pickle", "wb")
    pickle.dump(y_val, pickle_out)
    pickle_out.close()

def makeModel():
   #create model
    model = Sequential()
    model.add(Conv2D(64, (3, 3), input_shape=X_train.shape[1:]))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(512, activation='relu'))

    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=['accuracy'])

    model.fit(X_train, y_train, batch_size=15, epochs=25, verbose=1, validation_data=(X_val, y_val), callbacks=[early_stop, stop_at_1_accuracy])
    model.save("NeuralNetwork.keras")

def displayTestImages(X_test, y_test, y_pred, numImages):
    plt.figure(figsize=(15, 5))

    for i in range(numImages):
        idx = random.randint(0, len(X_test) - 1)
        plt.subplot(1, numImages, i + 1)

        plt.imshow(X_test[idx])
        plt.title(
            f"Actual: {'Pneumonia' if y_test[idx] == 1 else 'Normal'}\nPredicted: {'Pneumonia' if y_pred[idx] == 1 else 'Normal'}")
        plt.axis('off')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    stop_at_1_accuracy = StopAtAccuracy()
    early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    import os

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    # feature set
    X_train = []
    # labels
    y_train = []

    # feature set
    X_test = []
    # labels
    y_test = []

    # feature set
    X_val = []
    # labels
    y_val = []


    IMG_SIZE = 150
    training_data = []
    test_data = []
    val_data = []

    #create_training_data(X_train,y_train)

    #create_test_data(X_test,y_test)

    #create_val_data(X_val, y_val)

    #
    # pickle_in = open("X.pickle", "rb")
    # X_train = pickle.load(pickle_in)
    # X_train = np.array(X_train)
    #
    # pickle_in = open("y.pickle", "rb")
    # y_train = pickle.load(pickle_in)
    # y_train = np.array(y_train)

    pickle_inx = open("X_test.pickle", "rb")
    X_test = pickle.load(pickle_inx)
    X_test = np.array(X_test)

    pickle_iny = open("y_test.pickle", "rb")
    y_test = pickle.load(pickle_iny)
    y_test = np.array(y_test)
    #
    # pickle_inval = open("X_val.pickle", "rb")
    # X_val = pickle.load(pickle_inval)
    # X_val = np.array(X_val)
    #
    # pickle_inyval = open("y_val.pickle", "rb")
    # y_val = pickle.load(pickle_inyval)
    # y_val = np.array(y_val)

    # Normalize the test images
    X_test = X_test / 255.0

    # normalise data and train
    # X_train = X_train / 255.0

    # X_val = X_val / 255.0

    #makeModel()



    model = load_model("NeuralNetwork.keras")
    model.summary()

    y_pred_probs = model.predict((X_test))
    y_pred = [1 if prob > 0.5 else 0 for prob in y_pred_probs]




    # print("EVALUATION")
    model.evaluate(X_test, y_test)

    # Predict on the test set
    displayTestImages(X_test, y_test, y_pred, 5)


