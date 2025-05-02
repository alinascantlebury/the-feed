import gymnasium as gym
from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_atari_env
from stable_baselines3.common.vec_env import VecFrameStack
from huggingface_hub import login
from dotenv import load_dotenv
import os

load_dotenv()

try:
    import cv2
    import tensorboard
except ImportError:
    os.system("pip install opencv-python tensorboard")
    import cv2
    import tensorboard

login(token=os.getenv("HF_TOKEN"))

env_id = "Breakout-v4"
env = make_atari_env(
    env_id,
    n_envs=1,
    seed=42,
    wrapper_kwargs={
        "clip_reward": True,
        "terminal_on_life_loss": True
    }
)
env = VecFrameStack(env, n_stack=4)

model = DQN(
    "CnnPolicy",
    env,
    verbose=1,
    learning_rate=1e-4,
    buffer_size=100000,
    learning_starts=10000,
    batch_size=32,
    gamma=0.99,
    train_freq=4,
    gradient_steps=1,
    target_update_interval=10000,
    exploration_fraction=0.1,
    exploration_initial_eps=1.0,
    exploration_final_eps=0.01,
    tensorboard_log="./dqn_breakout_tensorboard/",
    device="auto"
)

print("Starting training...")
model.learn(
    total_timesteps=100000,
    progress_bar=True,
    log_interval=10
)

model.save("dqn_breakout")
print("Training completed successfully!")

if os.getenv("HF_TOKEN"):
    repo_id = "ascant/dqn-breakout"  # Change to your username
    model.push_to_hub(
        repo_id=repo_id,
        commit_message="Initial release of DQN Breakout agent",
        private=False
    )
    print(f"Model published to https://huggingface.co/{repo_id}")
else:
    print("HF_TOKEN not found in .env file - skipping Hub upload")

