import copy
import time

#Prepare the initial state (Duplicate)
def makeState(nw, n, ne, w, c, e, sw, s, se):
    state = [[nw, n, ne],[w, c, e], [sw, s, se]]
    for i in range(3):
        for j in range(3):
            if state[i][j] == "blank":
                state[i][j] = 0

    return state

#Draw the current state of the board and print the action taken (Duplicate)
def displayBoard(state,action):
    if action == 'U':
        print "Move Up"
    if action == 'D':
        print "Move Down"
    if action == 'L':
        print "Move Left"
    if action == 'R':
        print "Move Right"
                
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                print " ",
            else:
                print state[i][j],
            if j != 2:
                print "|",
        print ""


class Node:
    def __init__(self, parent = 0, action = ' ', pathcost = 0, state = []):
        self.parent = parent 
        self.action = action
        self.pathcost = pathcost
        self.state = state
        self.blank = []

#Generate a list of all possible actions from this state (Duplicate)
    def possibleAction(self):
        actionList = [];
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    if i != 0:
                        actionList = actionList + ['U',]
                    if i != 2:
                        actionList = actionList + ['D',]
                    if j != 0:
                        actionList = actionList + ['L',]
                    if j != 2:
                        actionList = actionList + ['R',]
                    self.blank = [i,j]
                    return actionList

#Apply the action to the current state to generate the next state (Duplicate)
    def result(self,action):
        newNode = copy.deepcopy(self.state)
        if action == 'L':
            newNode[self.blank[0]][self.blank[1]] = newNode[self.blank[0]][self.blank[1] - 1]
            newNode[self.blank[0]][self.blank[1] - 1] = 0
            return newNode
        if action == 'R':
            newNode[self.blank[0]][self.blank[1]] = newNode[self.blank[0]][self.blank[1] + 1]
            newNode[self.blank[0]][self.blank[1] + 1] = 0
            return newNode
        if action == 'U':
            newNode[self.blank[0]][self.blank[1]] = newNode[self.blank[0]-1][self.blank[1]]
            newNode[self.blank[0]-1][self.blank[1]] = 0
            return newNode
        if action == 'D':
            newNode[self.blank[0]][self.blank[1]] = newNode[self.blank[0]+1][self.blank[1]]
            newNode[self.blank[0]+1][self.blank[1]] = 0
            return newNode

#Calculate the distance of the state from the goal state. Using Similarity and L2 distance for this purpose
    def calcCost(self,goalState,heuristic1):
        heuristicValue = 0
        for i in range(3):
            for j in range(3):
                idealValue = goalState[i][j]
                if heuristic1:
                    # For permutation inversion (did not include it because the goal state can vary)
                    #pos = i*3+j
                    #for m in range(pos,9):
                    #    x = m/3
                    #    y = m%3
                    #    if (self.state[x][y] < self.state[i][j]) and (self.state[x][y] != 0):
                    #        heuristicValue += 1
                            
                    if self.state[i][j] != idealValue:
                        heuristicValue += 1
                else:
                    if self.state[i][j] != idealValue:
                        matchFound = False
                        for m in range(3):
                            for n in range(3):
                                if goalState[m][n] == self.state[i][j]:
                                    heuristicValue += abs(m-i) + abs(n-j)
                                    matchFound = True
                                    break
                            if matchFound == True:
                                break 
        self.pathcost = heuristicValue

#Check if the goal state is reached (Duplicate)
def testGoalState(state,goalState):
    for i in range(3):
        for j in range(3):
            if goalState[i][j] != state[i][j]:
                return False
    return True

#Check if the node has already been explored (Duplicate)
def isExplored(state,EXPLORED):
    for i in range(len(EXPLORED)):
        if EXPLORED[i].state == state:
            return True
    return False

#Add the new node to the Fringe list based on the heuristic measure at that state
def addToFringe(node, FRINGE):
    newFringe = []
    nodeAdded = False
    for i in range(len(FRINGE)):
        if (node.pathcost < FRINGE[i].pathcost) and (not nodeAdded):
            newFringe.append(node)
            nodeAdded = True
        newFringe.append(FRINGE[i])

    if nodeAdded == False:
        newFringe.append(node)

    return newFringe

#Algorithm to implement Best First Search
def testInformedSearch(initialState, goalState, maxIterations):
    FRINGE = []
    EXPLORED = []
    iterationCount = 0
    goalMet = False
    heuristic1 = False
#    MisClassification = True
#    Distance = False

    n = Node()
    n.state = initialState
    #n.state = [[0, 1, 3],[4, 2, 5],[7, 8, 6]]
    #n.state = [[2, 6, 4],[7, 8, 1],[5, 0, 3]]
    #displayBoard(n.state)

    start_time = time.time()

    FRINGE.append(n)        #add initial state to Fringe list

    while True:
        if iterationCount >= maxIterations:         #Exit program if iteration count exceeds limit
            print "Unable to find solution in given iterations"
            return False

        iterationCount += 1
            
        parent = FRINGE.pop(0)              #pop the first node in the queue
        goalMet = testGoalState(parent.state, goalState)
        if goalMet == True:                 #Check if goal state is reached
            print "Problem Solved!!"
            break

        EXPLORED.append(parent)             #add the explored node to a list of explored nodes

        #print "Current Node"
        #displayBoard(parent.state,' ')

        actionList = parent.possibleAction()

        for action in range(len(actionList)):
            childNode = Node()
            newState = parent.result(actionList[action])

            exploredFlag = isExplored(newState,EXPLORED)
            if exploredFlag == False:
                childNode.state = newState
                childNode.parent = parent
                childNode.action = actionList[action]
                childNode.calcCost(goalState,heuristic1)

                FRINGE = addToFringe(childNode,FRINGE)
                
                #displayBoard(childNode.state,actionList[action])

        if len(FRINGE) == 0:
            print "No Solutions available for this initial State"
            return False

        #print "FRINGE"
        #for i in range(len(FRINGE)):
        #    print FRINGE[i].state, FRINGE[i].pathcost

        #print "EXPLORED"
        #for i in range(len(EXPLORED)):
        #    print EXPLORED[i].state

    exec_time = time.time() - start_time;
    path = []
    path.append(parent)

    #Trace the path from goal state to initial state
    n = parent
    while True:         
        n = n.parent
        if n == 0:
            break
        path.append(n)

    for i in range(1,len(path)+1):
        displayBoard(path[-i].state,path[-i].action)

    #print len(path)-1, len(EXPLORED), exec_time

    return True

def buildCaseBase(testProbs):
    for i in testProbs:
        
    
