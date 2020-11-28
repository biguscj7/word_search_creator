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


def read_from_txt(txt_file: str = "untitled1.txt") -> list:
    """Opens a text file to get all words, called from outside the class instantiation"""
    with open(txt_file, "r") as words:
        lines = words.readlines()
        return [
            line.split(".")[1].strip().upper() for line in lines
        ]  # removes leading numbering w/ following '.'


class CreateWordSearch:
    """Class that generates a particular word search"""

    def __init__(self, words: list, out_file: str = "smaller_out.txt"):
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

        array_chars = total_chars / 0.65
        char_dim = int(sqrt(array_chars))
        logging.info(
            f"Dimesion based on word characters at 65% of available spaces: {char_dim}"
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

            is_valid = False
            counter = 0
            while not is_valid:
                counter += 1
                # pick orientation of word (vertical, horizontal, diagonal)
                orientation = random.choice(["vertical", "horizontal", "diagonal"])

                # pick a starting point for the word that won't bust size of grid
                if orientation == "vertical" or orientation == "diagonal":
                    start_row = random.randint(0, self.grid_dimension - len(word))
                else:
                    start_row = random.randint(0, self.grid_dimension - 1)

                if orientation == "horizontal" or orientation == "diagonal":
                    start_col = random.randint(0, self.grid_dimension - len(word))
                else:
                    start_col = random.randint(0, self.grid_dimension - 1)

                # check if placement is viable (no conflicting letters)
                if orientation == "vertical":
                    is_valid = self.check_vertical((start_row, start_col), word)
                elif orientation == "horizontal":
                    is_valid = self.check_horizontal((start_row, start_col), word)
                elif orientation == "diagonal":
                    is_valid = self.check_diagonal((start_row, start_col), word)

                if counter > 150:
                    raise Unsolveable

            logging.info(f"Took {counter} attempts to find a valid spot for {word}")

        self.before_fill = deepcopy(self.grid)

    def check_vertical(self, start: tuple, word: str) -> bool:
        """Executes logic to attempt vertical placement of word"""
        test_grid = deepcopy(self.grid)  # make copy of grid for test purposes

        for idx, letter in enumerate(word):
            if (
                test_grid[start[0] + idx][start[1]] != "_"
                and test_grid[start[0] + idx][start[1]] != letter
            ):
                return False  # early return if there's a conflict, edited test_grid 'disappears'
            else:
                test_grid[start[0] + idx][start[1]] = letter

        # if loop hasn't broken for a conflict, write the modified grid back to instance grid
        self.grid = test_grid
        return True

    def check_horizontal(self, start: tuple, word: str) -> bool:
        """Executes logic to attempt horizontal placement of word"""
        test_grid = deepcopy(self.grid)

        for idx, letter in enumerate(word):
            if (
                self.grid[start[0]][start[1] + idx] != "_"
                and self.grid[start[0]][start[1] + idx] != letter
            ):
                return False
            else:
                test_grid[start[0]][start[1] + idx] = letter

        self.grid = test_grid
        return True

    def check_diagonal(self, start: tuple, word: str) -> bool:
        """Executes logic to attempt diagonal placement of word"""
        test_grid = deepcopy(self.grid)

        for idx, letter in enumerate(word):
            if (
                self.grid[start[0] + idx][start[1] + idx] != "_"
                and self.grid[start[0] + idx][start[1] + idx] != letter
            ):
                return False
            else:
                test_grid[start[0] + idx][start[1] + idx] = letter

        self.grid = test_grid
        return True

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
    test = CreateWordSearch(["LONGWORD", "LONGWORD"])
