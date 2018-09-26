import cv2
import gym
import numpy as np
from random import randint

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

env = gym.make('BreakoutDeterministic-v4').unwrapped

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if torch.cuda.is_available():
    print("GPU")
else:
    print("CPU")

N_ACTIONS = env.action_space.n
print(env.get_action_meanings())

N_STEPS = 5
LOG_FRAME = 10000
LEARNING_RATE = 7e-6
GAMMA = 0.99
ENTROPY_COEF = 0.01
VALUE_LOSS_COEF = 1
TD_LAMBDA = 0.99
MAX_GRAD_NORM = 40

def process_img(raw_rgb):
    raw_grey = cv2.cvtColor(raw_rgb, cv2.COLOR_RGB2GRAY)
    res_grey = cv2.resize(raw_grey, dsize=(84, 110), interpolation=cv2.INTER_NEAREST)
    chop_grey = res_grey[21:105, :]
    return chop_grey


log_file = open('./A2C_log', 'w+')


def print_log(reward_count, episode_count, frame_count):
    episode_reward = reward_count / episode_count
    print(reward_count)
    print(episode_reward)
    log_file.write(str(episode_reward) + '\n')
    log_file.flush()
    print("========== " + str(frame_count) + " Frames ==========")

def layer_init(layer, w_scale=np.sqrt(2.)):
    nn.init.orthogonal_(layer.weight.data)
    layer.weight.data.mul_(w_scale)
    nn.init.constant_(layer.bias.data, 0)
    return layer

class ActorCritic(nn.Module):


    def __init__(self):
        super(ActorCritic, self).__init__()
        self.conv1 = layer_init(nn.Conv2d(1, 16, kernel_size=8, stride=4))
        self.conv2 = layer_init(nn.Conv2d(16, 32, kernel_size=4, stride=2))
        self.lin3 = layer_init(nn.Linear(32 * 9 * 9, 256))

        self.policy = layer_init(nn.Linear(256, N_ACTIONS), 1e-2)
        self.v = layer_init(nn.Linear(256, 1), 1)



    def forward(self, x):
        x = F.relu(self.conv1(x.cuda()))
        x = F.relu(self.conv2(x))
        x = F.relu(self.lin3(x.view(x.size(0), -1)))

        pi = self.policy(x)
        v = self.v(x)

        return pi, v


AC_net = ActorCritic().to(device)
AC_net.eval()

optimizer = optim.RMSprop(AC_net.parameters(), lr=LEARNING_RATE)

def train():
    done = True
    log_frame = LOG_FRAME
    frame_count = 0
    reward_count = 0
    episode_count = 0

    while True:
        values = []
        log_probs = []
        entropies = []
        rewards = []

        if done:
            episode_count += 1
            if frame_count > log_frame:
                print_log(reward_count, episode_count, frame_count)
                reward_count = 0
                episode_count = 0
                log_frame += LOG_FRAME

            state = process_img(env.reset())/255.0
            cur_life = env.ale.lives()
            new_life = env.ale.lives()
            done = False

        # breakout only ==========
        state = process_img(env.step(1)[0])/255.0
        # breakout only ==========

        for step in range(N_STEPS):
            frame_count += 1

            policy, value = AC_net(torch.FloatTensor(state, device=device).unsqueeze(0).unsqueeze(0))
            policy, value = policy.squeeze(), value.squeeze()


            prob = F.softmax(policy, dim=0)
            log_prob = F.log_softmax(policy, dim=0)

            entropy = (log_prob * prob).sum()

            # action = torch.tensor(randint(0,3), device=device)
            action = prob.multinomial(num_samples=1).detach()
            log_prob = log_prob.gather(0, action).squeeze()

            state, reward, done, info = env.step(action.cpu().numpy())
            reward = np.clip(reward, -1, 1)
            reward_count += reward
            state = process_img(state)/255.0
            new_life = info["ale.lives"]

            values.append(value)
            entropies.append(entropy)
            log_probs.append(log_prob)
            rewards.append(reward)

            # env.render()

            if new_life != cur_life:
                break
            # if done:
            #     break

        if new_life == cur_life:
            _, value = AC_net(torch.FloatTensor(state, device=device).unsqueeze(0).unsqueeze(0))
            final_reward = value.squeeze().detach()
        else:
            final_reward = torch.tensor(0.0).cuda()
            cur_life = new_life
        values.append(final_reward)

        policy_loss = 0
        value_loss = 0
        R = final_reward
        GAE = torch.tensor(0.0).cuda()
        for i in range(len(rewards) - 1, -1, -1):
            R = GAMMA * R + rewards[i]
            value_loss += 0.5*(R - values[i]).pow(2)

            TD_error = GAMMA * values[i + 1].detach() + rewards[i] - values[i].detach()
            GAE = GAE * GAMMA * TD_LAMBDA + TD_error
            policy_loss -= log_probs[i] * GAE - ENTROPY_COEF * entropies[i]

            # policy_loss = R.detach() - values[i].detach()

        optimizer.zero_grad()
        loss = policy_loss + VALUE_LOSS_COEF * value_loss
        loss.backward()
        nn.utils.clip_grad_norm_(AC_net.parameters(), MAX_GRAD_NORM)
        optimizer.step()

train()