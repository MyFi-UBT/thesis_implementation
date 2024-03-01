import pandas as pd
import optuna
import logging
import sys
from src import arm_model_builder, hyperparameter_definition
import os
import numpy as np


def print_best_callback(study, trial):
    print(f"Best value: {study.best_value}, Best params: {study.best_trial.params}")


def objective(trial, data_path, algorithm, prune_value, search_space):
    config_loader = arm_model_builder.JSONLoader()
#    attr = config_loader.get_attributes()

    params_trial_dict = {}
    for entry in search_space:
        if isinstance(search_space[entry][0], int):
            params_trial_dict.update({entry: trial.suggest_int(entry, search_space[entry][0], search_space[entry][len(search_space[entry])-1])})
        else:
            params_trial_dict.update({entry: trial.suggest_float(entry, search_space[entry].min(), search_space[entry].max())})

    if algorithm == "quant":
        if params_trial_dict['MAXSUPP'] <= params_trial_dict['SUPPORT'] or params_trial_dict['SUPPORT'] == 0.0 or params_trial_dict['SUPPORT'] == 0.05:
            return -1
    if algorithm == "hyclique":
        if params_trial_dict['HCONF'] > params_trial_dict['CONFIDENCE']:
            return -1

    scenario = pd.read_excel(data_path + ".xlsx").drop(labels="Image Names", axis=1)

    discretization = arm_model_builder.build_discretization_new(config_loader, scenario, params_trial_dict['INTERVALS'])

    if algorithm == "fpg":
        standard = arm_model_builder.StandardMiner(arm_model_builder.static_discretization,
                                                   arm_model_builder.classification_rules)
        standard.set_args(
            standard.transformer,
            {"discretization": discretization, "equi_depth": False},
        )
        standard.set_args(standard.itemset_miner, {"min_support": params_trial_dict['SUPPORT']})
        standard.set_args(standard.rule_miner, {"label": "Label", "min_conf": params_trial_dict['CONFIDENCE']})

        result = standard.run(scenario)

    if algorithm == "quant":
        quant = arm_model_builder.QuantitativeMiner(arm_model_builder.classification_rules)
        quant.set_args(
            quant.itemset_miner,
            {
                "minsupp": params_trial_dict['SUPPORT'],
                "R": 1.3,
                "discretization": discretization,
                "equi_depth": True,
                "maxsupp": params_trial_dict['MAXSUPP'],
            },
        )
        quant.set_args(quant.rule_miner, {"min_conf": params_trial_dict['CONFIDENCE'], "label": "Label"})
        result = quant.run(scenario)

    if algorithm == "hyclique":
        hyclique = arm_model_builder.HyperCliqueMiner(arm_model_builder.static_discretization, arm_model_builder.classification_rules)
        hyclique.set_args(
            hyclique.transformer, {"discretization": discretization, "equi_depth": False},)
        hyclique.set_args(
            hyclique.itemset_miner, {"support_threshold": params_trial_dict['SUPPORT'], "hconf_threshold": params_trial_dict['HCONF']},)
        hyclique.set_args(hyclique.rule_miner, {"min_conf": params_trial_dict['CONFIDENCE'], "label": "Label"})
        result = hyclique.run(scenario)

    if algorithm == "garplus":
        gp = arm_model_builder.GarPlusMiner()
        gp.set_args(
            gp.itemset_miner, {
                "num_cat_attrs": discretization,
                "num_rules": 7,
                "num_gens": params_trial_dict['NUMGENS'],
                "population_size": params_trial_dict['POPSIZE'],
                "w_s": params_trial_dict['WS'],
                "w_c": params_trial_dict['WC'],
                "n_a": -0.05,
                "w_a": params_trial_dict['WA'],
                "w_recov": params_trial_dict['WRECOV'],
                "consequent": "Label",
                "selection_percentage": 0.15,
                "recombination_probability": 0.5,
                "mutation_probability": 0.4,
                "attr_probability": 0.5
            })
        result = gp.run(scenario)


    try:
        exists = result['consequents']
        if prune_value:
            result = arm_model_builder.prune_by_improvement(scenario, result)
    except KeyError:
        return 0

    ruleIsPresent = False
    nrOfLabel1 = 0

    # Keep only the rules that meet the requirements: i) label = 1 in its consequent and ii) fulfill the condition
    # describing the relevant process details.
    try:
        consequents = result['consequents']
        for idx, c in enumerate(consequents):
            if c[0] == "Label = 1":
                nrOfLabel1 = nrOfLabel1 + 1
                # Condition which contains the relevant process details. If this condition is met, the relevant rule
                # is found.
                if result['antecedents'][idx][0] == "Colors = blue":
                    ruleIsPresent = True

        if ruleIsPresent and nrOfLabel1 != 0:
            return 1 / nrOfLabel1
        else:
            return 0
    except KeyError:
        return 0


optuna.logging.get_logger("optuna").addHandler(logging.StreamHandler(sys.stdout))


