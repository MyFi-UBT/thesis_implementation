## About
Here you will find the algorithms used in the experiments with the method based on Association Rule Mining as well as the results. The content of the subfolder "arm_optuna_results" is published in [6].

## Description
Our approach evaluates different algorithms applied on the designed use cases: FP-Growth (fpg) [1], GARPlus (garplus) [2], HyperClique (hycli) [3], Quantitative Miner (quant) [4].

The results of each algorithm [alg] for each scenario [scen] can be found in the respective subfolder in the path /arm_optuna_results/[scen]/[alg].
The version without pruning is stored in /arm_optuna_results/[scen]/[alg]/[alg]_pure, the one with pruning in /arm_optuna_results/[scen]/[alg]/[alg]_pruned.

A set of parameters has to be defined for each algorithm, while we explore the parameter space with optuna [5] by using a grid search.

The search spaces defined for our experiments are stored in the parameters.md file in the folders for the respective use cases.

## Opening of .db file
The results of the grid search are stored in .db files.
These can for example be opened by using the free-to-use software "DB Browser for SQLite" (https://sqlitebrowser.org/).
Detailed results can be queried by using SQL Statements.

## Acknowledgements
We want to thank Josef Würf from the University of Bayreuth for setting up the implementation and supporting the evaluation of our work.

## References
[1] Han, Jiawei, Jian Pei, and Yiwen Yin. "Mining frequent patterns without candidate generation." ACM sigmod record 29.2 (2000): 1-12.

[2] Alvarez, Victoria Pachon, and Jacinto Mata Vazquez. "An evolutionary algorithm to discover quantitative association rules from huge databases without the need for an a priori discretization." Expert Systems with Applications 39.1 (2012): 585-593.

[3] Xiong, Hui, P-N. Tan, and Vipin Kumar. "Mining strong affinity association patterns in data sets with skewed support distribution." third IEEE international conference on data mining. IEEE, 2003.

[4] Srikant, Ramakrishnan, and Rakesh Agrawal. "Mining quantitative association rules in large relational tables." Proceedings of the 1996 ACM SIGMOD international conference on Management of data. 1996.

[5] Akiba, Takuya, et al. "Optuna: A next-generation hyperparameter optimization framework." Proceedings of the 25th ACM SIGKDD international conference on knowledge discovery & data mining. 2019.

[6] Myriel Fichtner and Stefan Jablonski." Applying Association Rules to Enhance Process Models through the Extraction of Relevant Process Details from Image Data.", Communications of the IBIMA, Vol. 2024, Article ID 172169, https://doi.org/10.5171/2024.172169. 2024.