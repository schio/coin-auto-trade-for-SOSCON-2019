import sys
import gym
import pylab
import random
import numpy as np
from collections import deque
from keras.layers import Dense
from keras.optimizers import Adam
from keras.models import Sequential

class DQNAgent:
  def __init__(self, config, state_size, action_size):
    self.state_size = state_size
    self.action_size = action_size
    self.config = config
    print(config["dqn"]["epsilon"])

    self.discount_factor = self.config["dqn"]["discount_factor"]
    self.learning_rate = self.config["dqn"]["learning_rate"]
    self.epsilon = self.config["dqn"]["epsilon"]
    self.epsilon_decay = self.config["dqn"]["epsilon_decay"]
    self.epsilon_min = self.config["dqn"]["epsilon_min"]
    self.batch_size = self.config["dqn"]["batch_size"]
    self.train_start = self.config["dqn"]["train_start"]

    self.momory = deque(maxlen=2000)

    self.model = self.build_model()
    self.target_model = self.build_model()

    self.update_target_model()

  # 상태가 입력, 큐함수가 출력인 nn 생성
  def build_model(self):
    model = Sequential()
    # hidden unit size = 24
    model.add(Dense(24, input_dim=self.state_size, activation='relu',
                    kernel_initializer='he_uniform'))
    model.add(Dense(24, activation='relu',
                    kernel_initializer='he_uniform'))
    model.add(Dense(self.action_size, activation='relu',
                    kernel_initializer='he_uniform'))
    model.summary()
    model.compile(loss='rmse', optimizer=Adam(lr=self.learning_rate))

  def update_target_model(self):
    self.target_model.set_weights(self.model.get_weights())

  def get_action(self, state):
    if np.random.rand() <= self.epsilon:
      return random.randrange(self.action_size)
    else:
      q_value = self.model.predict(state)
      return np.argmax(q_value[0])

  def append_sample(self, state, action, reward, next_state, done):
      self.memory.append((state, action, reward, next_state, done))

  def train_model(self):
    if self.epsilon > self.epsilon_min:
        self.epsilon *= self.epsilon_decay

    # 메모리에서 배치 크기만큼 무작위로 샘플 추출
    mini_batch = random.sample(self.memory, self.batch_size)

    states = np.zeros((self.batch_size, self.state_size))
    next_states = np.zeros((self.batch_size, self.state_size))
    actions, rewards, dones = [], [], []

    for i in range(self.batch_size):
        states[i] = mini_batch[i][0]
        actions.append(mini_batch[i][1])
        rewards.append(mini_batch[i][2])
        next_states[i] = mini_batch[i][3]
        dones.append(mini_batch[i][4])

    # 현재 상태에 대한 모델의 큐함수
    # 다음 상태에 대한 타깃 모델의 큐함수
    target = self.model.predict(states)
    target_val = self.target_model.predict(next_states)

    # 벨만 최적 방정식을 이용한 업데이트 타깃
    for i in range(self.batch_size):
        if dones[i]:
            target[i][actions[i]] = rewards[i]
        else:
            target[i][actions[i]] = rewards[i] + self.discount_factor * (
                np.amax(target_val[i]))

    self.model.fit(states, target, batch_size=self.batch_size,
                    epochs=1, verbose=0)