# *** This .py serves to explain images stored in /data by using a CNN trained in trainCnn.py ***
# *** Input:
#       1) Trained CNN ("model")
#       2) Positive labelled images in /data
# *** Output:
#       Images with local explanations of positive labelled images in /data
# the code is from here: https://towardsdatascience.com/interpreting-image-classification-model-with-lime-1e7064a2f2e5

import numpy as np
import re
import json
import skimage.transform
import skimage.io
from skimage import measure
from tensorflow.keras.preprocessing import image
from lime.wrappers.scikit_image import SegmentationAlgorithm
from pathlib import Path
from lime import lime_image
from PIL import Image, ImageDraw, ImageFilter
import cv2
import matplotlib.pyplot as plt
from skimage.segmentation import mark_boundaries
import random
import tensorflow as tf

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

objects = []


def get_image_size(input_data_path):
    import os
    import skimage.io
    i = input_data_path + "/" + (os.listdir(input_data_path)[0])
    img = skimage.io.imread(i)
    return img.shape


# segmentation_algorithm = {'name':'squares_objectfilter','n_segments':50}

def squares_objectfilter_old(images, segment_size):
    # Segmentate the background with slic algorithm
    segment = skimage.segmentation.slic(images, compactness=10, n_segments=segment_size)
    #    plt.imshow(segment)
    #    plt.axis('off')
    #    plt.show()
    #    grid_size = segment_size / 50
    #    max = images.shape[1] / (50 * grid_size)
    #    for i in range(images.shape[0]):
    #        for j in range(images.shape[1]):
    #           segment[i][j] = round(i / (10 + 50 * grid_size)) * max + round(j / (50 * grid_size))

    #    plt.imshow(segment)
    #    plt.axis('off')
    #    plt.show()

    max_class = np.max(segment)
    # convert image to suitable form for contour algorithm
    data = 255 * images
    img = data.astype(np.uint8)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # mask1 should only have the objects (background should not be visible in mask1)
#    cv2.imshow("hsv", hsv)
#    cv2.waitKey()
    mask1 = cv2.inRange(hsv, (0, 200, 40), (255, 255, 255))
#    cv2.imshow("mask1", mask1)
#    cv2.waitKey()

    ret, thresh = cv2.threshold(mask1, 150, 255, cv2.THRESH_BINARY)

    # --- if use case 2:
    # first remove the circle coming from the robot on the right by "opening"
    # then fill in holes in the machine parts by "closing"
#    kernel = np.ones((2, 2), np.uint8)
#    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
#    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

#    cv2.imshow("objects",thresh)
#    cv2.waitKey()
    # find contours in the filtered image
    kernel = np.ones((2, 2), np.uint8)
    thresh = cv2.erode(thresh, kernel)
#    cv2.imshow("objects",thresh)
#    cv2.waitKey()
    contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

#    col = 0
#    for contour in contours:
#        cv2.drawContours(img, contour, -1, (0, col, 0), 3)
#        col = col+50
#    plt.figure()
#    plt.imshow(img)

    image_copy = img.copy()

    counter = max_class + 1
    for c in contours:
        # c should be the objects from the image
        area = cv2.contourArea(c)
        if area > 300:
            # extracting the object, that fits to the contour and add the object with own class number to segment
            blank_image = np.zeros(img.shape, np.uint8)
            cv2.fillPoly(blank_image, pts=[c], color=(255, 255, 255))
            gray = cv2.cvtColor(blank_image, cv2.COLOR_BGR2GRAY)
            thresh = 1
            im_bw = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)[1]
            im_bw = im_bw / 255
            im_bw = im_bw * counter
            box = cv2.boundingRect(c)
            for i in range(box[1], box[1] + box[3]):
                for j in range(box[0], box[0] + box[2]):
                    if (im_bw[i][j] != 0):
                        segment[i][j] = im_bw[i][j]
            counter = counter + 1

            # segment stores the different detected segments in the image using (1) slic algorithm for segmenting the background
    # after applying slic algorithm, each detected object gets its own class
#    plt.imshow(segment)
#    plt.axis('off')
#    plt.show()
    return segment


