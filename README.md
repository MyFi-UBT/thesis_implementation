Code for the thesis "Verbesserung von Prozessmodellen durch relevante Prozessdetails" by Myriel Fichtner.
--
**Project Description**

This repository contains the code referring to chapter 4, 5 and 6 of the thesis.
The code encompasses two methods to analyze relevant process details from execution data. The implemented methods use the techniques association rule mining (ARM) and Local-Interpretable Model Agnostic Explanations (LIME).
Data generators are provided to enable the use of synthetical data for the evaluation.
Furthermore, the user study results and the used evaluation script are provided.

**Structure**

The folders contain subfolders as follows:

analysis

- |_ARM

- |_LIME

--  |_LIME_basic
  
--  |_LIME_robotics

data_generator
|_image_data
  |_images_basic
  |_images_robotics
|_structured_data

user_study
|_Statistische Analyse


The analysis and data_generator folders refer to the experiments presented in chapter 4.

The user study folder refers to the experimental study presented in chapter 5. It contains the results of the descriptive (Deskriptive_Auswertung.xlsx) and statistical analysis (Folder: Statistische Analyse) of the collected data.
Please note that all descriptions there are only provided in german.
