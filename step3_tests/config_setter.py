"""
This script creates a ParameterGrid object with all the possibile hyperparameters' configurations and saves them into trpo/.
"""

import json
import torch
import torch.nn as nn
from tqdm import tqdm
from sklearn.model_selection import ParameterGrid

def write_config(FILE_NAME, configurations):
	configuration={'configurations':[]}
	with open(FILE_NAME, "w") as f:
		for config in tqdm(configurations):
			configuration['configurations'].append(config)
		json.dump(configuration, f, indent=4)
		print(f"Total number of configurations: {len(configuration['configurations'])}")

TRPO_PARAMS = {
	'policy':['MlpPolicy'],
	'lr':[1e-3],
	'gamma':[0.998],
	'target_kl':[0.01],
	'timesteps':[100000],
	'activation_function':['tanh'],
	'batch_size':[128],
	'm1_low_bounds':[2, 4],
	'm1_high_bounds':[4.5, 5.5],
	'm2_low_bounds':[3, 7],
	'm2_high_bounds':[4.5, 10],
	'm3_low_bounds':[1.5, 5],
	'm3_high_bounds':[6, 9],
}

write_config("trpo/trpo.txt", ParameterGrid(TRPO_PARAMS))


