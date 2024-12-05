import pygame
import random
import sys


pygame.init()


window_width = 400
window_height = 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Racer")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

player_image = pygame.image.load("car.png")
enemy_image = pygame.image.load("car2.png")
coin_image = pygame.image.load("coin.png")
background_image = pygame.image.load("road.png")


player_width = 50
player_height = 100
player_image = pygame.transform.scale(player_image, (player_width, player_height))
enemy_image = pygame.transform.scale(enemy_image, (player_width, player_height))
coin_width = 30
coin_height = 30
coin_image = pygame.transform.scale(coin_image, (coin_width, coin_height))
background_image = pygame.transform.scale(background_image, (window_width, window_height))


font = pygame.font.SysFont(None, 36)


player_x = window_width // 2 - player_width // 2
player_y = window_height - player_height - 10
player_speed = 5


enemy_x = random.randint(0, window_width - player_width)
enemy_y = -player_height
enemy_speed = 5  


coin_x = random.randint(0, window_width - coin_width)
coin_y = -coin_height
coin_speed = 5

coin_values = [1, 2, 5]
current_coin_value = random.choice(coin_values)


score = 0
coins_collected = 0


N = 5  


clock = pygame.time.Clock()
FPS = 60


running = True
while running:
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < window_width - player_width:
        player_x += player_speed

    enemy_y += enemy_speed

    
    if enemy_y > window_height:
        enemy_y = -player_height
        enemy_x = random.randint(0, window_width - player_width)

    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, player_width, player_height)
    if player_rect.colliderect(enemy_rect):
      
        screen.blit(background_image, (0, 0))
        message = font.render("Game Over", True, BLACK)
        screen.blit(message, (window_width // 2 - 80, window_height // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

   
    coin_y += coin_speed

    
    if coin_y > window_height:
        coin_y = -coin_height
        coin_x = random.randint(0, window_width - coin_width)
        current_coin_value = random.choice(coin_values)  

    
    coin_rect = pygame.Rect(coin_x, coin_y, coin_width, coin_height)
    if player_rect.colliderect(coin_rect):
        score += current_coin_value 
        coins_collected += 1  
      
        coin_y = -coin_height
        coin_x = random.randint(0, window_width - coin_width)
        current_coin_value = random.choice(coin_values)
        
        if coins_collected % N == 0:
            enemy_speed += 1  
 
    screen.blit(background_image, (0, 0))
    screen.blit(player_image, (player_x, player_y))
    screen.blit(enemy_image, (enemy_x, enemy_y))
    screen.blit(coin_image, (coin_x, coin_y))

    
    score_text = font.render(f"score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)
