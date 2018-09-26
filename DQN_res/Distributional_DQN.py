import cv2
import gym
import math
import random
import numpy as np

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T
from torch.autograd import Variable

env = gym.make('Breakout-v0').unwrapped

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if torch.cuda.is_available():
    print("GPU")
else:
    print("CPU")



BATCH_SIZE = 32
GAMMA = 0.99
# !!! Different from the paper due to computing power !!!
# TARGET_UPDATE = 10000
TARGET_UPDATE = 100
# NUM_EPISODES = 50000000
NUM_EPISODES = 50000
# LR_REDUCE_RATE = 0.0000009
LR_REDUCE_RATE = 0.0009
#REPLAY_MEMORY_SIZE = 1000000
REPLAY_MEMORY_SIZE = 40000
# !!! Different from the paper due to computing power !!!
LEARNING_RATE = 0.00025
N_ACTIONS = env.action_space.n
N_STATES = env.observation_space.shape[0]

N_ATOMS = 51
V_MIN = -10
V_MAX = 10
DELTA_Z = (V_MAX - V_MIN)/(N_ATOMS-1)
DIS_WEIGHT = torch.FloatTensor(np.linspace(V_MIN, V_MAX, N_ATOMS)).view(1, 1, N_ATOMS).cuda()


# memory format
# [
#   [state_tensor, action_tensor, next_state_tensor, reward_tensor]
#   [state_tensor, action_tensor, next_state_tensor, reward_tensor]
#   ...
# ]
# state_tensor & next_state_tensor - 1*4*84*84
# action_tensor - 1*1 ex.[[1]]
# reward_tensor - 1 ex.[0]

class ReplayMemory(object):
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.position = 0

    def push(self, *args):
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        self.memory[self.position] = [*args]
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


class Cov_net(nn.Module):

    def __init__(self):
        super(Cov_net, self).__init__()
        self.conv1 = nn.Conv2d(4, 32, kernel_size=8, stride=4)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=4, stride=2)
        self.bn2 = nn.BatchNorm2d(64)
        self.conv3 = nn.Conv2d(64, 64, kernel_size=3, stride=1)
        self.bn3 = nn.BatchNorm2d(64)
        self.lin4 = nn.Linear(3136, 512)
        self.lin5 = nn.Linear(512, N_ATOMS*N_ACTIONS)


    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x.cuda())))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))
        x = F.relu(self.lin4(x.view(x.size(0), -1)))
        x = self.lin5(x)

        #Batch*N_ACTION*N_ATOMS
        return F.softmax(x.view(-1, N_ACTIONS, N_ATOMS), dim = 2)




env.reset()

policy_net = Cov_net().to(device)
target_net = Cov_net().to(device)
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

optimizer = optim.Adam(policy_net.parameters(), lr = LEARNING_RATE)

memory = ReplayMemory(REPLAY_MEMORY_SIZE)

log_file = open('Distributional_DQN_log', 'w+')

steps_done = 0
def select_action(state):
    global steps_done
    sample = random.random()
    eps_threshold = steps_done*LR_REDUCE_RATE
    steps_done += 1
    if sample >= eps_threshold:
        return torch.tensor([[random.randrange(N_ACTIONS)]], device=device, dtype=torch.long)
    else: 
        with torch.no_grad():
            return (policy_net(state)*DIS_WEIGHT).sum(dim=2).max(1)[1].view(1,1)   


def optimize_model():
    if len(memory) < BATCH_SIZE:
        return
    batch = memory.sample(BATCH_SIZE)

    state_batch = torch.cat([row[0] for row in batch])
    action_batch = torch.cat([row[1] for row in batch])
    reward_batch = torch.stack([row[3] for row in batch])
    next_state_batch = torch.cat([row[2] for row in batch if row[2] is not None])
    mask = torch.tensor(tuple(map(lambda s: s is not None, [row[2] for row in batch])), device=device, dtype=torch.uint8)

    #Batch*N_ATOMS
    state_action_values = policy_net(state_batch).gather(1, action_batch.unsqueeze(2).expand(BATCH_SIZE, 1, N_ATOMS)).squeeze()

    #Batch*N_ATOMS
    next_state_values = torch.zeros((BATCH_SIZE,N_ATOMS), device=device) + 1/N_ATOMS
    #Next_batch*N_ACTIONS*N_ATOMS                                           ^----------reconsider!!!!!!!!!!
    raw_next_state_value = target_net(next_state_batch).detach()
    optimal_next_action= (raw_next_state_value*DIS_WEIGHT).sum(dim=2).max(1)[1].view(raw_next_state_value.size(0),1,1).expand(-1,-1,N_ATOMS)
    #Batch*N_ATOMS
    next_state_values[mask] = raw_next_state_value.gather(1, optimal_next_action).squeeze()

    Tz = GAMMA*DIS_WEIGHT.squeeze(0)*mask.float().unsqueeze(1)
    Tz = Tz + reward_batch
    Tz = Tz.clamp(V_MIN, V_MAX)
    b = (Tz - V_MIN)/DELTA_Z
    l = b.floor().long()
    u = b.ceil().long()
    m_l = (u.float() + (l == u).float() - b)*next_state_values
    m_u = (b - l.float())*next_state_values
    m = torch.zeros((BATCH_SIZE, N_ATOMS), device=device)
    
    for i in range(BATCH_SIZE):
        m[i].index_add_(0, l[i], m_l[i])
        m[i].index_add_(0, u[i], m_u[i])

    loss = -(Variable(m).cuda() * state_action_values.log()).sum(-1).mean()

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()


def process_img(raw_rgb):
    raw_grey = np.dot(raw_rgb[...,:3], [0.299, 0.587, 0.114])
    res_grey = cv2.resize(raw_grey, dsize=(84, 110), interpolation=cv2.INTER_NEAREST)
    chop_grey = res_grey[13:97,:]
    return chop_grey

def main():
    reward_count = 0
    for i_episode in range(NUM_EPISODES):
        states = [torch.FloatTensor(process_img(env.reset()), device=device)]
        for _ in range(3):
            states.append(torch.FloatTensor(process_img(env.step(random.randint(0, N_ACTIONS-1))[0]), device=device))
        state = torch.stack(states).unsqueeze(0)

        test_cout = 0
        while True:
            test_cout += 1
            action = select_action(state)
            observation, reward, done, _ = env.step(action.item())
            reward_count += reward
            reward = torch.tensor([reward], device=device)
            
            if test_cout == 3000:
                print('start debug')
            
            if test_cout > 3000 and action.item() == 1:
                print('fired')


            states.pop(0)
            states.append(torch.FloatTensor(process_img(observation), device=device))

            if not done:
                next_state = torch.stack(states).unsqueeze(0)
            else:
                next_state = None

            memory.push(state, action, next_state, reward)

            state = next_state

            optimize_model()
            if done:
                #print('updates  '+str(test_cout))
                #print('reward   '+str(reward_count) + '\n')
                #reward_count = 0
                break

        if i_episode % 10 == 0:
            print(reward_count)
            log_file.write(str(reward_count) + '\n')
            reward_count = 0
        if i_episode % 100 == 0:
            log_file.flush()
        if i_episode % TARGET_UPDATE == 0:
            target_net.load_state_dict(policy_net.state_dict())

    print('Complete')
    log_file.close()
    env.close()

main()
