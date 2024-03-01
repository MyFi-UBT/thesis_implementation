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
from util.supp import get_image_size
from pathlib import Path


def find_object(image, img_width, img_height, LIME_positive_results):

    # cv2.imshow('BGR Image', image)
    # cv2.waitKey(0)
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # cv2.imshow('RGB Image', img_rgb)
    # cv2.waitKey(0)
    # image is RGB now
    object_pixels = []
    for x in range(0, img_width):
        for y in range(0, img_height):

            p = img_rgb[y, x]

            if (p[0] == p[1] == p[2]):
                continue
            # object found (red, green or blue)
            else:
                if (p[0] > 150 and p[1] < 100 and p[2] < 100 or
                        p[0] < 100 and p[1] > 150 and p[2] < 100 or
                        p[0] < 100 and p[1] < 100 and p[2] > 150):
                    object_pixels.append((y, x))

    object_pixels = np.array(object_pixels)

    img = np.zeros([img_height, img_width, 3], dtype=np.uint8)

    img.fill(0)

    for o in object_pixels:
        #        print(o)
        img[o[0], o[1]] = [0, 255, 0]
        # img[o[0], o[1]] = img_rgb[o[0], o[1]]
    Path(LIME_positive_results+"/../tmp").mkdir(parents=True, exist_ok=True)
    cv2.imwrite(LIME_positive_results+"/../tmp/IdentifiedObject.jpg", img)
    return object_pixels


def analyze_object(object_pixels, new_img, black_image, orig_image, positions, sizes, shapes, colors,LIME_positive_results):

    changedimg, meanPosition = analyze_position(object_pixels, new_img, orig_image)
    black_image_with_object, meanPosition = analyze_position(object_pixels, black_image, orig_image)

    Path(LIME_positive_results+"/../tmp").mkdir(parents=True, exist_ok=True)
    cv2.imwrite(LIME_positive_results+"/../tmp/changedImgsingle.jpg", black_image_with_object)
    meanPos_x = int(meanPosition[1])
    meanPos_y = int(meanPosition[0])
    print("Position (x, y): " + str(meanPos_x) + ", " + str(meanPos_y))
    positions.append((meanPos_x, meanPos_y))

    size_x, size_y = analyze_size(object_pixels)
    print("Size (Width/Height): " + str(size_x) + ", " + str(size_y))
    sizes.append((size_x, size_y))

    color = analyze_color(object_pixels, black_image_with_object)
    print("Color: " + color)
    colors.append(color)

    shape = analyze_shape(black_image_with_object,LIME_positive_results)
    print("Shape: " + shape)
    shapes.append(shape)

    return changedimg, positions, sizes, shapes, colors


def analyze_position(object_pixels, img, orig_image):
    # this visualizes all object_pixels in order to produce a picture for evaluation
    for o in object_pixels:
        img[(o[0], o[1])] = orig_image[(o[0], o[1])]

    meanPosition = np.mean(object_pixels, axis=0)
    img[(int(meanPosition[0])), int((meanPosition[1]))] = [255, 255, 255]
    return img, meanPosition


#  for pixels in object_pixels:

def analyze_size(object_pixels):
    smallestPix_x = object_pixels[0][1]
    smallestPix_y = object_pixels[0][0]
    greatestPix_x = object_pixels[0][1]
    greatestPix_y = object_pixels[0][0]

    for o in object_pixels:
        if (o[1] < smallestPix_x):
            smallestPix_x = o[1]
        if (o[0] < smallestPix_y):
            smallestPix_y = o[0]
        if (o[1] > greatestPix_x):
            greatestPix_x = o[1]
        if (o[0] > greatestPix_y):
            greatestPix_y = o[0]

    if(greatestPix_y - smallestPix_y > 400):
        print("hallop")
    return (greatestPix_x - smallestPix_x, greatestPix_y - smallestPix_y)