def squares_objectfilter(images, segment_size):
    # Segmentate the background with slic algorithm
    #     segment = skimage.segmentation.slic(images, compactness=0.01, n_segments=segment_size)
    #     segment = skimage.segmentation.felzenszwalb(images, scale = 0.001, min_size= 5, sigma=0)
    random_seed = random.randrange(1, 1000)
    segment = skimage.segmentation.quickshift(images, kernel_size=10, max_dist=50, ratio=0.9, random_seed=random_seed)
    #    plt.imshow(segment)
    #    plt.axis('off')
    #    plt.show()

    data = 255 * images
    img = data.astype(np.uint8)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # mask1 should only have the objects (background should not be visible in mask1)
    mask1 = cv2.inRange(hsv, (0, 100, 40), (255, 255, 255))
    ret, thresh = cv2.threshold(mask1, 150, 255, cv2.THRESH_BINARY)
    #    cv2.imshow("objects",thresh)
    #    cv2.waitKey()
    # find contours in the filtered image
    contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

    #    for contour in contours:
    #        cv2.drawContours(img, contour, -1, (0, 255, 0), 3)
    #   plt.figure()
    #    plt.imshow(img)

    return segment


def segmentate(images):
    if (segmentation_algorithm['name'] == 'squares_objectfilter'):
        return squares_objectfilter(images, segmentation_algorithm['segment_size'])
    if (segmentation_algorithm['name'] == 'squares_objectfilter_old'):
        return squares_objectfilter_old(images, segmentation_algorithm['segment_size'])

    return


def get_lime_accuracy(mask, filename, csv_path):
    # get the csv file storing all objects, that should be detected by lime
    s = re.findall(r'\d+', filename)
    arr_metadata = np.loadtxt(csv_path + '/csv_' + str(s[0]) + '.csv', delimiter=',')

    # blank_image will be a matrix. Each matrix[i][j] has information about the image[i][j].
    # if matrix[i][j]=0, it means that the image[i][j] is a background pixel,
    # if matrix[i][j]=1, it means that pixel at image[i][j] is a pixel for object 1,...
    blank_image = np.zeros(mask.shape, np.uint8)
    object_used = [0] * 15
    # pixel_counter contains the appereances of each object and the background in the input image for lime
    pixel_counter = {0: 0}
    # mask_counter contains the appereances of each object and the background in the lime output
    mask_counter = {0: 0}
    for i in range(arr_metadata.shape[0]):
        img_id = int(arr_metadata[i][0])
        x0 = int(arr_metadata[i][1])
        y0 = int(arr_metadata[i][2])
        img = objects[img_id - 1]
        object_used[img_id - 1] = object_used[img_id - 1] + 1
        if (object_used[img_id - 1] > 1):
            offset = 100 * (object_used[img_id - 1] - 1)
            img = img + offset
            arr_metadata[i][0] = img_id + offset
            pixel_counter[(img_id + offset)] = 0
            mask_counter[(img_id + offset)] = 0
        else:
            pixel_counter[img_id] = 0
            mask_counter[img_id] = 0
        blank_image[y0:y0 + img.shape[0], x0:x0 + img.shape[1]] = img

    for i in range(blank_image.shape[0]):
        for j in range(blank_image.shape[1]):
            px_id = blank_image[i][j]
            pixel_counter[px_id] = pixel_counter[px_id] + 1
            if mask[i][j] == 1:
                mask_counter[px_id] = mask_counter[px_id] + 1

    # rel_cover contains for each object and background the percentage of cover in the output from lime
    # rel_cover = mask_counter/pixel_counter
    # rel_cover={x:float(mask_counter[x])/pixel_counter[x] for x in pixel_counter}
    # how many of the objects with conditions are represented in lime
    true_pos = 0
    false_pos = 0
    true_neg = 0
    false_neg = 0

    true_pos_area_sum = 0
    true_pos_cover_sum = 0
    true_neg_area_sum = 0
    true_neg_cover_sum = 0
    object_stats = []
    # for each object store the calculated information from pixel_counter,mask_counter and rel_cover
    for i in range(arr_metadata.shape[0]):
        id = int(arr_metadata[i][0])
        rel_cover = mask_counter[id] / pixel_counter[id]
        stats = {'id': id, 'area': pixel_counter[id], 'lime_cover_area': mask_counter[id], 'rel_cover': rel_cover}
        object_stats.append(stats)
        if arr_metadata[i][3] == True:
            true_pos_area_sum = true_pos_area_sum + pixel_counter[id]
            true_pos_cover_sum = true_pos_cover_sum + mask_counter[id]
            if rel_cover > 0.50:
                # if limes covers the object and the object is relevant
                true_pos = true_pos + 1
            else:
                # if lime covers the object but the object is irrelevant
                false_neg = false_neg + 1
        else:
            true_neg_area_sum = true_neg_area_sum + pixel_counter[id]
            true_neg_cover_sum = true_neg_cover_sum + mask_counter[id]
            if rel_cover > 0.50:
                # if limes doesn't cover the object but the object is relevant
                false_pos = false_pos + 1
            else:
                # if lime doesn't cover the object and the object is irrelevant
                true_neg = true_neg + 1

    true_pos_rel_cover = -1
    if true_pos_area_sum > 0:
        true_pos_rel_cover = true_pos_cover_sum / true_pos_area_sum
    true_neg_rel_cover = -1
    if true_neg_area_sum > 0:
        true_neg_rel_cover = true_neg_cover_sum / true_neg_area_sum
    # true_pos_cover_sum should be 100% (lime should cover each object),
    # true_neg_cover_sum, should be 0%(lime should not cover an irrelevant(neg) object)
    object_info = {'true_pos_area_sum': true_pos_area_sum, 'true_pos_cover_sum': true_pos_cover_sum,
                   'true_pos_rel_cover': true_pos_rel_cover,
                   'true_neg_area_sum': true_neg_area_sum, 'true_neg_cover_sum': true_neg_cover_sum,
                   'true_neg_rel_cover': true_neg_rel_cover,
                   'object_stats': object_stats}

    background_stats = {'area': pixel_counter[0], 'lime_cover_area': mask_counter[0],
                        'rel_cover': mask_counter[0] / pixel_counter[0]}

    stats = {'#objects': arr_metadata.shape[0], '#pos': true_pos + false_neg, '#neg': false_pos + true_neg,
             '#true_pos': true_pos, '#false_pos': false_pos, '#true_neg': true_neg, '#false_neg': false_neg,
             'object_stats': object_info, 'background_stats': background_stats}
    return stats


