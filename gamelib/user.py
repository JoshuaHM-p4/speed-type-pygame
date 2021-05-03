import pygame
from pygame.locals import *

class User:
    def __init__(self, font):
        self.font = font
        self.fontWidth = self.font.size('M')[0]
        self.fontHeight =  self.font.size('Tg')[1]
        self.text = self.difficulty = ''
    
    def display(self, screen, rect, color, aa = True):
        pygame.draw.rect(screen, color, rect, 2)

        
        text = self.text

        if self.difficulty == 'word-by-word':
            if ' ' in text[:-1]:
                text = text[text.rindex(' '):].strip()
            else:
                text = text.strip()

        rect = pygame.Rect(rect)

        while self.font.size(text)[0] > rect.width:
            i = 1
            while self.font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1
            text = text[i:]

        image = self.font.render(text, aa, color)
        screen.blit(image, (rect.left + 10, rect.y))

    def input(self, event):
        ctrl, backspace = pygame.key.get_pressed()[K_LCTRL], pygame.key.get_pressed()[K_BACKSPACE]
        space = pygame.key.get_pressed()[K_SPACE]

        if ctrl and backspace:
            try:
                self.text = self.text[:self.text.rindex(" ")]
            except ValueError:
                self.text = ''

        elif backspace:
            if self.difficulty == 'word-by-word':
                if self.text[-1] != ' ':
                    self.text = self.text[:-1]
            else:
                self.text = self.text[:-1]

        else:
            self.text += event.unicode
    
    def empty(self):
        self.text = ''
    
    def length(self):
        return len(self.text)
    
    def _show(self, text):
        self.text = text
    
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
    
    def cur_word(self):
        try:
            return self.text.count(' ')
        except:
            return 0