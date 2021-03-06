import time
import numpy as np
from .unity_env_provider import UnityEnvironmentProvider
from envs.base_env import BaseEnv
from gym import spaces, Wrapper, wrappers
import tempfile
import moviepy.editor as mpy
from skimage.transform import resize


class MLDriverEnvironment(BaseEnv):
    def __init__(self, env_name, id, seed, args):
        super().__init__(env_name, id)
        self.env = None
        self.default_brain = 'Brain_learning'
        self.make()
        self.seed = seed
        self.rewards = []
        self.summaries_dict = {'reward': 0, 'episode_length': 0}
        self.best_run_frames = []
        self.best_run_score = 0
        self.gif_created = False
        self.args = args
        self.skip = self.args['frames_skip']
        print(self.args)

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
            ss = resize(s, (64, 64))

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
            self.summaries_dict['reward'] = sum(self.rewards)
            self.summaries_dict['episode_length'] = len(self.rewards)

        info = self.summaries_dict

        return ss, r, is_done, info

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
        s = resize(s, (64, 64))

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
        filename = '{0}/score_{1}.gif'.format(
            self.args['experiment_dir'], self.best_run_score)
        clip.write_gif(filename, verbose=True)
