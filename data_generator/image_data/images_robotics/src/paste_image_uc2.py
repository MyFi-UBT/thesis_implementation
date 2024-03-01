from PIL import Image, ImageDraw, ImageFilter
import random
from random import randrange
from pathlib import Path
import os

def intersection_with_area(end_area_x, end_area_y, randomxx, randomyy, form):
    if ((randomxx + form.width) > end_area_x) or ((randomyy + form.height) > end_area_y):
        return True
    else:
        return False

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

def create_fixed_position(x, background_image, object_image, path):

    background = Image.open(background_image)
    img = Image.open(object_image)

    posx = 401
    posy = 886 - img.size[1]
    background.paste(img, (posx, posy), img.convert('RGBA'))

    print("printed fixed pos: data_" + str(x) + ".png")
    return background

def rotateObject_ninty(img):
    old_width = img.size[0]
    old_height = img.size[1]
    img = img.rotate(90, expand=True)
    img.size[0] = old_height
    img.size[1] = old_width
    return img

def check_bad_case_recursively(copy_array):
    end_areaA_x_first = 263
    end_areaA_x_snd = 401

    for pos_index, o in enumerate(copy_array):
        if (o[2] == '../raw_data/6_2.png' and o[0][0] < end_areaA_x_first) or (
                o[2] == '../raw_data/7_2.png' and end_areaA_x_first < o[0][0] < end_areaA_x_snd) or (
                o[2] == '../raw_data/5_2.png' and o[0][0] > end_areaA_x_snd):
            copy_array.remove(o)
            check_bad_case_recursively(copy_array)
    if len(copy_array) == 0:
        return True
    return False


def create_random_positions(x, background_image, object_images, path, label, data_type, nr_of_objects_upper_area):
    images = []

    background = Image.open(background_image)
    background = background.resize((int(background.size[0]/2), int(background.size[1]/2)))

    # Placement/Target area "A" => Divided into three parts
    areaAParts_x = []
    areaAParts_y = []
    start_areaA_x_first = 126
    end_areaA_x_first = 263
    areaAParts_x.append((start_areaA_x_first, end_areaA_x_first))
    start_areaA_x_snd = 264
    end_areaA_x_snd = 401
    areaAParts_x.append((start_areaA_x_snd, end_areaA_x_snd))
    start_areaA_x_third = 402
    end_areaA_x_third = 539
    areaAParts_x.append((start_areaA_x_third, end_areaA_x_third))

    start_areaA_y_first = 327
    end_areaA_y_first = 538
    areaAParts_y.append((start_areaA_y_first, end_areaA_y_first))
    start_areaA_y_snd = 327
    end_areaA_y_snd = 538
    areaAParts_y.append((start_areaA_y_snd, end_areaA_y_snd))
    start_areaA_y_third = 327
    end_areaA_y_third = 538
    areaAParts_y.append((start_areaA_y_third, end_areaA_y_third))


    # Placement/Target area "A" => full borders
    start_area_a_x = 126
    end_area_a_x = 539
    start_area_a_y = 327
    end_area_a_y = 539

    # Starting area "B" => full borders
    start_area_x = 249
    end_area_x = 875
    start_area_y = 1296
    end_area_y = 1481

    for oi in object_images:
        img = Image.open(oi)
        images.append(img)

    positions_and_sizes = []
    counter = 0
    index = 0

    for img_index, img in enumerate(images):
        orig_img = img.copy()
