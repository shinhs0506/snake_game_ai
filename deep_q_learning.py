from keras.layers import Dense, Activation, Dropout, Conv2D,  Flatten, MaxPooling2D
from keras.models import Sequential, load_model
from keras.optimizers import Adam
import numpy as np
from collections import deque
import random

'''
import os
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
'''

def build_dqn(lr, n_actions, input_dims):
    model = Sequential([
                Conv2D(16, (3, 3), strides = 3, input_shape = input_dims),
                Activation('relu'),
                Conv2D(32, (3, 3)),
                Activation('relu'),
                Flatten(),
                Dense(256),
                Activation('relu'),
                Dense(n_actions)])

    model.compile(optimizer=Adam(lr=lr), loss='mse')

    return model

class Agent(object):
    def __init__(self, lr, gamma, n_actions, epsilon, batch_size, input_dims, memory_size, epsilon_dec=0.998, epsilon_end=0.0, file_name='dqn_model.h5'):
        self.action_space = [i for i in range(n_actions)]
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_dec = epsilon_dec
        self.epsilon_min = epsilon_end
        self.batch_size = batch_size
        self.model_file = file_name
        self.memory = deque(maxlen=memory_size)
        self.model = build_dqn(lr, n_actions, input_dims)
        self.target_model = build_dqn(lr, n_actions, input_dims)
        self.target_model.set_weights(self.model.get_weights())
        self.nn_counter = 0
        self.nn_interval = 5

    def remember(self, transition):
        self.memory.append(transition)

    def choose_action(self, state):
        state = state[np.newaxis, : ]
        rand = np.random.random()
        if rand < self.epsilon:
            action = np.random.choice(self.action_space)
        else:
            actions = self.model.predict(state)
            action = np.argmax(actions)

        return action

    def learn(self):
        if len(self.memory) < self.batch_size:
        	return

        mini_batch = random.sample(self.memory, self.batch_size)

        states = np.array([transition[0] for transition in mini_batch])
        qs_list = self.model.predict(states)

        new_states = np.array([transition[3] for transition in mini_batch])
        new_qs_list = self.target_model.predict(new_states)

        x = []
        y = []

        for index, (state, action, reward, new_state, finished) in enumerate(mini_batch):
        	
        	new_q = reward + (self.gamma * np.max(new_qs_list[index]) * int(finished))
        	
        	qs = qs_list[index]
        	qs[action] = new_q

        	x.append(state)
        	y.append(qs)

        self.model.fit(np.array(x), np.array(y), verbose = 0)

        self.nn_counter += 1
        if self.nn_counter % self.nn_interval == 0 and self.nn_counter > 0:
        	self.target_model.set_weights(self.model.get_weights())


        self.epsilon = self.epsilon * self.epsilon_dec if self.epsilon > self.epsilon_min else self.epsilon_min

    def save_model(self):
        self.model.save(self.model_file)

    def load_model(self):
        self.model = load_model(self.model_file)
