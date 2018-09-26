from matplotlib import pyplot as plt

import cv2
import gym
import random
import numpy as np

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

env = gym.make('PhoenixDeterministic-v4').unwrapped

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if torch.cuda.is_available():
    print("GPU")
else:
    print("CPU")


BATCH_SIZE = 32
GAMMA = 0.99

LEARNING_START = 50000

OPTIMIZE_FREQUENCY = 1
TARGET_UPDATE = 10000
EXPLORE_REDUCE_RATE = 0.0000009
REPLAY_MEMORY_SIZE = 500000

NOOP = 13
# LEARNING_RATE = 0.0001
LEARNING_RATE = 0.00001
N_ACTIONS = env.action_space.n

print(env.get_action_meanings())

def process_img(raw_rgb):
    raw_grey = cv2.cvtColor(raw_rgb, cv2.COLOR_RGB2GRAY)
    res_grey = cv2.resize(raw_grey, dsize=(84, 110), interpolation=cv2.INTER_NEAREST)
    chop_grey = res_grey[15:99,:]
    return chop_grey

class ReplayMemory(object):
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.position = 0

    def populate(self, populate_count):
        frame_count = 0
        done = True
        cur_life = 0
        while True:
            env.reset()
            cur_life = env.ale.lives()
            # only needed for breakout====================================
            # env.step(1)

            states = []
            if done:
                no_op = random.randint(0, NOOP - 1)
                for i in range(no_op):
                    if no_op - i <= 4:
                        observation, _, _, _ = env.step(0)
                        states.append(process_img(observation))
                    else:
                        env.step(0)
            for _ in range(4 - len(states)):
                states.append(process_img(env.step(random.randint(0, N_ACTIONS-1))[0]))
            state = np.array(states, dtype=np.uint8)


            while True:
                frame_count += 1
                action = random.randrange(N_ACTIONS)
                observation, reward, done, info = env.step(action)
                reward = np.clip(reward,-1,1)
                states.pop(0)
                states.append(process_img(observation))
                new_life = info["ale.lives"]

                if cur_life == new_life:
                    next_state = np.array(states, dtype=np.uint8)
                    next_save_state = next_state
                elif not done:
                    next_state = np.array(states, dtype=np.uint8)
                    next_save_state = None
                    # only needed for breakout====================================
                    # env.step(1)
                else:
                    next_save_state = None

                self.push(state, action, next_save_state, reward)

                state = next_state
                cur_life = new_life
                
                if frame_count == populate_count:
                    return
                if done:
                    break


    def push(self, state, action, next_state, reward):
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        self.memory[self.position] = (state, action, next_state, reward)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)



class Cov_net(nn.Module):

    def __init__(self):
        super(Cov_net, self).__init__()
        self.conv1 = nn.Conv2d(4, 32, kernel_size=8, stride=4)
        nn.init.xavier_uniform_(self.conv1.weight)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=4, stride=2)
        nn.init.xavier_uniform_(self.conv2.weight)
        self.conv3 = nn.Conv2d(64, 64, kernel_size=3, stride=1)
        nn.init.xavier_uniform_(self.conv3.weight)
        self.lin4 = nn.Linear(3136, 512)
        nn.init.xavier_uniform_(self.lin4.weight)
        self.lin5 = nn.Linear(512, N_ACTIONS)
        nn.init.xavier_uniform_(self.lin5.weight)



    def forward(self, x):
        x = F.relu(self.conv1(x.cuda()))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = F.relu(self.lin4(x.view(x.size(0), -1)))
        x = self.lin5(x)
        return x


policy_net = Cov_net().to(device)
target_net = Cov_net().to(device)
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

optimizer = optim.Adam(policy_net.parameters(), lr = LEARNING_RATE)
memory = ReplayMemory(REPLAY_MEMORY_SIZE)

log_file = open('./Double_log', 'w+')


