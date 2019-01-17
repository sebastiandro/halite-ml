import tensorflow as tf
import os
import numpy as np
import time
from tqdm import tqdm
import random

from tensorflow.keras.datasets import cifar10
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import TensorBoard


LOAD_TRAIN_FILES = False
LOAD_PREV_MODEL = False
HALITE_THRESHOLD = 4300

TRAINING_CHUNK_SIZE = 500
PREV_MODEL_NAME = ""
VALIDATION_GAME_COUNT = 50
NAME = f"phase1-{int(time.time())}"
EPOCHS = 1

TRAINING_DATA_DIR = 'training_data'

training_file_names = []

### *  -≈[c00l generator is c00l]≈- * ###


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]


for f in os.listdir(TRAINING_DATA_DIR):
    halite_amount = int(f.split("-")[0])
    if halite_amount >= HALITE_THRESHOLD:
        training_file_names.append(os.path.join(TRAINING_DATA_DIR, f))

print(f"After the threshold we have {len(training_file_names)} games.")

random.shuffle(training_file_names)

if LOAD_TRAIN_FILES:
    test_x = np.load("test_x.npy")
    test_y = np.load("test_y.npy")
else:
    test_x = []
    test_y = []

    for f in tqdm(training_file_names[:VALIDATION_GAME_COUNT]):
        data = np.load(f)

        for d in data:
            test_x.append(np.array(d[0]))
            test_y.append(np.array(d[1]))

    np.save("test_x.npy", test_x)
    np.save("test_y.npy", test_y)


test_x = np.array(test_x)

tensorboard = TensorBoard(log_dir=f"logs/{NAME}")

if LOAD_PREV_MODEL:
    model = tf.keras.models.load_model(PREV_MODEL_NAME)
else:
    model = Sequential()
    model.add(
        Conv2D(256, (3, 3), input_shape=test_x.shape[1:], padding="same"))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), padding="same"))

    model.add(Conv2D(256, (3, 3), padding="same"))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), padding="same"))

    model.add(Flatten())

    model.add(Dense(5))
    model.add(Activation('softmax'))

opt = tf.keras.optimizers.Adam(lr=1e-3, decay=1e-3)
model.compile(loss="sparse_categorical_crossentropy",
              optimizer=opt, metrics=['accuracy'])


for e in range(EPOCHS):
    print(f"currently working on epoch {e}")
    training_file_chunks = chunks(
        training_file_names[VALIDATION_GAME_COUNT:], TRAINING_CHUNK_SIZE)

    for idx, training_files in enumerate(training_file_chunks):
        print(
            f"Working on data chunk {idx+1}/{round(len(training_file_names)/TRAINING_CHUNK_SIZE,2)}")
        if LOAD_TRAIN_FILES or e > 0:
            X = np.load(f"X-{idx}.npy")
            y = np.load(f"y-{idx}.npy")
        else:
            X = []
            y = []

            for f in tqdm(training_files):
                data = np.load(f)

                for d in data:
                    X.append(np.array(d[0]))
                    y.append(d[1])

            def balance(x, y):
                _0 = []
                _1 = []
                _2 = []
                _3 = []
                _4 = []

                for x, y in zip(x, y):
                    if y == 0:
                        _0.append([x, y])
                    elif y == 1:
                        _1.append([x, y])
                    elif y == 2:
                        _2.append([x, y])
                    elif y == 3:
                        _3.append([x, y])
                    elif y == 4:
                        _4.append([x, y])

                shortest = min([len(_0), len(_1), len(_2), len(_3), len(_4)])

                _0 = _0[:shortest]
                _1 = _1[:shortest]
                _2 = _2[:shortest]
                _3 = _3[:shortest]
                _4 = _4[:shortest]

                balanced = _0 + _1 + _2 + _3 + _4
                random.shuffle(balanced)

                print("The shortest file was", shortest)
                print(
                    f"The shortest file was {shortest}, total balanced length is {len(balanced)}")

                xs = []
                ys = []

                for x, y in balanced:
                    xs.append(x)
                    ys.append(y)

                return xs, ys

            X, y = balance(X, y)
            test_x, test_y = balance(test_x, test_y)

            X = np.array(X)
            y = np.array(y)
            test_x = np.array(test_x)
            test_y = np.array(test_y)

            np.save(f"X-{idx}.npy", X)
            np.save(f"y-{idx}.npy", y)

            model.fit(X, y, batch_size=32, epochs=1,
                      validation_data=(test_x, test_y), callbacks=[tensorboard])
            model.save(f"models/{NAME}")
