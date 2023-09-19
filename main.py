
"""
Common Libraries
"""
import os
import sys
import numpy as np
import random
import itertools

"""
Custom Libraries
"""
from Psychopy_util import Sequence_st_text_unit, Sequence_st_bundle, St_Package, Experiment, ISI_st_unit

def find_indexes(list, find_value, method = "equal"):
    """
    Search value from list
    
    :param list: list(list)
    :param find_value: value
    
    return: index of list matched to find_value
    """
    indexes = []
    for i in range(0, len(list)):
        if method == "equal":
            if list[i] == find_value:
                indexes.append(i)
        elif method == "in":
            if find_value in list[i]:
                indexes.append(i)
        elif method == "not_in":
            if find_value not in list[i]:
                indexes.append(i)
    return indexes

def get_random_sample_in_codes(sample_count, codes, appear_counts):
    """
    Getting code list from codes randomly

    :param sample_count: how many samples do you want ex) 10
    :param codes: sampling target ex) [1,2,3]
    :param appear_counts: How many appears specific value in sample_count ex) [2, 3, 5]
    :return: list of codes
    """
    result = ["empty"] * sample_count
    empty_value_indexes = find_indexes(result, "empty")

    for code_i in range(0, len(codes)):
        if code_i != len(codes) - 1:
            for j in range(0, appear_counts[code_i]):
                specific_index = empty_value_indexes[random.randint(0, len(empty_value_indexes)-1)]
                result[specific_index] = codes[code_i]
                empty_value_indexes.remove(specific_index)
        else:
            for g in empty_value_indexes.copy():
                result[g] = codes[code_i]
                empty_value_indexes.remove(g)
    return result


"""
Experiment Setting
"""
experiment_data_path = os.path.join(".")
participant_name = input("Input participant name: ")

exp_type = "exp_blueprint_0324v4"
exp_info = {
        "seqs" : [
            ["1", "4", "2", "3", "1", "2", "4", "3"],
            ["2", "1", "3", "4", "2", "3", "1", "4"],
            ["3", "4", "2", "1", "3", "2", "4", "1"],
            ["4", "1", "3", "2", "4", "3", "1", "2"],
        ],

        "tr" : 2,
        "run_length" : 4,
        "seq_length" : 8,
        "trial_count" : 24,
        "repetition_count" : 6,
        "move_time" : 10,
        "rest_time" : 20,
}

seqs = exp_info["seqs"]
sequence_count = len(seqs)
sequence_showing_time = exp_info["move_time"]
sequence_color = [0,0,0]
sequence_rest_time = exp_info["rest_time"]
sequence_bundle_count_per_run = int(exp_info["trial_count"] / len(exp_info["seqs"])) # 12

# Make dir
data_dir_path = os.path.join(experiment_data_path, "experiment", exp_type, participant_name)
if not os.path.exists(data_dir_path):
    os.makedirs(data_dir_path)
else:
    raise Exception("participant name is duplicated!!, Please check " + participant_name)


# Making sequences
candidate_seqs = list(map(lambda x: list(x), list(itertools.permutations(seqs, 4))))

text_unit_seqs = list(map(lambda seqs: list(map(lambda seq: Sequence_st_text_unit(seq,
                                                                                  showing_time=sequence_showing_time,
                                                                                  color=sequence_color,
                                                                                  text_height=0.1,
                                                                                  is_count_correct=True),
                                                seqs)),
                          candidate_seqs))

seq_bundles = list(map(lambda text_units: Sequence_st_bundle(text_units, ISI_interval = sequence_rest_time), text_unit_seqs))
candidate_bundle_indexes = np.arange(0, len(candidate_seqs))

"""
Data
"""
# Make blocks
def make_blocks(seq_bundles, run_count = 4):
    shuffles = []

    seq_bundle_length = len(seq_bundles)
    candidate_sample_sets = get_random_sample_in_codes(sample_count = seq_bundle_length,
                                             codes = np.arange(0, seq_bundle_length),
                                             appear_counts = np.repeat(1, seq_bundle_length))

    print(candidate_sample_sets)

    for run_index in range(0, run_count):
        first_ISI = Sequence_st_bundle([ISI_st_unit("+", showing_time=6)], ISI_interval=0)

        set_lower_index = run_index * sequence_bundle_count_per_run
        set_upper_index = run_index * sequence_bundle_count_per_run + sequence_bundle_count_per_run

        sample_sets = candidate_sample_sets[set_lower_index: set_upper_index]

        seq_set_list = [first_ISI] + list(map(lambda sample_set_value: seq_bundles[sample_set_value], sample_sets))

        shuffles.append(seq_set_list)

    blocks = []
    for s in shuffles:
        blocks.append([St_Package(bundles=s, bundle_intervals=[0], bundle_interval_text="Empty")])
    return blocks

blocks = make_blocks(seq_bundles, run_count=4)

# Experiments
exp = Experiment(monitor_size=[1200,500],
                 is_full_screen = True,
                 data_dir_path = data_dir_path,
                 participant_name = participant_name,
                 ready_keys=["r"],
                 start_keys=["s"],
                 stop_keys=["p"],
                 valid_keys=["4", "3", "2", "1"],
                 is_response = True,
                 input_device="keyboard")

exp.wait_blocks(blocks=blocks,
                iteration=0)



