def get_image_size(input_data_path):
    import os
    import skimage.io

    print("hier")
    print(input_data_path)
    i = os.path.abspath(input_data_path + "/" + (os.listdir(input_data_path)[0]))
    img = skimage.io.imread(i)
    return img.shape
