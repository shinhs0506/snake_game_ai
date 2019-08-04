# snake_game_ai
snake game ai using Keras implementation of deep-q-learning

Game
  - snake game built using pygame module
  - 20x20 grid with blue = head
                    green = body
                    red = food

Neural Network
  - 2 conv2d layers with 1 fully connected hidden layer.
  - takes 30x30 resized raw pixel data as input and outputs 4 values, each representing the 4 directions a snake can move
  - predicts the next move that maximizes the reward 
  
Overview of the game mechanics and deep-q-learning
 <during each move in a game>
  - the neural network evaluates the state and predicts the best possible move
  - the snake receives the following points as rewards food eaten = 1
                                                       moved closer to the food = 0.05
                                                       moved further away from the food = -0.05
                                                       dead = -1                                                       
  - the state, the reward the snake received, the next outcome state, and whether the snake died or not gets recorded in memory
  - the network is trained on batch of size 64 randomly chosed from the memory 
 <above process repeats until the snake dies>
