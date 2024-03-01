## About
This directory comprises the implemented analysis method to extract relevant process details from unstructured data, i.e. images, employing Local Interpretable Model-Agnostic Explanations (LIME) [1].
The results are described in chapter 6 of the thesis.
Some content is already published in [2].

NOTE: The execution of the analysis code necessitates the availability of data created by the data generators located in ./data_generator/image_data/images_robotics. It is imperative to generate this data before executing the analysis code.

## Installation Guide
The Python source code and the utilized packages can is located in /src.
We recommend opening this folder in a Python IDE such as PyCharm.
If PIP is installed, the required packages can be installed using the command line with "pip install -r requirements.txt".
Configure and execute the corresponding "main.py" file to initiate the analysis procedure. Within this script, the scenario that has to be analyzed needs to be specified.

## Acknowledgements
We want to thank Philipp Jahn and Carsten Scholle from the University of Bayreuth for supporting the evaluation of our work.

## References
[1] Ribeiro, Marco Tulio, Sameer Singh, and Carlos Guestrin. "" Why should i trust you?" Explaining the predictions of any classifier." Proceedings of the 22nd ACM SIGKDD international conference on knowledge discovery and data mining. 2016.

[2] Fichtner, Myriel, et al. "Enriching Process Models with Relevant Process Details for Flexible Human-Robot Teaming." International Conference on Collaborative Computing: Networking, Applications and Worksharing. Cham: Springer Nature Switzerland, 2023.