steps_done = 0
def select_action(state):
    global steps_done
    if steps_done < 1000000:
        eps_threshold = steps_done*EXPLORE_REDUCE_RATE
    elif steps_done < 24000000:
        eps_threshold = (steps_done - 1000000)*0.000000003913+0.9
    else:
        eps_threshold = 0.99
    steps_done += 1
    if random.random() >= eps_threshold:
        return random.randrange(N_ACTIONS)
    else: 
        with torch.no_grad():
            state = torch.from_numpy(state.astype(np.float32)/255.0).unsqueeze(0)
            return policy_net(state).max(1)[1].item()


def optimize_model():
    if len(memory) < BATCH_SIZE:
        return
    batch = memory.sample(BATCH_SIZE)

    raw_state_batch = [row[0] for row in batch]
    np_state_batch = np.stack(raw_state_batch).astype(np.float32)/255.0
    state_batch = torch.from_numpy(np_state_batch)

    action_batch = torch.tensor([[row[1]] for row in batch], device=device)
    reward_batch = torch.tensor([row[3] for row in batch], device=device)

    raw_next_state_batch = [row[2] for row in batch if row[2] is not None]
    np_next_state_batch = np.stack(raw_next_state_batch).astype(np.float32)/255.0
    next_state_batch = torch.from_numpy(np_next_state_batch)

    mask = torch.tensor(tuple(map(lambda s: s is not None, [row[2] for row in batch])), device=device, dtype=torch.uint8)

    state_action_values = policy_net(state_batch).gather(1, action_batch)

    next_state_values = torch.zeros(BATCH_SIZE, device=device)
    target_policy_evaluation = policy_net(next_state_batch).detach()
    target_policy_evaluation = target_policy_evaluation.max(1)[1].unsqueeze(1)
    next_state_estimate = target_net(next_state_batch).detach()
    next_state_values[mask] = next_state_estimate.gather(1, target_policy_evaluation).squeeze()

    expected_state_action_values = (next_state_values * GAMMA) + reward_batch

    loss_fn = torch.nn.SmoothL1Loss()
    loss = loss_fn(state_action_values, expected_state_action_values.unsqueeze(1))

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()


def main():
    #save_score = 250
    episode_count = 0

    memory.populate(LEARNING_START)
    print("finish populate: " + str(len(memory)))

    frame_count = 0
    reward_count = 0
    done = True
    cur_life = 0
    while True:
        env.reset()
        cur_life = env.ale.lives()
        # only needed for breakout====================================
        # env.step(1)

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
            frame_count += 1
            action = select_action(state)
            observation, reward, done, info = env.step(action)
            reward_count += reward
            reward = np.clip(reward,-1,1)
            states.pop(0)
            states.append(process_img(observation))
            new_life = info["ale.lives"]



            if cur_life == new_life:
                next_state = np.array(states, dtype=np.uint8)
                next_save_state = next_state
            elif not done:
                next_state = np.array(states, dtype=np.uint8)
                next_save_state = None
                # only needed for breakout====================================
                # env.step(1)
            else:
                next_save_state = None

            memory.push(state, action, next_save_state, reward)

            state = next_state
            cur_life = new_life

            if frame_count % OPTIMIZE_FREQUENCY == 0:
                optimize_model()

            if frame_count % TARGET_UPDATE == 0:
                target_net.load_state_dict(policy_net.state_dict())

            if frame_count % 1000000 == 0:
                print("========== " + str(frame_count/1000000) + " Million Frames ==========")

            if frame_count % 250000 == 0:
                episode_reward = reward_count/episode_count
                print(episode_reward)
                # if episode_reward > save_score:
                #     model_state = {
                #         "policy_net": policy_net.state_dict(),
                #         "target_net": target_net.state_dict(),
                #         "optimizer": optimizer.state_dict(),
                #         "frames": frame_count
                #     }
                #     torch.save(model_state, "DDQN_model_"+str(save_score))
                #     save_score += 20
                log_file.write(str(episode_reward) + '\n')
                log_file.flush()
                reward_count = 0
                episode_count = 0

            if done:
                episode_count += 1
                break
        

    print('Complete')
    log_file.close()
    env.close()

main()