def start_my_study(scenario_nr, data_path, algorithm, prune_value):
    print("Starting the study...")
    parameters = hyperparameter_definition.get_parameters(algorithm)
    search_space = {}
    if 'intervals' in parameters:
        interval_space = list(range(parameters['intervals']['interval_lb'],
                                    parameters['intervals']['interval_ub'] + parameters['intervals']['interval_ss']))
        search_space.update({'INTERVALS': interval_space})
    if 'support' in parameters:
        support_space = np.arange(parameters['support']['support_lb'],
                                  parameters['support']['support_ub'] + parameters['support']['support_ss'],
                                  parameters['support']['support_ss'])
        search_space.update({'SUPPORT': support_space})
    if 'confidence' in parameters:
        confidence_space = np.arange(parameters['confidence']['confidence_lb'],
                                     parameters['confidence']['confidence_ub'] + parameters['confidence'][
                                         'confidence_ss'], parameters['confidence']['confidence_ss'])
        search_space.update({'CONFIDENCE': confidence_space})
    if 'max_supp' in parameters:
        maxsupp_space = np.arange(parameters['max_supp']['max_supp_lb'],
                                  parameters['max_supp']['max_supp_ub'] + parameters['max_supp']['max_supp_ss'],
                                  parameters['max_supp']['max_supp_ss'])
        search_space.update({'MAXSUPP': maxsupp_space})
    if 'h_confidence' in parameters:
        hconfidence_space = np.arange(parameters['h_confidence']['h_confidence_lb'],
                                  parameters['h_confidence']['h_confidence_ub'] + parameters['h_confidence']['h_confidence_ss'],
                                  parameters['h_confidence']['h_confidence_ss'])
        search_space.update({'HCONF': hconfidence_space})
    if 'num_gens' in parameters:
        numgens_space = list(range(parameters['num_gens']['num_gens_lb'],
                                      parameters['num_gens']['num_gens_ub'] + parameters['num_gens']['num_gens_ss'], parameters['num_gens']['num_gens_ss']))
        search_space.update({'NUMGENS': numgens_space})
    if 'pop_size' in parameters:
        popsize_space = list(range(parameters['pop_size']['pop_size_lb'],
                                      parameters['pop_size']['pop_size_ub'] + parameters['pop_size']['pop_size_ss'], parameters['pop_size']['pop_size_ss']))
        search_space.update({'POPSIZE': popsize_space})
    if 'w_s' in parameters:
        ws_space = np.arange(parameters['w_s']['w_s_lb'],
                                      parameters['w_s']['w_s_ub'] + parameters['w_s']['w_s_ss'],
                                      parameters['w_s']['w_s_ss'])
        search_space.update({'WS': ws_space})
    if 'w_c' in parameters:
        wc_space = np.arange(parameters['w_c']['w_c_lb'],
                             parameters['w_c']['w_c_ub'] + parameters['w_c']['w_c_ss'],
                             parameters['w_c']['w_c_ss'])
        search_space.update({'WC': wc_space})

    if 'w_recov' in parameters:
        wrecov_space = np.arange(parameters['w_recov']['w_recov_lb'],
                                      parameters['w_recov']['w_recov_ub'] + parameters['w_recov']['w_recov_ss'],
                                      parameters['w_recov']['w_recov_ss'])
        search_space.update({'WRECOV': wrecov_space})

    if 'w_a' in parameters:
        wa_space = np.arange(parameters['w_a']['w_a_lb'],
                             parameters['w_a']['w_a_ub'] + parameters['w_a']['w_a_ss'],
                             parameters['w_a']['w_a_ss'])
        search_space.update({'WA': wa_space})

    if prune_value:
        study_name = "scen1_" + str(scenario_nr) + "-" + algorithm + "-pruned-" + "nrt" + str(parameters['n_trials'])  # Unique identifier of the study.
    else:
        study_name = "scen1_" + str(scenario_nr) + "-" + algorithm + "-" + "nrt" + str(parameters['n_trials'])  # Unique identifier of the study.

    storage_name = "sqlite:///{}.db".format(study_name)
    #    storage_name_string_url = "sqlite:///" + os.path.join(file_path, (study_name + ".db"))
    #    print(storage_name_string_url)
    #    storage_name_raw_bytes_url = r'{}'.format(storage_name_string_url)
    #    print(storage_name_raw_bytes_url)
    #    storage_name = optuna.storages.RDBStorage(url=storage_name_raw_bytes_url)
    #    print(storage_name)

    study = optuna.create_study(sampler=optuna.samplers.GridSampler(search_space), study_name=study_name,
                                load_if_exists=True,
                                storage=storage_name, direction="maximize")
    study.optimize(lambda trial: objective(trial, data_path, algorithm, prune_value, search_space), n_trials=parameters['n_trials'])

    res = optuna.study.get_all_study_summaries(storage_name, include_best_trial=True)


# begin optimization procedure with a certain algorithm (fpg, quant, hyclique or garplus) and the decision if it
# should be pruned or not
# please define parameters/the search space in the file "parameter_definition.py"
algorithm = "garplus"
prune_value = False

current_dir = os.getcwd()
data_path = os.path.join(os.path.abspath(os.path.dirname(
    os.path.dirname(os.path.dirname(current_dir))) + '/data_generator/structured_data/generated_data/scenario1'))

# If the range is (1,5), all four scenarios are computed. Modify the range if only single scenarios should be
# considered, e.g., if only scenario 1_3 should be considered, define the range as (3,4).
for i in range(1, 2):
    data_path = os.path.join(os.path.abspath(data_path + "/scenario_1_" + str(i)))
    start_my_study(i, data_path, algorithm, prune_value)
