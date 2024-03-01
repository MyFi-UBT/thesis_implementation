# Computes rules for a fixed hyper parameter set defined in "parameter_scripts/parameter.json"
# Standalone function, .i.e. does neither need arm_model_builder nor hyperparameter_optimization_scenarioX.py. just
# needs the json-file where the parameters are defined. All variants of a scenario are calculated, i.e.,
# four variants are computed for scenario 1 and two variant are computed for scenario 2

import datetime
import os
import pandas as pd
import numpy as np
import random
from algs.models import (
    StandardMiner,
    QuantitativeMiner,
    HyperCliqueMiner,
    GarPlusMiner,
)
from algs.quantitative import static_discretization, cluster_interval_data
from typing import Any, Dict, List, Tuple
from algs.rule_gen import (
    classification_rules,
    prune_by_improvement,
)
from os import listdir
from os.path import isfile, join, basename
import matplotlib.pyplot as plt
from sklearn.cluster import Birch
import json

# PYTHONHASHSEED=0
np.random.seed(17)
random.seed(17)

current_dir = os.getcwd()
scenario = "scenario1"
data_path = os.path.join(os.path.abspath(os.path.dirname(
    os.path.dirname(os.path.dirname(current_dir))) + '/data_generator/structured_data/generated_data/'+scenario))

PFAD = data_path

class JSONLoader:
    def __init__(self) -> None:
        self.load_data()
        if scenario == "scenario1":
            self.scenario = "scenario_1"
        elif scenario == "scenario2":
            self.scenario = "scenario_2"
        else:
            "Could not find scenario, please check name."

    def load_data(self) -> None:
        with open("parameter_scripts/parameters.json") as config:
            self.data = json.load(config)

    def get_attributes(self) -> Dict[str, bool]:
        return self.data["ATTRIBUTES"]

    def get_attribute(self, name: str) -> Dict[str, bool]:
        return self.data["ATTRIBUTES"][name]

    def set_scene(self, scenario: str) -> None:
        self.scenario = scenario

    def get_minsupp(self) -> float:
        return self.data[self.scenario]["MIN_SUPP"]

    def get_minconf(self) -> float:
        return self.data[self.scenario]["MIN_CONF"]

    def get_hconf(self) -> float:
        return self.data[self.scenario]["h_conf"]

    def get_maxsupp(self) -> float:
        return self.data[self.scenario]["max_supp"]

    def get_num_intervals(self) -> float:
        return self.data[self.scenario]["INTERVALS"]

    def get_cluster(self) -> List[Tuple[str, str]]:
        return [
            tuple(settings)
            for settings in self.data[self.scenario]["scenario_clusters"]
        ]

    def get_gar_plus_configs(self) -> Dict[str, float]:
        return self.data[self.scenario]["gp"]


