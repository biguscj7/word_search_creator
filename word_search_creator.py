from copy import copy, deepcopy
import random

def createWordSearch(words):
	# grid side length is the length of the longest word
	# --> makes word search possible to generate with given words and grid size
	gridSideLength = len(max(words, key=len))

	# generate 2d array with side lengths of gridSideLength, with each item having a content of ""
	grid = [[""]*gridSideLength]*gridSideLength

	# loop through words and place them randomly in the grid, either horizontally, vertically, or diagonally
	for word in words:
		# choose randomly between possible placement types (horizontal, vertical, and diagonal)
		placementType = random.choice(["horizontal", "vertical", "diagonal"])

		# placement status (when placed, placement status is True and while loop ends)
		placementStatus = False
		while(placementStatus == False):
			# create grid copy to be edited in testing
			gridCopy = deepcopy(grid)

			# create random coordinates for placement location
			placementLocation = [random.randrange(gridSideLength), random.randrange(gridSideLength)]
			if(placementType == "horizontal" or placementType == "diagonal"):
				placementLocation[0] = random.randrange(gridSideLength - len(word))
			if(placementType == "vertical" or placementType == "diagonal"):
				placementLocation[1] = random.randrange(gridSideLength - len(word))

			print "Type: " + placementType + "\nPosition: " + str(placementLocation) + "\n======"
	# fill the rest of grid with random letters
	for rowIndex in range(len(grid)):
		row = deepcopy(grid[rowIndex])
		for itemIndex in range(len(row)):
			if(row[itemIndex] == ""):
				row[itemIndex] = random.choice(list("abcdefghijklmnopqrstuvwxyz"))
		grid[rowIndex] = deepcopy(row)

	return grid


		
	

# convert word search grid to printable string
def stringifyWordSearch(wordSearchArray):
	returnValue = ""
	for row in wordSearchArray:
		returnValue += " ".join(row) + "\n"
	# return concatenated rows, joined with a newline --> the [:-1] is to remove the last trailing newline
	return returnValue[:-1]

# test createWordSearch function with 8 randomly generated words
returnedWordSearch = createWordSearch(["seemly", "exotic", "obese", "disagreeable", "earn", "spark", "strengthen", "colossal"])
print stringifyWordSearch(returnedWordSearch)