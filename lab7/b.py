import pygame
import sys


pygame.init()
pygame.mixer.init()


screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Музыкальный плеер")


playlist = ["track1.mp3", "track2.mp3", "track3.mp3"]
current_track = 0


pygame.mixer.music.load(playlist[current_track])

playing = False  

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: 
                if not playing:
                    pygame.mixer.music.play()
                    playing = True
                else:
                    pygame.mixer.music.pause()
                    playing = False
            elif event.key == pygame.K_s:  
                pygame.mixer.music.stop()
                playing = False
            elif event.key == pygame.K_RIGHT:  
                current_track = (current_track + 1) % len(playlist)
                pygame.mixer.music.load(playlist[current_track])
                pygame.mixer.music.play()
                playing = True
            elif event.key == pygame.K_LEFT:  
                current_track = (current_track - 1) % len(playlist)
                pygame.mixer.music.load(playlist[current_track])
                pygame.mixer.music.play()
                playing = True

    pygame.display.update()