#        print(index)
        rotate_degree = random.randint(0, 180)
        img = orig_img.rotate(rotate_degree, expand=True)
        if index < nr_of_objects_upper_area:

            if label == 1:
                randomxx_1 = random.randint(areaAParts_x[index][0], areaAParts_x[index][1])
                randomyy_1 = random.randint(areaAParts_y[index][0], areaAParts_y[index][1])
                # for the first object that is pasted, it is only necessary to check if there is an section with the
                # background/image border
                if counter == 0:
                    while (intersection_with_area(areaAParts_x[index][1], areaAParts_y[index][1], randomxx_1, randomyy_1, img)):
                        rotate_degree = random.randint(0, 180)
                        img = orig_img.rotate(rotate_degree, expand=True)
                        randomxx_1 = random.randint(areaAParts_x[index][0], areaAParts_x[index][1])
                        randomyy_1 = random.randint(areaAParts_y[index][0], areaAParts_y[index][1])

                # in case other objects already exist in the image, intersections between objects AND with the background
                # have to be avoided
                else:
                    while (intersection_with_area(areaAParts_x[index][1], areaAParts_y[index][1], randomxx_1, randomyy_1, img) or intersection_with_other_objects(randomxx_1, randomyy_1, img,
                                                                                                positions_and_sizes)):
                        rotate_degree = random.randint(0, 180)
                        img = orig_img.rotate(rotate_degree, expand=True)
                        randomxx_1 = random.randint(areaAParts_x[index][0], areaAParts_x[index][1])
                        randomyy_1 = random.randint(areaAParts_y[index][0], areaAParts_y[index][1])
                # last parameter in pasting process important for transparent images
            else:
                # label = 0 and the 3 parts can be placed anywhere in Area A
                rotate_degree = random.randint(0, 180)
                img = orig_img.rotate(rotate_degree, expand=True)
                randomxx_1 = random.randint(start_area_a_x, end_area_a_x)
                randomyy_1 = random.randint(start_area_a_y, end_area_a_y)
                # for the first object that is pasted, it is only necessary to check if there is an section with the
                # background/image border
                if counter == 0:
                    while (intersection_with_area(end_area_a_x, end_area_a_y, randomxx_1, randomyy_1, img)):
                        rotate_degree = random.randint(0, 180)
                        img = orig_img.rotate(rotate_degree, expand=True)
                        randomxx_1 = random.randint(start_area_a_x, end_area_a_x)
                        randomyy_1 = random.randint(start_area_a_y, end_area_a_y)

                # in case other objects already exist in the image, intersections between objects AND with the background
                # have to be avoided
                else:
                    while (intersection_with_area(end_area_a_x, end_area_a_y, randomxx_1, randomyy_1,
                                                  img) or intersection_with_other_objects(randomxx_1, randomyy_1, img,
                                                                                          positions_and_sizes)):
                        rotate_degree = random.randint(0, 180)
                        img = orig_img.rotate(rotate_degree, expand=True)
                        randomxx_1 = random.randint(start_area_a_x, end_area_a_x)
                        randomyy_1 = random.randint(start_area_a_y, end_area_a_y)

            background.paste(img, (randomxx_1, randomyy_1), img.convert('RGBA'))
            position = (randomxx_1, randomyy_1)
            size = (img.width, img.height)
            positions_and_sizes.append((position, size, images[img_index].filename))
            counter = counter + 1
        else:
            rotate_degree = random.randint(0, 180)
            img = orig_img.rotate(rotate_degree, expand=True)
            randomxx_1 = random.randint(start_area_x, end_area_x)
            randomyy_1 = random.randint(start_area_y, end_area_y)
            # for the first object that is pasted, it is only necessary to check if there is an section with the
            # background/image border
            if counter == 0:
                while (intersection_with_area(end_area_x, end_area_y, randomxx_1, randomyy_1, img)):
                    rotate_degree = random.randint(0, 180)
                    img = orig_img.rotate(rotate_degree, expand=True)
                    randomxx_1 = random.randint(start_area_x, end_area_x)
                    randomyy_1 = random.randint(start_area_y, end_area_y)

            # in case other objects already exist in the image, intersections between objects AND with the background
            # have to be avoided
            else:
                while (intersection_with_area(end_area_x, end_area_y, randomxx_1, randomyy_1,
                                              img) or intersection_with_other_objects(randomxx_1, randomyy_1, img,
                                                                                      positions_and_sizes)):
                    rotate_degree = random.randint(0, 180)
                    img = orig_img.rotate(rotate_degree, expand=True)
                    randomxx_1 = random.randint(start_area_x, end_area_x)
                    randomyy_1 = random.randint(start_area_y, end_area_y)
            # last parameter in pasting process important for transparent images

            background.paste(img, (randomxx_1, randomyy_1), img.convert('RGBA'))
            position = (randomxx_1, randomyy_1)
            size = (img.width, img.height)
            positions_and_sizes.append((position, size, images[img_index].filename))
            counter = counter + 1
        index = index+1
        # check if accidently a "good" image was created, then remove this example and recreate another one
        if img_index == 2 and label == 0:
            copy_array = positions_and_sizes.copy()

            if check_bad_case_recursively(copy_array):
                print ("I accidently created a good example due to randomization.")
                return False

    if label == 1:
        Path(path + '/good').mkdir(parents=True, exist_ok=True)
        nr_of_entries = os.listdir(path + '/good')
        background = background.convert("RGB")
        # the next line is only for reduced images!
        background = background.resize((int(background.size[0] / 2), int(background.size[1] / 2)))
        if data_type == "png":
            background.save(path + '/good/data_' + str(len(nr_of_entries)) + '.png')
        else:
            background.save(path + '/good/data_' + str(len(nr_of_entries)) + '.jpg')
        return True
    else:
        Path(path + '/bad').mkdir(parents=True, exist_ok=True)
        nr_of_entries = os.listdir(path + '/bad')
        background = background.convert("RGB")
        # the next line is only for reduced images!
        background = background.resize((int(background.size[0] / 2), int(background.size[1] / 2)))
        if data_type == "png":
            background.save(path + '/bad/data_' + str(len(nr_of_entries)) + '.png')
        else:
            background.save(path + '/bad/data_' + str(len(nr_of_entries)) + '.jpg')
        return True

    if data_type == "png":
        print("Successfully created a new image: data_" + str(len(nr_of_entries)) + ".png")
    else:
        print("Successfully created a new image: data_" + str(len(nr_of_entries)) + ".jpg")
