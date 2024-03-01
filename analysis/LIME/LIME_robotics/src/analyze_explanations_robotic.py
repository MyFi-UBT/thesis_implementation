# *** This .py serves to further analyze locally explained images to computer a global explanation ***
# *** Input:
#       Positive labelled and explained images (from LIME)
# *** Output:
#       Sets of values for predefined features (size, shape, color, position)

import imutils
import numpy as np
import os
import skimage
import cv2
from skimage import io
from PIL import Image
from pathlib import Path
import copy


def get_image_size(input_data_path):
    import os
    import skimage.io
    i = input_data_path + "/" + (os.listdir(input_data_path)[0])
    img = skimage.io.imread(i)
    return img.shape

def find_objects(img_name, image, img_width, img_height):
#    cv2.imshow('BGR Image', image)
#    cv2.waitKey(0)
    #    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # image is RGB now
    blue_object_pixels = []
    orange_object_pixels = []
    yellow_object_pixels = []
    green_object_pixels = []
    pink_object_pixels = []

    #    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    #    cv2.imshow('BGR Image', hsv)
    #    cv2.waitKey(0)

    # goal: detect yellow => boundary color of LIME
    # color from here: https://stackoverflow.com/questions/48109650/how-to-detect-two-different-colors-using-cv2-inrange-in-python-opencv
    #    mask2 = cv2.inRange(hsv, (0,80,0), (45, 255, 255))
    #    mask2 = cv2.inRange(image, (0,50,50), (100, 255, 255))
    #    cv2.imshow('mask', mask2)
    #    cv2.waitKey(0)

    # THIS WORK FOR RGB
    for x in range(0, img_width):
        for y in range(0, img_height):

            p = image[y, x]

            if (p[0] == p[1] == p[2]):
                continue
            # object found (red, green or blue)
            else:
#                if(x == 435 and y == 383):
#                    print("blubb")
                if (p[0] < 20 and p[1] < 20 and p[2] > 150):
                    if (y < 400):
                        blue_object_pixels.append((x,y))
                    else:
                        print("got edge case, double blue!")
                if (p[0] < 20 and p[1] > 150 and p[2] < 20):
                    green_object_pixels.append((x,y))
                if (p[0] > 150 and p[1] < 20 and p[2] > 150):
                    pink_object_pixels.append((x,y))
  #              if (p[0] > 150 and p[1] > 150 and p[2] < 20):
  #                  yellow_object_pixels.append((x,y))
                if (p[0] > 200 and 100 < p[1] < 150 and p[2] < 20):
                    orange_object_pixels.append((x,y))

    if len(orange_object_pixels) < 15:
        orange_object_pixels = []

    bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    mask2 = cv2.inRange(hsv, (20, 200, 200), (36, 255, 255))
    kernel = np.ones((5,5),np.uint8)
    opening = cv2.morphologyEx(mask2, cv2.MORPH_OPEN, kernel)
    # get yellow pixels (btw. white in this case), only if the image is not all black
    if np.count_nonzero(opening) != 0:
#        print(img_name)
#        cv2.imshow(img_name, opening)
#        cv2.waitKey(0)

        for x in range(0, img_width):
            for y in range(0, img_height):
                p = opening[y, x]
                if p != 0:
                    yellow_object_pixels.append((x,y))

#    cv2.imshow(img_name, opening)
#    cv2.waitKey(0)

    object_pixels = {
        "blue": blue_object_pixels,
        "orange": orange_object_pixels,
        "green": green_object_pixels,
        "pink": pink_object_pixels,
        "yellow": yellow_object_pixels
    }

    img = np.zeros([img_height, img_width, 3], dtype=np.uint8)

    img.fill(0)

    # THIS WANTS BGR!
    for key, val in object_pixels.items():
        if(key == "blue"):
            color = [255, 0, 0]
        if key == "green":
            color = [0, 255, 0]
        if key == "pink":
            color = [202, 6, 255]
        if key == "orange":
            color = [4, 120, 255]
        if key == "yellow":
            color = [0, 245, 252]
        if(len(val) == 0):
            continue
            #        print(o)
        for o in val:
            img[o[1], o[0]] = color
    # img[o[0], o[1]] = img_rgb[o[0], o[1]]
    Path("../tmp").mkdir(parents=True, exist_ok=True)
    cv2.imwrite("../tmp/IdentifiedObject.jpg", img)
    return object_pixels


