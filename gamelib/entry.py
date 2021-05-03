import json, random, pygame, glob
from urllib.request import urlopen
from urllib.error import URLError

def create_file():
    with open('empty.txt', 'x') as f:
        f.write("You have no .txt file in the directory, this is a default sentence that would appear" +
                "if you don't have a .txt containing your custom entry. " + 
                "Though you can edit empty.txt all you want now")

class Entry:
    def __init__(self, font):
        self.color = {None: (255,255,255),
                      'correct': (74, 203, 138),
                      'incorrect': (249, 67, 72),
                      'current': (147, 99, 251)
        }
        self.font = font
        self.entry_text = ''
        self.all_errors = self.wordcount = 0
    
    def with_setup(func):
        def inner(self, *args, **kwargs):
            self.checks = []
            func(self, *args, **kwargs)
            self.wordcount = self.entry_text.count(' ')
            if 'length' in kwargs:
                self.wordcount = kwargs['length']
            self.difficulty = kwargs['difficulty'] 
            if self.difficulty == 'word-by-word':
                self.checks.extend(['current' for _ in range(self.entry_text.find(' '))])
            self.checks.extend([None for _ in range(len(self.entry_text)-len(self.checks))])
            self.all_errors = 0

        return inner

    @with_setup
    def load_words(self, difficulty, language: str, length: int):
        """ Loads random set of words from a .json data file """
        with open('./resources/texts/random_words.json', encoding = 'utf-8') as f:
            data = json.load(f)
        data = data[language]

        _randomize = lambda data: random.randrange(0, len(data))
        self.entry_text = ' '.join([data[_randomize(data)] for _ in range(length)])

    @with_setup
    def load_quote(self, difficulty):
        """ Loads a quote from the api """
        try:
            with urlopen("http://api.quotable.io/random") as response:
                source = response.read()
            data = json.loads(source)['content']
        except URLError:
            with open('./resources/texts/random_quotes.json', encoding = 'utf-8') as f:
                data = json.load(f)
            data = data[random.randint(0,len(data)-1)]['quote']
            print(data)

        self.entry_text = data

    @with_setup
    def load_file(self, difficulty):
        """ Loads first .txt file in the directory """
        if not glob.glob('*.txt'):
            create_file()

        text_file = glob.glob('*.txt')[0]
        with open(f'./{text_file}', encoding = 'utf-8') as f:
            data = f.read()
            
        self.entry_text = str(data).strip()
    
    @with_setup
    def load_file_shuffled(self, difficulty, length):
        if not glob.glob('*.txt'):
            create_file()

        text_file = glob.glob('*.txt')[0]
        with open(f'./{text_file}', encoding = 'utf-8') as f:
            data = f.read()

        data = str(data).strip().split()
        _randomize = lambda data: random.randrange(0, len(data))
        self.entry_text = ' '.join([data[_randomize(data)] for _ in range(length)])

    def display(self, screen, rect, cur_pos, full = False, aa=True):
        text = self.entry_text
        rect = pygame.Rect(rect.x * 1.5, rect.y * 1.25, rect.width-50, rect.height-80)
        y = rect.top 

        cur_line = 0
        lineSpacing = -4
        fontHeight = self.font.size("Tg")[1]

        while text:
            i = 1
            if y + fontHeight > rect.bottom:
                break
            while self.font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1
            if i < len(text): 
                i = text.rfind(" ", 0, i) + 1

            if not cur_line + i < cur_pos or full:
                for s in range(len(text[:i])):
                    index = cur_line+s
                    stasus = self.checks[index]
                    if index == cur_pos and self.difficulty != 'word-by-word':
                        self.font.underline = True
                    else:
                        self.font.underline = False                    
                    letter_surface = self.font.render(text[s], aa, self.color[stasus])
                    screen.blit(letter_surface, ((rect.x + 5)+s*self.font.size(text[s])[0], y + 5))
                y += fontHeight + lineSpacing
            cur_line += i
            text = text[i:]
        return text
    
    def analyze_input(self, input_text):
        pos = len(input_text)-1
        new_checks = self.checks[:pos]
        
        try:
            if input_text[-1] == self.entry_text[pos]:
                new_checks.insert(pos, 'correct')
            else:
                new_checks.insert(pos, 'incorrect')
                self.all_errors += 1

            if not len(input_text) >= len(self.checks):
                new_checks.extend([None for _ in range(len(self.checks) - len(new_checks))])
        
            self.checks = new_checks
        except (ValueError, IndexError):
            pass
    
    def analyze_word(self, input_text, sbpress):
        if sbpress:
            f,l = int(self.checks.index('current')), int(len(self.checks) - self.checks[-1::-1].index('current'))
            word = self.entry_text[f:l].strip()

            user_word = input_text.strip()

            if ' ' in input_text[:-2]:
                user_word = input_text[input_text.rindex(' ',0,-1):].strip()

            new_checks = self.checks[:f]
            new_checks.extend(['correct' if word == user_word else 'incorrect' for _ in range(len(word))])
            if len(new_checks) < len(self.checks):
                new_checks.append('correct')

            if l+1 < len(self.entry_text):
                if ' ' in self.entry_text[l+1:]:
                    cur_length = self.entry_text.index(' ',l+1) - l -1
                else:
                    cur_length = len(self.entry_text[l+1:])
                new_checks.extend(['current' for _ in range(cur_length)])

            new_checks.extend([None for _ in range(len(self.checks)-len(new_checks))])
            self.checks = new_checks
            self.all_errors = self.count_errors()

    def done(self, input_text):
        return not None in self.checks and 'current' not in self.checks

    def retrieve_trim(self, length):
        return self.entry_text[:length]

    def difficulty_fail(self):
        if self.difficulty == 'expert':
            try:
                return self.entry_text[self.checks.index('incorrect')] != ' '
            except ValueError:
                pass

        if self.difficulty == 'master':
            if bool(self.all_errors):
                self.trim(self.checks.index(None))

        return False

    def trim(self, length):
        self.entry_text = self.entry_text[:length]
        self.checks = self.checks[:length]

    def count_errors(self):
        """ Only errors that are resulted and does not count corrected errors """
        return sum([1 for x in self.checks if x == 'incorrect'])

    def count_correct(self):
        """ Typed entries that are correct as the result of how many uncorrected erors """
        return self.length() - self.count_errors()
    
    def count_true_correct(self):
        """ Typed entries minus errors uncorrected and corrected """
        return self.length() - self.all_errors
    
    def length(self):
        return len(self.entry_text)
    