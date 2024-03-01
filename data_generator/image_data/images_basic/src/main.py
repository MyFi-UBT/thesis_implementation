from matplotlib import patches
from random import randrange
from PIL import Image
import paste_image
from pathlib import Path


def generate_data(scenario_type, rangeVal):

    # path: define the path and folders where the generated data should be stored
    if scenario_type == 1:
        path = '../generated_data/scenario1/scenario1_bghalf_w'+str(rangeVal)+'_images'

        sufficient_data = False
        x = 0
        while not sufficient_data:
            object_images = []
            # which image has to be painted could either be computed randomly or decided manually
            # in case you want to select them randomly, activate the randrange part
            # randNr = randrange(1,4)
            randNr = randrange(1,3)
            if randNr == 1:
                objectDataPath = '../raw_data/rectangle_blue.jpg'
            elif randNr == 2:
                objectDataPath = '../raw_data/rectangle_green.jpg'


            object_images.append(objectDataPath)

            background_image = '../raw_data/background_half.jpg'

            # check if given path where the generated data will be written to does already exist and if not; create it
            Path(path).mkdir(parents=True, exist_ok=True)
            sufficient_data = paste_image.create_random_positions(x, background_image, object_images, path, scenario_type, rangeVal)
            x = x+1

    if scenario_type == 2:
        path = '../generated_data/scenario2/scenario2_w' + str(rangeVal) + '_images'

        sufficient_data = False
        x = 0
        while not sufficient_data:
            object_images = []
            objectDataPath2 = '../raw_data/circle_red.png'
            objectDataPath = '../raw_data/rectangle_red.jpg'

            # in our 4-object-case we want 2 circles and 2 rectangles, for this reason we add each twice
            object_images.append(objectDataPath)
            object_images.append(objectDataPath)
            object_images.append(objectDataPath2)
            object_images.append(objectDataPath2)

            background_image = '../raw_data/background.jpg'

            # check if given path where the generated data will be written to does already exist and if not; create it
            Path(path).mkdir(parents=True, exist_ok=True)
            sufficient_data = paste_image.create_random_positions(x, background_image, object_images, path, scenario_type, rangeVal)
            x = x + 1
    print("Done with image generation.")


# first parameter = scenario_type: define which scenario should be created (e.g., 1 = one object in scene, 2 = four objects in scene)
# second parameter = number of images to be generated
generate_data(2, 1000)