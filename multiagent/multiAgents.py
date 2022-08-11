# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

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

        "*** YOUR CODE HERE ***"
        
        "Calculating the distance between pacman and ghost and finding the closest ghost"
        ClosestGhost = min(manhattanDistance(newPos, ghost.getPosition())for ghost in newGhostStates)           
        
        if ClosestGhost:
            GhostDistance = -10/ClosestGhost
        else:
            GhostDistance = -1000
        
        "Getting food as a list and counting it"
        Foodlist = newFood.asList()         
        
        Foodlenght = len(Foodlist)
     
        "If food exists, then calculating the distance between pacman and nearest food"
        if Foodlist:
            ClosestFood = min(manhattanDistance(newPos, food) for food in Foodlist)                  
        else:
            ClosestFood = 0
            
        return (-2 * ClosestFood) + GhostDistance - (100 * Foodlenght)                  

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        
        def minimax_agent(gameState, agentIndex, depth):
            if agentIndex == gameState.getNumAgents():
                
                "checking if the game state is a winning state or if its a loosing state"
                if gameState.isWin():
                    return self.evaluationFunction(gameState)
                elif gameState.isLose():
                    return self.evaluationFunction(gameState)
                elif depth == self.depth:
                    return self.evaluationFunction(gameState)
                else:
                    return minimax_agent(gameState, 0, depth + 1)
            else:
                
                "getting list of legal actions of the agent"
                actions = gameState.getLegalActions(agentIndex)
                
                if len(actions) == 0:
                    return self.evaluationFunction(gameState)
                score = (minimax_agent(gameState.generateSuccessor(agentIndex, action), agentIndex + 1 , depth) for action in actions)
                
                "if agent is pacman then return the max else min value"
                if agentIndex == 0:
                    return max(score)
                else:
                    return min(score)
        return max(gameState.getLegalActions(0),  key = lambda x : minimax_agent(gameState.generateSuccessor(0, x), 1 , 1) )
        
        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction"""
        "*** YOUR CODE HERE ***"
        
      
        inf = float('inf')
        action, score = self.alphabeta_agent( gameState, 0, 0, -inf, inf)  
        return action 

    def alphabeta_agent(self, gameState, depth, agentIndex, alpha, beta):
        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
            depth += 1
            
            "checking if the game state is a winning state or a loosing state"
            if gameState.isWin():
                return None, self.evaluationFunction(gameState)
            elif gameState.isLose():
                return None, self.evaluationFunction(gameState)
            elif depth == self.depth:
                return None, self.evaluationFunction(gameState)
         
        Value, bestaction = None, None
        
        "getting list of legal actions of the agent"
        actions = gameState.getLegalActions(agentIndex)
        
        if len(actions) == 0:
            return None, self.evaluationFunction(gameState)
        
        "get the legal action of max agent and prune the tree if alpha is greater then beta"
        if agentIndex == 0:  
            for action in actions:
                _, score = self.alphabeta_agent( gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1, alpha, beta)
                if Value is None or score > Value:
                    Value = score
                    bestaction = action
                alpha = max(alpha, score)
                if alpha > beta:
                    break
        else:
            
            "get the legal action of min agent and prune the tree if beta is less then alpha"
            for action in actions:    
                _, score = self.alphabeta_agent( gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1, alpha, beta)
                if Value is None or score < Value:
                    Value = score
                    bestaction = action
                beta = min(beta, score)
                if beta < alpha:
                    break
        
        if Value is None:
            return None, self.evaluationFunction(gameState)
        return  bestaction, Value
        
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        
        def expectmax_agent(gameState,agentIndex,depth):
            if agentIndex == gameState.getNumAgents():
                
                "checking if the gamestate is a winning or loosing state"
                if gameState.isWin():
                    return self.evaluationFunction(gameState)    
                elif gameState.isLose():
                    return self.evaluationFunction(gameState)
                elif depth == self.depth:
                    return self.evaluationFunction(gameState)
                else:
                    return expectmax_agent(gameState, 0, depth + 1)
            else:
                
                "getting list of legal actions of the agent"
                actions = gameState.getLegalActions(agentIndex)
                
                if len(actions) == 0:
                    return self.evaluationFunction(gameState)
                score = (expectmax_agent(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, depth)for action in actions)
                
                "if agent is pacman then return the max else avg value"
                if agentIndex == 0:
                    return max(score)
                else:
                    scorelist = list(score)
                    avg = sum(scorelist)/len(scorelist)
                    return avg
        return max(gameState.getLegalActions(0), key = lambda x : expectmax_agent(gameState.generateSuccessor(0,x),1,1))
    
        #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates  = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    newCapsules = currentGameState.getCapsules()
    
    "Calculating the distance between pacman and new capsules and finding the closest capsule"
    if newCapsules:
        ClosestCapsule = min (manhattanDistance(newPos, caps) for caps in newCapsules)
    else:
        ClosestCapsule = 0
    
    if ClosestCapsule:
        ClosestCapsule = -3/ClosestCapsule
    else:
        ClosestCapsule = 100
        
    "Calculating the distance between pacman and ghost and finding the closest ghost"
    ClosestGhost = min(manhattanDistance(newPos, ghost.getPosition())for ghost in newGhostStates)
    
    if ClosestGhost:
        GhostDistance = -10/ClosestGhost
    else:
        GhostDistance = -1000
    
    "Getting food as a list and counting it"    
    Foodlist = newFood.asList()
    Foodlenght = len(Foodlist)
    
    "If food exists, then calculating the distance between pacman and nearest food"
    if Foodlist:
        ClosestFood = min(manhattanDistance(newPos, food) for food in Foodlist)
    else:
        ClosestFood = 0
        
    return ((-3 * ClosestFood) + GhostDistance - (100 * Foodlenght) + ClosestCapsule)
        
    
    #util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
