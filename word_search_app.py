# import word_search_creator.py via the execfile function
exec(open("./word_search_creator.py").read())

# request name of word search
wordSearchName = input("\nName of word search: ")


def read_from_txt(txt_file: str = "ww2_words.txt") -> list:
    """Opens a text file to get all words"""
    with open(txt_file, "r") as words:
        lines = words.readlines()
        return [line.split(".")[1].lower().replace(" ", "").strip() for line in lines]


# request words from user
# wordListFile = input("Enter filename of your word list: ")
wordList = read_from_txt()

# list of accepted letters for words
acceptedLetters = list("abcdefghijklmnopqrstuvwxyz")

# filter word list into words with accepted letters
for wordIndex in range(len(wordList)):
    word = wordList[wordIndex]
    filteredWord = ""
    for letter in word:
        if letter in acceptedLetters:
            filteredWord += letter
    wordList[wordIndex] = filteredWord

# create word search via function in word_search_creator.py
wordSearchArray = createWordSearch(wordList)

# get stringified word search via function in word_search_creator.py, and split into rows
stringifiedWordSearch = stringifyWordSearch(wordSearchArray).split("\n")

# print word search name correctly centered
paddingLength = int(
    round(
        (
            4
            + len(max(wordList, key=len))
            + len(stringifiedWordSearch[0])
            - len(wordSearchName)
            - 2
        )
        / 2
    )
    + 1
)

print("")
print(("=" * paddingLength) + " " + wordSearchName + " " + ("=" * paddingLength))
print("")

# regenerate word list to fit initial user-inputted letter-cases
wordList = read_from_txt(wordListFile)

# list of accepted letters for words
acceptedLetters = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

# filter word list into words with accepted letters
for wordIndex in range(len(wordList)):
    word = wordList[wordIndex]
    filteredWord = ""
    for letter in word:
        if letter in acceptedLetters:
            filteredWord += letter
    wordList[wordIndex] = filteredWord

# print word search along with words to find
for rowIndex in range(len(stringifiedWordSearch)):
    if rowIndex < len(wordList):
        print(stringifiedWordSearch[rowIndex] + "    " + wordList[rowIndex])
    else:
        print(stringifiedWordSearch[rowIndex])
print("")
