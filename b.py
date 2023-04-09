import pygame
import random
import math
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import legacy
from tensorflow.keras.models import load_model
from collections import deque


model = Sequential([
    Dense(128, input_shape=(12,), activation='relu'),
    Dense(128, activation='relu'),
    Dense(4, activation='linear')
])
# model.save(r'C:\Users\samsu\model\snake.h5')
model = load_model(r'C:\Users\samsu\model\snake.h5')
model.compile(loss='mse', optimizer=legacy.Adam(learning_rate=0.01))

clock = pygame.time.Clock()
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
SNAKE_SIZE = 20
REWARD = 10
REPLAY_MEMORY_SIZE = 100000
DISCOUNT_FACTOR = 0.99
BATCH_SIZE = 128
score = 0
replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)
distance_to_wall =0
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.init()
snake = [(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)]
direction = random.choice(['up', 'down', 'left', 'right'])
food = (random.randint(0, WINDOW_WIDTH // SNAKE_SIZE - 1) * SNAKE_SIZE, 
        random.randint(0, WINDOW_HEIGHT // SNAKE_SIZE - 1) * SNAKE_SIZE)








state = np.array([snake[0][0], snake[0][1], food[0], food[1], 
                  int(direction == 'up'), int(direction == 'down'), 
                  int(direction == 'left'), int(direction == 'right'), 
                  snake[-1][0], snake[-1][1],distance_to_wall,REWARD,]) #기본
state_0 = [state[0], state[1], state[3], state[4], 
              state[5], state[6], state[7],state[8],
              state[9],state[10],distance_to_wall,REWARD,]
state_1 = [state[0], state[1], state[3], state[4], 
              state[5], state[6],state[7],state[8],
              state[9],state[10],distance_to_wall,0,]
state_2 = [state[0], state[1], state[3], state[4], 
              state[5], state[6], state[7],state[8],
              state[9],state[10],distance_to_wall,-10,] #나쁜거
state_3 = [state[0], state[1], state[3], state[4], 
              state[5], state[6], state[7],state[8],
              state[9],state[10],distance_to_wall,1,]  #무난
state_4 = [state[0], state[1], state[3], state[4], 
              state[5], state[6], state[7],state[8],
              state[9],state[10],distance_to_wall,3,]  #ㄱㅊ


def move_snake(snake, direction):
    x, y = snake[0]
    if direction == 'up':
        y -= SNAKE_SIZE
    elif direction == 'down':
        y += SNAKE_SIZE
    elif direction == 'left':
        x -= SNAKE_SIZE
    elif direction == 'right':
        x += SNAKE_SIZE
    snake.insert(0, (x, y))
    return snake


def eat_food(snake, food):
    global score
    if snake[0] == food:
        snake.append(snake[-1])
        score+= 1
        return True
    return False
def spawn_food(snake):
    while True:
        food = (random.randint(0, WINDOW_WIDTH // SNAKE_SIZE - 1) * SNAKE_SIZE, 
                random.randint(0, WINDOW_HEIGHT // SNAKE_SIZE - 1) * SNAKE_SIZE)
        if food not in snake:
            break
    return food

def start_game():
    global snake, direction, food,WINDOW_WIDTH,WINDOW_HEIGHT,state,food_distance,distance_to_wall
    snake = [(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)]
    direction = random.choice(['up', 'down', 'left', 'right'])
    food = spawn_food(snake)
    while True:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(f'Score: {score}')
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and direction != 'down':
            direction = 'up'
            distance_to_wall = snake[0][1]
        elif keys[pygame.K_DOWN] and direction != 'up':
            direction = 'down'
            distance_to_wall = WINDOW_HEIGHT - snake[0][1] - SNAKE_SIZE
        elif keys[pygame.K_LEFT] and direction != 'right':
            direction = 'left'
            distance_to_wall = WINDOW_HEIGHT - snake[0][1] - SNAKE_SIZE
        elif keys[pygame.K_RIGHT] and direction != 'left':
            direction = 'right'
            
        snake = move_snake(snake, direction)
        
        
       
        
        if snake[0] in snake[1:] or snake[0][0] < 0 or snake[0][0] > WINDOW_WIDTH - SNAKE_SIZE or snake[0][1] < 0 or snake[0][1] > WINDOW_HEIGHT - SNAKE_SIZE:
            snake = [(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)]  # 뱀의 길이를 초기화
            direction = random.choice(['up', 'down', 'left', 'right'])  # 방향을 무작위로 설정

            continue  # while 루프의 처음으로 이동
             
        if eat_food(snake, food):
            food = spawn_food(snake)
            state[2] = food[0]
            state[3] = food[1]
            state = np.array(state)
        else:
            snake.pop()
            state = np.array(state_1)
         
            
            
            

        
        state[:2] = snake[0]
        state[8:10] = snake[-1]
        state[4:8] = np.array([int(direction == 'up'), int(direction == 'down'), 
                               int(direction == 'left'), int(direction == 'right')])
        if direction == 'up':
             distance_to_wall = snake[0][1]
             state[-2] = distance_to_wall
             
        elif direction == 'down':
             distance_to_wall = WINDOW_HEIGHT - snake[0][1] - SNAKE_SIZE
             state[-2] = distance_to_wall
        elif direction == 'left':
             distance_to_wall = snake[0][0]
             state[-2] = distance_to_wall
        elif direction == 'right':
             distance_to_wall = WINDOW_WIDTH - snake[0][0] - SNAKE_SIZE
             state[-2] = distance_to_wall
          # 뱀과 먹이의 좌표를 이용하여 거리 계산
        distance_to_food = abs(snake[0][0] - food[0]) + abs(snake[0][1] - food[1])
        if distance_to_food <= 5*SNAKE_SIZE:
         # 먹이 주변 5x5에 있을 경우 보상 추가
            
            if distance_to_food <= 3*SNAKE_SIZE:
                state = np.array(state_4)
            else:
                state = np.array(state_3)

                        #화면 출력
        window.fill((0, 0, 0))
#       # 5x5 범위 그리기
#         for i in range(food[0]-2*SNAKE_SIZE, food[0]+3*SNAKE_SIZE, SNAKE_SIZE):
#             for j in range(food[1]-2*SNAKE_SIZE, food[1]+3*SNAKE_SIZE, SNAKE_SIZE):
#                 pygame.draw.rect(window, (255, 165, 0), (i, j, SNAKE_SIZE, SNAKE_SIZE))

# # 3x3 범위 그리기
#         for i in range(food[0]-1*SNAKE_SIZE, food[0]+2*SNAKE_SIZE, SNAKE_SIZE):
#             for j in range(food[1]-1*SNAKE_SIZE, food[1]+2*SNAKE_SIZE, SNAKE_SIZE):
#                 pygame.draw.rect(window, (255, 69, 0), (i, j, SNAKE_SIZE, SNAKE_SIZE))
   # 5x5 범위 그리기
        for i in range(food[0]-2*SNAKE_SIZE, food[0]+3*SNAKE_SIZE, SNAKE_SIZE):
            for j in range(food[1]-2*SNAKE_SIZE, food[1]+3*SNAKE_SIZE, SNAKE_SIZE):
             pygame.draw.rect(window, (255, 165, 0), (i, j, SNAKE_SIZE, SNAKE_SIZE))

# 3x3 범위 그리기
        for i in range(food[0]-SNAKE_SIZE, food[0]+2*SNAKE_SIZE, SNAKE_SIZE):
            for j in range(food[1]-SNAKE_SIZE, food[1]+2*SNAKE_SIZE, SNAKE_SIZE):
               pygame.draw.rect(window, (255, 69, 0), (i, j, SNAKE_SIZE, SNAKE_SIZE))


        pygame.draw.rect(window, (255, 0, 0), (food[0], food[1], SNAKE_SIZE, SNAKE_SIZE))
        for s in snake:
            pygame.draw.rect(window, (0, 255, 0), (s[0], s[1], SNAKE_SIZE, SNAKE_SIZE))
        pygame.display.flip()
        print(state)
        

while True:
    start_game()

    print(f'Score: {score}')
