# scene: width: 507px, height: 672 px
# rectangular object size: 50(width)x150(height)
# circular object size: 60x60

# valid positions for rectangular objects (centroid): x = [25;482] y = [75;597]
# valid positions for circular objects (centroid): x = [30;477], y = [30; 120]

# no intersections between objects allowed

# interesting aspects:
# how many data (entries) is needed overall? (500? 1000? 5000?)
# do the different labels have to appear the same number of times? (20% good, 80 % bad? 50%/50%?)
# how robust is the algorithm depending on the level of noise (e.g. size of an object varies by some pixels)
from pathlib import Path
from brick import brick
from scenario_1_1 import compute_scenario1_1
from scenario_1_2 import compute_scenario1_2
from scenario_1_3 import compute_scenario1_3
from scenario_1_4 import compute_scenario1_4
from scenario_2_1 import compute_scenario2_1
from scenario_2_2 import compute_scenario2_2

scene_width = 507
scene_height = 672

# 2 object types
# "rect"
rect_obj_width = 50
rect_obj_height = 150
rect_obj_shape = "rectangular"

# "circ"
circ_obj_width = 60
circ_obj_height = 60
circ_obj_shape = "circular"

circ_obj_width_2 = 50
circ_obj_height_2 = 50
circ_obj_shape_2 = "circular"

obj1 = brick()
obj1.color = "blue"
obj1.shape = rect_obj_shape
# width, height
obj1.size = (rect_obj_width, rect_obj_height)
obj1.position = (0, 0)

obj2 = brick()
obj2.color = "green"
obj2.shape = rect_obj_shape
# width, height
obj2.size = (rect_obj_width, rect_obj_height)
obj2.position = (0, 0)

obj3 = brick()
obj3.color = "red"
obj3.shape = circ_obj_shape
# width, height
obj3.size = (circ_obj_width, circ_obj_height)
obj3.position = (0, 0)

obj3_1 = brick()
obj3_1.color = "red"
obj3_1.shape = circ_obj_shape
# width, height
obj3_1.size = (circ_obj_width, circ_obj_height)
obj3_1.position = (0, 0)

obj3_2 = brick()
obj3_2.color = "red"
obj3_2.shape = circ_obj_shape
# width, height
obj3_2.size = (circ_obj_width_2, circ_obj_height_2)
obj3_2.position = (0, 0)

obj4 = brick()
obj4.color = "red"
obj4.shape = rect_obj_shape
# width, height
obj4.size = (rect_obj_width, rect_obj_height)
obj4.position = (0, 0)

obj4_1 = brick()
obj4_1.color = "red"
obj4_1.shape = rect_obj_shape
# width, height
obj4_1.size = (rect_obj_width, rect_obj_height)
obj4_1.position = (0, 0)

path = '../generated_data/scenario1'
compute_scenario1_1(500, scene_width, scene_height, obj1, obj2, path)
#path = '../generated_data/scenario2'
#compute_scenario2_2(500, scene_width, scene_height, obj3, obj3_2, obj4, obj4_1, path)
