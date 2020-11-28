from copy import copy, deepcopy
import random
from math import sqrt
import string
import logging

# TODO: Update the reader fuction to handle multiple .txt file formats of words

logging.basicConfig(
    filename="word_search.log",
    format="%(asctime)s : %(levelname)s : %(message)s",
    level=logging.DEBUG,
)


def read_from_txt(txt_file: str = "untitled.txt") -> list:
    """Opens a text file to get all words, called from outside the class instantiation"""
    with open(txt_file, "r") as words:
        lines = words.readlines()
        return [
            line.split(".")[1].strip().upper() for line in lines
        ]  # removes leading numbering w/ following '.'


class CreateWordSearch:
    """Class that generates a particular word search"""

    def __init__(self, words: list, out_file: str = "intx_test.txt"):
        self.words = words
        logging.info(f"Word list has {len(self.words)} words.")
        self.search_words = self.reverse_sort_words()
        self.grid = self.create_grid()
        self.fill_words()
        self.fill_grid()
        self.write_grid(out_file)
        self.write_words(out_file)

    def reverse_sort_words(self, rev_percent: int = 25):
        """Reverses a percentage of the words and returns a list sorted from longest to shortest words to help with filling the sheet"""
        rev_words = deepcopy(self.words)
        for idx, word in enumerate(rev_words):
            if random.randint(0, 100) <= rev_percent:
                rev_words[idx] = word[::-1].replace(" ", "")
            else:
                rev_words[idx] = word.replace(" ", "")

        rev_words.sort(
            key=len, reverse=True
        )  # starting with long words minimizes chance of looping

        return rev_words

    def create_grid(self) -> list:
        """Builds an 'empty' grid based on characteristics of the word list supplied."""
        str_lengths = [len(word) for word in self.search_words]
        total_chars = sum(str_lengths)
        logging.info(f"Total characters in word list: {total_chars}")

        array_chars = total_chars / 0.70
        char_dim = int(sqrt(array_chars))
        logging.info(
            f"Dimesion based on word characters at 70% of available spaces: {char_dim}"
        )

        longest_word_len = len(max(self.search_words, key=len))
        buffer = int(longest_word_len * 0.3)

        long_word_dim = longest_word_len + buffer
        logging.info(f"Dimension based on longest word: {long_word_dim}")

        self.grid_dimension = char_dim if char_dim >= long_word_dim else long_word_dim
        logging.info(f"Chosen maximum dimension: {self.grid_dimension}")

        grid = []
        for _ in range(self.grid_dimension):
            grid.append(list("_" * self.grid_dimension))
        return grid

    def fill_words(self):
        """Loops through words and adds them to the grid"""
        for word in self.search_words:

            # pick orientation of word (vertical, horizontal, diagonal)
            orientation = random.choice(["vertical", "horizontal", "diagonal"])

            options = self.assess_options(orientation, word)

            if options is None:
                logging.warning(f"Unable to find valid placement for '{word}'")
                raise Exception()

            intx_options = [option for option in options if option[2] > 0]

            if intx_options:  # there's at least one valid option
                self.place_word(random.choice(intx_options), orientation, word)
            else:
                self.place_word(random.choice(options), orientation, word)

        self.before_fill = deepcopy(self.grid)

    def assess_options(self, orientation: str, word: str) -> list:
        """Assesses all possible placements of a word and returns a list with viable
        orientations & number of intersections"""

        valid_starts = []  # will store in tuple (row, col, intx)

        if orientation == "horizontal":
            max_row = self.grid_dimension - 1
            max_col = self.grid_dimension - len(word)

            for row in range(0, max_row):
                for col in range(0, max_col):
                    intx = self.check_horizontal((row, col), word)
                    if intx >= 0:
                        valid_starts.append((row, col, intx))

        elif orientation == "vertical":
            max_row = self.grid_dimension - len(word)
            max_col = self.grid_dimension - 1

            for row in range(0, max_row):
                for col in range(0, max_col):
                    intx = self.check_vertical((row, col), word)
                    if intx >= 0:
                        valid_starts.append((row, col, intx))

        else:
            max_row = self.grid_dimension - len(word)
            max_col = self.grid_dimension - len(word)

            for row in range(0, max_row):
                for col in range(0, max_col):
                    intx = self.check_diagonal((row, col), word)
                    if intx >= 0:
                        valid_starts.append((row, col, intx))

        return valid_starts

    def check_vertical(self, start: tuple, word: str) -> int:
        """Attempts to place word vertically and returns number of intersections"""
        intx = 0

        for idx, letter in enumerate(word):
            if (
                self.grid[start[0] + idx][start[1]] != "_"
                and self.grid[start[0] + idx][start[1]] != letter
            ):
                return -1
            elif self.grid[start[0] + idx][start[1]] == letter:
                intx += 1

        return intx

    def check_horizontal(self, start: tuple, word: str) -> int:
        """Attempts to place word horizontally and returns number of intersections"""
        intx = 0

        for idx, letter in enumerate(word):
            if (
                self.grid[start[0]][start[1] + idx] != "_"
                and self.grid[start[0]][start[1] + idx] != letter
            ):
                return -1
            elif self.grid[start[0]][start[1] + idx] == letter:
                intx += 1

        return intx

    def check_diagonal(self, start: tuple, word: str) -> int:
        """Attempts to place word diagonally and returns number of intersections"""
        intx = 0

        for idx, letter in enumerate(word):
            if (
                self.grid[start[0] + idx][start[1] + idx] != "_"
                and self.grid[start[0] + idx][start[1] + idx] != letter
            ):
                return -1
            elif self.grid[start[0] + idx][start[1] + idx] == letter:
                intx += 1

        return intx

    def place_word(self, start: tuple, orientation: str, word: str):
        """Places word on the grid from a start point and given orientation"""
        for idx, letter in enumerate(word):
            if orientation == "vertical":
                self.grid[start[0] + idx][start[1]] = letter
            elif orientation == "horizontal":
                self.grid[start[0]][start[1] + idx] = letter
            else:
                self.grid[start[0] + idx][start[1] + idx] = letter

    def fill_grid(self):
        """Fill the empty spots on the grid with random letters"""
        fill_opts = list(string.ascii_uppercase)
        for idx, row in enumerate(self.grid):
            for i, col in enumerate(row):
                if self.grid[idx][i] == "_":
                    self.grid[idx][i] = random.choice(fill_opts)

    def write_grid(self, filename: str):
        """Write the grid to a text file"""
        with open(filename, "w") as write_file:
            for row in self.grid:
                write_file.write(" ".join(row))
                write_file.write("\n")

    def write_words(self, filename: str):
        """Write the word list to the text file below the grid"""
        with open(filename, "a") as write_file:
            write_file.write("\n")
            for word in self.words:
                write_file.write(word + "\n")


if __name__ == "__main__":
    word_list = read_from_txt("US_States_Cities.txt")
    test = CreateWordSearch(word_list, "States_cities_puzzle.txt")
