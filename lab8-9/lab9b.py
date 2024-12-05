import pygame
import random
import sys


pygame.init()


window_width = 600
window_height = 400
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Змейка")


WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
RED = (200, 0, 0)
PURPLE = (128, 0, 128)


cell_size = 20  
clock = pygame.time.Clock()


font = pygame.font.SysFont(None, 36)

def draw_snake(snake_list):

    for x, y in snake_list:
        pygame.draw.rect(screen, GREEN, [x, y, cell_size, cell_size])

def message(msg, color, position):
    text = font.render(msg, True, color)
    screen.blit(text, position)

def game_loop():
   
    snake_pos = [window_width // 2, window_height // 2]  
    snake_body = [snake_pos.copy()]  
    snake_direction = 'RIGHT'  
    change_to = snake_direction  

   
    speed = 10

    
    score = 0

   
    food_spawn = False
    food_pos = []
    food_weight = 0
    food_spawn_time = 0
    food_life_time = 5000 

    
    food_types = {
        1: YELLOW,  # Вес 1, цвет желтый
        2: ORANGE,  # Вес 2, цвет оранжевый
        3: RED,     # Вес 3, цвет красный
        5: PURPLE   # Вес 5, цвет фиолетовый
    }

    game_over = False

    while not game_over:
        current_time = pygame.time.get_ticks()  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
           
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and snake_direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                    change_to = 'RIGHT'

      
        snake_direction = change_to

       
        if snake_direction == 'UP':
            snake_pos[1] -= cell_size
        elif snake_direction == 'DOWN':
            snake_pos[1] += cell_size
        elif snake_direction == 'LEFT':
            snake_pos[0] -= cell_size
        elif snake_direction == 'RIGHT':
            snake_pos[0] += cell_size

      
        if (snake_pos[0] < 0 or snake_pos[0] >= window_width or
            snake_pos[1] < 0 or snake_pos[1] >= window_height):
            game_over = True

       
        if snake_pos in snake_body[1:]:
            game_over = True

        
        snake_body.insert(0, list(snake_pos))

       
        if not food_spawn:
            food_weight = random.choice(list(food_types.keys()))  
            food_color = food_types[food_weight]  
            food_pos = [random.randrange(0, window_width // cell_size) * cell_size,
                        random.randrange(0, window_height // cell_size) * cell_size]
            
            while food_pos in snake_body:
                food_pos = [random.randrange(0, window_width // cell_size) * cell_size,
                            random.randrange(0, window_height // cell_size) * cell_size]
            food_spawn = True
            food_spawn_time = current_time 

     
        if snake_pos == food_pos:
            score += food_weight  
            food_spawn = False 
           
        else:
            snake_body.pop()  

        
        if food_spawn and current_time - food_spawn_time > food_life_time:
            food_spawn = False  

        
        screen.fill(BLACK)
        draw_snake(snake_body)
        if food_spawn:
            pygame.draw.rect(screen, food_color, [food_pos[0], food_pos[1], cell_size, cell_size])

        message(f"Счет: {score}", WHITE, [10, 10])

        pygame.display.update()
        clock.tick(speed)

    
    screen.fill(BLACK)
    message("Game over", RED, [window_width // 2 - 100, window_height // 2 - 50])
    message(f"Ваш счет: {score}", WHITE, [window_width // 2 - 100, window_height // 2])
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
