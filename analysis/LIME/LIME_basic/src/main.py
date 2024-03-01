# Step 1: Train a CNN with labelled image data. The trained CNN is stored in "model"
# Step 2: Make local explanations of the model's decisions regarding positive labelled images with LIME
# Step 3: Make a global explanation across all local explanations by analyzing all LIME images regarding the predefined
# features (e.g., size, shape, color, position)

import os

from train_cnn import start_training, get_image_size
import tensorflow as tf
from explain_images import use_lime
from analyze_explanations import start_analysis_routine

from pathlib import Path

current_dir = os.getcwd()

scenario = "scenario2"
scenario_path = scenario+'/scenario2_w1000_images'
#scenario_path = scenario+'/scenario1_bghalf_w1000_images'


# Path to train and test directory
input_data_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))))+'/data_generator/image_data/images_basic/generated_data/'+scenario_path))
# Path to positive labelled input data
input_data_path_positive = os.path.join(os.path.abspath(input_data_path+'/good'))
#input_data_path_positive = os.path.join('../lime_results/'+scenario_path+'/lel')
print(input_data_path)
print(input_data_path_positive)
# Path where the LIME results should be stored in step 2
Path('../lime_results/'+scenario).mkdir(parents=True, exist_ok=True)
path_lime_results = os.path.join('../lime_results/'+scenario_path)

# Step 1
#model = start_training(input_data_path)
#Path(path_lime_results + "/model").mkdir(parents=True, exist_ok=True)
#model.save(path_lime_results + "/model")
#model = tf.keras.models.load_model(path_lime_results + "/model")


# Step 2
#path_lime_results_positive = use_lime(input_data_path_positive, model, path_lime_results)

# Step 3
path_lime_results_positive = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))))+'/analysis/LIME/LIME_basic/lime_results/scenario2/analysetest/'))
start_analysis_routine(path_lime_results_positive)


