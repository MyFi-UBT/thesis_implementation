import os

import pandas as pd
from pathlib import Path
import random

from pandas._typing import Axes


def create_noise(obj_feature, noise_size):
    if len(obj_feature) == 2:
        random_x = random.randint(obj_feature[0]-noise_size, obj_feature[0]+noise_size)
        random_y = random.randint(obj_feature[1]-noise_size, obj_feature[1]+noise_size)
        obj_feature = random_x, random_y
    return obj_feature


def compute_random_position(scene_width, scene_height, obj):
    obj_width = obj.size[0]
    obj_height = obj.size[1]

    valid_x_min = round(obj_width / 2)
    valid_x_max = round(scene_width - (obj_width / 2))
    valid_y_min = round(obj_height / 2)
    valid_y_max = round(scene_height - (obj_height / 2))
    random_x = random.randint(valid_x_min, valid_x_max)
    random_y = random.randint(valid_y_min, valid_y_max)
    return random_x, random_y

def compute_random_positions_without_intersections(scene_width, scene_height, obj_array):

    tmp_objs = []


    counter = 1
    for obj in obj_array:
#        print("I consider " + obj.shape)
#        print("entry: " + str(counter))
        not_yet_found = False
        obj_width = obj.size[0]
        obj_height = obj.size[1]
        valid_x_min = round(obj_width / 2)
        valid_x_max = round(scene_width - (obj_width / 2))
        valid_y_min = round(obj_height / 2)
        valid_y_max = round(scene_height - (obj_height / 2))

        if len(tmp_objs) == 0:
            random_x = random.randint(valid_x_min, valid_x_max)
            random_y = random.randint(valid_y_min, valid_y_max)
            obj.position = random_x, random_y
            tmp_objs.append(obj)
        else:
            intersections_occur = True
            while intersections_occur:
                breaked = False
                random_x = random.randint(valid_x_min, valid_x_max)
                random_y = random.randint(valid_y_min, valid_y_max)
                obj.position = random_x, random_y
                for tmp_obj in tmp_objs:
 #                   print(check_intersections(obj, tmp_obj))
                    if check_intersections(obj, tmp_obj):
                        breaked = True
                        break

                if not breaked:
                    intersections_occur = False
                    if not intersections_occur:
                       # print("Found valid positions")
                        tmp_objs.append(obj)
        counter = counter + 1

# return False if no intersections occurs, True if there are intersections
def check_intersections(obj, tmp_obj):
    if ((obj.position[0] + obj.size[0] / 2) < (tmp_obj.position[0] - tmp_obj.size[0] / 2)) or ((tmp_obj.position[0] + tmp_obj.size[0] / 2) < (obj.position[0] - obj.size[0]/2)):
        if ((obj.position[1] + obj.position[1] / 2) < (tmp_obj.position[1] - tmp_obj.size[1] / 2)) or ((tmp_obj.position[1] + tmp_obj.size[1] / 2) < (obj.position[1] + obj.size[1]/2)):
            return False
    return True

def save_tmp(nr, obj, tmp_label, image_names, position_x, position_y, size_x, size_y, shapes, colors, label):
    image_names.append(nr)
    position_x.append(obj.position[0])
    position_y.append(obj.position[1])
    size_x.append(obj.size[0])
    size_y.append(obj.size[1])
    shapes.append(obj.shape)
    colors.append(obj.color)
    label.append(tmp_label)

def save_tmp_4objects(nr, obj, tmp_label, image_names, positions, sizes, shapes, colors, label):
    image_names.append(nr)
    for index, o in enumerate(obj):
        positions[2*index].append(o.position[0])
        positions[2*index+1].append(o.position[1])
        sizes[2*index].append(o.size[0])
        sizes[2*index+1].append(o.size[1])
        shapes[index].append(o.shape)
        colors[index].append(o.color)
    label.append(tmp_label)

def createList(data_frame_names, data_frame_objects):
    data_frame_list = {}
    for i in range(len(data_frame_names)):
        dicti = {data_frame_names[i] : data_frame_objects[i]}
        data_frame_list.update(dicti)
    return data_frame_list

def save_values_as_xlsx(path, file_name, image_names, positions_x, positions_y, sizes_x, sizes_y, shapes, colors, label):
    # Create a Pandas dataframe from some data.
    df = pd.DataFrame({
        'Image Names': image_names,
        'Position X': positions_x,
        'Position Y': positions_y,
        'Sizes X': sizes_x,
        'Sizes Y': sizes_y,
        'Shapes': shapes,
        'Colors': colors,
        'Label': label
    })

    Path(path).mkdir(parents=True, exist_ok=True)
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(path + "/" + file_name, engine='xlsxwriter')
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
    writer.save()

def save_values_as_xlsx_4objects(path, file_name, image_names, positions, sizes, shapes, colors, label):

    data_frame_names = 'Image Names', 'Obj1 Positions X', 'Obj1 Positions Y', 'Obj1 Sizes X', 'Obj1 Sizes Y', 'Obj1 Shapes', 'Obj1 Colors', 'Obj2 Positions X', 'Obj2 Positions Y', 'Obj2 Sizes X', 'Obj2 Sizes Y', 'Obj2 Shapes', 'Obj2 Colors', 'Obj3 Positions X', 'Obj3 Positions Y', 'Obj3 Sizes X', 'Obj3 Sizes Y', 'Obj3 Shapes', 'Obj3 Colors', 'Obj4 Positions X', 'Obj4 Positions Y', 'Obj4 Sizes X', 'Obj4 Sizes Y', 'Obj4 Shapes', 'Obj4 Colors', 'Label'
    data_frame_objects = []
    data_frame_objects.append(image_names)
    for index in range(len(shapes)):
        data_frame_objects.append(positions[2*index])
        data_frame_objects.append(positions[2*index+1])
        data_frame_objects.append(sizes[2*index])
        data_frame_objects.append(sizes[2*index+1])
        data_frame_objects.append(shapes[index])
        data_frame_objects.append(colors[index])
    data_frame_objects.append(label)
    # Create a Pandas dataframe from some data.
    df = pd.DataFrame(createList(data_frame_names, data_frame_objects))

    Path(path).mkdir(parents=True, exist_ok=True)
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(path + "/" + file_name, engine='xlsxwriter')
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
    writer.save()

def paint_image(label, reason, random_nr, random_nr_2, scene_height, scene_width, obj_array, path):
    import numpy as np
    from PIL import Image
    Path(path).mkdir(parents=True, exist_ok=True)
    data = np.zeros((scene_height, scene_width, 3), dtype=np.uint8)
    img = Image.fromarray(data)  # Create a PIL image
    for o in obj_array:
        for i in range(round(o.size[0] / 2)):
            data[o.position[1], o.position[0] - i] = [254, 0, 0]
            data[o.position[1], o.position[0] + i] = [254, 0, 0]
        for j in range(round(o.size[1] / 2)):
            data[o.position[1] + j, o.position[0]] = [254, 0, 0]
            data[o.position[1] - j, o.position[0]] = [254, 0, 0]
            # Makes the middle pixel red
    img = Image.fromarray(data)  # Create a PIL image
    if not os.path.exists(path):
     os.mkdir(path)
    img.save(path + str(random_nr) + str(random_nr_2) + "__label_" +str(label)+"__reason_is_"+reason+".png")
    # img.show()