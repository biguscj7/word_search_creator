from copy import copy, deepcopy
import random


def read_from_txt(txt_file: str = "ww2_words.txt") -> list:
    """Opens a text file to get all words"""
    with open(txt_file, "r") as words:
        lines = words.readlines()
        return [line.split(".")[1].lower().replace(" ", "").strip() for line in lines]


class CreateWordSearch:
    """Class that generates a particular word search"""

    def __init__(self, words: list):
        self.words = words
        self.reverse_words()
        self.grid = self.create_grid()

    def reverse_words(self, rev_percent: int = 25):
        for idx, word in enumerate(self.words):
            if random.randint(0, 100) <= rev_percent:
                self.words[idx] = word[::-1]

    def create_grid(self) -> list:
        """Find longest word and and 6 then create blank grid"""
        self.grid_dimension = len(max(self.words, key=len)) + 6
        return list(
            (self.grid.append(list(" " * self.grid_dimension)) * self.grid_dimension)
        )