def load_objects(objects_path):
    # load each object as image
    for i in range(1, 2):
        img = cv2.imread(objects_path + '/' + str(i) + '.png')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = 1
        im_bw = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)[1]
        im_bw = im_bw / 255
        im_bw = im_bw * i
        objects.append(im_bw)


def read_and_transform_img(url, input_data_path_positive):
    import os
    img = skimage.io.imread(url)

    img_size = get_image_size(input_data_path_positive)
    img_height = img_size[0]
    img_width = img_size[1]

    img = skimage.transform.resize(img, (img_height, img_width, 3))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)

    return img


def get_mean_metrics(metrics):
    mean_metrics = {}
    mean_metrics['pictures_ranking'] = -1
    mean_metrics['#true_pos_mean'] = -1
    mean_metrics['#false_pos_mean'] = -1
    mean_metrics['#true_neg_mean'] = -1
    mean_metrics['#false_neg_mean'] = -1
    mean_metrics['true_pos_rel_cover_mean'] = -1
    mean_metrics['true_neg_rel_cover_mean'] = -1
    mean_metrics['rel_cover_background_mean'] = -1
    if (len(metrics) > 0):
        correct_objects = [0] * (metrics[0]['#objects'] + 1)
        true_pos_mean = 0
        false_pos_mean = 0
        true_neg_mean = 0
        false_neg_mean = 0
        true_pos_rel_cover_mean = 0
        true_neg_rel_cover_mean = 0
        rel_cover_background_mean = 0
        for metric in metrics:
            n_correct_objects = metric['#true_pos'] + metric['#true_neg']
            correct_objects[n_correct_objects] = correct_objects[n_correct_objects] + 1
            true_pos_mean = true_pos_mean + metric['#true_pos']
            false_pos_mean = false_pos_mean + metric['#false_pos']
            true_neg_mean = true_neg_mean + metric['#true_neg']
            false_neg_mean = false_neg_mean + metric['#false_neg']
            true_pos_rel_cover_mean = true_pos_rel_cover_mean + metric['object_stats']['true_pos_rel_cover']
            true_neg_rel_cover_mean = true_neg_rel_cover_mean + metric['object_stats']['true_neg_rel_cover']
            rel_cover_background_mean = rel_cover_background_mean + metric['background_stats']['rel_cover']
        mean_metrics['#true_pos_mean'] = true_pos_mean / len(metrics)
        mean_metrics['#false_pos_mean'] = false_pos_mean / len(metrics)
        mean_metrics['#true_neg_mean'] = true_neg_mean / len(metrics)
        mean_metrics['#false_neg_mean'] = false_neg_mean / len(metrics)
        mean_metrics['true_pos_rel_cover_mean'] = true_pos_rel_cover_mean / len(metrics)
        mean_metrics['true_neg_rel_cover_mean'] = true_neg_rel_cover_mean / len(metrics)
        mean_metrics['rel_cover_background_mean'] = rel_cover_background_mean / len(metrics)
        mean_metrics['pictures_ranking'] = correct_objects
    return mean_metrics


