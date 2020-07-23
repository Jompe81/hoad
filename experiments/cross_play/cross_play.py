import sys
from os.path import dirname as opd
from os.path import realpath as opr
sys.path.insert(0, opd(opd(opd(opr(__file__))))) # place /path/to/hoad/ in sys.path

import csv
import glob
import numpy as np
from experiments.cross_play.wrappers import create_agent_data
import argparse 

parser = argparse.ArgumentParser() 
parser.add_argument(
    '--num_games', '--n', type=int, default=50, 
    help='The number of games to run per agent-agent combo.') 
parser.add_argument(
    '--pattern', '--p', type=str, default='./best_models/*.h5', 
    help='A bash file pattern for the replica agent model files.')
               
args = parser.parse_args()


def cross_play(num_games, pattern):
    agents = glob.glob(pattern)
    agents.sort()
    full_score = 25
    score_matrix = []
    avg_scores = []
    for agent0 in agents:
        scores_list = []
        avg_list = []
        for agent1 in agents:
            scores = create_agent_data.DataCreator(num_games, agent0, agent1).create_data()
            scores_list.append(scores)
            avg_list.append(sum(scores) * 1.0 / num_games)
        score_matrix.append(scores_list)
        avg_scores.append(avg_list)

    return score_matrix, avg_scores, agents


if __name__ == "__main__":
    score_matrix, avg_scores, agent_names = cross_play(args.num_games, args.pattern)
    import pdb; pdb.set_trace()
    print(np.array(avg_scores), agent_names)
