import pygame
import math
import time


pygame.init()


WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")


clock_bg = pygame.image.load("mickeyclock.jpeg")  
clock_bg = pygame.transform.scale(clock_bg, (WIDTH, HEIGHT))


right_hand = pygame.image.load("right_hand.png")  
left_hand = pygame.image.load("left_hand.png") 


right_hand = pygame.transform.scale(right_hand, (150, 20)) 
left_hand = pygame.transform.scale(left_hand, (150, 20))  


CENTER = (WIDTH // 2, HEIGHT // 2)


def draw_hand(surface, hand_image, angle, center):
    rotated_hand = pygame.transform.rotate(hand_image, angle)
    rect = rotated_hand.get_rect(center=center)
    surface.blit(rotated_hand, rect.topleft)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    current_time = time.localtime()
    seconds = current_time.tm_sec
    minutes = current_time.tm_min

    
    second_angle = -seconds * 6 + 90  
    minute_angle = -minutes * 6 + 90 

    
    screen.fill((255, 255, 255))
    screen.blit(clock_bg, (0, 0))  
    draw_hand(screen, left_hand, second_angle, CENTER)  
    draw_hand(screen, right_hand, minute_angle, CENTER)  

    
    pygame.display.flip()
    pygame.time.Clock().tick(30)


pygame.quit()

