import pygame
import sys
import math


pygame.init()


window_height = 600
window_width = 800  

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("paint")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
current_color = BLACK  


drawing = False
start_pos = None
mode = 'brush'  
radius = 5 


screen.fill(WHITE)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

      
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                mode = 'brush'  # Режим кисти
            elif event.key == pygame.K_r:
                mode = 'rectangle'  # Режим рисования прямоугольника
            elif event.key == pygame.K_s:
                mode = 'square'  # Режим рисования квадрата
            elif event.key == pygame.K_t:
                mode = 'right_triangle'  # Режим рисования прямоугольного треугольника
            elif event.key == pygame.K_e:
                mode = 'equilateral_triangle'  # Режим рисования равностороннего треугольника
            elif event.key == pygame.K_h:
                mode = 'rhombus'  # Режим рисования ромба
            elif event.key == pygame.K_c:
                mode = 'circle'  # Режим рисования круга
            elif event.key == pygame.K_x:
                mode = 'eraser'  # Режим ластика
            elif event.key == pygame.K_1:
                current_color = (0, 0, 0)  # Черный цвет
            elif event.key == pygame.K_2:
                current_color = (255, 0, 0)  # Красный цвет
            elif event.key == pygame.K_3:
                current_color = (0, 255, 0)  # Зеленый цвет
            elif event.key == pygame.K_4:
                current_color = (0, 0, 255)  # Синий цвет
            elif event.key == pygame.K_5:
                current_color = (255, 255, 0)  # Желтый цвет
            elif event.key == pygame.K_6:
                current_color = (255, 165, 0)  # Оранжевый цвет
            elif event.key == pygame.K_7:
                current_color = (128, 0, 128)  # Фиолетовый цвет
            elif event.key == pygame.K_UP:
                radius = min(50, radius + 1)  # Увеличение толщины кисти
            elif event.key == pygame.K_DOWN:
                radius = max(1, radius - 1)  # Уменьшение толщины кисти
            elif event.key == pygame.K_BACKSPACE:
                screen.fill(WHITE)  # Очистка экрана

      
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                drawing = True
                start_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:  
                end_pos = event.pos
                if mode == 'rectangle':
                   
                    rect = pygame.Rect(start_pos, (end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                    pygame.draw.rect(screen, current_color, rect, 2)
                elif mode == 'square':
                   
                    side = min(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))
                    rect = pygame.Rect(start_pos, (side, side))
                    pygame.draw.rect(screen, current_color, rect, 2)
                elif mode == 'circle':
                   
                    radius_circle = int(math.hypot(end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                    pygame.draw.circle(screen, current_color, start_pos, radius_circle, 2)
                elif mode == 'right_triangle':
                    
                    points = [start_pos, (start_pos[0], end_pos[1]), end_pos]
                    pygame.draw.polygon(screen, current_color, points, 2)
                elif mode == 'equilateral_triangle':
                    
                    height = abs(end_pos[1] - start_pos[1])
                    base = height / math.sqrt(3)
                    points = [
                        (start_pos[0], start_pos[1] - 2 * height / 3),
                        (start_pos[0] - base, start_pos[1] + height / 3),
                        (start_pos[0] + base, start_pos[1] + height / 3)
                    ]
                    pygame.draw.polygon(screen, current_color, points, 2)
                elif mode == 'rhombus':
                   
                    dx = end_pos[0] - start_pos[0]
                    dy = end_pos[1] - start_pos[1]
                    points = [
                        (start_pos[0], start_pos[1] - dy),
                        (start_pos[0] - dx, start_pos[1]),
                        (start_pos[0], start_pos[1] + dy),
                        (start_pos[0] + dx, start_pos[1])
                    ]
                    pygame.draw.polygon(screen, current_color, points, 2)
                drawing = False
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                if mode == 'brush':
                   
                    pygame.draw.line(screen, current_color, start_pos, event.pos, radius)
                    start_pos = event.pos
                elif mode == 'eraser':
                    
                    pygame.draw.line(screen, WHITE, start_pos, event.pos, radius)
                    start_pos = event.pos

    pygame.display.flip()

pygame.quit()
sys.exit()
