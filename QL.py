import numpy
from copy import deepcopy
import math
from tabulate import tabulate
def qlearning(input, r , d, e, a, start_location, N):
    numpy.random.seed(62)

    table_data = []
    table_headers = [" "]

    map_row = len(input)
    map_col = len(input[0])

    map_value = []
    states = []         # states location
    states_move = {}    # moving up down right left value
    counter = 0
    for row in range(map_row):
        row_temp = []
        for col in range(map_col):
            if input[row][col][0] == "E":
                states.append([row,col])
                table_headers.append("s" + str(counter))
                counter += 1
                states_move.update({(row,col): list(numpy.zeros(4))})
            row_temp.append(input[row][col][1])

        map_value.append(row_temp)





    for step in range(N):
        current_location = [start_location[0], start_location[1]]
        while True:

            if input[current_location[0]][current_location[1]][0] == "T":
                break

            now_state_list = states_move[(current_location[0],current_location[1])]
            next_state = numpy.argmax(now_state_list)

            if numpy.random.rand() <= e:
                next_state = numpy.random.randint(0,4)

            straight_randomness = numpy.random.rand()
            if 0.8 < straight_randomness and straight_randomness < 0.9:
                next_state = ((next_state - 1) + 4) % 4
            elif 0.9 < straight_randomness:
                next_state = (next_state + 1) % 4

            now_state_list[next_state] = (1-a) * now_state_list[next_state] + a * (r + d * getValue(input,states_move,next_state,current_location[0],current_location[1]))

            states_move.update({(current_location[0],current_location[1]):now_state_list})

            '''
            while not isLegalMove(map_value,input,next_state,current_location[0],current_location[1]):
                temp[numpy.argmax(temp)] = -math.inf
                next_state = numpy.argmax(temp)
            '''

            if next_state == 0:
                if current_location[0] - 1 > -1 and input[current_location[0]-1][current_location[1]][0] != "B":
                    current_location[0] = current_location[0] - 1
            elif next_state == 1:
                if current_location[0] + 1 < map_row and input[current_location[0]+1][current_location[1]][0] != "B":
                    current_location[0] = current_location[0] + 1
            elif next_state == 2:
                if current_location[1] + 1 < map_col and input[current_location[0]][current_location[1]+1][0] != "B":
                    current_location[1] = current_location[1] + 1
            elif next_state == 3:
                if current_location[1] - 1 > - 1 and input[current_location[0]][current_location[1]-1][0] != "B":
                    current_location[1] = current_location[1] - 1
            else:
                print("Error during QLearning at line 65")

    for i in range(4):
        table_row = ["Action " + str(i)]
        for row, col in states:
            temp = states_move[(row, col)]
            table_row.append(temp[i])
        table_data.append(table_row)
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


def getValue(input, states_move, arrowIndex, currentRow, currentCol):
    rowSize = len(input)
    colSize = len(input[0])

    if arrowIndex == 0:
        if currentRow - 1 > -1:
            if input[currentRow-1][currentCol][0] == "T" or input[currentRow-1][currentCol][0] == "B":
                return input[currentRow-1][currentCol][1]
            else:
                return numpy.max(states_move[(currentRow-1,currentCol)])
        else:
            return 0.0
    elif arrowIndex == 1:
        if currentRow + 1 < rowSize:
            if input[currentRow + 1][currentCol][0] == "T" or input[currentRow + 1][currentCol][0] == "B":
                return input[currentRow + 1][currentCol][1]
            else:
                return numpy.max(states_move[(currentRow+1,currentCol)])
        else:
            return 0.0
    elif arrowIndex == 2:
        if currentCol + 1 < colSize:
            if input[currentRow][currentCol + 1][0] == "T" or input[currentRow][currentCol + 1][0] == "B":
                return input[currentRow][currentCol + 1][1]
            else:
                return numpy.max(states_move[(currentRow,currentCol + 1)])
        else:
            return 0.0
    elif arrowIndex == 3:
        if currentCol - 1 > -1:
            if input[currentRow][currentCol-1][0] == "T" or input[currentRow][currentCol-1][0] == "B":
                return input[currentRow][currentCol-1][1]
            else:
                return numpy.max(states_move[(currentRow,currentCol-1)])
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

def isLegalMove(map_value, input, arrowIndex,row, col):
    map_row = len(map_value)
    map_col = len(map_value[0])

    if arrowIndex == 0:
        if row - 1 > -1 and input[row - 1][col][0] != "B":
            return 1
    elif arrowIndex == 1:
        if row + 1 < map_row and input[row + 1][col][0] != "B":
            return 1
    elif arrowIndex == 2:
        if col + 1 < map_col and input[row][col + 1][0] != "B":
            return 1
    elif arrowIndex == 3:
        if col - 1 > -1 and input[row][col - 1][0] != "B":
            return 1
    else:
        print("Error during isLegalMove in QL")

    return 0





