import os
import sys
import pickle
import numpy as np
import random
from datetime import datetime

# Set path TODO: remove the ones that won't be used in the end
PATH_IMI = os.path.dirname(os.path.abspath(__file__))
PATH_GANABI = os.path.dirname(os.path.dirname(PATH_IMI))
PATH_HANABI_ENV = os.path.join(PATH_GANABI, "hanabi_env")
PATH_EXPERTS = os.path.join(PATH_GANABI, 'experts')
PATH_UTILS = os.path.join(PATH_GANABI, 'utils')
sys.path.insert(0, PATH_GANABI)
sys.path.insert(0, PATH_HANABI_ENV)
sys.path.insert(0, PATH_UTILS)

import binary_list_to_int as b2int

# Global Variable Class
class glb:
    SIZE_OBS_VEC = 658
    SIZE_ACT_VEC = 20

# TODO: remove this before shipping
PATH_EX_PKL = os.path.join(PATH_GANABI,
    'output/WTFWT_data_2_1000000/0/WTFWT_2_25000.pkl')
PATH_EX_DIR = os.path.join(PATH_GANABI, 'output/WTFWT_data_2_1000000/')

def CV(path_dir=PATH_EX_DIR, size_train=0.9, seed=1234):
    """ Convert a Pickle file of observations and actions into np matrices with
        a boolean mask indicating the training rows.

    Arguments:
        - path_pkl: str
            Path to the pickle file containing the game data.
        - size_train: float
            Size of the training set.
        - seed: int
            Seed for choosing which rows for training.
    Returns:
      - X: np.matrix
          Matrix that contains the observations in following format:
          [[observatoin of round 1 in game 1],
           [observatoin of round 2 in game 1],
           ...
           [observatoin of round 1 in game 2],
           ...
           [observatoin of round N in game M]]
      - Y: np.matrix
          Matrix that contains the actions in following format:
          [[action of round 1 in game 1],
           [action of round 2 in game 1],
           ...
           [action of round 1 in game 2],
           ...
           [action of round N in game M]]
      - mask: np.array
          A boolean mask for the training set.
          Training and validation sets can be accessed by:
            - Training pair:   X[mask, :]  Y[mask, :]
            - Validation pair: X[~mask, :] Y[~mask, :]
    """
    # with open(path_pkl, 'rb') as f:
    #     pkl = pickle.load(f)
    np.random.seed(seed)

    path_pkls = []
    for root, dirs, files in os.walk(path_dir):
        for file in files:
            path_pkls.append(os.path.join(root, file))

    # Number of rows == total number of turns across all games
    n_rows = 0
    for path in path_pkls:
        print(path)
        with open(path, 'rb') as f:
            pkl = pickle.load(f)
        for game in range(len(pkl)):
            n_rows += len(pkl[game][0])

    glb.SIZE_ACT_VEC = len(pkl[game][1][0])
    X = np.zeros([n_rows, 1], dtype=object) # 0.5 gB
    Y = np.zeros([n_rows, glb.SIZE_ACT_VEC], dtype=np.int8) # 1.4 gB

    cur_idx = 0
    for path in path_pkls:
        print(path)
        with open(path, 'rb') as f:
            pkl = pickle.load(f)
        for game in range(len(pkl)):
            # Use arbitrary length python integer to store large ints
            obs = np.matrix(pkl[game][0], dtype=object).T
            act = np.matrix(pkl[game][1])
            X[cur_idx:(cur_idx + obs.shape[0]), :] = obs
            Y[cur_idx:(cur_idx + act.shape[0]), :] = act
            cur_idx += act.shape[0]
            assert(obs.shape[0] == act.shape[0])

    idx = np.random.choice(n_rows, int(n_rows * size_train) , replace=False)
    mask = np.full(n_rows, False)
    mask[idx] = True

    # TOTAL MEMORY: ~10 gB
    #   X: 0.5 + 7.5 gB
    #   Y: 1.4 gB
    return X, Y, mask