class AIDS:
    """Association rules for image datasets(AIDS)"""

    def __init__(self, loader: JSONLoader, datasets: List[str], dir_name: str) -> None:
        self.loader = loader
        self.datasets = datasets
        self.datasets = datasets
        self.final_directory = dir_name
        self.make_dir(dir_name)

    def make_dir(self, dir_name: str) -> None:
        current_directory = os.getcwd()
        self.final_directory = os.path.join(current_directory, r"" + dir_name)
        if not os.path.exists(self.final_directory):
            os.makedirs(self.final_directory)

    def build_discretization(self, df: pd.DataFrame) -> Dict[str, int]:
        dic = {}
        for name in df.columns:
            if not self.loader.get_attribute(name):
                dic[name] = 0
            # Numeric attributes with just one or up to eleven values are treated as categorical attribute.
            elif df[name].max() == df[name].min():
                dic[name] = 0
            else:
                dic[name] = self.loader.get_num_intervals()
        return dic

    def build_cluster_radius(
        self, df: pd.DataFrame, names: List[Tuple[str]], factor: int = 15
    ) -> Dict[str, float]:
        remaining_names = list(df.columns)
        dic = {}
        for name1, name2 in names:
            radius = (df[name1].max() - df[name1].min()) / factor
            radius2 = (df[name2].max() - df[name2].min()) / factor
            radius += radius2
            dic[(name1, name2)] = radius if radius != 0 else 1e-10
            remaining_names.remove(name1)
            remaining_names.remove(name2)

        for name in remaining_names:
            if not self.loader.get_attribute(name):
                pass
            # Numeric attributes with just one or up to eleven values are treated as categorical attribute.
            elif df[name].max() == df[name].min():
                pass
            else:
                # dic[(name,)] = (df[name].max() - df[name].min() + 1e-10) / factor
                dic[(name,)] = 5
        return dic

    def build_models(
        self,
        discretizations: Dict[str, Any],
        attr_threshold: Dict[str, float],
        equi_depth: bool,
    ) -> Dict[str, Any]:
        min_supp = self.loader.get_minsupp()
        min_conf = self.loader.get_minconf()

        quant = QuantitativeMiner(classification_rules)
        quant.set_args(
            quant.itemset_miner,
            {
                "minsupp": min_supp,
                "R": 1.3,
                "discretization": discretizations,
                "equi_depth": equi_depth,
                "maxsupp": self.loader.get_maxsupp(),
            },
        )
        quant.set_args(quant.rule_miner, {"min_conf": min_conf, "label": "Label"})

        standard = StandardMiner(static_discretization, classification_rules)
        standard.set_args(
            standard.transformer,
            {"discretization": discretizations, "equi_depth": False},
        )
        standard.set_args(standard.itemset_miner, {"min_support": min_supp})
        standard.set_args(standard.rule_miner, {"label": "Label", "min_conf": min_conf})

        hyper = HyperCliqueMiner(static_discretization, classification_rules)
        hyper.set_args(
            hyper.transformer,
            {"discretization": discretizations, "equi_depth": False},
        )
        hyper.set_args(
            hyper.itemset_miner,
            {"support_threshold": min_supp, "hconf_threshold": self.loader.get_hconf()},
        )
        hyper.set_args(hyper.rule_miner, {"min_conf": min_conf, "label": "Label"})


        gp = GarPlusMiner()
        gp.set_args(
            gp.itemset_miner,
            dict(
                {
                    "num_cat_attrs": discretizations,
                },
                **self.loader.get_gar_plus_configs(),
            ),
        )

        return {
            "StandardMiner": standard,
            "QuantitativeMiner": quant,
            "HyperCliqueMiner": hyper,
            "GarPlusMiner": gp,
        }

    def write_to_sheet(
        self, df: pd.DataFrame, writer: pd.ExcelWriter, sheet_name: str
    ) -> None:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        writer.save()

    def run_model(
        self,
        model: Any,
        df: pd.DataFrame,
        prune: bool = False,
    ) -> None:
        result = model.run(df)
#        if prune:
#            result = prune_by_improvement(df, result)

        return result

    def run(self) -> None:
        for dataset in self.datasets:
            scenario = pd.read_excel(dataset).drop(labels="Image Names", axis=1)
            scenario_name = basename(dataset)

            self.loader.set_scene(scenario_name[: scenario_name.find("_") + 2])

            radius = self.build_cluster_radius(scenario, [])
            discretization = self.build_discretization(scenario)
            models = self.build_models(discretization, radius, True)

            print(f"Running scenario {scenario_name} with {len(scenario)} entries.")
            pd.DataFrame().to_excel(
                os.path.join(self.final_directory, scenario_name), index=False
            )
            writer = pd.ExcelWriter(
                os.path.join(self.final_directory, scenario_name), engine="openpyxl"
            )
            for name, model in models.items():
                if name == "QuantitativeMiner" and scenario_name.startswith(
                    "scenario_2"
                ):
                    continue
                start = datetime.datetime.now().replace(microsecond=0)
                print(f"Now starting {name}")
                model_result = self.run_model(
                    model, scenario, False if name == "GarPlusMiner" else True
                )
                end = datetime.datetime.now().replace(microsecond=0)
                print(
                    f"Finished with {name}; Found {len(model_result)} rules in {end-start} time."
                )
                self.write_to_sheet(model_result, writer, name)
            writer.close()


config_loader = JSONLoader()
aids = AIDS(
    config_loader,
    [join(PFAD, f) for f in listdir(PFAD) if isfile(join(PFAD, f))],
    "../arm_results",
)

aids.run()
