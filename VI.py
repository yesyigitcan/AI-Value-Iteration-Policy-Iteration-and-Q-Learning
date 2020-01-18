from copy import deepcopy
from tabulate import tabulate
import numpy

def isConvergence(previous_map_value, map_value, map_row, map_col):
    for row in range(map_row):
        for col in range(map_col):
            if abs(map_value[row][col] - previous_map_value[row][col]) >= 0.0001:
                return 0
    return 1


def value_iteration(input, r, d, p, showPolicy = 0):
    MAX_ITER_NUMBER = 100000
    map_row = len(input)
    map_col = len(input[0])

    states = [] # locations of states
    table_headers = [" "]
    table_data = []
    #   Table Headers Creation and Storing States Location#
    counter = 0
    for row in range(map_row):
        for col in range(map_col):
            if input[row][col][0] == "E":
                states.append([row, col])
                table_headers.append("s" + str(counter))
                counter += 1

    map_value = []
    for i in range(map_row):
        map_value.append(list(numpy.zeros(map_col)))

    previous_map_value = deepcopy(map_value)

    table_row = ["it0"]
    for row, col in states:
        table_row.append(map_value[row][col])
    table_data.append(table_row)

    for row in range(map_row):
        for col in range(map_col):
            if input[row][col][0] == "T":
                map_value[row][col] = input[row][col][1]

    table_row = ["it1"]
    for row, col in states:
        table_row.append(map_value[row][col])
    table_data.append(table_row)

    counter = 2

    while isConvergence(previous_map_value, map_value, map_row, map_col) == False and counter < MAX_ITER_NUMBER:
        previous_map_value = deepcopy(map_value)
        table_row = ["it" + str(counter)]
        for row, col in states:
            # up, down, right, left
            new_value = r + d * max(utilityValueList(previous_map_value, p, row, col))
            table_row.append(new_value)
            map_value[row][col] = new_value
        table_data.append(table_row)
        counter += 1



    print(tabulate(table_data,headers=table_headers))
    if showPolicy:
        table_data = []

        for row in range(map_row):
            table_row = []
            for col in range(map_col):
                if input[row][col][0] == "E":
                    table_row.append(["UP","DOWN","RIGHT","LEFT"][getArrowIndex(map_value,row,col)])
                else:
                    table_row.append(input[row][col][0])
            table_data.append(table_row)
        print(tabulate(table_data))


    return map_value


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