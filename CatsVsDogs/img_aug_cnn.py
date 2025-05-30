import os
import random
import warnings
warnings.filterwarnings("ignore")
from utils import train_test_split
import time

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Dropout, Flatten, Dense, BatchNormalization #batch normalization may be used for optimizing so i added it
from keras.preprocessing.image import ImageDataGenerator

start_time = time.time()

# from project pdf:
# Conv2D class will be used for the convolution layers, MaxPooling2D for pooling layers,
# and Dense for the fully connected layers. (Note that you will need to add a Flatten layer
# between the last pooling layer and the first fully connected layer for reshaping purposes).

#keras documentation: https://keras.io/2/api/

#these will be the hyperparameters:

filterSize = (3,3) 
numOfFilters = 24
inputSize = (150,150,3) # every image will be resized to this size, and it will have 3 color channels aka rgb
poolingSize = (2,2)
batchSize = 64
epochs = 25

model = Sequential()

#following the diagram on the project pdf, i only have 2 convolution+pooling layers then the last
#is the fully connected layer responsible for the predictions. to optimize, maybe an another hidden layer
#with either the same or more filters than the last layer.

model.add((Conv2D(numOfFilters,filterSize, activation='relu',input_shape = inputSize)))
# model.add(BatchNormalization()) # could be used to optimize
model.add((MaxPooling2D(pool_size=poolingSize,strides=2)))
# Dropout(0.2)


model.add((Conv2D(numOfFilters*2,filterSize, activation='relu')))
# model.add(BatchNormalization()) # could be used to optimize
model.add(MaxPooling2D(pool_size=poolingSize))
# Dropout(0.2)


model.add((Conv2D(numOfFilters*4,filterSize, activation='relu')))
# model.add(BatchNormalization()) # could be used to optimize
model.add(MaxPooling2D(pool_size=poolingSize))
# Dropout(0.2)

model.add(Flatten())
model.add(Dense(128, activation='relu'))
# Dropout(0.5)
model.add(Dense(1, activation='sigmoid')) #pdf says to use sigmoid for the classification
#if model overfits during training, consider using dropout 

#to start off question 3
model.compile(optimizer = "adam", loss = "binary_crossentropy", metrics = ["accuracy"])

# Takes in the images from Dataset/PetImages/Train and trains the model
train_img_gen = ImageDataGenerator(
    rescale=1./255,
    horizontal_flip=True,
    rotation_range=30,
    shear_range=0.2,
    width_shift_range=0.1,
    height_shift_range=0.1
)
training_gen = train_img_gen.flow_from_directory(
    directory="./CatsVsDogs/Dataset/PetImages/Train",
    batch_size=batchSize,
    target_size=(inputSize[0], inputSize[1]),
    class_mode="binary",
    shuffle=True
)
model.fit_generator(
    generator=training_gen,
    steps_per_epoch=len(training_gen),
    epochs=epochs,
    shuffle=True
)

# Takes in the images from Dataset/PetImages/Test and evaluates
# the model's performance on these testing images
test_img_gen = ImageDataGenerator(rescale=1./255)
testing_gen = test_img_gen.flow_from_directory(
    directory="./CatsVsDogs/Dataset/PetImages/Test",
    batch_size=batchSize,
    target_size=(inputSize[0], inputSize[1]),
    class_mode="binary",
    shuffle=True
)
[loss, accuracy] = model.evaluate_generator(
    generator=testing_gen,
    steps=len(testing_gen)
)

print("Loss: " + str(loss))
print("Accuracy: " + str(accuracy * 100) + "%")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time / 60} minutes")