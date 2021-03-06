from gc import callbacks
from tqdm import tqdm

import sys
import os
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from commons.utils import FileSaver
from commons import saveModel
import numpy as np

def train(agent,
agent_type,
env,
actorCriticCheck=False,
batch_size=0,
episodes=50000,
print_every=10,
file_name=None,
callback=None,
timesteps=100000,
print_bool=False,
save_to_file_bool=True,
info_file_path='./'):
    """
    This function trains a specific agent and regulates the workflow of the overall application:
    agent: the agent object employed in the task.
    agent_type: string used to discriminate between agents' different implementations.
    env: specific environment object retrived by makeEnvironment.
    actorCriticCheck: bool to discriminate between A2C and REINFORCE. Fundamental since A2C policy updates are performed in batches.
    batch_size: int used to indicate the batch chunk size for A2C policy updates.
    episodes: number of training episodes.
    print_every: number of episodes to skip before printing to episode's return to standard output.
    file_name: if save_to_file_bool==True then saves the information in the file specified here via utils.FileSaver() object.
    callback: specific callback given to TRPO and PPO agents.
    timesteps: number of training timesteps for PPO and TRPO.
    print_bool: bool used to indicate wheather to print or not episode's return to standard output.
    save_to_file_bool: bool used to indicate if the current training process informations should be saved or not.
    info_file_path: file path for utils.FileSaver() object instantiation.
    """
    if agent_type.lower() == 'reinforce' or agent_type.lower() == 'actorcritic':
        if save_to_file_bool:
            files = [
                f'{file_name}_reward_file.txt',
                f'{file_name}_action_file.txt'
                ]
            fs_reward = FileSaver(file_name=files[0], path=info_file_path)
            fs_action = FileSaver(file_name=files[1], path=info_file_path)

            fs_reward.write_header("EpisodeID,Return\n")
            fs_action.write_header("EpisodeID,ActionMeasure\n")
    
        episodes_counter = 0
        timestep_counter = 0
        for episode in tqdm(range(episodes)):
            episode_return = 0
            episodes_counter += 1
            batch_counter = 0
            done = False
            train_reward = 0
            state = env.reset()

            timestep_per_episode = 0
            episode_actions = np.array([])
            while not done:
                batch_counter += 1
                timestep_counter += 1
                timestep_per_episode += 1
            
                action, action_probabilities = agent.get_action(state)

                episode_actions = np.append(episode_actions, action)

                previous_state = state

                state, reward, done, info = env.step(action.detach().cpu().numpy())
                agent.store_outcome(previous_state, state, action_probabilities, reward, done)

                train_reward += reward
                episode_return += reward

                if actorCriticCheck and batch_counter == batch_size: 
                    agent.update_policy()
                    agent.clear_history()
                    batch_counter = 0
                    continue
                
            if actorCriticCheck:
                agent.clear_history()

            if not actorCriticCheck: 
                agent.update_policy()

            if save_to_file_bool:
                action_derivative = np.diff(episode_actions.reshape(3, -1))
                action_measure = np.abs(action_derivative).max(axis = 0) - np.abs(action_derivative).min(axis = 0)
                action_measure = action_measure.max() - action_measure.min()

                fs_reward.append_content(f"{episodes_counter},{episode_return}\n")
                fs_action.append_content(f"{episodes_counter},{action_measure}\n")

            if print_bool:
                if (episode+1)%print_every == 0:
                    print('Training episode:', episode)
                    print('Episode return:', train_reward)

    elif agent_type == 'ppo' or agent_type == 'trpo':
        agent.learn(total_timesteps=timesteps, callback=callback)
        saveModel.save_model(agent=agent, agent_type=agent_type, folder_path=info_file_path)
