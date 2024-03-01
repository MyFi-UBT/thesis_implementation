# Step 1: Train a CNN with labelled image data. The trained CNN is stored in "model"
# Step 2: Make local explanations of the model's decisions regarding positive labelled images with LIME
# Step 3: Make a global explanation across all local explanations by analyzing all LIME images regarding the predefined
# features (e.g., size, shape, color, position)

import os

from src.analyze_explanations_robotic import start_analysis_routine
from train_cnn_robotic import start_training, get_image_size
from explain_images_robotic_ownseg import use_lime
from pathlib import Path
import tensorflow as tf
import pandas as pd


#def retrieve_metadata(super_path):
#    metadata_generator = pd.read_csv(super_path + "/metadata_generator.csv", sep=",", index_col=0)
#    metadata_lime = pd.read_csv(super_path + "/metadata_lime.csv", index_col=0, sep=",")
#    frames = [metadata_generator, metadata_lime]
#    metadata = pd.concat(frames, axis=1)
#    return metadata


def run_lime(model, super_path, path_lime_results, n_boundaries, num_samples, segmentation_fn=None, background_image_path = None):
    # Set up LIME
    input_data_path_positive = os.path.join(super_path + '/good')  # Path to positive labelled input data
    csv_path = os.path.join(super_path + '/csv_files/good')  # path, where the image information about objects is stored
    # objects_path is needed for calculating the accuracy on lime (changes with different object_sizes)

    # segmentation_fn = {'name': metadata.loc[0, 'segmentation_algo'], 'segment_size': metadata.loc[0, 'segment_size']}
    # path_lime_results_positive, pic_metrics, mean_metrics = use_lime(input_data_path_positive, model, path_lime_results,
    #                                                                  csv_path, objects_path, n_lime_images,
    #                                                                  segmentation=segmentation_fn)

    """Generates explanation images.


           Args:
               input_data_path_positive: the path of the positive labelled images which will be explained by LIME
               model: the trained model
               path_lime_results: the path where the LIME results should be stored to
               csv_path: TODO
               objects_path: the path of the images showing the objects that are in the scene. This serves for the 
               validation/metric step of the LIME results
               n_lime_images: the number of images that should be explained => not necessary for us
               n_boundaries: the number of objects (= contours) that should be highlighted in a LIME image
               num_samples: the number of flickenteppich-images LIME should produce
               segmentation: segmentation algorithm, if None is selected, the basic version of Lime is used, 
               i.e. quickshift
    """
    path_lime_results_positive, pic_metrics, mean_metrics = use_lime(input_data_path_positive, model, path_lime_results,
                                                                     csv_path, n_boundaries, num_samples,
                                                                     segmentation=segmentation_fn, background_image_path= background_image_path)

    return mean_metrics

# default run =>  so many object as may take part in the scene: n_boundaries=8
def default_run(model, input_data_path, path_lime_results_default, scenario):
    if scenario == "scenario1":
        run_lime(model=model, super_path=input_data_path, path_lime_results=path_lime_results_default, n_boundaries=8, num_samples=1000)
    if scenario == "scenario2":
        run_lime(model=model, super_path=input_data_path, path_lime_results=path_lime_results_default,
                                n_boundaries=7, num_samples=1000)


# optimized run
def optimized_run(model, input_data_path, path_lime_results_optimal, background_image_path, scenario):
    if scenario == "scenario1":
        segmentation_fn = {'name': "squares_objectfilter_old", 'segment_size': 100}
        run_lime(model=model, super_path=input_data_path, path_lime_results=path_lime_results_optimal, n_boundaries=1, num_samples=1000, segmentation_fn=segmentation_fn, background_image_path = background_image_path)
    if scenario == "scenario2":
        segmentation_fn = {'name': "squares_objectfilter_old", 'segment_size': 10}
        run_lime(model=model, super_path=input_data_path, path_lime_results=path_lime_results_optimal, n_boundaries=3, num_samples=1000, segmentation_fn=segmentation_fn,
                 background_image_path=background_image_path)

# determine the scenario, i.e., scenario1 or scenario2
scenario = "scenario2"
# determine if the default configuration should be used or the optimized one
# default = True loads the default config., default = False load the optimized config.
default = False

# Path to train and test directory
input_data_path = os.path.join('../../../../data_generator/image_data/images_robotics/generated_data/'+scenario)
Path(input_data_path).mkdir(parents=True, exist_ok=True)
# Path to positive labelled input data
input_data_path_positive = os.path.join('../../../../data_generator/image_data/images_robotics/generated_data/'+scenario+'/good')
# Path where the LIME results should be stored in step 2
path_lime_results_default = os.path.join('../lime_results/'+scenario+'/default')
Path(path_lime_results_default).mkdir(parents=True, exist_ok=True)
path_lime_results_optimal = os.path.join('../lime_results/'+scenario+'/optimized')
Path(path_lime_results_optimal).mkdir(parents=True, exist_ok=True)
model_saving_path = os.path.join('../lime_results/'+scenario+'/model')
Path(model_saving_path).mkdir(parents=True, exist_ok=True)

# path to background image
background_image_path = '../../../../data_generator/image_data/images_robotics/raw_data/original_mat_cut.png'

# Either create new model or load an existing trained model
model = start_training(input_data_path, model_saving_path)
# model = tf.keras.models.load_model('../../robotic/use_case_1/model/model_14_4_2023--12_5_27')

# Explain model decisions (default or optimized)
if default is True:
    default_run(model, input_data_path, path_lime_results_default, scenario)
else:
    optimized_run(model, input_data_path, path_lime_results_optimal, background_image_path, scenario)


# Step 3
if default is True:
    start_analysis_routine(path_lime_results_default, scenario)
else:
    start_analysis_routine(path_lime_results_optimal, scenario)
