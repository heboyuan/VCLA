import time
import cv2
import gym
import random
import numpy as np
import sys

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

env = gym.make('EnduroDeterministic-v4').unwrapped

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

EXPLORE = 0
NOOP = 1

N_ACTIONS = env.action_space.n


def process_img(raw_rgb):
    raw_grey = cv2.cvtColor(raw_rgb, cv2.COLOR_RGB2GRAY)
    res_grey = cv2.resize(raw_grey, dsize=(84, 110), interpolation=cv2.INTER_NEAREST)
    chop_grey = res_grey[15:99,:]
    return chop_grey

# class Cov_net(nn.Module):

#     def __init__(self):
#         super(Cov_net, self).__init__()
#         self.conv1 = nn.Conv2d(4, 32, kernel_size=8, stride=4)
#         nn.init.xavier_uniform_(self.conv1.weight)
#         self.conv2 = nn.Conv2d(32, 64, kernel_size=4, stride=2)
#         nn.init.xavier_uniform_(self.conv2.weight)
#         self.conv3 = nn.Conv2d(64, 64, kernel_size=3, stride=1)
#         nn.init.xavier_uniform_(self.conv3.weight)
#         self.lin4 = nn.Linear(3136, 512)
#         nn.init.xavier_uniform_(self.lin4.weight)
#         self.lin5 = nn.Linear(512, N_ACTIONS)
#         nn.init.xavier_uniform_(self.lin5.weight)



#     def forward(self, x):
#         x = F.relu(self.conv1(x.cuda()))
#         x = F.relu(self.conv2(x))
#         x = F.relu(self.conv3(x))
#         x = F.relu(self.lin4(x.view(x.size(0), -1)))
#         x = self.lin5(x)
#         return x

class Cov_net(nn.Module):

    def __init__(self):
        super(Cov_net, self).__init__()
        self.conv1 = nn.Conv2d(4, 32, kernel_size=8, stride=4)
        nn.init.xavier_uniform_(self.conv1.weight)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=4, stride=2)
        nn.init.xavier_uniform_(self.conv2.weight)
        self.conv3 = nn.Conv2d(64, 64, kernel_size=3, stride=1)
        nn.init.xavier_uniform_(self.conv3.weight)
        
        self.lin4_adv = nn.Linear(3136, 512)
        self.lin5_adv = nn.Linear(512, N_ACTIONS)

        self.lin4_val = nn.Linear(3136, 512)
        self.lin5_val = nn.Linear(512, 1)


    def forward(self, x):
        x = F.relu(self.conv1(x.cuda()))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = x.view(x.size(0), -1)
        
        x_adv = F.relu(self.lin4_adv(x))
        x_adv = self.lin5_adv(x_adv)

        x_val = F.relu(self.lin4_val(x))
        x_val = self.lin5_val(x_val)

        return x_val.expand_as(x_adv) + x_adv - x_adv.mean(1).unsqueeze(1).expand_as(x_adv)


policy_net = Cov_net().to(device)
policy_net.load_state_dict(torch.load(sys.argv[1])["policy_net"])


def select_action(state):
    eps_threshold = 1 - EXPLORE
    if random.random() >= eps_threshold:
        return random.randrange(N_ACTIONS)
    else: 
        with torch.no_grad():
            state = torch.from_numpy(state.astype(np.float32)/255.0).unsqueeze(0)
            return policy_net(state).max(1)[1].item()


def main():
    episode_count = 0
    reward_count = 0
    done = True
    cur_life = 0
    while True:
        env.reset()
        cur_life = env.ale.lives()
        env.step(1)

        states = []
        if done:
            no_op = random.randint(0, NOOP - 1)
            for i in range(no_op):
                if no_op - i <= 4:
                    states.append(process_img(env.step(0)[0]))
                else:
                    env.step(0)
        for _ in range(4 - len(states)):
            states.append(process_img(env.step(random.randint(0, N_ACTIONS-1))[0]))
        state = np.array(states, dtype=np.uint8)

        while True:
            time.sleep(0.02)
            env.render()
            action = select_action(state)
            observation, reward, done, info = env.step(action)
            states.pop(0)
            states.append(process_img(observation))
            new_life = info["ale.lives"]
            reward_count += reward


            if cur_life != new_life and not done:
                env.step(1)
            next_state = np.array(states, dtype=np.uint8)           


            state = next_state
            cur_life = new_life


            if done:
                episode_count += 1
                print(reward_count/episode_count)
                print(episode_count)
                break
        

    print('Complete')
    env.close()

main()
