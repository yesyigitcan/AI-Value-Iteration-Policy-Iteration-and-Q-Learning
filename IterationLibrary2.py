from copy import deepcopy
from tabulate import tabulate
import numpy
def utilityValueList(input, p, i, j):
    pf = p
    po = float((1-p)/2)
    rowSize = len(input)
    colSize = len(input[0])
    utility_scores = []
    # up
    temp = 0.0
    if i - 1 > -1:
        temp += pf * input[i - 1][j]
    if j + 1 < colSize:
        temp += po * input[i][j + 1]
    if j - 1 > -1:
        temp += po * input[i][j - 1]
    utility_scores.append(temp)
    # down
    temp = 0.0
    if i + 1 < rowSize:
        temp += pf * input[i + 1][j]
    if j + 1 < colSize:
        temp += po * input[i][j + 1]
    if j - 1 > -1:
        temp += po * input[i][j - 1]
    utility_scores.append(temp)
    # right
    temp = 0.0
    if j + 1 < colSize:
        temp += pf * input[i][j + 1]
    if i - 1 > -1:
        temp += po * input[i - 1][j]
    if i + 1 < rowSize:
        temp += po * input[i + 1][j]
    utility_scores.append(temp)
    # left
    temp = 0.0
    if j - 1 > -1:
        temp += pf * input[i][j - 1]
    if i - 1 > -1:
        temp += po * input[i - 1][j]
    if i + 1 < rowSize:
        temp += po * input[i + 1][j]
    utility_scores.append(temp)
    return utility_scores

def utilityValueDirected(input, arrow, i, j):
    rowSize = len(input)
    colSize = len(input[0])
    if arrow == "UP":
        if i - 1 > -1:
            return input[i - 1][j]
        else:
            return 0.0
    elif arrow == "RIGHT":
        if j + 1 < colSize:
            return input[i][j + 1]
        else:
            return 0.0
    elif arrow == "LEFT":
        if j - 1 > -1:
            return input[i][j - 1]
        else:
            return 0.0
    elif arrow == "DOWN":
        if i + 1 < rowSize:
            return input[i + 1][j]
        else:
            return 0.0
    else:
        print("Error in function :: utilityValueDirected")

def valueIteration(input, d = 1, r = -0.03, p = 0.8, n = 1, isMapShown = 0):
    arrows = ["UP", "DOWN", "RIGHT", "LEFT"]
    map = deepcopy(input)
    utility = deepcopy(input)
    rowSize = len(utility)
    colSize = len(utility[0])

    tableHeaders = [" "]
    tableData = []

    featureCounter = 0
    iterationCounter = 0
    tableRow = ["it" + str(iterationCounter)]
    for rowNum in range(rowSize):
        for colNum in range(colSize):
            if type(utility[rowNum][colNum]) != int and type(utility[rowNum][colNum]) != float:
                utility[rowNum][colNum] = 0.0
                if map[rowNum][colNum] == ".":
                    tableHeaders.append("s" + str(featureCounter))
                    tableRow.append(utility[rowNum][colNum])
                    featureCounter += 1
    tableData.append(tableRow)
    iterationCounter += 1
    utility_step = deepcopy(utility)

    for step in range(n-1):
        utility = deepcopy(utility_step)
        tableRow = ["it" + str(iterationCounter)]
        for rowNum in range(rowSize):
            for colNum in range(colSize):
                if map[rowNum][colNum] == "." or map[rowNum][colNum] in arrows:
                    tableRow.append(utility_step[rowNum][colNum])
                    utilityScores = utilityValueList(utility, p, rowNum, colNum)
                    map[rowNum][colNum] = arrows[utilityScores.index(max(utilityScores))]
                    utility_step[rowNum][colNum] = r + d * max(utilityScores)

        iterationCounter += 1
        tableData.append(tableRow)
    print(tabulate(tableData, headers=tableHeaders))

    if isMapShown:
        print()
        tableData = []
        for i in range(rowSize):
            tableData.append(map[i])
        print(tabulate(tableData))
    return map

