Code for the thesis "Verbesserung von Prozessmodellen durch relevante Prozessdetails" by Myriel Fichtner.
--
**Project Description**

This repository contains the code referring to chapter 4, 5 and 6 of the thesis.
The code encompasses two methods to analyze relevant process details from execution data. The implemented methods use the techniques association rule mining (ARM) and Local-Interpretable Model Agnostic Explanations (LIME).
Data generators are provided to enable the use of synthetical data for the evaluation.
Furthermore, the user study results and the used evaluation script are provided.

**Structure**
root/

  - analysis
   - ARM
     - arm_optuna_results
       - scenario1
         - fpg/
            - fpg_pruned/
              - scen1_1_fpg_pruned.db
              - scen1_2_fpg_pruned.db
              - ...
            - fpg_pure/
              - scen1_1_fpg_pure.db
              - ...
          - garplus/
            - garplus_pruned/
              - ...
            - garplus_pure/
              - ...
          - hycli/
            - hycli_pruned/
              - ...
            - hycli_pure/
              - ...
          - quant
            - quant_pruned/
              - ...
            - quant_pure/
              - ...
          - parameters.md 
       - scenario2
         - fpg/
            - fpg_pruned/
              - scen2_1_fpg_pruned.db
              - scen2_2_fpg_pruned.db
            - fpg_pure/
              - scen2_1_fpg_pure.db
              - ...
          - garplus/
            - garplus_pruned/
              - ...
            - garplus_pure/
              - ...
          - hycli/
            - hycli_pruned/
              - ...
            - hycli_pure/
              - ...
          - parameters.md
     - src
     - readme.md 
   - LIME
     - LIME_basic
       - src
       - readme.md 
     - LIME_robotics
       - src
       - readme.md 
   - readme.md
  - data_generator
  - user_study


**Overview**

The folders "analysis" and "data_generator" refer to the experiments presented in chapter 4.
The folder "user_study" contains the data and results of the experimental user study described in chapter 5.
Within all folders and within the code files you will find further information regarding the implementation, e.g., how to use it, as well as references to the original work where the code is based on.

## Reusage
The content may be used for any non-commercial application or future research.

## Contact
In case of questions please contact Myriel.Fichtner@uni-bayreuth.de.
