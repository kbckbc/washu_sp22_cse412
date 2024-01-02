# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from re import T
from util import manhattanDistance
from game import Directions
import random
import util

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
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

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
        currFood = currentGameState.getFood()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        currGhostStates = currentGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        debug = False
        # debug = True
        ghostDist = 0  # total dist between of ghosts. Further is better
        foodScore = 0   # total dist sum of foods. Less is better
        nX, nY = newPos[0], newPos[1]

        if debug:
            print 'action', action
            print 'curr', currentGameState.getPacmanPosition(), currentGameState.getLegalActions()
            print 'succ', successorGameState.getPacmanPosition(), successorGameState.getLegalActions()
            print 'ghos', [i.getPosition() for i in currGhostStates],  [i.getDirection() for i in currGhostStates]

        # Sum total distance between foods
        foodDist = []
        for i in currFood.asList():
            x, y = i[0], i[1]
            # foodDist.append(((x, y), abs(nX-x) + abs(nY-y)))
            foodDist.append(abs(nX-x) + abs(nY-y))

        # print 'foodDist', foodDist
        foodScore = min(foodDist) * -1
        if foodScore == 0:
            foodScore = 1

        # Sum total distance between ghost
        ghostDist = 0
        for i in currGhostStates:
            gX, gY = i.getPosition()[0], i.getPosition()[1]
            ghostDist += abs(nX - gX) + abs(nY - gY)

        if debug:
            print 'ghostDist', ghostDist, 'foodScore', foodScore
        if ghostDist <= 1:
            customScore = -10000
        else:
            customScore = foodScore
        # customScore = ghostDist + foodScore

        if debug:
            print 'customScore', customScore

        try:
            if debug:
                input()
                print ''
            pass
        except Exception:
            pass

        "*** YOUR CODE HERE ***"
        return customScore
        return successorGameState.getScore() + customScore


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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

        Directions.STOP:
            The stop direction, which is always legal

        gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        debug = False

        if debug: print '=================== getAction ===================='

        """
        input : gameState, player index, depth of the minimax tree
        output : [score, direction]
        """
        def minimax(currState, depth, player):
            currEval = []

            if debug:
                print 'minimax() called: P{}, Depth {}/{}'.format(player, depth, self.depth)

            # check termination
            # Terminate state #
            currActions = currState.getLegalActions(player)
            if not currActions:
                endScore = scoreEvaluationFunction(currState)
                if debug:
                    print '\t>>>>> Terminate. No legal action, score {}'.format(endScore)
                return [scoreEvaluationFunction(currState), Directions.STOP]

            # if reached at the end of the depth, then terminate
            if depth == self.depth:
                endScore = scoreEvaluationFunction(currState)
                if debug:
                    print '\t>>>>> Terminate. Touch the end, score {}'.format(endScore)
                return [endScore, Directions.STOP]

            # set next player
            # it reached at the end of the ghost, then pacman again
            nextPlayer = player + 1
            if nextPlayer == currState.getNumAgents():
                nextPlayer = 0
                depth += 1

            for action in currActions:
                if debug:
                    if player == 0:
                        print '====== for start: P{}{} => {}'.format(player, currActions, action)
                        try:
                            if debug:
                                input()
                            pass
                        except Exception:
                            pass
                    else:
                        print '\tfor loop: P{}{} => {}'.format(player, currActions, action)

                nextState = currState.generateSuccessor(player, action)
                nextEval = minimax(nextState, depth, nextPlayer)

                # prevent abnormal case
                if len(nextEval) == 0:
                    continue

                # if eval is empty, it is first time called
                if len(currEval) == 0:
                    currEval.append(nextEval[0])
                    currEval.append(action)

                # if it is not, then compare value and try to choose the max or min value
                else:
                    if currEval[0] < nextEval[0]:
                        # if a player is pacman, choose the bigger value
                        if player == 0:
                            currEval[0] = nextEval[0]
                            currEval[1] = action
                    else:
                        # if a player is ghost, choose the smaller value
                        if player != 0:
                            currEval[0] = nextEval[0]
                            currEval[1] = action
                if debug:
                    print '\t\tfor end: P{} -  eval c{}'.format(player, currEval)

            return currEval

        startDepth = 0
        startPlayer = self.index
        result = minimax(gameState, startDepth, startPlayer)
        print 'getAction End', result
        try:
            if False: 
                input()
                pass    
        except Exception:
            pass            
        if len(result) == 0:
            return Directions.STOP
        else:
            return result[1] 
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        debug = False

        if debug: print '=================== getAction ===================='

        """
        input : gameState, player index, depth of the minimax tree
                and alpha, beta value
        output : [score, direction]
        """
        def minimax(currState, depth, player, a, b):
            currEval = []

            if debug:
                print 'minimax() called: P{}, Depth {}/{}, {}/{}'.format(player, depth, self.depth, a, b)

            # check termination
            # Terminate state #
            currActions = currState.getLegalActions(player)
            if not currActions:
                endScore = scoreEvaluationFunction(currState)
                if debug:
                    print '\t>>>>> Terminate. No legal action, score {}'.format(endScore)
                return [scoreEvaluationFunction(currState), Directions.STOP]

            # if reached at the end of the depth, then terminate
            if depth == self.depth:
                endScore = scoreEvaluationFunction(currState)
                if debug:
                    print '\t>>>>> Terminate. Touch the end, score{}'.format(endScore)
                return [endScore, Directions.STOP]

            # set next player
            # it reached at the end of the ghost, then pacman again
            nextPlayer = player + 1
            if nextPlayer == currState.getNumAgents():
                nextPlayer = 0
                depth += 1

            for action in currActions:
                if debug:
                    if player == 0:
                        print '====== for start: P{}{} => {}'.format(player, currActions, action)
                        try:
                            if debug:
                                input()
                            pass
                        except Exception:
                            pass
                    else:
                        print '\tfor loop: P{}{} => {}'.format(player, currActions, action)


                # pruning
                if a >= b:
                    if debug: print '*********** PRUNE {},{} ***********'.format(a, b)
                    return currEval

                nextState = currState.generateSuccessor(player, action)
                nextEval = minimax(nextState, depth, nextPlayer, a, b)

                # prevent abnormal case
                if len(nextEval) == 0:
                    continue

                # if eval is empty, it is first time called
                if len(currEval) == 0:

                    currEval.append(nextEval[0])
                    currEval.append(action)                    
                    # if player is pacman, it should be max search
                    if player == 0:
                        a = max(a, currEval[0])
                    # if player is ghost, it should be min search
                    else:
                        b = min(b, currEval[0])

                # if it is not, then compare value and try to choose the max or min value
                else:
                    if currEval[0] < nextEval[0]:
                        # if a player is pacman, choose the bigger value
                        if player == 0:
                            currEval[0] = nextEval[0]
                            currEval[1] = action
                            a = max(a, currEval[0])
                    else:
                        # if a player is ghost, choose the smaller value
                        if player != 0:
                            currEval[0] = nextEval[0]
                            currEval[1] = action
                            b = min(b, currEval[0])
                    

                if debug:
                    print '\t\tfor end: P{} -  eval c{}'.format(player, currEval)

            return currEval

        startDepth = 0
        startPlayer = self.index
        result = minimax(gameState, startDepth, startPlayer, float("-inf"), float("inf"))
        print 'getAction End', result
        try:
            if False: 
                input()
                pass    
        except Exception:
            pass            
        if len(result) == 0:
            return Directions.STOP
        else:
            return result[1] 

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        debug = False

        def minimax(currState, depth, player):
            currEval = []

            if debug:
                print 'minimax() called: P{}, Depth {}/{}'.format(player, depth, self.depth)

            # check termination
            # Terminate state #
            currActions = currState.getLegalActions(player)
            if not currActions:
                endScore = scoreEvaluationFunction(currState)
                if debug:
                    print '\t>>>>> Terminate. No legal action, score {}'.format(endScore)
                return [self.evaluationFunction(currState), Directions.STOP]

            # if reached at the end of the depth, then terminate
            if depth == self.depth:
                endScore = self.evaluationFunction(currState)
                if debug:
                    print '\t>>>>> Terminate. Touch the end, score {}'.format(endScore)
                return [endScore, Directions.STOP]

            # set next player
            # it reached at the end of the ghost, then pacman again
            nextPlayer = player + 1
            if nextPlayer == currState.getNumAgents():
                nextPlayer = 0
                depth += 1

            for action in currActions:
                if debug:
                    if player == 0:
                        print '====== for start: P{}{} => {}'.format(player, currActions, action)
                        try:
                            if debug:
                                input()
                            pass
                        except Exception:
                            pass
                    else:
                        print '\tfor loop: P{}{} => {}'.format(player, currActions, action)

                nextState = currState.generateSuccessor(player, action)
                nextEval = minimax(nextState, depth, nextPlayer)

                # prevent abnormal case
                if len(nextEval) == 0:
                    continue

                # if eval is empty, it is first time called
                if len(currEval) == 0:
                    # if a player is pacman, choose the bigger value
                    if player == 0:
                        currEval.append(nextEval[0])
                        currEval.append(action)
                    else:
                        currEval.append(nextEval[0]/len(currActions))
                        currEval.append(action)

                # if it is not, then compare value and try to choose the max or min value
                else:
                    if currEval[0] <= nextEval[0]:
                        # if a player is pacman, choose the bigger value
                        if player == 0:
                            currEval[0] = nextEval[0]
                            currEval[1] = action
                    else:
                        # if a player is ghost, choose the smaller value
                        if player != 0:
                            currEval[0] = currEval[0] + nextEval[0]/len(currActions)
                            currEval[1] = action
                if debug:
                    print '\t\tfor end: P{} -  eval c{}'.format(player, currEval)

            return currEval

        startDepth = 0
        startPlayer = self.index
        result = minimax(gameState, startDepth, startPlayer)
        # print 'getAction End', result
        try:
            if False: 
                input()
                pass    
        except Exception:
            pass            
        if len(result) == 0:
            return Directions.STOP
        else:
            return result[1] 


