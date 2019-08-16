# pseudo-code to implement two stage transfer learning
import gin
import numpy as np
from utils.parse_args import parse
from create_load_data import create_load_data
#from sklearn.model_selection import cross_val_score, cross_validate, KFold

'''
- algorithm from Stone and Rosenfeld 2013
- T is target data set
- S is set of source data sets S = {S_1, S_2, ..., S_n}
- m is num of boosting iterations
- k is num of folds for cross validation, k should be 10 as we have 10 games
- b is max num of source data sets to include
- S^w means data set S taken with weight w spread over instances
- F is ??? #FIXME

TwoStageTransfer (T, S, m, k, b)
    for all S_i in S: do
        wi ← CalculateOptimalWeight(T, ∅, Si, m, k)
    Sort S in decreasing order of w_i's
    F ← ∅
    for i from 1 to b do
        w ← CalculateOptimalWeight(T, F, S_i, m, k)
        F ← F ∪ S^w_i
    Train classifier c on T ∪ F
    return c

CalculateOptimalWeight(T, F, S, m, k):
    for i from 1 to m do
        w_i = (len(T) / (len(T) + len(S))) *  (1 − i /(m − 1))
    Calculate erri from k-fold cross validation on T using F and S wi as additional training data
    return wj such that j = argmaxi(erri)
'''

def two_stage_transfer(target_data_set, source_data_sets, num_boosting_iter, num_cross_val_folds, max_num_source_data_sets):
    #weights = []
    weight_sourcedata_dict = {}
    for data_set in source_data_sets:
        #phi is an empty set
        weight = calculate_optimal_weight(target_data_set, [], data_set, num_boosting_iter, num_cross_val_folds)
        source_weight_dict[weight] = data_set

    #sort S in decreasing order of wi
    sortedS = sort_data_by_weight(weight_sourcedata_dict)
    '''
    F = []
    for set_num in range(1, max_num_source_data_sets):
        weight = calculate_optimal_weight(target_data_set, F, source_data_sets[set_num], num_boosting_iter, num_cross_val_folds)
        F = F union source_data_sets[set_num] ^ weight
    train classifier on target_data_set  union F
    return classifier
    '''

# FIXME: rename F accordingly and update above
def calculate_optimal_weight(target_data_set, F, source_data_sets, num_boosting_iter, num_cross_val_folds):
    weights = []
    max_err = 0
    max_err_ind = 0
    for boosting_iter in range(1, num_boosting_iter):
        weights.append ((len(target_data_set) / (len(target_data_set) + len(source_data_sets))) * (1 - (boosting_iter / (num_boosting_iter - 1))))
    #find the index of the maximum error and return the weight at that index
        err = 0#calculating error from k-fold cross validation on T using F and Swi as addtional training data
        if err > max_err:
            max_err = err
            max_err_ind = boosting_iter-1
    return weights[max_err_ind]

def sort_data_by_weight(weight_sourcedata_dict):
    return [weight_sourcedata_dict[key] for key in sorted(weight_sourcedata_dict.keys(), reverse=True)]

# def train_classifier(data, args):
#
#     retun classifier
def main():
    args = parse()
    #loading data
    data = create_load_data(args)
    print(data.test_data)

    #produce classifier
    # T, S, m, k, b = parse_args(args)
    # classifier = two_stage_transfer(T, S, m, 10, b)
    # return classifier

if __name__== '__main__':
    main()
