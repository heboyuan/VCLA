import gym
import matplotlib.pyplot as plt
import keyboard
import time
import cv2

env = gym.make('EnduroDeterministic-v4').unwrapped

PhoenixActions = ['NOOP', 'FIRE', 'RIGHT', 'LEFT', 'DOWN', 'RIGHTFIRE', 'LEFTFIRE', 'DOWNFIRE']
EnduroActions = ['NOOP', 'FIRE', 'RIGHT', 'LEFT', 'DOWN', 'DOWNRIGHT', 'DOWNLEFT', 'RIGHTFIRE', 'LEFTFIRE']

ACTIONMAP = {
    "c"     : "NOOP",
    " " 	: "FIRE",
    "w"     : "UP",
    "d"     : "RIGHT",
    "a"     : "LEFT",
    "s"     : "DOWN",
    "q"     : "UPLEFT",
    "e"     : "UPRIGHT",
    "z"     : "DOWNLEFT",
    "x"     : "DOWNRIGHT",
    "i"		: "UPFIRE",
    "k"		: "DOWNFIRE",
    "o"		: "RIGHTFIRE",
    "u"		: "LEFTFIRE"
}

INPUTMAP = { val:i for i, val in enumerate(EnduroActions)}

def process_img(raw_rgb):
    raw_grey = cv2.cvtColor(raw_rgb, cv2.COLOR_RGB2GRAY)
    res_grey = cv2.resize(raw_grey, dsize=(84, 110), interpolation=cv2.INTER_NEAREST)
    chop_grey = res_grey[15:99,:]
    return chop_grey

def step(key):
    if key not in ACTIONMAP:
        print("Invalid Input")
        return None
    action = ACTIONMAP[key]
    if not action in INPUTMAP:
        print("Invalid Action")
        return None
    else:
        action = INPUTMAP[action]


    observation, reward, done, info = env.step(action)
    env.render()
    img = process_img(observation)


    print("==========================")
    print("reward: " + str(reward))
    print("life: " + str(info["ale.lives"]))
    print("\n")

    if done:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("done\n")
        keyboard.wait("enter")
        env.reset()
    return img


def main():
    plt.ion()
    img = process_img(env.reset())
    image = plt.imshow(img)
    plt.draw()
    while True:
        # event = keyboard.read_key()
        key = input()
        #print(key)
        image_data = step(key)
        if image_data is None:
            continue
        image.set_data(image_data)
        plt.draw()


main()
