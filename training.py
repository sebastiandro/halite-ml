import tensorflow as tf
import os
import numpy as np
import time
from tqdm import tqdm

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

for f in os.listdir(TRAINING_DATA_DIR):
    halite_amount = int(f.split("-")[0])
    if halite_amount >= HALITE_THRESHOLD:
        training_file_names.append(os.path.join(TRAINING_DATA_DIR, f))

print(f"After the threshold we have {len(training_file_names)} games.")

random.shuffle(training_file_names)
