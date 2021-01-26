import json, random, pygame
from urllib.request import urlopen

class Entry:
    def __init__(self):
        categories = ('standard', 'word-by-word', 'expert', 'master')
        self.color = {None: (255,255,255),
                      'correct': (74, 203, 138),
                      'incorrect': (249, 67, 72)}
        font_size = 20
        self.font = pygame.font.Font('./resources/fonts/RobotoMono-Regular.ttf', font_size)
        self.entry_text = ''

    def load_random_words(self, category: str, length: int, difficulty = 'standard'):
        with open('./resources/texts/random_words.json', encoding = 'utf-8') as f:
            data = json.load(f)
        data = data[category]
        
        _randomize = lambda data: random.randrange(0, len(data))
        if difficulty == 'standard':
            self.entry_text = ' '.join([data[_randomize(data)] for _ in range(length)])
            self.check = [None for _ in range(len(self.entry_text))]

    def load_quotes(self, difficulty = 'standard'):
        with urlopen("http://api.quotable.io/random") as response:
            source = response.read()
        data = json.loads(source)

        if difficulty == 'standard':
            self.entry_text = data['content']
            self.check = [None for _ in range(len(self.entry_text))]
        
    def draw_text(self, screen, rect, aa=True):
        text = self.entry_text
        rect = pygame.Rect(rect.x * 1.5, rect.y * 1.25, rect.width-50, rect.height)
        y = rect.top 

        cur_line = 0
        lineSpacing = -4
        fontHeight = self.font.size("Tg")[1]

        while text:
            i = 1

            # determine if the row of text will be outside our area
            if y + fontHeight > rect.bottom:
                break

            # determine maximum width of line
            while self.font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1
            
            # if we've wrapped the text, then adjust the wrap to the last word      
            if i < len(text): 
                i = text.rfind(" ", 0, i) + 1

            for s in range(len(text[:i])):
                stasus = self.check[cur_line+s]
                letter_surface = self.font.render(text[s], aa, self.color[stasus])
                screen.blit(letter_surface, ((rect.x + 5)+s*self.font.size(text[s])[0], y + 5))
            
            y += fontHeight + lineSpacing
            cur_line += i
            text = text[i:]

        return text
    
    def analyze_input(self, input_text):
        # arr = list(input_text)
        new_check = []
        for i,character in enumerate(input_text):
            if character == self.entry_text[i]:
                new_check.append('correct')
            else: 
                new_check.append('incorrect')

        if len(new_check) < len(self.check):
            new_check.extend([None for _ in range(len(self.check)-len(new_check))])
        else:
            pass

        self.check = new_check