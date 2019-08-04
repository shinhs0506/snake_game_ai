import random

class Snake:
	def __init__(self, width, height):
		self.x = random.randint(0, width - 1)
		self.y = random.randint(0, height - 1)
		self.body = []
		self.body.insert(0, [self.x, self.y])
		self.direction = 2 
		self.live_MAX = (width * height) / 2
		self.live = self.live_MAX

class Food:
	def __init__(self, width, height):
		self.loc = [random.randint(0, width-1), random.randint(0, height-1)]
	
class SnakeGame:
	def __init__(self, game_width, game_height):
		self.width = game_width
		self.height = game_height
		self.snake = Snake(self.width, self.height)
		self.food = Food(self.width, self.height)
		self.finished = False

	def reset(self):
		self.snake = Snake(self.width, self.height)
		self.food = Food(self.width, self.height)

		# if food is in the body relocate the food
		while self.food.loc in self.snake.body:
			self.food = Food(self.width, self.height)

		self.direction = 1
		self.finished = False

	def take_action(self, action):
		new_head = []
		
		if action == 0:
			if self.snake.direction == 1 and len(self.snake.body) >= 2:
				new_head = [self.snake.x + 1, self.snake.y]
			else:
				new_head = [self.snake.x - 1, self.snake.y]
				self.snake.direction = 0
		elif action == 1:
			if self.snake.direction == 0 and len(self.snake.body) >= 2:
				new_head = [self.snake.x - 1, self.snake.y]
			else:
				new_head = [self.snake.x + 1, self.snake.y]
				self.snake.direction = 1
		elif action == 2:
			if self.snake.direction == 3 and len(self.snake.body) >= 2:
				new_head = [self.snake.x, self.snake.y + 1]
			else:
				new_head = [self.snake.x, self.snake.y - 1]
				self.snake.direction = 2
		else:
			if self.snake.direction == 2 and len(self.snake.body) >= 2:
				new_head = [self.snake.x, self.snake.y - 1]
			else:
				new_head = [self.snake.x, self.snake.y + 1]
				self.snake.direction = 3
			

		self.snake.live -= 1

		self.snake.x = new_head[0]
		self.snake.y = new_head[1]

		self.finished = self.is_finished(new_head) or self.snake.live == 0
		reward = self.get_reward(new_head)

		if self.finished:
			self.snake.body = []
		else:
			self.snake.body.insert(0, new_head)
			if reward == 1:
				print("eaten")
				self.snake.live = self.snake.live_MAX
				self.food = Food(self.width, self.height)
				while self.food.loc in self.snake.body:
					self.food = Food(self.width, self.height)
			else:
				self.snake.body.pop()

		return reward, self.finished

	def is_finished(self, new_head):
		return new_head[0] < 0 or new_head[0] >= self.width or new_head[1] < 0 or new_head[1] >= self.height or new_head in self.snake.body

	def get_reward(self, new_head):
		if self.finished:
			return -1
		elif new_head[0] == self.food.loc[0] and new_head[1] == self.food.loc[1]:
			return 1
		elif abs(new_head[0] - self.food.loc[0]) < abs(self.snake.body[0][0] - self.food.loc[0]) or abs(new_head[1] - self.food.loc[1]) < abs(self.snake.body[0][1] - self.food.loc[1]):
			return 0.05
		else:
			return -0.05




