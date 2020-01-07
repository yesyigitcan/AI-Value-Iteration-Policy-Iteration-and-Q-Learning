class ValueIterationMap:
    def __init__(self, map, alpha = 1, rs = -0.03, probability_forward = 0.8, N = 1):
        self.alpha = alpha
        self.rs = rs
        self.pf = probability_forward            # probability forward
        self.po = (1 - probability_forward) / 2  # probability others
        self.N = N
        self.utility = []
        self.map = map
        self.rowlen = len(self.map)
        self.collen = len(self.map[0])
        self.special_coordinates = []
        for i in range(self.rowlen):
            temp = []
            for j in range(self.collen):
                temp.append(0)
            self.utility.append(temp)
            for j in range(self.collen):
                if type(self.map[i][j]) == int:
                    self.utility[i][j] = self.map[i][j]
                    self.special_coordinates.append([i,j])

    def getUtilityMatrix(self, i, j):
        utility_scores = []
        # up
        temp = 0.0
        if i - 1 > -1:
            temp += self.pf * self.utility[i - 1][j]
        if j + 1 < self.collen:
            temp += self.po * self.utility[i][j + 1]
        if j - 1 > -1:
            temp += self.po * self.utility[i][j - 1]
        utility_scores.append(temp)
        # down
        temp = 0.0
        if i + 1 < self.rowlen:
            temp += self.pf * self.utility[i + 1][j]
        if j + 1 < self.collen:
            temp += self.po * self.utility[i][j + 1]
        if j - 1 > -1:
            temp += self.po * self.utility[i][j - 1]
        utility_scores.append(temp)
        # right
        temp = 0.0
        if j + 1 < self.collen:
            temp += self.pf * self.utility[i][j + 1]
        if i - 1 > -1:
            temp += self.po * self.utility[i - 1][j]
        if i + 1 < self.rowlen:
            temp += self.po * self.utility[i + 1][j]
        utility_scores.append(temp)
        # left
        temp = 0.0
        if j - 1 > -1:
            temp += self.pf * self.utility[i][j - 1]
        if i - 1 > -1:
            temp += self.po * self.utility[i - 1][j]
        if i + 1 < self.rowlen:
            temp += self.po * self.utility[i + 1][j]
        utility_scores.append(temp)
        return utility_scores

    def getUtilityCalculatedMap(self):
        utility_arrows = ["UP","DOWN","RIGHT","LEFT"]
        featureCounter = 0
        for i in range(self.rowlen):
            for j in range(self.collen):
                if self.map[i][j] in utility_arrows:
                    self.map[i][j] = "."
                    featureCounter += 1
                elif self.map[i][j] != "W" and self.map[i][j] != "B" and type(self.map[i][j]) != int:
                    featureCounter += 1

        print("\t\t", end="")
        for i in range(featureCounter):
            print("s" + str(i), end="\t\t")
        print()

        iterationCount = 0
        self.printUtilityTable(iterationCount)

        for step in range(self.N):
            iterationCount += 1
            self.printUtilityTable(iterationCount)
            for i in range(self.rowlen):
                for j in range(self.collen):
                    j = self.collen - j - 1
                    if self.map[i][j] == ".":
                        utility_matrix = self.getUtilityMatrix(i, j)
                        max_index = utility_matrix.index(max(utility_matrix))
                        self.map[i][j] = utility_arrows[max_index]
                        self.utility[i][j] = self.rs + self.alpha * utility_matrix[max_index]

        return self.map

    def printArrowMap(self):
        for i in range(self.rowlen):
            for j in range(self.collen):
                if self.map[i][j] != "W":
                    if self.map[i][j] == "B":
                        self.map[i][j] = "BLOCK"
                    word_len = len(str(self.map[i][j]))
                    print(self.map[i][j], end="")
                    for k in range(10 - word_len):
                        print("",end=" ")
            print("")

    def printUtilityMap(self):
        for i in range(self.rowlen):
            for j in range(self.collen):
                if self.map[i][j] != "W":
                    print("{0:.4f}".format(self.utility[i][j]), end="")
                    if self.utility[i][j] < 0:
                        print("", end="   ")
                    else:
                        print("", end="    ")
            print("")

    def printUtilityTable(self, iterationNumber):
        utility_arrows = ["UP", "DOWN", "RIGHT", "LEFT"]
        counter = 0

        if iterationNumber < 10:
            print("it" + str(iterationNumber), end="\t\t")
        elif iterationNumber < 100:
            print("it" + str(iterationNumber), end="\t")
        else:
            print("it" + str(iterationNumber), end="   ")

        for i in range(self.rowlen):
            for j in range(self.collen):
                if self.map[i][j] in utility_arrows or self.map[i][j] == ".":
                    print("{0:.4f}".format(self.utility[i][j]), end="\t")
        print()





