import pygame
from pygame import *
from pygame.locals import *
import sys
import os

import numpy as np 
import random

from snakegame import SnakeGame
from deep_q_learning import Agent

WIDTH = HEIGHT = 200
BLOCK_SIZE = 20

GAME_WIDTH  = GAME_HEIGHT = WIDTH // BLOCK_SIZE

NUM_GAMES = 100

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREY = (128, 128, 128)


def render(screen, game):
	screen.fill((BLACK))

	if not game.finished:
		for cell in game.snake.body:
			pygame.draw.rect(screen, GREEN, ((cell[0]) * BLOCK_SIZE, (cell[1]) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))	
		pygame.draw.rect(screen, BLUE, ((game.snake.x) * BLOCK_SIZE, (game.snake.y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
		pygame.draw.rect(screen, RED, ((game.food.loc[0]) * BLOCK_SIZE, (game.food.loc[1]) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
		
	pygame.display.flip()

	state = pygame.surfarray.array3d(pygame.transform.scale(screen, (30, 30)))

	return state


def main(load, iterations):
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Snake Game")
	clock = pygame.time.Clock()

	game = SnakeGame(GAME_WIDTH, GAME_HEIGHT)
	agent = Agent(gamma = 0.99, epsilon = 0.9, lr = 0.0002, input_dims = (30, 30, 3), n_actions = 4, memory_size = 50000, batch_size = 64)

	if load.lower() == "load":
		agent.load_model()
	elif load.lower() == "new":
		pass
	else:
		print("unknown command: ", load)
		return

	scores = []


	for episode in range(int(iterations)):
		game.reset()
		state = render(screen, game)
		score = 0
		finished = False
		print("start:", episode)
		while not finished:
			pygame.event.get()
			clock.tick()
			action = agent.choose_action(state)
			reward, finished = game.take_action(action)
			new_state = render(screen, game)
			score += reward
			agent.remember(transition = (state, action, reward, new_state, finished))
			state = new_state
			agent.learn()

		if episode % 10 == 0 and episode > 1:
			agent.save_model()

		scores.append(score)
		print(score)

	print(max(scores))
	print(len([score for score in scores if score >= 0]))
	pygame.quit()
	sys.exit()

		

if __name__ == "__main__":
	assert len(sys.argv) == 3
	name = sys.argv[0]
	load = sys.argv[1]
	iterations = sys.argv[2]
	main(load, iterations)