import random
from pathlib import Path

# define the number of data which should be generated
from src import paste_image_uc2

def start_generation(rangeVal, result_path, raw_data_path, label):
    for x in range(rangeVal):
        background_image = raw_data_path+'original_mat_cut.png'
        object_images = []
        data_type = "jpg"
        nr_of_objects_upper_area = 0
        # missing_images is only needed for label = 0 and is used to ensure that always one blue, orange and green object is visible in the scene
        missing_images = []

        # object that MUST take place in region A good case (CAUTION: image is reversed):
        # goal: from robotic: blue, orange, green

        # order here is: green, orange, blue since the image is painted from left to right
        if label == 1:
            object_images.append(raw_data_path+'6_2.png')
            object_images.append(raw_data_path+'7_2.png')
            object_images.append(raw_data_path+'5_2.png')
            nr_of_objects_upper_area = len(object_images)
        # bad case
        # repeat shuffeling until the objects do not longer have the order: 6-7-5:
        if label == 0:
            image_array = [raw_data_path+'6_2.png', raw_data_path+'7_2.png',
                           raw_data_path+'5_2.png']

            for i in range(3):
                randNr = random.randrange(0, 2)
                if randNr == 1:
                    object_images.append(image_array[i])
                else:
                    missing_images.append(image_array[i])

            random.shuffle(object_images)
            if len(object_images) == 3:
                while object_images[0] == raw_data_path+'6_2.png' and object_images[1] == raw_data_path+'7_2.png' and object_images[2] == raw_data_path+'5_2.png':
                    random.shuffle(object_images)
            nr_of_objects_upper_area = len(object_images)
            for i in missing_images:
                object_images.append(i)

        # random objects taking place in region B (0 to 4 objects)
        randChoice = random.randrange(0, (5 - len(missing_images)))
        for r in range(randChoice):
            randNr = random.randrange(1, 6)
            if randNr == 1:
                object_images.append(raw_data_path+'5_2.png')
            if randNr == 2:
                object_images.append(raw_data_path+'6_2.png')
            if randNr == 3:
                object_images.append(raw_data_path+'7_2.png')
            if randNr == 4:
                object_images.append(raw_data_path+'8_2.png')
            if randNr == 5:
                object_images.append(raw_data_path+'9_2.png')

        # check if given path where the generated data will be written to does already exist and if not; create it
        Path(result_path).mkdir(parents=True, exist_ok=True)

        while not paste_image_uc2.create_random_positions(x, background_image, object_images, result_path, label, data_type, nr_of_objects_upper_area):
            print ("I repeat this iteration.")

    print("Done with image generation.")

# define the number of data which should be generated
rangeVal = 5000
# define if you want to create positive or negative examples.
label = 1
# define the path and folders where the generated data should be stored. Depending on the label, appropriate
# subfolder are generated implicitly.
result_path = '../generated_data/scenario2'
# define the path of the input data
raw_data_path = "../raw_data/"
start_generation(rangeVal, result_path, raw_data_path, label)