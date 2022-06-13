import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

ALGS = [
    "actorcritic",
    "reinforce"
]

seedless_df_a2c_rewards = pd.read_csv(f"seedless_{ALGS[0]}_rewards.txt")
seedless_df_reinforce_rewards = pd.read_csv(f"seedless_{ALGS[1]}_rewards.txt")

seedless_df_a2c_actions = pd.read_csv(f"seedless_{ALGS[0]}_actions.txt")
seedless_df_reinforce_actions = pd.read_csv(f"seedless_{ALGS[1]}_actions.txt")

fig1 = plt.figure(figsize=(24,12))

plot = sns.lineplot(x=seedless_df_a2c_rewards.iloc[:, 0], y=seedless_df_a2c_rewards.iloc[:, 1], data=seedless_df_a2c_rewards)
plot = sns.lineplot(x=seedless_df_reinforce_rewards.iloc[:, 0], y=seedless_df_reinforce_rewards.iloc[:, 1], data=seedless_df_reinforce_rewards)

plot.set_xlabel("Timestep")
plot.set_ylabel("Reward")
plot.set(title=f"Reward per timesteps")
plot.lines[0].set_linestyle("--")
plot.lines[0].set_label("a2c")
plot.lines[1].set_linestyle("dotted")
plot.lines[1].set_label("reinforce")
plot.collections[0].set_label(None)
plot.collections[1].set_label(None)
plt.legend()
plt.savefig("reward_per_timestep.png")
plt.close(fig1)


fig2 = plt.figure(figsize=(24,12))

action_plot = sns.lineplot(x=seedless_df_a2c_actions.iloc[:, 0], y=seedless_df_a2c_actions.iloc[:, 1], data=seedless_df_a2c_actions)
action_plot = sns.lineplot(x=seedless_df_reinforce_actions.iloc[:, 0], y=seedless_df_reinforce_actions.iloc[:, 1], data=seedless_df_reinforce_actions)

action_plot.set_xlabel("Episode")
action_plot.set_ylabel("ActionMeasure")
action_plot.set(title="ActionMeasure per episode")

action_plot.lines[0].set_linestyle("--")
action_plot.lines[0].set_label("a2c")
action_plot.lines[1].set_linestyle("dotted")
action_plot.lines[1].set_label("reinforce")
action_plot.collections[0].set_label(None)
action_plot.collections[1].set_label(None)

plt.legend()
plt.savefig("action_measure_per_episode.png")
plt.close(fig2)