## About
This directory comprises the implemented analysis methods designed to extract relevant process details from structured data utilizing Association Rule Mining (ARM), and from unstructured data, i.e. images, employing Local Interpretable Model-Agnostic Explanations (LIME). The results are described in chapter 4 and 6 of the thesis.
Some content is already published in [1], [2] and [3].

NOTE: The execution of the analysis code necessitates the availability of data created by the data generators located in ./data_generator. It is imperative to generate this data before executing the analysis code.

## Description
The implemented algorithms are stored according to their used techniques in the subfolders "ARM" and "LIME".
The subfolder "LIME" contains two subdirectories "LIME_basic" and "LIME_robotics".
They contain the algorithms to conduct the analysis in chapter 4 ("LIME_basic") and chapter 6 ("LIME_robotics") of the thesis.

## Installation Guide
The Python source code and the utilized packages is located in [method]/src (where [method] refers to one of the previously described subfolders of "LIME" or to "ARM").
We recommend opening the corresponding folder (e.g., "LIME_basic") in a Python IDE such as PyCharm.
If PIP is installed, the required packages can be installed using the command line with "pip install -r requirements.txt".
Then configure and execute the respective entry file to start the analysis procedure (explained in the README-files in the subfolders). 

## References
[1] Fichtner, Myriel, Stefan Schönig, and Stefan Jablonski. "How LIME Explanation Models Can Be Used to Extend Business Process Models by Relevant Process Details." ICEIS (2). 2022.

[2] Fichtner, Myriel, et al. "Enriching Process Models with Relevant Process Details for Flexible Human-Robot Teaming." International Conference on Collaborative Computing: Networking, Applications and Worksharing. Cham: Springer Nature Switzerland, 2023.

[3] Myriel Fichtner and Stefan Jablonski." Applying Association Rules to Enhance Process Models through the Extraction of Relevant Process Details from Image Data.", Communications of the IBIMA, Vol. 2024, Article ID 172169, https://doi.org/10.5171/2024.172169. 2024.