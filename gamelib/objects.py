from itertools import cycle
import pygame

class Time:
    def __init__(self, font):
        self.font = font
        self.start_time =  self.time = self.timer_left =  0
        self.time_started = False
    
    def started(self):
        return self.time_started

    def set_timer(self, timer_left): 
        """ 
        Used in "time" gamemode only, Set timer in a set time (e.g. 60 seconds) until it reaches to 0
        "Timer" should not be confused with regular stopwatch that is used in the "words" gamemode
        """
        self.timer_left = int(timer_left)
    
    def timer_done(self):
        # Return if Timer has already passed timer
        return (self.time_started and
                self.timer_left != 0 and
                (self.timer_left - self.time) < 1)

    def start(self):
        self.time_started = True
        self.start_time = pygame.time.get_ticks()

    def stop(self):
        self.time_started = False

    def restart(self):
        self.start_time =  self.time = self.timer_left =  0
        self.time_started = False

    def get_time(self):
        return self.time

    def update(self): # Main update function
        if self.time_started:
            self.time = (pygame.time.get_ticks() - self.start_time)//1000

    def display(self, screen, rect, color):
        if self.timer_left != 0:
            time_left = self.timer_left - self.time
            time_surface = self.font.render(str(time_left), True, color)
            screen.blit(time_surface, rect)
        else:
            time_surface = self.font.render(str(self.time), True, color)
            screen.blit(time_surface, rect)

class Gamemode_GUI:
    def __init__(self, init_rect, gamemodes:cycle):
        font_size = 16
        self.font = pygame.font.Font('./resources/fonts/RobotoMono-Regular.ttf', font_size)
    
        self.gamemodes = gamemodes
        self.gamemode_rect = pygame.Rect(init_rect.x, init_rect.y - init_rect.h-2, self.font.size('words')[0], init_rect.h)
        self.option_rects = pygame.Rect(init_rect)

    def display(self, screen, color, gamemode):
        # pygame.draw.rect(screen, color, self.gamemode_rect, 2)
        gamemode_surface = self.font.render(gamemode.title(), True, color)
        screen.blit(gamemode_surface, (self.gamemode_rect.x, self.gamemode_rect.y))

    def check_collision(self, pos):
        return self.gamemode_rect.collidepoint(pos)
    
    def next_gamemode(self):
        new_gamemode = next(self.gamemodes)
        self.gamemode_rect = pygame.Rect(self.gamemode_rect.x, 
                                         self.gamemode_rect.y,
                                         self.font.size(new_gamemode)[0], 
                                         self.gamemode_rect.h)
        return new_gamemode

class Options_GUI:
    def __init__(self, init_rect, wordcounts, timecounts):
        font_size = 16
        self.font = pygame.font.Font('./resources/fonts/RobotoMono-Regular.ttf', font_size)
        self.wordcounts = wordcounts
        self.timecounts = timecounts
        self.setup_rects(init_rect)

    def setup_rects(self, init_rect):
        self.rects = []

        for i,g in enumerate(self.wordcounts):
            width = self.font.size(g)[0]
            long = self.font.size(g)[0] if len(str(g)) > 2 else 0
            space = self.font.size('0')[0] if i != 0 else 0 
            self.rects.append(
                pygame.Rect(
                    (init_rect.x + (space*i) + (width * i)) - long,
                    init_rect.y,
                    width,
                    init_rect.h
                    )
                )

    def display(self, screen, color, current_twc, gamemode):
        if gamemode == 'words' or gamemode == 'shuffled custom':
            for twc_rect, twc in zip(self.rects, self.wordcounts):
                # pygame.draw.rect(screen, color, twc_rect, 2)
                self.font.underline = str(current_twc) == twc
                twc_surface = self.font.render(str(twc), True, color)
                screen.blit(twc_surface, twc_rect)

        if gamemode == 'time':
            for twc_rect, twc in zip(self.rects, self.timecounts):
                # pygame.draw.rect(screen, color, twc_rect, 2)
                self.font.underline = str(current_twc) == twc
                twc_surface = self.font.render(str(twc), True, color)
                screen.blit(twc_surface, twc_rect)

    def check_collision(self, pos, timeword_count, gamemode):
        if gamemode == 'words' or gamemode == 'shuffled custom':
            for i in range(len(self.rects)):
                if self.rects[i].collidepoint(pos) and timeword_count != self.timecounts[i]:
                    timeword_count = self.wordcounts[i]
        
        if gamemode == 'time':
            for i in range(len(self.rects)):
                if self.rects[i].collidepoint(pos) and timeword_count != self.timecounts[i]:
                    timeword_count = self.timecounts[i]

        return timeword_count