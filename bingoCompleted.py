import math


class Bingo:
    #initialize
    def __init__(self,bingo_size = 5, bingo_range = 15):
        #define size and range
        self.bingoSize = bingo_size
        self.bingoRange = bingo_range
        
        #init cell
        self.usedCells = [[] for i in range((2 * bingo_size) + 3)]
        self.unUsedCells = [[] for i in range((2 * bingo_size) + 3)]

        #all card
        self.allCards = (self.perm(bingo_range,bingo_size))**\
           (bingo_size-1) * self.perm(bingo_range,bingo_size-1)
        
        #realNumber
        self.rowNumber = [0] * bingo_size
        #probability
        self.probability = []
        #bingoCard
        self.bingoCard = []

        #calculate
        self.countusedCells()

    
        
    #permutation
    def perm(self,n,r):
        return math.factorial(n) // math.factorial(n-r)

    #combination
    def comb(self,n,r):
        return math.factorial(n) // (math.factorial(n-r) * math.factorial(r))

    #add to virtualnumber
    def add(self,x):
        self.rowNumber[(x-1)//self.bingoRange] += 1

    #count bingo
    def countMaxBingo(self):
        bingoNumber = 0

        #count the number of bingos using usedcells

        #i: the number of bingo  j: all arrays in each i k: eachRow
        for i in range(2 * self.bingoSize + 3):
            for j in range(len(self.usedCells[i])):
                satisfied = True
                for k in range(self.bingoSize):
                    #print(usedCells[i][j])
                    if self.usedCells[i][j][k] > self.rowNumber[k]:
                        satisfied = False

                if satisfied:
                    bingoNumber = i

        return bingoNumber

    #used cell by bingo
    def countusedCells(self):
        #find all bingo
        for row in range(2 ** self.bingoSize):
            for column in range(2 ** self.bingoSize):
                for cross in range(2**2):
                    tmpRow = []
                    tmpColumn = []
                    tmpCross = []

                    tmpusedCells = [0] * self.bingoSize

                    #bit finding
                    for i in range(self.bingoSize):
                        if ((row >> i) & 1):
                            tmpRow.append(i)
                        if ((column >> i) & 1):
                            tmpColumn.append(i)
                        if (i <= 1 and ((cross >> i) & 1)):
                            tmpCross.append(i)

                    #count usedCells in row
                    for eachRow in tmpRow:
                        if eachRow != self.bingoSize//2:
                            tmpusedCells[eachRow] = self.bingoSize
                        else:
                            tmpusedCells[eachRow] = self.bingoSize -1

                    #count usedCells in column
                    for eachColumn in tmpColumn:
                        if eachColumn == (self.bingoSize//2):
                            for i in range(self.bingoSize):
                                if i == (self.bingoSize // 2):
                                    continue
                                else:
                                    tmpusedCells[i] = min(self.bingoSize, tmpusedCells[i] + 1)

                        else:
                            for i in range(self.bingoSize):
                                if i == (self.bingoSize // 2):
                                    tmpusedCells[i] = min(self.bingoSize-1, tmpusedCells[i] + 1)

                                else:
                                    tmpusedCells[i] = min(self.bingoSize, tmpusedCells[i] + 1)

                    #count usedCells in cross
                    for eachCross in tmpCross:
                        checkCell = [x for x in range(self.bingoSize)]
                        if eachCross == 1:
                            checkCell.reverse()

                        for i in range(self.bingoSize):
                            if tmpColumn.count(checkCell[i]) == 0:
                                tmpusedCells[i] = min(self.bingoSize, tmpusedCells[i] + 1)
                                if i == (self.bingoSize // 2):
                                    tmpusedCells[i] = max(0,tmpusedCells[i] - 1)


                    #append to usedCells by each number of bingos
                    bingoCount = len(tmpRow) + len(tmpColumn) + len(tmpCross)
                    self.usedCells[bingoCount].append(tmpusedCells)

    #return bingo cards
    def countBingoCards(self):
        #limit of loop
        maxBingo = self.countMaxBingo()

        cards = 0
        """
        this is function of evaluating cards
        """
        for i in range(1,maxBingo + 1):
            for cells in self.usedCells[i]:
                tmpCard = 1
                #if used cells are more than called number, this flag turns into false
                canCalculate = True
                for j in range(self.bingoSize):

                    #evaluating the number of cards
                    if j != (self.bingoSize//2):
                        if (self.rowNumber[j] >= cells[j] and self.bingoRange - cells[j] >=  self.bingoSize-cells[j]):
                            tmpCard *= self.perm(self.rowNumber[j],cells[j]) * \
                                self.perm(self.bingoRange-cells[j],self.bingoSize - cells[j])

                            #print(rowNumber[j],cells[j],bingoRange - cells[j], bingoSize-cells[j])
                        else:
                            canCalculate = False
                    else:
                        if (self.rowNumber[j] >= cells[j] and self.bingoRange - cells[j] >=  self.bingoSize-cells[j]-1):
                            tmpCard *= self.perm(self.rowNumber[j],cells[j]) * \
                                self.perm(self.bingoRange-cells[j],self.bingoSize - cells[j]-1)

                            #print(rowNumber[j],cells[j],bingoRange - cells[j], bingoSize-cells[j])
                        else:
                            canCalculate = False

                #all requiers are cleared
                if canCalculate:
                    #print(cells)
                    #print(tmpCard,i)
                    cards += tmpCard* ((-1)**(i+1))
        return cards

    def addProbabilityAndCard(self):
        cards = self.countBingoCards()
        prob = ((cards + 0.0)/self.allCards) * 100
        self.bingoCard.append(cards)
        self.probability.append(prob)
    
    #cond prob means Conditional Probability
    def showProbability(self):
        self.addProbabilityAndCard()

        #print("Probability: {:2.4f}".format(self.probability[-1]))
        return self.probability[-1]
    
    def showConditionalProb(self):
        condProb = 0
        if sum(self.rowNumber) >= 2 and self.allCards - self.bingoCard[-2] != 0:
            condProb = (self.bingoCard[-1] - self.bingoCard[-2] + 0.0)/(self.allCards - self.bingoCard[-2])*100
        #print(condProb)
        return condProb
        
    def addAndShow(self,x):
        self.add(x)
        self.showProbability()
    

    def allClear(self):
        #realNumber
        self.rowNumber = [0] * self.bingoSize
        #probability
        self.probability = []
        #bingoCard
        self.bingoCard = []








#random number generator
"""
for i in range(1,bingoRange * bingoSize + 1):
    add((i * 7) % (bingoRange * bingoSize + 1))

    ans = countBingoCards()
    Probability.append(((ans+0.0)/allCards)*100)
    print(rowNumber)
    print('Probability: {:.4f} Cards of Bingo: {} allCards {}'.format(((ans+0.0)/allCards)*100,ans,allCards))
    #print(countMaxBingo())

"""
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    Size = 5
    Range = 15
    bingo = Bingo(Size,Range)
    
    """
    this cord is bugged
    for i in range(1,Size * Range + 1):
        #bingo.addProbabilityAndCard((i * 11)%(Size * Range + 1))
        #a = bingo.showConditionalProb()
        print(bingo.rowNumber)
        print(bingo.probability)

    x = [x for x in range(1,Size * Range + 1)]
    #plt.plot(x)
    #plt.show()
    """



