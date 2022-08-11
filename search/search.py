# search.py
# ---------
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
    
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    
    from util import Stack
    
    fringe = Stack()            #Finge using slack datastructure
    closed = []                 #initializating List storing all the visited nodes
    action = []                    #initializating List for storing the actions
    
    fringe.push((problem.getStartState(),action))          #Pushing the start node onto fringe
    while not fringe.isEmpty():                                          
        node,action = fringe.pop()                      #when fringe not empty, pop the values out of fringe
        if problem.isGoalState(node):               #if present node is goal state return the actions
            return action
        if (node not in closed):                #if node is not visited then add the node onto closed list
            closed.append(node)
            for nxtnode, nxtaction, nxtcost in problem.getSuccessors(node):     #get next node, next action and next cost from successors function 
                fringe.push((nxtnode, action + [nxtaction]))                    #push the nextnode and list of actions onto stack fringe
    return action
   
       
   
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    from util import Queue
    
    fringe = Queue()            #Uning Queue datastructue
    closed = []                 #initializating List Storing all the visited nodes
    action = []                 #initializating List of actions
    
    fringe.push((problem.getStartState(),action))       #Pushing start node onto fringe
    while not fringe.isEmpty():                         #when fringe not empty, poping the values from front of Queue
        node,action = fringe.pop()
        if problem.isGoalState(node):                   #if present node is goal state return the actions
            return action
        if (node not in closed):                      #if node is not visited then add the node onto closed list
            closed.append(node)
            for nxtnode, nxtaction, nxtcost in problem.getSuccessors(node):         #get next node, next action and next cost from successors function
                fringe.push((nxtnode, action + [nxtaction]))                    #push the nextnode and list of actions onto queue fringe
    return action
        

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    
    from util import PriorityQueue
    
    fringe = PriorityQueue()                #Using PriorityQueue datastructue
    closed = []                         #initializating List for storing all the visited nodes
    action = []                     #initializating List for storing actions
    cost = 0                    #initializating cost to zero
    
    fringe.push((problem.getStartState(), action, cost), cost)     #Pushing start node onto fringe     
    while not fringe.isEmpty():
        node, action, cost = fringe.pop()                       #when fringe not empty, poping the values from PriorityQueue
        if problem.isGoalState(node):                       #if present node is goal state return the actions
            return action
        if (node not in closed):                        #if node is not visited then add the node onto closed list
            closed.append(node)
            for nxtnode, nxtaction, nxtcost in problem.getSuccessors(node):                 #get next node, next action and next cost from successors function
                fringe.update((nxtnode, action+[nxtaction], cost+nxtcost), cost+nxtcost)        #updating Priorityqueue with next node, list of actions and cummulative cost
    return action
                    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    from util import PriorityQueue
    
    fringe = PriorityQueue()            #Using PriorityQueue datastructue
    closed = []                     #initializating List for storing all the visited nodes
    action = []                     #initializating List for storing actions
    cost = 0                    #initializating cost to zero
    
    fringe.push((problem.getStartState(), action, cost), cost)              #Pushing start node onto fringe
    while not fringe.isEmpty():
        node, action, cost = fringe.pop()                       #when fringe not empty, poping the values from PriorityQueue
        if problem.isGoalState(node):                       #if present node is goal state return the actions
            return action
        if (node not in closed):                            #if node is not visited then add the node onto closed list
            closed.append(node)
            for nxtnode, nxtaction, nxtcost in problem.getSuccessors(node):             #get next node, next action and next cost from successors function
                fringe.update((nxtnode, action+[nxtaction], cost+nxtcost), cost+nxtcost+ heuristic(nxtnode, problem))               #updating Priorityqueue with next node, list of actions, cummulative cost and Heuristic cost
    return action


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
