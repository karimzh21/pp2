import pygame
import sys


pygame.init()


window_width = 400
window_height = 300
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Шар")


WHITE = (255, 255, 255)
RED = (255, 0, 0)


ball_radius = 25
ball_pos = [window_width // 2, window_height // 2]
ball_speed = 20


running = True
while running:
    screen.fill(WHITE) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

   
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if ball_pos[0] - ball_radius - ball_speed >= 0:
            ball_pos[0] -= ball_speed
    if keys[pygame.K_RIGHT]:
        if ball_pos[0] + ball_radius + ball_speed <= window_width:
            ball_pos[0] += ball_speed
    if keys[pygame.K_UP]:
        if ball_pos[1] - ball_radius - ball_speed >= 0:
            ball_pos[1] -= ball_speed
    if keys[pygame.K_DOWN]:
        if ball_pos[1] + ball_radius + ball_speed <= window_height:
            ball_pos[1] += ball_speed

   
    pygame.draw.circle(screen, RED, ball_pos, ball_radius)

    pygame.display.update()

pygame.quit()
sys.exit()
