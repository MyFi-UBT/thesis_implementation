# *** This .py serves to explain images stored in /data by using a CNN trained in trainCnn.py ***
# *** Input:
#       1) Trained CNN ("model")
#       2) Positive labelled images in /data
# *** Output:
#       Images with local explanations of positive labelled images in /data
# the code is from here: https://towardsdatascience.com/interpreting-image-classification-model-with-lime-1e7064a2f2e5

import numpy as np
import skimage.transform
import skimage.io
from tensorflow.keras.preprocessing import image
from pathlib import Path
import cv2
from PIL import Image

from util.supp import get_image_size


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


def use_lime(input_data_path_positive, model, path_lime_results):
    import os

    img_size = get_image_size(input_data_path_positive)
    img_height = img_size[0]
    img_width = img_size[1]

    # if you only want to analyze a limited set of images (e.g., for test reasons) you can set the variable
    # "explainAllImages" to True and set a value in "upperLimit" referring to the number of images you want to analyze
    explainAllImages = True
    counter = 0
    upperLimit = 10

    for filename in os.listdir(input_data_path_positive):
        if (explainAllImages == False) and (counter == upperLimit):
            break
        counter = counter + 1

        i = input_data_path_positive + "/" + filename
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
            from lime import lime_image

            explainer = lime_image.LimeImageExplainer()
            explanation = explainer.explain_instance(images[0].astype('double'), model.predict,
                                                     top_labels=2, hide_color=0, num_samples=1000)

            from skimage.segmentation import mark_boundaries

            #bw
            temp_1, mask_1 = explanation.get_image_and_mask(explanation.top_labels[0], positive_only=True,
                                                            num_features=2, hide_rest=True)
            # rg
            temp_2, mask_2 = explanation.get_image_and_mask(explanation.top_labels[0], positive_only=False,
                                                            num_features=2, hide_rest=False)

            import matplotlib.pyplot as plt

            # get only the file name, e.g., "data_10234"
            filename_without_datatype = str(filename).split(".")[0]

            # only relevant parts are kept colored, the rest is black
            fig = mark_boundaries(temp_1, mask_1)

#            fig = cv2.cvtColor(fig, cv2.COLOR_BGR2RGB)
#            fig = 255 * fig

#            cv2.imwrite(path_lime_results + '/bw/good/' + filename_without_datatype + '_pred_' + str(prediction) + '_' + str(
#                    pct) + '_bw.png', fig)

#            fig.savefig(path_lime_results + '/bw/good/' + filename_without_datatype + '_pred_' + str(prediction) + '_' + str(pct))
            fig2 = Image.fromarray((fig * 255).astype(np.uint8))
            Path(path_lime_results + '/local_explanations').mkdir(parents=True, exist_ok=True)
            fig2.save(path_lime_results + '/local_explanations/' + filename_without_datatype + '_pred_' + str(prediction) + '_' + str(pct) + '_bw.png')

#            fig.show()
#            skimage.io.imsave(
#                path_lime_results + '/bw/good/' + filename_without_datatype + '_pred_' + str(prediction) + '_' + str(
#                    pct) + '_bw.jpg', fig)

            # paint irrelevant parts red, relevant parts green, other parts are preserved as in the original
            # (note: if the object was originally red, the relevant parts will appear yellow since color values are added)
#            fig2 = mark_boundaries(temp_2, mask_2)
#            Path(path_lime_results + '/rg/good').mkdir(parents=True, exist_ok=True)
#            skimage.io.imsave(
#                path_lime_results + '/rg/good/' + filename_without_datatype + '_pred_' + str(prediction) + '_' + str(
#                    pct) + '_rg.jpg', fig2)

    return path_lime_results + '/local_explanations/'