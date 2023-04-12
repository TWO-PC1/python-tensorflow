
import pygame 
import numpy as np
import random



clock = pygame.time.Clock()
WINDOW_WIDTH = 600 #가로 너비
WINDOW_HEIGHT = 600 #세로 너비
SNAKE_SIZE = 20
score =0


snake = [(random.randint(0,WINDOW_WIDTH//SNAKE_SIZE -1)*SNAKE_SIZE,
        random.randint(0,WINDOW_HEIGHT//SNAKE_SIZE -1)*SNAKE_SIZE)] #snake 기본위치 설정


snake2 = [(random.randint(0,WINDOW_WIDTH//SNAKE_SIZE -1)*SNAKE_SIZE,
        random.randint(0,WINDOW_HEIGHT//SNAKE_SIZE -1)*SNAKE_SIZE)] #snake2 기본위치 설정


direction = random.choice(['up','down','left','right'])

direction2 = random.choice(['up','down','left','right'])

food = (random.randint(0,WINDOW_WIDTH//SNAKE_SIZE -1)*SNAKE_SIZE,
        random.randint(0,WINDOW_HEIGHT//SNAKE_SIZE -1)*SNAKE_SIZE)


state = np.array([snake[0][0], snake[0][1], food[0], food[1], 
                  int(direction == 'up'), int(direction == 'down'), 
                  int(direction == 'left'), int(direction == 'right'), 
                  snake[-1][0], snake[-1][1]]) #기본

state2 = np.array([snake2[0][0], snake2[0][1], food[0], food[1], 
                  int(direction2 == 'up'), int(direction2 == 'down'), 
                  int(direction2 == 'left'), int(direction2 == 'right'), 
                  snake2[-1][0], snake2[-1][1]]) #기본

def move_snake(snake, direction):
    if snake == snake2:
        x, y = snake[0]
        if direction == 'up':
            y -= SNAKE_SIZE
        elif direction == 'down':
            y += SNAKE_SIZE
        elif direction == 'left':
            x -= SNAKE_SIZE
        elif direction == 'right':
            x += SNAKE_SIZE
        snake2.insert(0, (x, y))
        snake2.pop()
        return snake
    else:
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
        snake.pop()
        return snake


def eat_food(snake, food):
    global score
    if snake[0] == food:
        snake.append(snake[-1])
        score = score+1
        return True
    elif snake2[0] == food:
        snake2.append(snake2[-1])
        score = score+1
        return True
    else:
        return False


def spawn_food():
    while True:
        food = (random.randint(0, WINDOW_WIDTH // SNAKE_SIZE - 1) * SNAKE_SIZE, 
                random.randint(0, WINDOW_HEIGHT // SNAKE_SIZE - 1) * SNAKE_SIZE)
        if food not in snake and snake2:
            break
    return food

    


window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.init()
print(state)

def start_game():
    global snake,snake2, direction,direction2,food,WINDOW_WIDTH,WINDOW_HEIGHT,state,state2
    
    
    food = spawn_food()
    while True:
        clock.tick(8)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(f'Score: {score}')
                pygame.quit()
                quit()
            allkey = pygame.key.get_pressed()
            if allkey[pygame.K_UP] or allkey[pygame.K_DOWN] or allkey[pygame.K_LEFT] or allkey[pygame.K_RIGHT]:
                keys = pygame.key.get_pressed()
            
                if keys[pygame.K_UP] and direction != 'down':
                    direction = 'up'
                    
                elif keys[pygame.K_DOWN] and direction != 'up':
                    direction = 'down'
                
                elif keys[pygame.K_LEFT] and direction != 'right':
                    direction = 'left'
                    
                elif keys[pygame.K_RIGHT] and direction != 'left':
                    direction = 'right'

            if allkey[pygame.K_w] or allkey[pygame.K_s] or allkey[pygame.K_a] or allkey[pygame.K_d]:
                key2s = pygame.key.get_pressed()
                if key2s[pygame.K_w] and direction2 != 'down':
                    direction2 = 'up'
                    
                elif key2s[pygame.K_s] and direction2 != 'up':
                    direction2 = 'down'
                
                elif key2s[pygame.K_a] and direction2 != 'right':
                    direction2 = 'left'
                    
                elif key2s[pygame.K_d] and direction2 != 'left':
                    direction2 = 'right'
            
                


        snake = move_snake(snake, direction)
        snake2 = move_snake(snake2, direction2)
        
        
       
        
        if snake[0] in snake[1:] or snake[0][0] < 0 or snake[0][0] > WINDOW_WIDTH - SNAKE_SIZE or snake[0][1] < 0 or snake[0][1] > WINDOW_HEIGHT - SNAKE_SIZE or snake[0] in snake2[0:]:#죽는 경우
            snake = [(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)]  # 뱀의 길이를 초기화
            direction = random.choice(['up', 'down', 'left', 'right'])  # 방향을 무작위로 설정

            continue  # while 루프의 처음으로 이동
        if snake2[0] in snake2[1:] or snake2[0][0] < 0 or snake2[0][0] > WINDOW_WIDTH - SNAKE_SIZE or snake2[0][1] < 0 or snake2[0][1] > WINDOW_HEIGHT - SNAKE_SIZE or snake2[0] in snake[0:]:#죽는 경우
            snake2 = [(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)]  # 뱀의 길이를 초기화
            direction2 = random.choice(['up', 'down', 'left', 'right'])  # 방향을 무작위로 설정

            continue  # while 루프의 처음으로 이동


        if eat_food(snake, food):
            food = spawn_food()
            state[2] = food[0]
            state[3] = food[1]
            x,y =snake[0]
            #뱀 추가

        if eat_food(snake2, food):
            food = spawn_food()
            state2[2] = food[0]
            state2[3] = food[1]
            x,y =snake2[0]
            snake2.insert(0, (x, y))                     
            
        
            
         
            
            
            

        
        state[:2] = snake[0]
        state[8:10] = snake[-1]
        state[4:8] = np.array([int(direction == 'up'), int(direction == 'down'), 
                               int(direction == 'left'), int(direction == 'right')])
  
            
        state2[:2] = snake2[0]
        state2[8:10] = snake2[-1]
        state2[4:8] = np.array([int(direction == 'up'), int(direction == 'down'), 
                               int(direction == 'left'), int(direction == 'right')])
  
            
                    
        window.fill((0, 0, 0))



        pygame.draw.rect(window, (255, 0, 0), (food[0], food[1], SNAKE_SIZE, SNAKE_SIZE))
        for s in snake:
            pygame.draw.rect(window, (0, 255, 0), (s[0], s[1], SNAKE_SIZE, SNAKE_SIZE))
        for s in snake2:
            pygame.draw.rect(window, (0, 0, 255), (s[0], s[1], SNAKE_SIZE, SNAKE_SIZE))
        pygame.display.flip()
        print(state)
        print(snake)
    
        

while True:
    start_game()

    print(f'Score: {score}')

