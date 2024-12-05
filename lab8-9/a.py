import pygame
import random
import sys


pygame.init()


window_width = 400
window_height = 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Racer")


WHITE = (255, 255, 255)


car_image = pygame.image.load("car.png")
coin_image = pygame.image.load("coin.png")
road_image = pygame.image.load("road1.png")


car_width = 50
car_height = 100
car_image = pygame.transform.scale(car_image, (car_width, car_height))
coin_width = 30
coin_height = 30
coin_image = pygame.transform.scale(coin_image, (coin_width, coin_height))
road_image = pygame.transform.scale(road_image, (window_width, window_height))


font = pygame.font.SysFont(None, 36)


car_x = window_width // 2 - car_width // 2
car_y = window_height - car_height - 10
car_speed = 5


coin_x = random.randint(0, window_width - coin_width)
coin_y = -coin_height
coin_speed = 5

score = 0

clock = pygame.time.Clock()
FPS = 60

running = True
while running:
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_x > 0:
        car_x -= car_speed
    if keys[pygame.K_RIGHT] and car_x < window_width - car_width:
        car_x += car_speed

   
    coin_y += coin_speed

   
    if coin_y > window_height:
        coin_y = -coin_height
        coin_x = random.randint(0, window_width - coin_width)

   
    car_rect = pygame.Rect(car_x, car_y, car_width, car_height)
    coin_rect = pygame.Rect(coin_x, coin_y, coin_width, coin_height)
    if car_rect.colliderect(coin_rect):
        score += 1  
        coin_y = -coin_height
        coin_x = random.randint(0, window_width - coin_width)

    screen.blit(road_image, (0, 0))

    screen.blit(car_image, (car_x, car_y))

  
    screen.blit(coin_image, (coin_x, coin_y))

    score_text = font.render(f"Счет: {score}", True, WHITE)
    screen.blit(score_text, (window_width - 150, 10))

    
    pygame.display.flip()

  
    clock.tick(FPS)
