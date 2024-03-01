import math

interval_lb = 1
interval_ub = 10
interval_ss = 1

# refers to min_conf
confidence_lb = 0.1
confidence_ub = 1.0
confidence_ss = 0.1

# refers to min_supp
support_lb = 0.01
support_ub = 0.5
support_ss = 0.01

max_supp_lb = 0.1
max_supp_ub = 0.5
max_supp_ss = 0.1

h_confidence_lb = 0.1
h_confidence_ub = 1.0
h_confidence_ss = 0.1

# GARPLUS params:
num_gens_lb = 30
num_gens_ub = 70
num_gens_ss = 10

pop_size_lb = 30
pop_size_ub = 70
pop_size_ss = 10

w_s_lb = 0.3
w_s_ub = 0.7
w_s_ss = 0.1

w_c_lb = 0.5
w_c_ub = 1.0
w_c_ss = 0.1

w_recov_lb = 0.2
w_recov_ub = 0.5
w_recov_ss = 0.1

w_a_lb = 0.2
w_a_ub = 0.5
w_a_ss = 0.1


def get_parameters(algorithm):
    if algorithm == "fpg":
        fpg_dict = {
            "intervals": {
                "interval_lb": interval_lb,
                "interval_ub": interval_ub,
                "interval_ss": interval_ss
            },
            "confidence": {
                "confidence_lb": confidence_lb,
                "confidence_ub": confidence_ub,
                "confidence_ss": confidence_ss
            },
            "support": {
                "support_lb": support_lb,
                "support_ub": support_ub,
                "support_ss": support_ss
            },
            "n_trials": (support_ub - support_lb) / support_ss * (interval_ub - interval_lb) / interval_ss * (
                    confidence_ub - confidence_lb) / confidence_ss
        }
        return fpg_dict

    if algorithm == "quant":
        quant_dict = {
            "intervals": {
                "interval_lb": interval_lb,
                "interval_ub": interval_ub,
                "interval_ss": interval_ss
            },
            "confidence": {
                "confidence_lb": confidence_lb,
                "confidence_ub": confidence_ub,
                "confidence_ss": confidence_ss
            },
            "support": {
                "support_lb": support_lb,
                "support_ub": support_ub,
                "support_ss": support_ss
            },
            "max_supp": {
                "max_supp_lb": max_supp_lb,
                "max_supp_ub": max_supp_ub,
                "max_supp_ss": max_supp_ss
            },
            "n_trials": (support_ub - support_lb) / support_ss * (interval_ub - interval_lb) / interval_ss * (
                    confidence_ub - confidence_lb) / confidence_ss * (max_supp_ub-max_supp_lb) / max_supp_ss
        }
        return quant_dict

    if algorithm == "hyclique":
        hyclique_dict = {
            "intervals": {
                "interval_lb": interval_lb,
                "interval_ub": interval_ub,
                "interval_ss": interval_ss
            },
            "confidence": {
                "confidence_lb": confidence_lb,
                "confidence_ub": confidence_ub,
                "confidence_ss": confidence_ss
            },
            "support": {
                "support_lb": support_lb,
                "support_ub": support_ub,
                "support_ss": support_ss
            },
            "h_confidence": {
                "h_confidence_lb": h_confidence_lb,
                "h_confidence_ub": h_confidence_ub,
                "h_confidence_ss": h_confidence_ss
            },
            "n_trials": (support_ub - support_lb) / support_ss * (interval_ub - interval_lb) / interval_ss * (
                    confidence_ub - confidence_lb) / confidence_ss * (h_confidence_ub - h_confidence_lb) / h_confidence_ss
        }
        return hyclique_dict

    if algorithm == "garplus":
        garplus_dict = {
            "intervals": {
                "interval_lb": interval_lb,
                "interval_ub": interval_ub,
                "interval_ss": interval_ss
            },
            "num_gens": {
                "num_gens_lb": num_gens_lb,
                "num_gens_ub": num_gens_ub,
                "num_gens_ss": num_gens_ss
            },
            "pop_size": {
                "pop_size_lb": pop_size_lb,
                "pop_size_ub": pop_size_ub,
                "pop_size_ss": pop_size_ss
            },
            "w_s": {
                "w_s_lb": w_s_lb,
                "w_s_ub": w_s_ub,
                "w_s_ss": w_s_ss
            },
            "w_c": {
                "w_c_lb": w_c_lb,
                "w_c_ub": w_c_ub,
                "w_c_ss": w_c_ss
            },
            "w_recov": {
                "w_recov_lb": w_recov_lb,
                "w_recov_ub": w_recov_ub,
                "w_recov_ss": w_recov_ss
            },
            "w_a": {
                "w_a_lb": w_a_lb,
                "w_a_ub": w_a_ub,
                "w_a_ss": w_a_ss
            },
            "n_trials": math.ceil((interval_ub-interval_lb) / interval_ss * (num_gens_ub - num_gens_lb)/ num_gens_ss * (pop_size_ub - pop_size_lb) / pop_size_ss * (w_s_ub - w_c_lb) / w_s_ss * (w_c_ub - w_c_lb) / w_c_ss * (w_recov_ub - w_recov_lb) / w_recov_ss * (w_a_ub - w_a_lb) / w_a_ss)

        }
        return garplus_dict
