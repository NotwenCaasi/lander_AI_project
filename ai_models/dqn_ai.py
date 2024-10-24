# -*- coding: utf-8 -*-

# ai_models/dqn_ai.py

import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np

class DQNAI:
    def __init__(self, lander, planet, state_size, action_size, max_memory_size=10000):
        self.lander = lander
        self.planet = planet
        self.state_size = state_size
        self.thrust_bins = np.linspace(0, 1, 5)  # 5 discrete thrust levels (0 to 1)
        self.angle_bins = np.linspace(-15, 15, 5)  # 5 discrete angle changes (-15 to 15 degrees)

        self.action_size = len(self.thrust_bins) * len(self.angle_bins)  # Total number of discrete actions
        self.memory = []  # Replay memory
        self.max_memory_size = max_memory_size
        self.gamma = 0.95  # Discount factor
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.05
        self.epsilon_decay = 0.99995
        self.learning_rate = 0.0001
        self.batch_size = 128

        # Neural network model
        self.model = self._build_model()
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        self.loss_fn = nn.MSELoss()

    def _build_model(self):
        model = nn.Sequential(
            nn.Linear(self.state_size, 128),
            nn.ReLU(),
            nn.LayerNorm(128),  # Use LayerNorm instead of BatchNorm1d
            nn.Dropout(0.2),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.LayerNorm(128),  # Use LayerNorm here as well
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.LayerNorm(64),  # Use LayerNorm for this layer too
            nn.Linear(64, self.action_size)
        )
        return model

    def remember(self, state, action, reward, next_state, done):
        # Save experience to replay memory
        if len(self.memory) >= self.max_memory_size:
            self.memory.pop(0)
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        # Epsilon-greedy action selection
        if np.random.rand() <= self.epsilon:
            # Explore: select random actions
            thrust_idx = random.randint(0, len(self.thrust_bins) - 1)
            angle_idx = random.randint(0, len(self.angle_bins) - 1)
        else:
            # Exploit: select the best action based on predicted Q-values
            state_tensor = torch.FloatTensor(state).unsqueeze(0)
            with torch.no_grad():
                action_values = self.model(state_tensor).cpu().numpy()[0]
            
            # Get the index of the best action
            action_idx = np.argmax(action_values)
    
            # Convert the flat action index to thrust_idx and angle_idx
            thrust_idx = action_idx // len(self.angle_bins)
            angle_idx = action_idx % len(self.angle_bins)
    
        thrust = self.thrust_bins[thrust_idx]
        angle_change = self.angle_bins[angle_idx]
        return thrust, angle_change, thrust_idx, angle_idx


    def replay(self):
        if len(self.memory) < self.batch_size:
            return
        minibatch = random.sample(self.memory, self.batch_size)
    
        states = []
        targets = []
    
        for state, action, reward, next_state, done in minibatch:
            state_tensor = torch.FloatTensor(state)
            next_state_tensor = torch.FloatTensor(next_state)
            action_idx = action[0] * len(self.angle_bins) + action[1]  # Flattened action index
            
            target = reward
            if not done:
                with torch.no_grad():
                    target = reward + self.gamma * torch.max(self.model(next_state_tensor)).item()

            target_f = self.model(state_tensor).detach().numpy()
            
            # Update the Q-value for the chosen action
            target_f[action_idx] = target
    
            states.append(state_tensor)
            targets.append(torch.FloatTensor(target_f))
    
        states = torch.stack(states)
        targets = torch.stack(targets)
    
        self.optimizer.zero_grad()
        outputs = self.model(states)
        loss = self.loss_fn(outputs, targets)
        loss.backward()
        self.optimizer.step()
    
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


    def save(self, filepath):
        # Save the model parameters
        torch.save(self.model.state_dict(), filepath)

    def load(self, filepath):
        # Load the model parameters
        self.model.load_state_dict(torch.load(filepath))