def policyIteration(input, d = 1, r = -0.03, p = 0.8, n = 1, isMapShown = 0):
    numpy.random.seed(62)
    arrows = ["UP","DOWN","RIGHT","LEFT"]
    map = deepcopy(input)
    utility = deepcopy(input)
    rowSize = len(utility)
    colSize = len(utility[0])

    tableHeaders = [" "]
    tableData = []

    featureCounter = 0
    iterationCounter = 0
    tableRow = ["it" + str(iterationCounter)]
    for rowNum in range(rowSize):
        for colNum in range(colSize):
            if type(utility[rowNum][colNum]) != int and type(utility[rowNum][colNum]) != float:
                utility[rowNum][colNum] = 0.0
                if map[rowNum][colNum] == ".":
                    map[rowNum][colNum] = arrows[numpy.random.randint(0,4)]
                    tableHeaders.append("s" + str(featureCounter))
                    tableRow.append(utility[rowNum][colNum])
                    featureCounter += 1
    tableData.append(tableRow)
    iterationCounter += 1
    utility_step = deepcopy(utility)
    for step in range(n-1):
        utility = deepcopy(utility_step)
        tableRow = ["it" + str(iterationCounter)]
        for rowNum in range(rowSize):
            for colNum in range(colSize):
                if map[rowNum][colNum] in arrows:
                    tableRow.append(utility_step[rowNum][colNum])
                    utility_step[rowNum][colNum] = utilityValueDirected(utility, map[rowNum][colNum], rowNum, colNum)

        for rowNum in range(rowSize):
            for colNum in range(colSize):
                if map[rowNum][colNum] in arrows:
                    utilityScores = utilityValueList(utility_step, p, rowNum, colNum)
                    map[rowNum][colNum] = arrows[utilityScores.index(max(utilityScores))]

        iterationCounter += 1
        tableData.append(tableRow)
    print(tabulate(tableData, headers=tableHeaders))
    if isMapShown:
        print()
        tableData = []
        for i in range(rowSize):
            tableData.append(map[i])
        print(tabulate(tableData))
    return map

def printMap(input):
    tableData = []
    for i in range(len(input)):
        tableData.append(input[i])
    print(tabulate(tableData))

def nextState(input, arrow, i, j):
    rowSize = len(input)
    colSize = len(input[0])
    if arrow == "UP":
        if i - 1 > -1:
            if input[i-1][j] == ".":
                return 0.0, 1, i-1, j   # utility value, isMovable, nextRow, nextCol
            elif input[i-1][j] == "B":
                return 0.0, 0, i, j
            elif type(input[i-1][j]) == int or type(input[i-1][j]) == float:
                return input[i-1][j], 1, i-1, j
            else:
                print("Error during function :: nextStateReward")
        else:
            return 0.0, 0, i, j
    elif arrow == "RIGHT":
        if j + 1 < colSize:
            if input[i][j+1] == ".":
                return 0.0, 1, i, j+1   # utility value, isMovable
            elif input[i][j+1] == "B":
                return 0.0, 0, i, j
            elif type(input[i][j+1]) == int or type(input[i][j+1]) == float:
                return input[i][j+1], 1, i, j+1
            else:
                print("Error during function :: nextStateReward")
        else:
            return 0.0, 0, i, j
    elif arrow == "LEFT":
        if j - 1 > -1:
            if input[i][j-1] == ".":
                return 0.0, 1, i, j-1   # utility value, isMovable
            elif input[i][j-1] == "B":
                return 0.0, 0, i, j
            elif type(input[i][j-1]) == int or type(input[i][j-1]) == float:
                return input[i][j-1], 1, i, j-1
            else:
                print("Error during function :: nextStateReward")
        else:
            return 0.0, 0, i, j
    elif arrow == "DOWN":
        if i + 1 < rowSize:
            if input[i+1][j] == ".":
                return 0.0, 1, i+1, j   # utility value, isMovable
            elif input[i+1][j] == "B":
                return 0.0, 0, i, j
            elif type(input[i+1][j]) == int or type(input[i+1][j]) == float:
                return input[i+1][j], 1, i+1, j
            else:
                print("Error during function :: nextStateReward")
        else:
            return 0.0, 0, i, j
    else:
        print("Error during function :: nextStateReward at last step")

# a : Learning rate
def QLearning(input, a = 1, d = 1, r = -0.03, e = 0.8, n = 1, isMapShown = 0):
    arrows = ["UP", "DOWN", "RIGHT", "LEFT"]

    numpy.random.seed(62)
    map = deepcopy(input)
    rowSize = len(input)
    colSize = len(input[0])
    targets = []
    for rowNum in range(rowSize):
        for colNum in range(colSize):
            if type(map[rowNum][colNum]) == int or type(map[rowNum][colNum]) == int:
                targets.append([rowNum,colNum])
    currentRow = 0
    currentCol = 0
    printMap(map)
    for step in range(n):
        if [currentRow, currentCol] in targets:
            QLearning(map, n=n)
        nextStepArrow = arrows[numpy.random.randint(0,4)]
        reward, isMovable, nextRow, nextCol = nextState(map, nextStepArrow, currentRow, currentCol)
        if map[currentRow][currentCol] == ".":
            map[currentRow][currentCol] = reward
        elif type(map[currentRow][currentCol]) == int or type(map[currentRow][currentCol]) == float:
            map[currentRow][currentCol] += reward
        else:
            print("Error during qlearning")
        print(nextStepArrow)
        printMap(map)
        print()
        if isMovable:
            currentRow = nextRow
            currentCol = nextCol

