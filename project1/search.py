# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]


# for debug purpose, print Stack
def printStack(l):
    temp = list()
    while l.isEmpty() == False:
        node = l.pop()
        temp.insert(0, node)
    
    print 'Print Stack'
    for x in temp:
        print '', x
        l.push(x)            
    print ''


# for debug purpose, print Queue
def printQueue(l):
    temp = list()
    while l.isEmpty() == False:
        node = l.pop()
        temp.append(node)
    
    print 'Print Queue'
    for x in temp:
        print '', x
        l.push(x)            
    print ''


# for debug purpose, print Priority Queue
def printPQ(pq):
    temp = list()
    while pq.isEmpty() == False:
        node = pq.pop()
        temp.append(node)
    
    print 'Print PriorityQ'
    for x in temp:
        print '\t', x
        # x is [currNode, prevPos]
        # Node is [((posX,posY), 'East', 1), sumF, sumG, sumH]
        # therefore, x[0][1] is sumF
        pq.push(x, x.getSumF())  
    print ''          


# Node def : [(state, direction, gValue), sumF, sumG, sumH, pathSofar]
#   state = ((x,y), targetState), targetState is optinal 
#   direction = N S E W
#   gValue = edge cost
#   sumF = sumG + sumH
#   sumG = sum of distance so far
#   sumH = sum of heuristic so far
#   pathSofar = keep track of the path to this node
class Node:
    def __init__(self, info=None, sumF=0, sumG=0, sumH=0, path=[]):
        self.info = info
        self.sumF = sumF
        self.sumG = sumG
        self.sumH = sumH
        self.path = path
    def getInfo(self):
        return self.info
    def getSumF(self):
        return self.sumF
    def getSumG(self):
        return self.sumG
    def getSumH(self):
        return self.sumH
    def getState(self):
        return self.info[0]
    def getDir(self):
        return self.info[1]
    def getPath(self):
        return self.path
    def __str__(self):
        return '{}, {}, {}, {}, PATH SO FAR {}'.format(
            self.info, self.sumF, self.sumG, self.sumH, self.path
        )


# type 
#   'dfs' Deapth First Search
#   'bfs' Bread First Search
#   'ucs' Uniform Cost Search
#   'astar' Astar Search
# d : debug option
# heuristic : heuristic function you want to use
def costSearch(problem, d, type, heuristic):
    import util

    debug = d

    if debug:
        print "Start:", problem.getStartState()
        print "Is the start a goal?", problem.isGoalState(problem.getStartState())
        print "Start's successors:", problem.getSuccessors(problem.getStartState())
        print '\n'

    # waitList is queue which is consist of nodes in order
    #   [ Node, Node, Node .. , Node ] 
    #   Look at the Node class definition in detail
    waitList = None
    if type == 'dfs':
        waitList = util.Stack()
    elif type == 'bfs':
        waitList = util.Queue()
    elif type == 'ucs' or type == 'astar':
        waitList = util.PriorityQueue()
    else:
        quit()

    # visited is a list consist of 'State's
    # State Def
    #   it can be two ways of definition
    #   it is decided by searchAgent
    #   type 1
    #       it a tuple with xy Position
    #       (4, 5)
    #   type 2
    #       it's a tuple with xy Position and target visit information
    #       (4, 5), [target visit information]
    visited = list()

    # push a Node class with priority
    startState = problem.getStartState()
    startNode = Node((startState, 'Start', 1))
    if type == 'dfs' or type == 'bfs':
        waitList.push(startNode)
    elif type == 'ucs' or type == 'astar':
        waitList.push(startNode, startNode.getSumF())


    while waitList.isEmpty() == False:
        if debug: 
            if type == 'dfs': printStack(waitList)
            elif type == 'bfs': printQueue(waitList)
            else: printPQ(waitList)

        # popNode is a Node class 
        # Node def : [(state, direction, gValue), sumF, sumG, sumH, pathSofar]
        popNode = waitList.pop()
        popState = popNode.getState()

        if debug: 
            print '<< POP Node >> ==>', popNode

        if problem.isGoalState(popState):
            if debug: 
                print '!!!!!!!!!! GOAL FOUNDED !!!!!!!!!!'
                print 'result path', popNode.getPath()
        
            return popNode.getPath()

        elif popState not in visited: # not visited
            if debug: print '\tvisit check: has NOT visited.'

            # getSuccessors return a tupel of 'State'
            # State could be (state, direction, cost)
            #   or ((state, direction, cost), [target visit information])
            succNode = problem.getSuccessors(popState)
            if debug: print '\tsuccNode', succNode

            # x is like (state, direction, cost)
            for x in succNode:
                xState = x[0]
                xDir = x[1]
                if xState not in visited:
                    xSumG = x[2] + popNode.getSumG()
                    xSumH = heuristic(x[0], problem)
                    xSumF = xSumG + xSumH

                    path = popNode.getPath() + [xDir]
                    newNode = Node(x, xSumF, xSumG, xSumH, path)
                    
                    if type == 'dfs' or type == 'bfs':
                        waitList.push(newNode)
                    elif type == 'ucs' or type == 'astar':
                        waitList.push(newNode, newNode.getSumF())

                    if debug: print '\t\t<< PUSH node >>', newNode 
                else:
                    if debug: print '\t\t<< DONT PUSH node >>', xState, 'already visited'

            # save for visited after finishing expanding
            if debug: print '\tvisit SAVE :', popNode 
            visited.append(popState)
        else:
            if debug: print '\tvisit check: already visited.'
        
        if debug: 
            print '\tVisited list'
            for x in visited:
                print '\t', x

            try:
                input()
            except Exception:
                pass


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    #resultPath = uniSearch('stack', problem, False)
    resultPath = costSearch(problem, False, 'dfs', nullHeuristic)
    return resultPath


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """
    "*** YOUR CODE HERE ***"
    #resultPath = uniSearch('queue', problem, False)
    resultPath = costSearch(problem, False, 'bfs', nullHeuristic)
    return resultPath


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    resultPath = costSearch(problem, False, 'ucs', nullHeuristic)
    return resultPath


def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    resultPath = costSearch(problem, False, 'astar', heuristic)
    return resultPath


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
