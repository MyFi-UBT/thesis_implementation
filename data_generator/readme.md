## About
This folder contains the data generators to create image data and structured data. This data is used in the experiments to evaluate the analysis methods in the folder ./analysis.

## Description
The subfolder "image_data" contains two folders "images_basic" and "images_robotics".
They contains the algorithms to generate images which were used to evaluate the analysis methods in chapter 4 ("images_basic") and chapter 6 ("images_robotics") of the thesis.

## Installation Guide
The Python source code and the utilized packages can be located in [.]/src (where [.] refers to one of the previously described subfolders of "image_data" or to "structured_data").
We recommend opening the corresponding folder (e.g., "images_basic") in a Python IDE such as PyCharm.
If PIP is installed, the required packages can be installed using the command line with "pip install -r requirements.txt".
Then conigure and execute the respective "main.py" to create the data.