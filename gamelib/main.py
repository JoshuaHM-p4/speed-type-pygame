import pygame, sys
from itertools import cycle

from pygame.locals import *
from gamelib.entry import *
from gamelib.objects import *
from gamelib.utils import *
from gamelib.user import *

def main():
    global done, user_active

    ### Initialization ###
    screen_width = 800
    screen_height = 600
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([screen_width, screen_height])

    ## Game elements ##
    _font = './resources/fonts/RobotoMono-Regular.ttf'
    font_size = 16
    base_font = pygame.font.Font(_font, font_size)
    top_font = pygame.font.Font(_font, font_size * 2)
    entry_font = pygame.font.Font(_font, font_size + 4)
    # user_font = pygame.font.Font(_font, font_size + 4)
    font_width = base_font.size('M')[0]
    font_height =  base_font.size('Tg')[1]

    difficulties = cycle(('standard', 'word-by-word', 'expert', 'master'))
    gamemodes = cycle(('words', 'quote', 'time', 'custom', 'shuffled custom'))
    wordcount_options = ('10','25','50','100','250')
    timecount_options = ('15', '30', '60', '120', '240')

    ## Colors ##
    background_color = (18, 21, 32)
    purple = (147, 99, 251)
    orange = (255, 147, 73)
    yellow = (255, 213, 67)
    green = (74, 203, 138)
    blue = (60, 197, 248)
    color_active = (255, 255, 255)
    color_passive = (108, 113, 120)
    game_box_color = (41, 45, 61)

    ## Game Buttons/UX/UI ##
    game_box_rect = pygame.Rect(50, 100, 700, 350)
    ui_size = 20
    ui_rect = pygame.Rect(game_box_rect.x, game_box_rect.y - ui_size - 10, ui_size, ui_size)
    gm_gui = Gamemode_GUI(ui_rect, gamemodes)
    options_gui = Options_GUI(ui_rect, wordcount_options, timecount_options)

    ## Game entry ##
    entry = Entry(entry_font)
    gamemode =  next(gm_gui.gamemodes)
    difficulty = next(difficulties)
    language = 'english'

    timeword_count = 25
    entry.load_words(difficulty = difficulty, length = timeword_count, language = language)

    ## User Input and Box ##
    user = User(entry_font)
    user_rect = pygame.Rect(70, 400, 660, font_height + 5)
    text_color = color_passive
    user_active = True
    user.set_difficulty(difficulty)

    ## Timer ##
    time = Time(top_font)
    time_rect = pygame.Rect(screen_width//2 -30,  int(screen_height* 0.10), 50, 50)
    done = False

    ## Debug and Results ##
    debug_rect = pygame.Rect(game_box_rect.x, game_box_rect.y, 200, font_height + 5)
    debug_visible = False
    result_rect = pygame.Rect(578, 66, 25, font_height + 5)
    result_text = 'WPM: XX / ACC: XX'
    
    def load_game():
        global done, game_active
        done = False
        game_active = True
        time.restart()
        user.empty()
        user.set_difficulty(difficulty)

        if gamemode == 'words':
            entry.load_words(difficulty = difficulty, language = language, length = int(timeword_count))
        elif gamemode == 'quote':
            entry.load_quote(difficulty = difficulty)
        elif gamemode == 'time':
            time.set_timer(timeword_count)
            entry.load_words(difficulty = difficulty, language = language, length = 999)
        elif gamemode == 'custom':
            entry.load_file(difficulty = difficulty)
        elif gamemode == 'shuffled custom':
            entry.load_file_shuffled(difficulty = difficulty, length = int(timeword_count))

    ### Main game loop ###
    while True:
        clock.tick(60)
        text_color = color_active if user_active else color_passive

        ## Game Background ##
        screen.fill(background_color)
        pygame.draw.rect(screen, game_box_color, game_box_rect)

        ## Display Text/Entry ##
        entry.display(screen, game_box_rect, user.length(), full = done)

        ## Display User Area ##
        user.display(screen, user_rect, text_color)

        ## Display Time ##
        if user_active:
            time.update()
        if gamemode == 'time':
            time.display(screen, time_rect, text_color)
        else:
            text = f"{user.length()}/{entry.length()}"
            if difficulty == 'word-by-word':
                text = f"{user.cur_word()}/{entry.wordcount}"

            prog_surface = top_font.render(text, True, text_color)
            prog_rect = (screen_width//2 -60,  int(screen_height* 0.10), 50, 50)
            screen.blit(prog_surface, prog_rect)

        ## Display UI Elements ##
        gm_gui.display(screen, orange, gamemode)
        options_gui.display(screen, orange, timeword_count, gamemode)

        ## Result Text ##
        result_image = base_font.render(result_text, True, yellow)
        screen.blit(result_image, result_rect)

        ## Debug ##
        if debug_visible:
            fields = [
                f"{difficulty}",
                f"{gamemode}",
                f"{timeword_count} sec" if gamemode == 'time' else f"{timeword_count} words"
                f"{user.length()}/{entry.length()}" if difficulty != 'word-by-word' else f"{user.length()}|{entry.length()}",
                f"{time.get_time()}s passed",
                f"{entry.count_errors()} ({entry.all_errors}) errors",
                f"{int(acc(entry.length(), entry.count_true_correct()))}% acc"
            ]
            debug_text = ' | '.join(fields)
            debug_image = base_font.render(debug_text, True, purple)
            screen.blit(debug_image, debug_rect)

        ## Result Text ##
        if not done:
            if entry.done(user.text) or time.timer_done() or entry.difficulty_fail():
                done = True
                time.stop()
                if gamemode == 'time' or difficulty == 'expert' or difficulty == 'master':
                    entry.trim(user.length())

                try:
                    user_wpm = net_wpm(entry.length(), time.get_time(), entry.count_errors())
                    user_acc = int(acc(entry.length(), entry.count_true_correct()))
                    # user_wpm = int(gross_wpm(entry.length(), time))
                    # user_acc = int(acc2(entry.length(), time.get_time(), entry.all_errors))
                except ZeroDivisionError:
                    user_wpm = user_acc = 0
                result_text = f"WPM: {user_wpm} / ACC: {user_acc}"

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                cur_twc = timeword_count
                pos = event.pos
                if user_rect.collidepoint(pos):
                    user_active = True
                elif gm_gui.check_collision(pos):
                    gamemode = gm_gui.next_gamemode()
                    timeword_count = 30 if gamemode == 'time' else 25
                    load_game()
                elif (timeword_count := options_gui.check_collision(pos, timeword_count, gamemode)) != cur_twc:
                    load_game()
                else:
                    user_active = False

            if event.type == KEYDOWN:
                if not time.started() and not time.get_time(): 
                    user_active = True
                    time.start()

                if event.key == K_TAB or event.key == K_ESCAPE:
                    load_game()
                
                if event.key == K_F1:
                    debug_visible = not debug_visible

                if event.key == K_F2:
                    difficulty = next(difficulties) 
                    load_game()
                
                elif not done:
                    if user_active and event.unicode or event.key == K_BACKSPACE:
                        user_active = True
                        if difficulty == 'word-by-word':
                            user.input(event)
                            entry.analyze_word(user.text, event.key == K_SPACE)
                        else:
                            user.input(event)
                            entry.analyze_input(user.text)
                else:
                    user_active = False