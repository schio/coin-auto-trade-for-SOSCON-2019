from agent.dqn_agent import DQNAgent
from function import *
import sys

if len(sys.argv) != 4:
	print("Usage: python train.py [stock] [window] [episodes]")
	exit()

stock_name, window_size, episode_count = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])

agent = DQNAgent(window_size)
data = getStockDataVec(stock_name)
len_data = len(data)
l = len(data) - 1
batch_size = 32

for e in range(episode_count + 1):
	print("Episode " + str(e) + "/" + str(episode_count))
	state = getState(data, 0, window_size + 1, len_data)
	total_profits = []
	total_profit = 0
	agent.inventory = []

	for t in range(l):
		action = agent.act(state)
		next_state = getState(data, t + 1, window_size + 1, len_data)
		reward = 0	

		if action == 1: # buy
			agent.inventory.append(data[t][1])
			total_profits.append(['buy', total_profit])
			print(f"Buy: {formatPrice(data[t][1])}\t{total_profits[-1][1]}")

		elif action == 2 and len(agent.inventory) > 0: # sell
			bought_price = inventory.inventory.pop(0)
			reward = max(data[t][1] - bought_price, 0)
			total_profit += data[t][1] - bought_price
			total_profits.append(['sell', total_profit])
			print(f"Sell: {formatPrice(data[t][1])}\t{total_profits[-1][1]}")
		
		# sit
		else:
			total_profits.append(['hold', total_profit])
			print(f"Hold: {formatPrice(data[t][1])}\t{total_profits[-1][1]}")

		done = True if t == l - 1 else False
		agent.memory.append((state, action, reward, next_state, done))
		state = next_state

		if done:
			print("--------------------------------")
			print("Total Profit: " + formatPrice(total_profit))
			print("--------------------------------")

		if len(agent.memory) > batch_size:
			agent.expReplay(batch_size)

	if e % 10 == 0:
		agent.model.save(f"models/model_ep_{str(e)}")