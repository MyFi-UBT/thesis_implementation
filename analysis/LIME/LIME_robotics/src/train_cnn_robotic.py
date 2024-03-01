# *** This .py serves to train a CNN with images stored in /data ***
# *** Input:
#       Path to input data
# *** Output:
#       Trained CNN ("model")
# the code is from here: https://towardsdatascience.com/interpreting-image-classification-model-with-lime-1e7064a2f2e5

from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
from pathlib import Path
import datetime

# tf.config.experimental_run_functions_eagerly(True)

# Section to enable training on GPU
def get_image_size(input_data_path):
    import os
    import skimage.io
    i = input_data_path + "/" + (os.listdir(input_data_path)[0])
    img = skimage.io.imread(i)
    return img.shape


def configure_gpu_training():
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        try:
            # Currently, memory growth needs to be the same across GPUs
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            logical_gpus = tf.config.experimental.list_logical_devices('GPU')
            print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
        except RuntimeError as e:
            # Memory growth must be set before GPUs have been initialized
            print(e)
    physical_devices = tf.config.experimental.list_physical_devices('GPU')
    assert len(physical_devices) > 0, "Not enough GPU hardware devices available"
    config = tf.config.experimental.set_memory_growth(physical_devices[0], True)


def start_training(input_data_path, model_saving_path):
#    configure_gpu_training()
    img_size = get_image_size(input_data_path+"/good")
    img_height = img_size[0]
    img_width = img_size[1]

    # Generate training and test data with Image Generator
    train_datagen = ImageDataGenerator(rescale=1 / 255,
                                       validation_split=0.2)

    # batch_size: 1920
    # 12.09.2022: batch_size = 32
    train_generator = train_datagen.flow_from_directory(input_data_path, target_size=(img_height, img_width),
                                                        batch_size=32,
                                                        class_mode='categorical',
                                                        shuffle=False,
                                                        subset='training')
    # batch_size: 480
    # 12.09.2022: batch_size = 32
    test_generator = train_datagen.flow_from_directory(input_data_path,
                                                       target_size=(img_height, img_width),
                                                       batch_size=32,
                                                       class_mode='categorical',
                                                       shuffle=False,
                                                       subset='validation')

    # Fetch the data and the labels
    x_train, y_train = next(train_generator)
    x_test, y_test = next(test_generator)

    # Fix the filepath
    test_filepath = []
    for filepath in test_generator.filepaths:
        filepath = filepath.replace('\\', '/')
        test_filepath.append(filepath)

    model = Sequential([

        #    CoordinateChannel2D(),
        # First convolution
        # 100, 100 = img_width, img_height
        Conv2D(16, (3, 3), activation='relu', strides=2, input_shape=(img_height, img_width,  3)),
        MaxPooling2D(2, 2),

        #   CoordinateChannel2D(use_radius=True),
        # Second convolution
        Conv2D(32, (3, 3), activation='relu', strides=2),
        MaxPooling2D(2, 2),

        #   CoordinateChannel2D(use_radius=True),
        # Third convolution
        Conv2D(64, (3, 3), activation='relu', strides=2),
        MaxPooling2D(2, 2),

        Flatten(),

        # Dense hidden layer
        Dense(512, activation='relu'),
        Dropout(0.2),

        # Output neuron.
        Dense(2, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # 20 epochs are enough for use case 1
    history = model.fit(
        train_generator,
        epochs=10,
        verbose=1)

    e = datetime.datetime.now()
    print(e)
    firstPart = "%s_%s_%s" % (e.day, e.month, e.year)
    secondPart = "%s_%s_%s" % (e.hour, e.minute, e.second)

    Path(model_saving_path).mkdir(parents=True, exist_ok=True)
    model.save(model_saving_path+"/model_" + firstPart+"--"+secondPart)

    return model
