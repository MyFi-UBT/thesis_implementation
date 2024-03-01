from PIL import Image, ImageDraw, ImageFilter
import random
from random import randrange
from pathlib import Path


def intersection_with_background(background, randomxx, randomyy, form):
    if ((randomxx + form.width) > background.width) or ((randomyy + form.height) > background.height):
        return True
    else:
        return False


def intersection_with_other_objects(randomxx_1, randomyy_1, img, positions_and_sizes):
    for p in positions_and_sizes:
        pos = p[0]
        size = p[1]

        min_obj1_x = pos[0]
        max_obj1_x = pos[0] + size[0]
        min_obj2_x = randomxx_1
        max_obj2_x = randomxx_1 + img.width

        min_obj1_y = pos[1]
        max_obj1_y = pos[1] + size[1]
        min_obj2_y = randomyy_1
        max_obj2_y = randomyy_1 + img.height

        # check if the objects intersect in x direction, continue means no intersection
        if min_obj2_x > max_obj1_x or min_obj1_x > max_obj2_x:
            continue
        else:
            # check if the objects intersect in y direction
            if min_obj2_y > max_obj1_y or min_obj1_y > max_obj2_y:
                continue
            else:
                # there is an intersection (in x AND in y direction)
                return True
    return False


def create_random_positions(x, background_image, object_images, path):
    images = []
    background = Image.open(background_image)
    for oi in object_images:
        img = Image.open(oi)
        images.append(img)

    positions_and_sizes = []
    counter = 0

    for img in images:
        randomx = random.uniform(0, 1)
        randomy = random.uniform(0, 1)
        randomxx_1 = int(randomx * background.size[0])
        randomyy_1 = int(randomy * background.size[1])
        # for the first object that is pasted, it is only necessary to check if there is an section with the
        # background/image border
        if counter == 0:
            while (intersection_with_background(background, randomxx_1, randomyy_1, img)):
                randomx = random.uniform(0, 1)
                randomy = random.uniform(0, 1)
                randomxx_1 = int(randomx * background.size[0])
                randomyy_1 = int(randomy * background.size[1])

        # in case other objects already exist in the image, intersections between objects AND with the background
        # have to be avoided
        else:
            while (intersection_with_background(background, randomxx_1, randomyy_1,
                                                img) or intersection_with_other_objects(randomxx_1, randomyy_1, img,
                                                                                        positions_and_sizes)):
                randomx = random.uniform(0, 1)
                randomy = random.uniform(0, 1)
                randomxx_1 = int(randomx * background.size[0])
                randomyy_1 = int(randomy * background.size[1])
        # last parameter in pasting process important for transparent images
        background.paste(img, (randomxx_1, randomyy_1), img.convert('RGBA'))
        position = (randomxx_1, randomyy_1)
        size = (img.width, img.height)
        positions_and_sizes.append((position, size))
        counter = counter + 1

    # define condition for being positive labelled
    # TODO: this condition has to be adjusted manually for each generation case.
    #  We need an (semi-)automated solution here
#    if (positions_and_sizes[2][0][1] < background.size[1]/7 or positions_and_sizes[3][0][1] < background.size[1]/7):
    if ("blue" in object_images[0] and positions_and_sizes[0][0][1] > background.size[1]/2):
        Path(path+'/good').mkdir(parents=True, exist_ok=True)
        background.save(path + '/good/data_' + str(x) + '.jpg')
    else:
        Path(path+'/bad').mkdir(parents=True, exist_ok=True)
        background.save(path + '/bad/data_' + str(x) + '.jpg')
    print("Successfully created a new image: data_" + str(x) + ".png")
