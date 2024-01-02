# analysis.py
# -----------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
  answerDiscount = 0.9
   # If the dot moves exactly where it should go, it will start to move
  answerNoise = 0.001
  return answerDiscount, answerNoise

def question3a():
  # To move to the near one, discount should be like a penalty
  answerDiscount = 0.3
  answerNoise = 0.0
  answerLivingReward = 0.0
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3b():
  # Again, discount should be like a penalty
  # If there's possibility of noise, the dot won't go near death cliff
  answerDiscount = 0.2
  answerNoise = 0.1
  answerLivingReward = 0.0
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3c():
  # To move to the further one, not to discount much on every step
  answerDiscount = 0.95
  answerNoise = 0.0
  answerLivingReward = 0.0
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3d():
  # To move to the further one, not to discount much on every step
  # If there's possibility of noise, the dot won't go near death cliff
  answerDiscount = 0.95
  answerNoise = 0.1
  answerLivingReward = 0.0
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3e():
  # If the dot is alive, give it a reward
  answerDiscount = 0.0
  answerNoise = 0.0
  answerLivingReward = 1.0
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question6():
  answerEpsilon = 1.0
  answerLearningRate = 0.3
  return 'NOT POSSIBLE'
  return answerEpsilon, answerLearningRate
  # If not possible, return 'NOT POSSIBLE'
  
if __name__ == '__main__':
  print 'Answers to analysis questions:'
  import analysis
  for q in [q for q in dir(analysis) if q.startswith('question')]:
    response = getattr(analysis, q)()
    print '  Question %s:\t%s' % (q, str(response))
