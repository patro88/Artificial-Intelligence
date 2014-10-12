# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    # print "Start:", problem.getStartState()
    # print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    # print "Start's successors:", problem.getSuccessors(problem.getStartState())
    #print dir(problem)
    #print problem._expanded
    
    exploredSet = [];
    resultArray = []
    # get the start state
    currentState = problem.getStartState()
    exploredSet.append(currentState)
    # create stack for LIFO
    stack = util.Stack()
    currentElement = ()
    nodeDict = {}
    #push first node successors into stack
    x = problem.getSuccessors(currentState)
    nodeDict[currentState] = x
    for element in x:
        stack.push(element)

    loopCnt = 0
    
    resultStack = util.Stack()
    result = []
    
    #loop till goal is achieved
    while (not stack.isEmpty()):
        loopCnt= loopCnt +1
        parentElement = currentElement
        currentElement = stack.pop()
        currentState = currentElement[0]
        
        if (currentState not in exploredSet):
            exploredSet.append(currentState)
            resultStack.push(currentElement)
            if(problem.isGoalState(currentState)):
                break;
            x = problem.getSuccessors(currentState)
            nodeDict[currentState] = x;
            for element in x:
                stack.push(element)
        

    goalNode = resultStack.pop()
    result.append(goalNode[1])

    while(not resultStack.isEmpty()):
        currentNode = resultStack.pop();    
        if(goalNode in nodeDict[currentNode[0]]):
            goalNode = currentNode;
            result.append(goalNode[1])
        
    
    #print "Loop Count :\n " , loopCnt
    #print "results :\n",result
    result.reverse()
    #print "reslut length : ", len(result)
    return result
    #util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    exploredSet = [];
    resultArray = []
    # get the start state
    currentState = problem.getStartState()
    exploredSet.append(currentState)
    # create stack for LIFO
    stack = util.Queue()
    currentElement = ()
    nodeDict = {}
    #push first node successors into stack
    x = problem.getSuccessors(currentState)
    nodeDict[currentState] = x
    for element in x:
        stack.push(element)

    loopCnt = 0
    
    resultStack = util.Stack()
    result = []
    
    #loop till goal is achieved
    while not stack.isEmpty():
        loopCnt= loopCnt +1
        parentElement = currentElement
        currentElement = stack.pop()
        currentState = currentElement[0]
        
        if (currentState not in exploredSet):
            exploredSet.append(currentState)
            resultStack.push(currentElement)
            if(problem.isGoalState(currentState)):
                break;
            x = problem.getSuccessors(currentState)
            nodeDict[currentState] = x;
            for element in x:
                stack.push(element)
        

    goalNode = resultStack.pop()
    if(type(currentState[0]) is not tuple):
        result.append(goalNode[1])
    while(not resultStack.isEmpty()):
        currentNode = resultStack.pop();    
        if(goalNode in nodeDict[currentNode[0]]):
            goalNode = currentNode;
            result.append(goalNode[1])
        
    
    #print "Loop Count :\n " , loopCnt
    print "results :\n",result
    result.reverse()    
    #print "reslut length : ", len(result)
    return result
    #util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    exploredSet = [];
    resultArray = []
    # get the start state
    currentState = problem.getStartState()
    exploredSet.append(currentState)
    # create stack for LIFO
    stack = util.PriorityQueue()
    currentElement = ()
    nodeDict = {}
    
    #contains node and its distance from root
    costFromNode = {};
    #push first node successors into stack
    x = problem.getSuccessors(currentState)
    nodeDict[currentState] = x
    #helperList = []
    for element in x:
        stack.push(element , element[2])
        costFromNode[element] = element[2]
        #helperList.append(element[2])
    loopCnt = 0
    #print "Cost Outside : ", costFromNode
    resultStack = util.Stack()
    result = []
    
    #loop till goal is achieved
    while (not stack.isEmpty()):
        loopCnt= loopCnt +1
        currentElement = stack.pop()
        costUntil = costFromNode[currentElement]
        #print "costUntil : ", costUntil
        #print "element popped :", currentElement
        currentState = currentElement[0]
        #if min(helperList) != currentElement[2]:
         #   stack.push(currentElement,currentElement[2])
          #  break
        #helperList.remove(currentElement[2])
        if (currentState not in exploredSet):
            exploredSet.append(currentState)
            resultStack.push(currentElement)
            if(problem.isGoalState(currentState)):
                break;
            x = problem.getSuccessors(currentState)
            nodeDict[currentState] = x;
            for element in x:
                stack.push(element,costUntil + element[2])
                costFromNode[element] = costUntil + element[2]
                #helperList.append(element[2])
            #print "Cost Inside : ", costFromNode


    goalNode = resultStack.pop()
    result.append(goalNode[1])
    #print "dict : ",costFromNode
    while(not resultStack.isEmpty()):
        currentNode = resultStack.pop();    
        if(goalNode in nodeDict[currentNode[0]]):
            goalNode = currentNode;
            result.append(goalNode[1])
        
    
    #print "Loop Count :\n " , loopCnt
    #print "results :\n",result
    result.reverse()
    #print "reslut length : ", len(result)
    return result
    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    exploredSet = [];
    resultArray = []
    # get the start state
    currentState = problem.getStartState()
    exploredSet.append(currentState)
    # create stack for LIFO
    stack = util.PriorityQueue()
    currentElement = ()
    nodeDict = {}
    
    #contains node and its distance from root
    costFromNode = {};
    #push first node successors into stack
    x = problem.getSuccessors(currentState)
    nodeDict[currentState] = x
    #helperList = []
    for element in x:
        stack.push(element , element[2]+ heuristic(element[0],problem))
        costFromNode[element] = element[2]
        #helperList.append(element[2])
    loopCnt = 0
    #print "Cost Outside : ", costFromNode
    resultStack = util.Stack()
    result = []
    
    #loop till goal is achieved
    while (not stack.isEmpty()):
        loopCnt= loopCnt +1
        currentElement = stack.pop()
        #print "currElement after pop: ",currentElement
        #print "explore set :   " , exploredSet
        costUntil = costFromNode[currentElement]
        #print "costUntil : ", costUntil
        #print "element popped :", currentElement
        currentState = currentElement[0]
        #if min(helperList) != currentElement[2]:
         #   stack.push(currentElement,currentElement[2])
          #  break
        #helperList.remove(currentElement[2])
        if (currentState not in exploredSet):
            exploredSet.append(currentState)
            resultStack.push(currentElement)
            if(problem.isGoalState(currentState)):
                break;
            x = problem.getSuccessors(currentState)
            nodeDict[currentState] = x;
            for element in x:
                stack.push(element,costUntil + element[2]+heuristic(element[0],problem))
                costFromNode[element] = costUntil + element[2]
            #print "Cost Inside : ", costFromNode


    goalNode = resultStack.pop()
    result.append(goalNode[1])
    #print "dict : ",costFromNode
    while(not resultStack.isEmpty()):
        currentNode = resultStack.pop();    
        if(goalNode in nodeDict[currentNode[0]]):
            goalNode = currentNode;
            result.append(goalNode[1])
        
    
    #print "Loop Count :\n " , loopCnt
    #print "results :\n",result
    result.reverse()
    #print "reslut length : ", len(result)
    return result
    #util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
