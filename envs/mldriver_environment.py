import time
import numpy as np
from .unity_env_provider import UnityEnvironmentProvider
from envs.base_env import BaseEnv
from gym import spaces, Wrapper, wrappers
import tempfile
import moviepy.editor as mpy


class MLDriverEnvironment(BaseEnv):
    def __init__(self, env_name, id, seed):
        self.env_name = env_name
        self.rank = id
        self.env = None
        self.default_brain = 'Brain_learning'
        self.make()
        self.seed = seed
        self.skip = 5
        self.rewards = []
        self.summaries_dict = {'reward': 0, 'episode_length': 0}
        self.best_run_frames = []
        self.best_run_score = 0
        self.gif_created = False

    def make(self):
        env_provider = UnityEnvironmentProvider(
            'environments/mldriver-discrete-steering')
        env = env_provider.provide()
        self.env = env
        return env

    def step(self, action):

        skip_frames_count = 0
        
        while(skip_frames_count < self.skip):
            step_info = self.env.step([[action]])
            info = step_info[self.default_brain]
            r = info.rewards[0]
            s = info.visual_observations[0][0]
            is_done = info.local_done[0]
            frame = s * 255
            frame = frame.astype(int)
            self.best_run_frames.append(frame)
            self.rewards.append(r)
            skip_frames_count += 1
            if is_done:
                break
                print(len(self.best_run_frames))

        if is_done:
            print("Is Done")
            self.summaries_dict['reward'] = sum(self.rewards)
            self.summaries_dict['episode_length'] = len(self.rewards)

        info = self.summaries_dict

        return s, r, is_done, info

    def reset(self):

        print('cur score: {0} | best score: {1}'.format(
            sum(self.rewards), self.best_run_score))

        if sum(self.rewards) > self.best_run_score:
            self.best_run_score = sum(self.rewards)
            self.save_image()

        self.best_run_frames = []
        self.summaries_dict['reward'] = -1
        self.summaries_dict['episode_length'] = -1
        self.rewards = []

        config = {
            "reward": 1,
            "penalty": -15
        }

        info = self.env.reset(
            train_mode=True, config=config)[self.default_brain]
        s = info.visual_observations[0][0]

        return s

    def get_action_space(self):
        return spaces.Discrete(3)

    def get_observation_space(self):
        return spaces.Box(low=0, high=1, shape=(64, 64, 1))

    def monitor(
      self,
      is_monitor, is_train, experiment_dir="", record_video_every=2):
        raise NotImplementedError("monitor method is not implemented")

    def render(self):
        raise NotImplementedError("render method is not implemented")

    def save_image(self):
        clip = mpy.ImageSequenceClip(self.best_run_frames, fps=30)
        filename = 'records/score_{0}.gif'.format(self.best_run_score)
        clip.write_gif(filename, verbose=True)
