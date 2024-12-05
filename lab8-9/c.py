import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("графический редактор")
    clock = pygame.time.Clock()

    
    radius = 10  
    drawing = False
    mode = 'pen'  
    color = (0, 0, 0)  
    start_pos = (0, 0) 

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

           
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    mode = 'pen'
                elif event.key == pygame.K_r:
                    mode = 'rectangle'
                elif event.key == pygame.K_c:
                    mode = 'circle'
                elif event.key == pygame.K_e:
                    mode = 'eraser'
                elif event.key == pygame.K_1:
                    color = (0, 0, 0)  # Черный
                elif event.key == pygame.K_2:
                    color = (255, 0, 0)  # Красный
                elif event.key == pygame.K_3:
                    color = (0, 255, 0)  # Зеленый
                elif event.key == pygame.K_4:
                    color = (0, 0, 255)  # Синий
                elif event.key == pygame.K_UP:
                    radius = min(100, radius + 1)  # Увеличение толщины
                elif event.key == pygame.K_DOWN:
                    radius = max(1, radius - 1)  # Уменьшение толщины
                elif event.key == pygame.K_ESCAPE:
                    screen.fill((255, 255, 255))  # Очистка экрана

          
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    drawing = True
                    start_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    end_pos = event.pos
                    if mode == 'rectangle':
                        rect = pygame.Rect(start_pos, (end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                        pygame.draw.rect(screen, color, rect, 2)
                    elif mode == 'circle':
                        radius_circle = int(((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2)**0.5)
                        pygame.draw.circle(screen, color, start_pos, radius_circle, 2)
                    drawing = False
            elif event.type == pygame.MOUSEMOTION:
                if drawing:
                    if mode == 'pen':
                        pygame.draw.line(screen, color, start_pos, event.pos, radius)
                        start_pos = event.pos
                    elif mode == 'eraser':
                        pygame.draw.line(screen, (255, 255, 255), start_pos, event.pos, radius)
                        start_pos = event.pos

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