def analyze_shape(image,LIME_positive_results):
    # https://www.pyimagesearch.com/2016/02/08/opencv-shape-detection/
    from util.shape_detector import ShapeDetector
    resized = imutils.resize(image, width=300)
    ratio = image.shape[0] / float(resized.shape[0])
    # convert the resized image to grayscale, blur it slightly,
    # and threshold it
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.threshold(blurred, 10, 255, cv2.THRESH_BINARY)[1]
    Path(LIME_positive_results+"/../tmp").mkdir(parents=True, exist_ok=True)
    cv2.imwrite(LIME_positive_results+"/../tmp/thresh.jpg", thresh)
    # find contours in the thresholded image and initialize the
    # shape detector
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()
    # loop over the contours
    for c in cnts:
        # compute the center of the contour, then detect the name of the
        # shape using only the contour
        M = cv2.moments(c)
        if (M["m00"] == 0):
            continue;
        cX = int((M["m10"] / M["m00"]) * ratio)
        cY = int((M["m01"] / M["m00"]) * ratio)
        shape = sd.detect(c)
        # multiply the contour (x, y)-coordinates by the resize ratio,
        # then draw the contours and the name of the shape on the image
        c = c.astype("float")
        c *= ratio
        c = c.astype("int")
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 255, 255), 2)
        # show the output image
        # cv2.imshow("Image", image)
        # cv2.waitKey(0)
        return shape
    return ("undefined")


def analyze_color(object_pixels, image):
    redPart = 0
    greenPart = 0
    bluePart = 0
    undefinedCol = 0

    for o in object_pixels:
        p = image[o[0], o[1]]
        # still BGR !! DONT KNOW WHY
    if (p[0] > 150 and p[1] < 100 and p[2] < 100):
        bluePart = bluePart + 1
    elif (p[0] < 100 and p[1] > 150 and p[2] < 100):
        greenPart = greenPart + 1
    elif (p[0] < 100 and p[1] < 100 and p[2] > 150):
        redPart = redPart + 1
    else:
        undefinedCol = undefinedCol + 1
    if (redPart > greenPart and redPart > bluePart and redPart > undefinedCol):
        return "Red"
    if (greenPart > redPart and greenPart > bluePart and greenPart > undefinedCol):
        return "Green"
    if (bluePart > redPart and bluePart > greenPart and bluePart > undefinedCol):
        return "Blue"
    if (undefinedCol > redPart and undefinedCol > bluePart and undefinedCol > greenPart):
        return "Undefined Color"


def further_analyze_position(positions, img_width, img_height,LIME_positive_results):
    smallestPos_x = positions[0][0]
    smallestPos_y = positions[0][1]
    greatestPos_x = positions[0][0]
    greatestPos_y = positions[0][1]

    for p in positions:
        if (p[0] < smallestPos_x):
            smallestPos_x = p[0]
        if (p[1] < smallestPos_y):
            smallestPos_y = p[1]
        if (p[0] > greatestPos_x):
            greatestPos_x = p[0]
        if (p[1] > greatestPos_y):
            greatestPos_y = p[1]

    print("Smallest Position in x: " + str(smallestPos_x))
    print("Smallest Position in y: " + str(smallestPos_y))
    print("Greatest Position in x: " + str(greatestPos_x))
    print("Greatest Position in y: " + str(greatestPos_y))

    resimg = np.zeros([img_height, img_width, 3], dtype=np.uint8)
    resimg.fill(0)

    for x in range(smallestPos_x, greatestPos_x):
        for y in range(smallestPos_y, greatestPos_y):
            resimg[y, x] = [0, 255, 0]
    im2 = Image.fromarray(resimg)
    Path(LIME_positive_results+"/../tmp").mkdir(parents=True, exist_ok=True)
    im2.save(LIME_positive_results+"/../tmp/result.jpg")

def save_values_as_xlsx(path, file_name, image_names, positions, sizes, shapes, colors):
    import pandas as pd
    # Create a Pandas dataframe from some data.
    df = pd.DataFrame({
        'Image Names': image_names,
        'Positions': positions,
        'Sizes': sizes,
        'Shapes': shapes,
        'Colors': colors
    })

    Path(path).mkdir(parents=True, exist_ok=True)
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(path+"/"+file_name, engine='xlsxwriter')
    # Write the dataframe data to XlsxWriter. Turn off the default header and
    # index and skip one row to allow us to insert a user defined header.
    df.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False, index=False)

    # Get the xlsxwriter workbook and worksheet objects.
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

    # Get the dimensions of the dataframe.
    (max_row, max_col) = df.shape

    # Create a list of column headers, to use in add_table().
    column_settings = [{'header': column} for column in df.columns]

    # Add the Excel table structure. Pandas will add the data.
    worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})

    # Make the columns wider for clarity.
    worksheet.set_column(0, max_col - 1, 12)

    # Close the Pandas Excel writer and output the Excel file.
