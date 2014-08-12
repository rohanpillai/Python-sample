import copy
import time

def makeState(nw, n, ne, w, c, e, sw, s, se):
    state = [[nw, n, ne],[w, c, e], [sw, s, se]]
    for i in range(3):
        for j in range(3):
            if state[i][j] == "blank":
                state[i][j] = 0

    return state


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

def testGoalState(state,goalState):
    for i in range(3):
        for j in range(3):
            if goalState[i][j] != state[i][j]:
                return False
    return True

def isExplored(state,EXPLORED):
    for i in range(len(EXPLORED)):
        if EXPLORED[i].state == state:
            return True
    return False


def testUninformedSearch(initState, goal, limit):
    FRINGE = []
    EXPLORED = []
    iterationCount = 0
    BFS = True
    DFS = not BFS
    goalMet = False

    n = Node()
    n.state = initState
    #n.state = [[2, 6, 4],[7, 8, 1],[5, 0, 3]]
    #displayBoard(n.state)

    FRINGE.append(n)


    while True:

        if interationCount >= limit:
            print "Unable to find solution in given iterations"
            return False

        iterationCount += 1
        
        if BFS:
            parent = FRINGE.pop(0)
        else:
            parent = FRINGE.pop()
        EXPLORED.append(parent)

        actionList = parent.possibleAction()

        for action in range(len(actionList)):
            childNode = Node()
            newState = parent.result(actionList[action])

            exploredFlag = isExplored(newState,EXPLORED)
            if exploredFlag == False:
                childNode.state = newState
                childNode.parent = parent
                childNode.action = actionList[action]
                childNode.pathcost = parent.pathcost + 1

                goalMet = goalState(childNode.state)
                if goalMet == True:
                    print "Problem Solved!!"
                    break

                FRINGE.append(childNode)
                
                #print actionList[action]
                #displayBoard(childNode.state)

        if goalMet == True:
            break

        if len(FRINGE) == 0:
            print "No Solutions available for this initial State"
            return False
        
        #print "FRINGE"
        #for i in range(len(FRINGE)):
        #    print FRINGE[i].state

        #print "EXPLORED"
        #for i in range(len(EXPLORED)):
        #    print EXPLORED[i].state

    exec_time = time.time() - start_time;

    path = []
    path.append(childNode)

    n = childNode
    while True:
        n = n.parent
        if n == 0:
            break
        path.append(n)

    for i in range(1,len(path)+1):
        displayBoard(path[-i].state,path[-i].action)

    print len(path)-1, "\t", len(EXPLORED), "\t", exec_time

    return True