def betterEvaluationFunction(state):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>

    >> Byeongchan Gwak, b.gwak@wustl.edu <<
    First, I set every aspect to negative.
    The more minus value the Pacman gets, the more chances to get died.

    I've used several criteria to calculate the proper value and I've applied weight to criteria.
    I spent several hours making the best criteria values and weights.
    Surprisingly, simple 3 combinations worked most...

    * Originally, my criteria were like this.
    ghostPenalty : It is used to alarm when a ghost is near the Pacman. 
    capsulePenalty : It is used to alarm when a capsule is near the Pacman. 
    foodDistPenalty : The summation of the whole food distance from the Pacman.
    foodRemainPenalty : The summation of the whole food remains
    minFoodDist : It tells the Pacman which gameStage is closer to the food
    scorePenalty : As the name suggests, score penalty

    * Finally, I only use 3 things
    ghostPenalty
    minFoodDist
    scorePenalty

    Consequently, I admit that this is a kind of bad evaluation function.
    Because the decision Pacman makes is mainly driven by ghost avoiding.
    If there is no ghost, the Pacman could be stuck somewhere or could move weirdly.
    However, it works in this special case, so I just stop here.
    """
    "*** YOUR CODE HERE ***"
    food = state.getFood().asList()
    ghosts = state.getGhostStates()
    currPos = state.getPacmanPosition()
    totalCapsules = len(state.getCapsules())
    foodRemain = len(food)
    score = state.getScore()
    result = 0 

    debug = False
    # debug = True
    foodDist = 0   # total dist sum of foods. Less is better
    ghostDist = 0  # total dist between of ghosts. Further is better
    pX, pY = currPos[0], currPos[1]
    defaultPenalty = -1
    
    # avoid ghost is the top priority
    ghostPenalty = 0
    for i in ghosts:
        ghostDist = 9999
        gX, gY = i.getPosition()[0], i.getPosition()[1]
        ghostDist = abs(pX - gX) + abs(pY - gY)
        if ghostDist <= 1:
            if debug: print 'RUNAWAYRUNAWAYRUNAWAYRUNAWAYRUNAWAY'
            ghostPenalty = -9999
            #return float("-inf")

    # # capsule is near then follow it
    # capsuleDist = []
    # for i in state.getCapsules():
    #     x, y = i[0], i[1]
    #     #foodDist.append(((x, y), abs(pX-x) + abs(pY-y)))
    #     capsuleDist.append(abs(pX-x) + abs(pY-y))
    # if debug: print 'capsuleDist', capsuleDist    
    # capsuleDistPenalty = defaultPenalty * sum(capsuleDist)
    # capsuleDistPenalty = capsuleDistPenalty * 2

    # # capsule is near then follow it
    capsulePenalty = 0
    for i in state.getCapsules():
        capsuleDist = 1000
        x, y = i[0], i[1]
        capsuleDist = abs(pX - gX) + abs(pY - gY)
        if capsuleDist <= 2:
            if debug: print 'CAPSULECAPSULECAPSULECAPSULECAPSULECAPSULE'
            capsulePenalty = 1000

    # capsule dist
    capsuleDist = []
    for i in state.getCapsules():
        x, y = i[0], i[1]
        capsuleDist.append(abs(pX-x) + abs(pY-y))
    capsuleDist = sum(capsuleDist)

    # food distance penalty : further food distance more penalty
    foodDist = []
    for i in food:
        x, y = i[0], i[1]
        #foodDist.append(((x, y), abs(pX-x) + abs(pY-y)))
        foodDist.append(abs(pX-x) + abs(pY-y))
    minFoodDist = 0
    if len(foodDist) != 0: 
        minFoodDist = min(foodDist)

    foodDistPenalty = defaultPenalty * sum(foodDist)
    if foodDistPenalty == 0:
        foodDistPenalty = 1

    if debug: print 'foodDist', foodDist

    # food remain penalty: more food remains more penalty
    foodRemainWeight = 5
    if foodRemain <= 10: foodRemainWeight = 11
    elif foodRemain <= 20 : foodRemainWeight = 10
    elif foodRemain <= 30 : foodRemainWeight = 9
    elif foodRemain <= 40 : foodRemainWeight = 8
    elif foodRemain <= 50 : foodRemainWeight = 7
    foodRemainPenalty = defaultPenalty * foodRemain * foodRemainWeight


    # ghost is in fear, then follow it


    
    # score penalty
    scoreWeight = 1
    if score <= 100: scoreWeight = 2
    elif score <= 200: scoreWeight = 1.5
    elif score <= 400: scoreWeight = 0.6
    elif score <= 600 : scoreWeight = 0.3
    elif score <= 900 : scoreWeight = 0
    scoreWeight = 1
    
    scorePenalty = score * scoreWeight


    result += ghostPenalty
    # result += foodDistPenalty
    result += minFoodDist * -1
    # result += foodRemain * -1

    # if minFoodDist >= 7:
    #     result += foodDistPenalty 
    # else:
    #     result += foodDistPenalty
    #     result += foodRemainPenalty     


    # result += foodDistPenalty 
    # result += foodRemainPenalty 
    # result += capsuleDistPenalty
    # result += capsulePenalty
        
    result += scorePenalty

    if False:
        print '({},{}) RS[{}] m[{}] Fdp[{},{}] Frw[{},{}] Sswp[{},{},{}] Go[{}] Ca[{},{}]'.format(
            pX, pY, result, minFoodDist, 
            foodDistPenalty, foodRemainPenalty, foodRemain, foodRemainWeight, 
            scorePenalty, score, scoreWeight, 
            ghostPenalty,
            capsuleDist, capsulePenalty)
    try:
        if debug:
            input()
            print ''
        pass
    except Exception:
        pass

    "*** YOUR CODE HERE ***"
    return result

# Abbreviation
better = betterEvaluationFunction



def betterEvaluationFunction2(state):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>

    >> Byeongchan Gwak, b.gwak@wustl.edu <<
    First, I set every aspect to negative.
    The more minus value the Pacman gets, the more chances to get died.

    I've used several criteria to calculate the proper value and I've applied weight to criteria.
    I spent several hours making the best criteria values and weights.
    Surprisingly, simple 3 combinations worked most...

    * Originally, my criteria were like this.
    ghostPenalty : It is used to alarm when a ghost is near the Pacman. 
    capsulePenalty : It is used to alarm when a capsule is near the Pacman. 
    foodDistPenalty : The summation of the whole food distance from the Pacman.
    foodRemainPenalty : The summation of the whole food remains
    minFoodDist : It tells the Pacman which gameStage is closer to the food
    scorePenalty : As the name suggests, score penalty

    * Finally, I only use 3 things
    ghostPenalty
    minFoodDist
    scorePenalty

    Consequently, I admit that this is a kind of bad evaluation function.
    Because the decision Pacman makes is mainly driven by ghost avoiding.
    If there is no ghost, the Pacman could be stuck somewhere or could move weirdly.
    However, it works in this special case, so I just stop here.
    """
    "*** YOUR CODE HERE ***"
    food = state.getFood().asList()
    ghosts = state.getGhostStates()
    currPos = state.getPacmanPosition()
    totalCapsules = len(state.getCapsules())
    foodRemain = len(food)
    capsuleRemain = len(state.getCapsules())
    score = state.getScore()
    result = 0 

    isGhostScared = True
    debug = False
    # debug = True
    foodDist = 0   # total dist sum of foods. Less is better
    ghostDist = 0  # total dist between of ghosts. Further is better
    pX, pY = currPos[0], currPos[1]
    defaultPenalty = -1
    
    # avoid ghost is the top priority
    ghostPenalty = 0
    for i in ghosts:
        ghostDist = 9999
        x, y = i.getPosition()[0], i.getPosition()[1]
        ghostDist = abs(pX - x) + abs(pY - y)
        if ghostDist <= 1 and i.scaredTimer == 0:
            if debug: print 'RUNAWAYRUNAWAYRUNAWAYRUNAWAYRUNAWAY'
            ghostPenalty = -9999
            #return float("-inf")
        if i.scaredTimer == 0:
            isGhostScared = False

    # # capsule is near then follow it
    # capsuleDist = []
    # for i in state.getCapsules():
    #     x, y = i[0], i[1]
    #     #foodDist.append(((x, y), abs(pX-x) + abs(pY-y)))
    #     capsuleDist.append(abs(pX-x) + abs(pY-y))
    # if debug: print 'capsuleDist', capsuleDist    
    # capsuleDistPenalty = defaultPenalty * sum(capsuleDist)
    # capsuleDistPenalty = capsuleDistPenalty * 2

    # # capsule is near then follow it
    capsulePenalty = 0
    for i in state.getCapsules():
        capsuleDist = 20
        x, y = i[0], i[1]
        capsuleDist = abs(pX - x) + abs(pY - y)
        if capsuleDist <= 1:
            capsulePenalty = 1250
        elif capsuleDist <= 2:
            capsulePenalty = 1000
        elif capsuleDist <= 3:
            capsulePenalty = 750

    # capsule dist
    capsuleDist = []
    for i in state.getCapsules():
        x, y = i[0], i[1]
        capsuleDist.append(abs(pX-x) + abs(pY-y))
    minCapsuleDist = 0
    if len(capsuleDist) != 0:
        minCapsuleDist = min(capsuleDist) * defaultPenalty

    capsuleDistPenalty = defaultPenalty * sum(capsuleDist) * 2    
    if capsuleDistPenalty == 0:
        capsuleDistPenalty = -1

    # food distance penalty : further food distance more penalty
    foodDist = []
    for i in food:
        x, y = i[0], i[1]
        #foodDist.append(((x, y), abs(pX-x) + abs(pY-y)))
        foodDist.append(abs(pX-x) + abs(pY-y))
    minFoodDist = 0
    if len(foodDist) != 0: 
        minFoodDist = min(foodDist) * defaultPenalty

    foodDistPenalty = defaultPenalty * sum(foodDist)
    if foodDistPenalty == 0:
        foodDistPenalty = -1

    if debug: print 'foodDist', foodDist

    # food remain penalty: more food remains more penalty
    foodRemainWeight = 5
    if foodRemain <= 10: foodRemainWeight = 11
    elif foodRemain <= 20 : foodRemainWeight = 10
    elif foodRemain <= 30 : foodRemainWeight = 9
    elif foodRemain <= 40 : foodRemainWeight = 8
    elif foodRemain <= 50 : foodRemainWeight = 7
    foodRemainPenalty = defaultPenalty * foodRemain * foodRemainWeight


    # ghost is in fear, then follow it


    
    # score penalty
    scoreWeight = 1
    if score <= 100: scoreWeight = 2
    elif score <= 200: scoreWeight = 1.5
    elif score <= 400: scoreWeight = 0.6
    elif score <= 600 : scoreWeight = 0.3
    elif score <= 900 : scoreWeight = 0
    # scoreWeight = 1
    
    scorePenalty = score * scoreWeight

    result += ghostPenalty
    # result += capsulePenalty
    #result += capsuleDistPenalty
    result += foodDistPenalty
    result += scorePenalty     
    # if not isGhostScared:
    #     result += capsuleDistPenalty
    #     result += capsulePenalty
    # else:
    #     result += foodDistPenalty
    #     result += scorePenalty        
    # result += capsuleRemain * -50

    # if minFoodDist < minCapsuleDist:
    #     result += minCapsuleDist
    # else:
    #     result += minFoodDist
    
    # result += minCapsuleDist
    #result += capsuleDistPenalty


    # result += minFoodDist
    # result += foodDistPenalty
    # result += foodRemain * -1

    # if minFoodDist >= 7:
    #     result += foodDistPenalty 
    # else:
    #     result += foodDistPenalty
    #     result += foodRemainPenalty     


    # result += foodDistPenalty 
    # result += foodRemainPenalty 
    # result += capsuleDistPenalty
    # result += capsulePenalty
        


    if True:
        print '2{}({},{}) RS[{}] mf[{}] mc[{}] Fdp[{},{}] Frw[{},{}] Sswp[{},{},{}] Go[{}] Ca[{},{},{},{}]'.format(
            isGhostScared, pX, pY, result, minFoodDist, minCapsuleDist,
            foodDistPenalty, foodRemainPenalty, foodRemain, foodRemainWeight, 
            scorePenalty, score, scoreWeight, 
            ghostPenalty,
            capsuleDist, capsuleDistPenalty, capsuleRemain, capsulePenalty)
    try:
        if False:
            input()
            print ''
        pass
    except Exception:
        pass

    "*** YOUR CODE HERE ***"
    return result

class ContestAgent(ExpectimaxAgent):
    """
      Your agent for the mini-contest
    """

    # I just use what I've developed so far
    def __init__(self, evalFn='betterEvaluationFunction2', depth='2'):
      self.index = 0
      self.evaluationFunction = util.lookup(evalFn, globals())
      self.depth = int(depth)