#    writer.save()
    writer._save()

def start_analysis_routine(LIME_positive_results):

    images = []
    img_size = get_image_size(LIME_positive_results)
    img_height = img_size[0]
    img_width = img_size[1]

    # read in all images in a given folder and store them in the array "images"
    for filename in os.listdir(LIME_positive_results):
        images.append((skimage.io.imread(LIME_positive_results + '/'+filename), filename))

    #    print("added "+ filename)

    img = np.zeros([img_height, img_width, 3], dtype=np.uint8)
    img.fill(0)

    image_names = []
    positions = []
    sizes = []
    shapes = []
    colors = []

    for image in images:
        # object_pixels contains all red pixels that refer to an object
        img_rgb = cv2.cvtColor(image[0], cv2.COLOR_BGR2RGB)
        # cv2.imshow('BGR Image', img_rgb)
        # cv2.waitKey(0)

        object_pixels = find_object(img_rgb, img_width, img_height, LIME_positive_results)
        print("-----------------------analyze_object------------------")
        print("Information for image: " + image[1])
        image_names.append(image[1])
        black_img = np.zeros([img_height, img_width, 3], dtype=np.uint8)
        black_img.fill(0)
        if (object_pixels.size != 0):
            img, positions, sizes, shapes, colors = analyze_object(object_pixels, img, black_img, img_rgb, positions,
                                                                   sizes,
                                                                   shapes, colors,LIME_positive_results)
        else:
            print("empty img")
    # im = Image.fromarray(img)
    # im.save("recommend.jpg")
    # we assume that the found any criteria that can say which objects are "similar"
    # perhaps we have to make something like an object recognition here or that we assume that all objects that possibly
    # take part at the scene are identifyable by one feature, e.g. the color or the Shape
    # in our case we assume that we know this because we only have one object in each LIME pic
    print("Image Names:")
    print(image_names)
    print("Positions:")
    print(set(positions))
    print("Sizes:")
    print(set(sizes))
    print("Shapes:")
    print(set(shapes))
    print("Colors:")
    print(set(colors))

    print("Number of images analyzed: " + str(len(image_names)))
    print("Number of positions analyzed: " + str(len(positions)))
    print("Number of sizes analyzed: " + str(len(sizes)))
    print("Number of shapes analyzed: " + str(len(shapes)))
    print("Number of colors analyzed: " + str(len(colors)))

#    further_analyze_position(positions, img_width, img_height,LIME_positive_results)

    output_file_path = LIME_positive_results+"/../aggregation_results_"+str(len(image_names))+"_.txt"
    with open(output_file_path, "w") as file:
        # Schreiben der Informationen in die Datei
        file.write("Image Names:\n")
        file.write(str(image_names) + "\n")
        file.write("Positions:\n")
        file.write(str(set(positions)) + "\n")
        file.write("Sizes:\n")
        file.write(str(set(sizes)) + "\n")
        file.write("Shapes:\n")
        file.write(str(set(shapes)) + "\n")
        file.write("Colors:\n")
        file.write(str(set(colors)) + "\n\n")

        file.write("Number of images analyzed: " + str(len(image_names)) + "\n")
        file.write("Number of positions analyzed: " + str(len(positions)) + "\n")
        file.write("Number of sizes analyzed: " + str(len(sizes)) + "\n")
        file.write("Number of shapes analyzed: " + str(len(shapes)) + "\n")
        file.write("Number of colors analyzed: " + str(len(colors)) + "\n")

    print("Die Daten wurden erfolgreich in die Datei geschrieben: " + output_file_path)

    save_values_as_xlsx(LIME_positive_results+"/../", 'segmentation_results_'+str(len(image_names))+'_.xlsx', image_names, positions, sizes, shapes, colors)