def analyze_object(object_pixels):
    mean_dict = {}
    for key, val in object_pixels.items():
        if len(val) == 0:
            continue
 #       for v in val:
        meanPosition = (np.rint(np.mean(val, axis=0))).astype(int)
        mean_dict.update({key: meanPosition})

    return mean_dict

def save_values_as_xlsx(path, file_name, global_dict):
    import pandas as pd
    with open(path + "/" + file_name, "w") as text_file:
        for k,v in global_dict.items():
            text_file.write(k+": ")
            smallest_x = 1000000
            greatest_x = 0
            smallest_y = 1000000
            greatest_y = 0
            for v_ in v:
                if v_[0] < smallest_x:
                    smallest_x = v_[0]
                if v_[0] > greatest_x:
                    greatest_x = v_[0]
                if v_[1] < smallest_y:
                    smallest_y = v_[1]
                if v_[1] > greatest_y:
                    greatest_y = v_[1]
                text_file.write(str(v_))

            text_file.write(":::: ("+str(smallest_x)+", "+str(smallest_y)+") to ("+str(greatest_x)+", "+str(greatest_y)+")")
            text_file.write("\n")


def start_analysis_routine(path_lime_results_optimal, scenario):
    LIME_positive_results=path_lime_results_optimal+"/bw/good/"
    images = []
    img_size = get_image_size(LIME_positive_results)
    img_height = img_size[1]
    img_width = img_size[0]

    # read in all images in a given folder and store them in the array "images"
    for filename in os.listdir(LIME_positive_results):
        images.append((skimage.io.imread(LIME_positive_results + filename), filename))

    #    print("added "+ filename)

    img = np.zeros([img_height, img_width, 3], dtype=np.uint8)
    img.fill(0)
    image_names = []
    positions = []

    global_dict = {}

    for image in images:
        # object_pixels contains all red pixels that refer to an object
 #       img_rgb = cv2.cvtColor(image[0], cv2.COLOR_BGR2RGB)
        #        cv2.imshow('BGR Image', img_rgb)
        #        cv2.waitKey(0)
        img_rgb = cv2.rotate(image[0], cv2.ROTATE_90_COUNTERCLOCKWISE)
        #        cv2.imshow('RGB Image', img_rgb)
        #        cv2.waitKey(0)

        object_pixels = find_objects(image[1], img_rgb, img_width, img_height)
        image_names.append(image[1])

        res_dict = analyze_object(object_pixels)
        for key, val in res_dict.items():
            if key in global_dict:
                #if np.any(np.all(val == global_dict[key],  axis=1)):
                #    continue
                # check if 9er neighbood is already contained
                # TODO => lieber sortieren und von der mitte aus dann maske drueber legen
                neighbor_mask = [-2, -1, 0, 1, 2]
                is_in_neighbor = False
                for n in neighbor_mask:
                    for n_ in neighbor_mask:
                        val_ = copy.deepcopy(val)
                        val_[0] = val_[0]+n
                        val_[1] = val_[1]+n_
                        if np.any(np.all(val_ == global_dict[key], axis=1)):
                            is_in_neighbor = True
                            break
                    if is_in_neighbor:
                        break
                if is_in_neighbor:
                    continue
                global_dict[key].append(val)
 #               global_dict[key] = global_dict[key], val
            else:
                global_dict[key] = [val]

    print("ready")
    print(global_dict)
    # im = Image.fromarray(img)
    # im.save("recommend.jpg")
    # we assume that the found any criteria that can say which objects are "similar"
    # perhaps we have to make something like an object recognition here or that we assume that all objects that possibly
    # take part at the scene are identifyable by one feature, e.g. the color or the Shape
    # in our case we assume that we know this because we only have one object in each LIME pic


    save_values_as_xlsx(path_lime_results_optimal, scenario+'_results.txt', global_dict)


