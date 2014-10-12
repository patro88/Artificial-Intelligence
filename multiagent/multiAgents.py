# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        #chosenIndex = max(bestIndices)

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        #walls = successorGameState.getWalls()
        #wallDistances = [manhattanDistance(newPos,food) for food in walls.asList()]
        ghostPositions = [ghost.configuration.getPosition() for ghost in newGhostStates]
        ghostDistances = [manhattanDistance(newPos,ghost) for ghost in ghostPositions]
        foodDistances = [manhattanDistance(newPos,food) for food in newFood.asList()]
        maxDistFromWall = max(newFood.height,newFood.width)
        foodLeft = successorGameState.getNumFood()
        minFoodDistance = 0
        if len(foodDistances) == 0:
            minFoodDistance = 0
        else:
            minFoodDistance = min(foodDistances)
        score = successorGameState.getScore() + min(ghostDistances) + (maxDistFromWall - minFoodDistance ) + (100/(foodLeft+0.001)) 
        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    def maxValue(self, gameState, agent, depth):
    #initialize maximizer value to -infinity
        action = Directions.STOP
        maxval = (action,float("-inf"))
        v = maxval[1]
        newAgent = (agent+1)
        for act in gameState.getLegalActions(agent):
            v = max(maxval[1], self.value(gameState.generateSuccessor(agent,act), newAgent, depth)[1])
            if v > maxval[1]:
                maxval = (act, v)
        return maxval

    def minValue(self, gameState, agent, depth):
        #initialize maximizer value to infinity
        action = Directions.STOP
        newAgent = (agent+1)
        minval = (action,float("inf"))
        for act in gameState.getLegalActions(agent):
            v = min(minval[1], self.value(gameState.generateSuccessor(agent,act), newAgent, depth)[1])
            if v < minval[1]:
                minval = (act, v)
        return minval

    def value(self, gameState, agent, depth):
        if agent >= gameState.getNumAgents():
            agent = 0
            depth += 1
        if (gameState.isWin() or gameState.isLose() or depth == self.depth):
            return (Directions.STOP, self.evaluationFunction(gameState))
        elif agent == 0:
            return self.maxValue(gameState,agent,depth)
        else:
            return self.minValue(gameState,agent,depth)

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        currentDepth = 0
        currentAgent = 0
        val = self.value(gameState, currentAgent, currentDepth)
        return val[0]
        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def maxValue(self, gameState, agent, depth, alpha, beta):
    #initialize maximizer value to -infinity
        action = Directions.STOP
        maxval = (action,float("-inf"))
        v = maxval[1]
        newAgent = (agent+1)
        for act in gameState.getLegalActions(agent):
            v = max(maxval[1], self.value(gameState.generateSuccessor(agent,act), newAgent, depth, alpha, beta)[1])
            if v > beta:
                maxval = (act, v)
                return maxval
            else:
                alpha = max(alpha, v)
                if(v > maxval[1]):
                    maxval = (act,v)
        return maxval

    def minValue(self, gameState, agent, depth, alpha, beta):
        #initialize maximizer value to infinity
        action = Directions.STOP
        newAgent = (agent+1)
        minval = (action,float("inf"))
        for act in gameState.getLegalActions(agent):
            v = min(minval[1], self.value(gameState.generateSuccessor(agent,act), newAgent, depth, alpha, beta)[1])
            if v < alpha:
                minval = (act, v)
                return minval
            else:
                beta = min(beta, v)
                if v < minval[1]:
                    minval = (act, v)
        return minval

    def value(self, gameState, agent, depth, alpha, beta):
        if agent >= gameState.getNumAgents():
            agent = 0
            depth += 1
        if (gameState.isWin() or gameState.isLose() or depth == self.depth):
            return (Directions.STOP, self.evaluationFunction(gameState))
        elif agent == 0:
            return self.maxValue(gameState,agent,depth, alpha, beta)
        else:
            return self.minValue(gameState,agent,depth, alpha, beta)

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        currentDepth = 0
        currentAgent = 0
        val = self.value(gameState, currentAgent, currentDepth, float("-inf"), float("inf"))
        return val[0]
        #util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def maxValue(self, gameState, agent, depth):
    #initialize maximizer value to -infinity
        action = Directions.STOP
        maxval = (action,float("-inf"))
        v = maxval[1]
        newAgent = (agent+1)
        for act in gameState.getLegalActions(agent):
            v = max(maxval[1], self.value(gameState.generateSuccessor(agent,act), newAgent, depth)[1])
            if v > maxval[1]:
                maxval = (act, v)
        return maxval

    def minValue(self, gameState, agent, depth):
        #initialize maximizer value to infinity
        action = Directions.STOP
        newAgent = (agent+1)
        minval = (action,float(0))
        probability = 1.0/ len(gameState.getLegalActions(agent))
        for act in gameState.getLegalActions(agent):
            v = minval[1] + probability *(self.value(gameState.generateSuccessor(agent,act), newAgent, depth)[1])
            minval = (act, v)
        return minval

    def value(self, gameState, agent, depth):
        if agent >= gameState.getNumAgents():
            agent = 0
            depth += 1
        if (gameState.isWin() or gameState.isLose() or depth == self.depth):
            return (Directions.STOP, self.evaluationFunction(gameState))
        elif agent == 0:
            return self.maxValue(gameState,agent,depth)
        else:
            return self.minValue(gameState,agent,depth)
        
    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        currentDepth = 0
        currentAgent = 0
        val = self.value(gameState, currentAgent, currentDepth)
        return val[0]

        # Choose one of the best actions
        

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    successorGameState = currentGameState
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    capsulesList = successorGameState.getCapsules()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    #walls = successorGameState.getWalls()
    #wallDistances = [manhattanDistance(newPos,food) for food in walls.asList()]
    capsuleDistances = [manhattanDistance(newPos,capsules) for capsules in capsulesList]
    ghostPositions = [ghost.configuration.getPosition() for ghost in newGhostStates]
    ghostDistances = [manhattanDistance(newPos,ghost) for ghost in ghostPositions]
    foodDistances = [manhattanDistance(newPos,food) for food in newFood.asList()]
    maxDistFromWall = max(newFood.height,newFood.width)
    foodLeft = successorGameState.getNumFood()
    minFoodDistance = 0
    if len(foodDistances) == 0:
        minFoodDistance = 0
    else:
        minFoodDistance = min(foodDistances)
    if not len(capsuleDistances) == 0:
        minCapsuleDist = maxDistFromWall - min(capsuleDistances)
    else:
        minCapsuleDist = 0
    if not len(newScaredTimes) == 0:
        maxScaredTime = max(newScaredTimes)
    else:
        maxScaredTime = 0
    score = successorGameState.getScore() + min(ghostDistances) + (maxDistFromWall - minFoodDistance ) + (100/(foodLeft+0.001)) + (minCapsuleDist) + maxScaredTime
    return score

# Abbreviation
better = betterEvaluationFunction