def use_lime(input_data_path_positive, model, path_lime_results, csv_path, n_boundaries,
             num_samples, segmentation, background_image_path = None):
    import os
    img_size = get_image_size(input_data_path_positive)
    img_height = img_size[0]
    img_width = img_size[1]
    global segmentation_algorithm
    segmentation_algorithm = segmentation

    pic_metrics = []

    if background_image_path is not None:
       background_image = read_and_transform_img(background_image_path, input_data_path_positive)[0]

    for filename in os.listdir(input_data_path_positive):

        i = input_data_path_positive + "/" + filename

        print("prediction for: " + str(filename))
        images = read_and_transform_img(i, input_data_path_positive)
        preds = model.predict(images)
        print(preds)
        prediction = np.argmax(preds)
        pct = np.max(preds)

        print("prediction for: " + str(filename))
        if prediction == 0:
            print('It\'s bad')
        elif prediction == 1:
            print('It\'s good!')
        else:
            print("I dont know what I am doing!")

        #  print(pct)

        # explain only positive examples values
        if prediction == 1:

            explainer = lime_image.LimeImageExplainer()

            if segmentation is None:
                explanation = explainer.explain_instance(images[0].astype('double'), model.predict, top_labels=2,
                                                         hide_color=0, num_samples=num_samples)
            else:
                explanation = explainer.explain_instance(images[0].astype('double'), model.predict,
                                                         top_labels=2, hide_color=0, num_samples=num_samples,
                                                         segmentation_fn=segmentate, background_image = background_image)
              

            #
            # find out, how many objects are in this image, this defines the number of features shown in lime
            # in this method, the segments are sorted by "trust" value and are cut off by num_features
            # bw
            temp_1, mask_1 = explanation.get_image_and_mask(explanation.top_labels[0], positive_only=True,
                                                            num_features=n_boundaries, hide_rest=True)
            # rg
            temp_2, mask_2 = explanation.get_image_and_mask(explanation.top_labels[0], positive_only=False,
                                                            num_features=n_boundaries, hide_rest=False)

            #            lime_accuracy = get_lime_accuracy(mask_1, filename, csv_path)
            #            pic_metrics.append(lime_accuracy)

            # get only the file name, e.g., "data_10234"
            filename_without_datatype = str(filename).split(".")[0]
            # print(arr_metadata.shape[0])
            # only relevant parts are kept colored, the rest is black
            fig = mark_boundaries(temp_1, mask_1)
            Path(path_lime_results + '/bw/good').mkdir(parents=True, exist_ok=True)
            skimage.io.imsave(
                path_lime_results + '/bw/good/' + filename_without_datatype + '_pred_' + str(prediction) + '_' + str(
                    pct) + '_bw.jpg', fig)

#            img = Image.open(i)
#            img.save(path_lime_results + '/bw/good/' + filename)

            # store lime accuracy data as json
            #            with open(path_lime_results + '/bw/good/' + filename + '.json', "w") as fp:
            #                json.dump(lime_accuracy, fp)

            # paint irrelevant parts red, relevant parts green, other parts are preserved as in the original
            # (note: if the object was originally red, the relevant parts will appear yellow since color values are added)
            fig2 = mark_boundaries(temp_2, mask_2)
            Path(path_lime_results + '/rg/good').mkdir(parents=True, exist_ok=True)
            skimage.io.imsave(
                path_lime_results + '/rg/good/' + filename_without_datatype + '_pred_' + str(prediction) + '_' + str(
                    pct) + '_rg.jpg', fig2)

    #  mean_metrics = get_mean_metrics(pic_metrics)
    return path_lime_results + '/bw/good/'
