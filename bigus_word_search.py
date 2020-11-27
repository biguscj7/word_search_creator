from copy import copy, deepcopy
import random
from math import sqrt
import string

def read_from_txt(txt_file: str = "ww2_words.txt") -> list:
    """Opens a text file to get all words"""
    with open(txt_file, "r") as words:
        lines = words.readlines()
        return [line.split(".")[1].strip().upper() for line in lines]


class CreateWordSearch:
    """Class that generates a particular word search"""

    def __init__(self, words: list, out_file: str = "smaller_out.txt"):
        self.words = words
        self.search_words = self.reverse_words()
        self.grid = self.create_grid()
        self.fill_words()
        self.fill_grid()
        self.write_grid(out_file)
        self.write_words(out_file)

    def reverse_words(self, rev_percent: int = 25):
        rev_words = deepcopy(self.words)
        for idx, word in enumerate(rev_words):
            if random.randint(0, 100) <= rev_percent:
                rev_words[idx] = word[::-1].replace(" ", "")
            else:
                rev_words[idx] = word.replace(" ", "")
                
        return rev_words

    def create_grid(self) -> list:
        """Find longest word and and 6 then create blank grid"""
        #number_of_words = len(self.words)
        
        str_lengths = [len(word) for word in self.search_words]
        total_chars = sum(str_lengths)
        
        array_chars = total_chars / 0.4
        char_dim = int(sqrt(array_chars))
                
        longest_word_len = len(max(self.search_words, key=len))
        buffer = int(longest_word_len * 0.3)
        
        long_word_dim = longest_word_len + buffer
                
        self.grid_dimension = char_dim if char_dim >= long_word_dim else long_word_dim
        grid = []
        for _ in range(self.grid_dimension):
            grid.append(list("_" * self.grid_dimension))
        return grid
    
    def fill_words(self):
        """Will loop through words and add them to the grid"""
        for word in self.search_words:        

            is_valid = False
            while not is_valid:
                # pick orientation of word (vertical, horizontal, diagonal)
                orientation = random.choice(['vertical', 'horizontal', 'diagonal'])
                
                # pick a starting point for the word that won't bust size of grid
                if orientation == 'vertical' or orientation == 'diagonal':
                    start_row = random.randint(0, self.grid_dimension - len(word))
                else:
                    start_row = random.randint(0, self.grid_dimension - 1)

                if orientation == 'horizontal' or orientation == 'diagonal':
                    start_col = random.randint(0, self.grid_dimension - len(word))
                else:
                    start_col = random.randint(0, self.grid_dimension - 1)

                # check if placement is viable (no conflicting letters)
                if orientation == 'vertical':
                    is_valid = self.check_vertical((start_row, start_col), word)
                elif orientation == 'horizontal':
                    is_valid = self.check_horizontal((start_row, start_col), word)
                elif orientation == 'diagonal':
                    is_valid = self.check_diagonal((start_row, start_col), word)

    def check_vertical(self, start: tuple, word: str) -> bool:
        test_grid = deepcopy(self.grid)
        
        for idx, letter in enumerate(word):
            if (test_grid[start[0] + idx][start[1]] != "_" and 
                test_grid[start[0] + idx][start[1]] != letter):
                return False # early return if there's a conflict
            else:
                test_grid[start[0] + idx][start[1]] = letter
        
        # if loop hasn't broken for a conflict, write the modified grid back to instance grid
        self.grid = test_grid        
        return True       

    def check_horizontal(self, start: tuple, word: str) -> bool:
        test_grid = deepcopy(self.grid)
        
        for idx, letter in enumerate(word):
            if (self.grid[start[0]][start[1] + idx] != "_" and 
                self.grid[start[0]][start[1] + idx] != letter):
                return False
            else:
                test_grid[start[0]][start[1] + idx] = letter
                
        self.grid = test_grid 
        return True 

    def check_diagonal(self, start: tuple, word: str) -> bool:
        test_grid = deepcopy(self.grid)
        
        for idx, letter in enumerate(word):
            if (self.grid[start[0] + idx][start[1] + idx] != "_" and 
                self.grid[start[0] + idx][start[1] + idx] != letter):
                return False
            else:
                test_grid[start[0] + idx][start[1] + idx] = letter
        
        self.grid = test_grid 
        return True 
            
    def fill_grid(self):
        fill_opts = list(string.ascii_uppercase)
        for idx, row in enumerate(self.grid):
            for i, col in enumerate(row):
                if self.grid[idx][i] == "_":
                    self.grid[idx][i] = random.choice(fill_opts)

    def write_grid(self, filename: str):
        with open(filename, 'w') as write_file:
            for row in self.grid:
                write_file.write(" ".join(row))
                write_file.write("\n")
    
    def write_words(self, filename: str):
        with open(filename, 'a') as write_file:
            write_file.write("\n")
            for word in self.words:
                write_file.write(word + "\n")
            