| PARAMETERS [min, max], step size |  intervals |      min_supp     |     min_conf    |     max_supp    |   h-confidence  |    n_gens    |    p_size    |       w_s       |       w_c       |       w_a       |       w_r       |
|:--------------------------------:|:----------:|:-----------------:|:---------------:|:---------------:|:---------------:|:------------:|:------------:|:---------------:|:---------------:|:---------------:|:---------------:|
|    **FP-G (pure and pruned)**    | [1, 10], 1 | [0.01, 0.5], 0.01 | [0.1, 1.0], 0.1 |        -        |        -        |       -      |       -      |        -        |        -        |        -        |        -        |
|    **Quant (pure and pruned)**   | [1, 10], 1 | [0.05, 0.5], 0.05 | [0.1, 1.0], 0.1 | [0.1, 0.5], 0.1 |        -        |       -      |       -      |        -        |        -        |        -        |        -        |
|    **HyCli (pure and pruned)**   | [1, 10], 1 |  [0.1, 0.5], 0.1  | [0.1, 1.0], 0.1 |        -        | [0.1, 1.0], 0.1 |       -      |       -      |        -        |        -        |        -        |        -        |
|    **GAR+ (pure and pruned)**    | [1, 10], 1 |         -         |                 |        -        |        -        | [30, 70], 10 | [30, 70], 10 | [0.3, 0.7], 0.1 | [0.5, 1.0], 0.1 | [0.2, 0.5], 0.1 | [0.2, 0.5], 0.1 |

-----
Note for Quant: We fix the interest score $R = 1.3$.

-----
Note for GAR+: The following parameters were fixed across all experiments (for details please refer to the original work).

$n_r$ (number of rules)= 7

$s_{perc}$ (individuals passed to next generation)= 0.15

$w_{na}$ (weightening factor for number of attributes)= -0.05

$r_{prob}$ (recombination probability)= 0.5

$m_{prob}$ (mutation probability)= 0.4

$a_{prob}$ (selection probability of attributes)= 0.5

$seed = 17$

-----
Note for Pruning: We fix $minimp = 0.002$.