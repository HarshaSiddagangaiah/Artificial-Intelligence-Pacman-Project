# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextstate)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for iteration in range(self.iterations):
            temp = util.Counter()
            for state in self.mdp.getStates():
                if self.mdp.isTerminal(state):
                    temp[state] = 0
                else:
                    maxValue = -99999
                    actions = self.mdp.getPossibleActions(state)
                    for action in actions:
                        value = 0
                        for nextstate in self.mdp.getTransitionStatesAndProbs(state, action):
                            value += nextstate[1] * ((self.mdp.getReward(state, action, nextstate[1])) + self.discount * self.values[nextstate[0]])
                        maxValue = max(value, maxValue)
                    if maxValue != -99999:
                        temp[state] = maxValue
            self.values = temp
            
                        
    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        QValue = 0
        for nextstate in self.mdp.getTransitionStatesAndProbs(state, action):
            QValue += nextstate[1] * ((self.mdp.getReward(state, action, nextstate[1])) + self.discount * self.values[nextstate[0]])
        return QValue        
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        
        if self.mdp.isTerminal(state):
            return None
        
        actions = self.mdp.getPossibleActions(state)
        allActions = {}
        for action in actions:
            allActions[action] = self.computeQValueFromValues(state, action)
        return max(allActions, key = allActions.get)
        
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
       
        for iteration in range(self.iterations):
            states = self.mdp.getStates()
            num_states = len(states)
            state = states[iteration % num_states]
            if not self.mdp.isTerminal(state):
                values = []
                for action in self.mdp.getPossibleActions(state):
                    QValue = self.computeQValueFromValues(state, action)
                    values.append(QValue)
                self.values[state] = max(values)
                
        
class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        
        PriorityQueue = util.PriorityQueue()
        nextstates = {}
        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                for action in self.mdp.getPossibleActions(state):
                    for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
                        if nextState in nextstates:
                            nextstates[nextState].add(state)
                        else:
                            nextstates[nextState] = {state}

        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                values = []
                for action in self.mdp.getPossibleActions(state):
                    QValue = self.computeQValueFromValues(state, action)
                    values.append(QValue)
                diff = abs(max(values) - self.values[state])
                PriorityQueue.update(state, - diff)

        for iiteration in range(self.iterations):
            if PriorityQueue.isEmpty():
                break
            temp = PriorityQueue.pop()
            if not self.mdp.isTerminal(temp):
                values = []
                for action in self.mdp.getPossibleActions(temp):
                    QValue = self.computeQValueFromValues(temp, action)
                    values.append(QValue)
                self.values[temp] = max(values)

            for nextstate in nextstates[temp]:
                if not self.mdp.isTerminal(nextstate):
                    values = []
                    for action in self.mdp.getPossibleActions(nextstate):
                        QValue = self.computeQValueFromValues(nextstate, action)
                        values.append(QValue)
                    diff = abs(max(values) - self.values[nextstate])
                    if diff > self.theta:
                        PriorityQueue.update(nextstate, -diff)