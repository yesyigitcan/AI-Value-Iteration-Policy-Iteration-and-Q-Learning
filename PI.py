from copy import deepcopy
from tabulate import tabulate
import numpy
def isConvergence(previous_map_policy, map_policy):
    if previous_map_policy == map_policy:
        return 1
    else:
        return 0

def policy_iteration(input, r, d, p):
    transition = [[-1,0],[1,0],[0,1],[0,-1]] # up,down,right,left
    MAX_ITER_NUMBER = 100000
    numpy.random.seed(62)
    map_row = len(input)
    map_col = len(input[0])

    table_headers = [" "]
    table_data = []

    states = []
    counter = 0
    for row in range(map_row):
        for col in range(map_col):
            if input[row][col][0] == "E":
                states.append([row, col])
                table_headers.append("s" + str(counter))
                counter += 1

    map_value = []


    for row in range(map_row):
        map_value.append(list(numpy.zeros(map_col)))

    map_policy = {} # row, col, policy
    previous_map_policy = deepcopy(map_policy)

    for row, col in states:
        map_policy.update({tuple([row,col]) : numpy.random.randint(0,4)})
        #map_policy.update({tuple([row, col]): 3})

    for row in range(map_row):
        for col in range(map_col):
            if input[row][col][0] == "T":
                map_value[row][col] = input[row][col][1]

    counter = 0
    while isConvergence(previous_map_policy, map_policy) == False and counter < MAX_ITER_NUMBER:
        previous_map_policy = deepcopy(map_policy)
        previous_map_value = deepcopy(map_value)
        table_row = ["it" + str(counter)]


        for row, col in states:
            map_value[row][col] = getValue(previous_map_value,previous_map_policy[(row,col)],row,col)
            table_row.append(previous_map_value[row][col])

        for row, col in states:
            new_value = r + d * max(utilityValueList(map_value, p, row, col))
            map_value[row][col] = new_value

        for row,col in states:
            map_policy.update({(row,col): getArrowIndex(map_value,row,col)})

        table_data.append(table_row)

        counter += 1
    print(tabulate(table_data,headers=table_headers))













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


def getValue(map_value, arrowIndex, currentRow, currentCol):
    rowSize = len(map_value)
    colSize = len(map_value[0])

    if arrowIndex == 0:
        if currentRow - 1 > -1:
            return map_value[currentRow-1][currentCol]
        else:
            return 0.0
    elif arrowIndex == 1:
        if currentRow + 1 < rowSize:
            return map_value[currentRow + 1][currentCol]
        else:
            return 0.0
    elif arrowIndex == 2:
        if currentCol + 1 < colSize:
            return map_value[currentRow][currentCol + 1]
        else:
            return 0.0
    elif arrowIndex == 3:
        if currentCol - 1 > -1:
            return map_value[currentRow][currentCol-1]
        else:
            return 0.0
    else:
        print("Error in PI")

def getArrowIndex(map_value, currentRow, currentCol):
    rowSize = len(map_value)
    colSize = len(map_value[0])
    temp = []
    if currentRow - 1 > -1:
        temp.append(map_value[currentRow-1][currentCol])
    else:
        temp.append(0.0)
    if currentRow + 1 < rowSize:
        temp.append(map_value[currentRow + 1][currentCol])
    else:
        temp.append(0.0)
    if currentCol + 1 < colSize:
        temp.append(map_value[currentRow][currentCol+1])
    else:
        temp.append(0.0)
    if currentCol - 1 > -1:
        temp.append(map_value[currentRow][currentCol-1])
    else:
        temp.append(0.0)
    return numpy.argmax(temp)