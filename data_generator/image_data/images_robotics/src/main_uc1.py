from pathlib import Path

from src import paste_image_uc1


def start_generation(rangeVal, result_path, raw_data_path, label):
    for x in range(rangeVal):
        # TODO: Determine label and type here!
        data_type = "png"
        object_images = []
        # which image has to be painted could either be computed randomly or decided manually
        # in case you want to select them randomly, activate the randrange part
        # randNr = randrange(1,4)

        if label == 1:
            # Position 1 determines the object that is placed on the circuit board
            objectDataPath = raw_data_path + '6_2_shortened_breiter_rand.png'
            objectDataPath2 = raw_data_path + '8_2.png'
            objectDataPath22 = raw_data_path + '9_2.png'
        else:
            # do this two times: once with 9_2 as first element and once with 8_2 as first element
            objectDataPath = raw_data_path + '8_2_shortened_breiter_rand.png'
            objectDataPath2 = raw_data_path + '6_2.png'
            objectDataPath22 = raw_data_path + '9_2.png'

        # in our 4-object-case we want 2 circles and 2 rectangles, for this reason we add each twice
        # object_images.append(objectDataPath)
        object_images.append(objectDataPath2)
        object_images.append(objectDataPath22)

        # which background will be selected could either be computed randomly or decided manually
        # in case you want to select it randomly, activate the randrange part
        # bgRandnr = randrange(1,4)
        bgRandnr = 1
        background_image = ""
        if bgRandnr == 1:
            background_image = raw_data_path + "original_mat_with_cb_breiter_rand.png"
            # background_image = '../raw_data/paper_data/mat_w_cb.jpg'
        elif bgRandnr == 2:
            background_image = '../raw_data/grass.jpg'
        else:
            background_image = '../raw_data/waves.jpg'

        # check if given path where the generated data will be written to does already exist and if not; create it
        Path(result_path).mkdir(parents=True, exist_ok=True)
        # first we paste the object on the circuit board
        background_image_fixed = paste_image_uc1.create_fixed_position(x, background_image, objectDataPath)
        background_image_fixed.save("tmp.png")
        background_image_fixed_path = 'tmp.png'

        paste_image_uc1.create_random_positions(x, background_image_fixed_path, object_images, result_path, label,
                                                data_type)

    print("Done with image generation.")


# define the number of data which should be generated
rangeVal = 666
# define if you want to create positive or negative examples.
label = 0
# define the path and folders where the generated data should be stored. Depending on the label, appropriate
# subfolder are generated implicitly.
result_path = '../generated_data/scenario1'
# define the path of the input data
raw_data_path = "../raw_data/"
start_generation(rangeVal, result_path, raw_data_path, label)