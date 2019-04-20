def createWordSearch(words):
	gridSideLength = 0
	for word in words:
		# grid side length is 4 added to the length of the longest word
		# --> makes word search harder and possible to generate with given words and grid size
		if(gridSideLength - 4 < len(word)):
			gridSideLength = len(word) + 4

	# generate 2d array with side lengths of gridSideLength, with each item having a content of ""
	grid = [[""]*gridSideLength]*gridSideLength
	