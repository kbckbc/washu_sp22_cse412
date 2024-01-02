# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  debug = False

  def __init__(self, mdp, discount = 0.9, iterations = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.
    
      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.values = util.Counter() # A Counter is a dict with default 0
    self.policies = util.Counter() # To save policies

    if False:
      # it's a test code
      print "discount {}".format(discount)
      print "iterations {}".format(iterations)
      print "values {}".format(self.values)
      print "getState() {}".format(mdp.getStates())
      print "getPossibleActions() {}".format(mdp.getPossibleActions((0,0)))
      print "getTransitionStatesAndProbs() {}".format(mdp.getTransitionStatesAndProbs((0,0),"north"))
      print "getReward() {}".format(mdp.getReward((0,0),"north",(1,0)))
    "*** YOUR CODE HERE ***"
    for i in range(self.iterations):
      if self.debug: print 'i {}'.format(i)
      newValues = util.Counter()
      for s in mdp.getStates():
        if self.debug: print '\tstate {}'.format(s)
        maxQ = -9999
        for a in mdp.getPossibleActions(s):
          if self.debug: print '\t\taction {}, qvalue {}'.format(a, self.getQValue(s,a))
          currQ = self.getQValue(s,a)
          if currQ > maxQ:
            maxQ = currQ
            self.policies[s] = a
            newValues[s] = maxQ
      self.values = newValues


    
  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    return self.values[state]


  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    qvalue = 0
    for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
      # qvalue equation
      # qvalue += prob * (reward + discount * getValue(nextState))

      reward = self.mdp.getReward(state, action, nextState)
      discount = self.discount
      nextValue = self.getValue(nextState)
      qvalue += prob * (reward + discount * self.getValue(nextState))

      # print '\t\t\tgetQ -> {}, prob {}, re {}, dis {}, nextValue {}, qvalue {}'.format(
      #           nextState, prob, reward, discount, nextValue, qvalue)
             
    return qvalue                


  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """
    "*** YOUR CODE HERE ***"
    if False:
      # it' a test code for getQValue
      print 'getPolicy: state {}, policy {}, action {}'.format(state, self.policies[state], self.mdp.getPossibleActions(state))

      actions = self.mdp.getPossibleActions(state)
      for a in actions:
        self.getQValue(state, a)
      # print 'sortedKeys', self.values.sortedKeys()
      # print 'argMax', self.values.argMax()
      # print 'totalCount', self.values.totalCount()

      try:
        input()
      except Exception:
          pass 
    if self.policies[state] == 0:
      return None
    else:
      return self.policies[state]
    # util.raiseNotDefined()

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
  
