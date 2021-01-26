import pygame, sys
from pygame.locals import *
from gamelib.entry import *

def main():
    ### Initialization ###
    screen_width = 800
    screen_height = 600
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([screen_width, screen_height])

    ## Game elements ##
    font_size = 20
    base_font = pygame.font.Font('./resources/fonts/RobotoMono-Regular.ttf', font_size)
    font_width = base_font.size('M')[0]
    font_height =  base_font.size('Tg')[1]

    background_color = (18, 21, 32)
    purple = (147, 99, 251)

    game_box_rect = pygame.Rect(50, 100, 700, 350)
    game_box_color = (41, 45, 61)

    # User Input #
    user_text = ''
    input_rect = pygame.Rect(70, game_box_rect.y*3.90, 660, font_height + 5)
    color_active = (255, 255, 255)
    color_passive = (18, 21, 32)
    text_color = color_passive
    active = True

    # Game entry #
    entry_count = 25
    entry = Entry()
    entry.load_random_words("english", length = entry_count)
    # entry.load_quotes()

    # entry_rect = pygame.Rect(game_box_rect.x * 1.5, game_box_rect.y * 1.35, len(entry_text)*font_width, font_height + 2)
    # entry_rect = pygame.Rect(50, 100, 700, 350)

    ### Main game loop ###
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
                    elif event.key == K_TAB or event.key == K_ESCAPE:
                        entry.load_random_words('english', length = entry_count)
                        user_text = ''
                    # elif not base_font.size(user_text)[0] > input_rect.width-30:
                    else:
                        user_text += event.unicode # Which key is pressed in unicode
                    entry.analyze_input(user_text)

        screen.fill(background_color)
        pygame.draw.rect(screen, game_box_color, game_box_rect)
        if active:
            text_color = color_active
        else:
            text_color = color_passive

        ## Text/Entry Display ##
        entry.draw_text(screen, game_box_rect)

        ## Display User Typing Bar ##
        pygame.draw.rect(screen, text_color, input_rect, 2)
        text_surface = base_font.render(user_text, True, text_color)
        screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 3))

        #input_rect.w = max(100, text_surface.get_width() + 10)

        pygame.display.flip()
        clock.tick(60)