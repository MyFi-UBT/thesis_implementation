from matplotlib import patches
from random import randrange
from PIL import Image
import paste_image
from pathlib import Path


# define the number of data which should be generated
rangeVal = 10000

# define the path and folders where the generated data should be stored
path = '../generated_data/wuerf_data/scen1_2'

for x in range(rangeVal):
    label = 0
    object_images = []
    # which image has to be painted could either be computed randomly or decided manually
    # in case you want to select them randomly, activate the randrange part
    # randNr = randrange(1,4)
    randNr = randrange(1,3)
    if randNr == 1:
        objectDataPath = '../raw_data/rectangle_wuerf_blue.jpg'
#        objectDataPath2 = '../raw_data/circle_wuerf.png'
    elif randNr == 2:
        # objectDataPath = 'generator_data/circle.jpg'
        objectDataPath = '../raw_data/rectangle_wuerf_green.jpg'
    elif randNr == 3:
        # objectDataPath = 'generator_data/circle.jpg'
        objectDataPath = '../raw_data/rectangle.png'
    else:
        objectDataPath = '../raw_data/rectangle.png'

    # in our 4-object-case we want 2 circles and 2 rectangles, for this reason we add each twice
    object_images.append(objectDataPath)
#    object_images.append(objectDataPath)
#    object_images.append(objectDataPath2)
#    object_images.append(objectDataPath2)

    # which background will be selected could either be computed randomly or decided manually
    # in case you want to select it randomly, activate the randrange part
    # bgRandnr = randrange(1,4)
    bgRandnr = 1
    background_image = ""
    if bgRandnr == 1:
        background_image = '../raw_data/tischplatte_kleiner_30_prozent.jpg'
    elif bgRandnr == 2:
        background_image = '../raw_data/grass.jpg'
    else:
        background_image = '../raw_data/waves.jpg'

    # check if given path where the generated data will be written to does already exist and if not; create it
    Path(path).mkdir(parents=True, exist_ok=True)
    paste_image.create_random_positions(x, background_image, object_images, path)

print("Done with image generation.")
