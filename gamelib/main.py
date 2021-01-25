import pygame, sys
from pygame.locals import *

## Initialization
screen_width = 800
screen_height = 600
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([screen_width, screen_height])
# base_font = pygame.font.Font(None, 32)
base_font = pygame.font.Font('./resources/alagard_by_pix3m-d6awiwp.ttf', 32)
user_text = 'Hello world!'

input_rect = pygame.Rect(200,200, 140, 32)
color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('gray15')
color = color_passive

active = False

def gameloop():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False

            if event.type == KEYDOWN: # Checks if any key is pressed
                if active:
                    if event.key == K_BACKSPACE:
                        user_text = user_text[:-1]
                    elif event.key == K_RETURN:
                        user_text += '\n'
                    else:
                        user_text += event.unicode # Which key is pressed in unicode

        
        screen.fill((0,0,0))

        if active:
            color = color_active
        else:
            color = color_passive

        pygame.draw.rect(screen, color, input_rect, 2)

        text_surface = base_font.render(user_text, True, (255,255,255))
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        input_rect.w = max(100, text_surface.get_width() + 10)

        pygame.display.flip()
        clock.tick(60)