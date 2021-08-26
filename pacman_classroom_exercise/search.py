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

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    frontier = util.Stack() # DFS uses Stack
    # track visited nodes
    visited = []
    # push initial state to frontier
    # We are pushing the current position and the path to get up to this point + cost
    frontier.push((problem.getStartState(), [], 1))
    
    while not frontier.isEmpty():
        state, actions, _ = frontier.pop()
        # visited node
        # goal check
        if problem.isGoalState(state):
            return actions
        
        # If we have already visited, skip
        if state in visited:
            continue

        visited.append(state)
        # visit child nodes
        successors = problem.getSuccessors(state)
        for child_state, child_action, _ in successors:
            # store state, action and cost = 1
            if child_state not in visited:
                # add child nodes - remember to put the previous paths
                # BEFORE the next path to reconstruct what we do up to the
                # current step
                child_action = actions + [child_action]
                frontier.push((child_state, child_action, 1))

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"   
    frontier = util.Queue() # BFS uses Queue
    # track visited nodes
    visited = []
    # push initial state to frontier
    frontier.push((problem.getStartState(), [], 1))
    
    while not frontier.isEmpty():
        state, actions, _ = frontier.pop()
        # goal check
        if problem.isGoalState(state):
            return actions
        
        # If we have already visited, skip
        if state in visited:
            continue

        visited.append(state)
        # visit child nodes
        successors = problem.getSuccessors(state)
        for child_state, child_action, _ in successors:
            # store state, action and cost = 1
            if child_state not in visited:
                # add child nodes
                child_action = actions + [child_action]
                frontier.push((child_state, child_action, 1))

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    # Almost the same, but we now use a Priority Queue to determine what
    # path to explore next    
    # Frontier is going to contain triples - each one contains
    # position, list of actions up to this point, total cost
    # PriorityQueue expects a tuple (item, priority)
    frontier = util.PriorityQueue()
    # track visited nodes
    visited = []
    # push initial state to frontier - we push a node and its corresponding priority
    frontier.push((problem.getStartState(), [], 1), 1)
    while not frontier.isEmpty():
        state, actions, _ = frontier.pop()
        # goal check
        if problem.isGoalState(state):
            return actions

        # If we have already visited, skip
        if state in visited:
            continue
        
        visited.append(state)
        # visit child nodes
        successors = problem.getSuccessors(state)
        for child_state, child_action, _ in successors:
            # store state, action and cost = cumulative cost from beginning up to this point
            if child_state not in visited:
                # add child nodes
                child_action = actions + [child_action]
                # For the priority queue, we are now calculating cumulative cost from the
                # beginning up to the current action                
                cost = problem.getCostOfActions(child_action)
                # For the next iteration, choose the path with the lowest cost
                frontier.push((child_state, child_action, 0), cost)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    # Almost the same as uniform cost search, but we maintain the cost to get from the beginning to the
    # current node as well as the distance to the goal
    frontier = util.PriorityQueue()
    # track visited nodes
    visited = []
    # push initial state to frontier - we push a node and its corresponding priority
    frontier.push((problem.getStartState(), [], 0), heuristic(problem.getStartState(), problem))
    while not frontier.isEmpty():
        state, actions, _ = frontier.pop()
        # goal check
        if problem.isGoalState(state):
            return actions
        
        # If we have visited the node, skip
        if state in visited:
            continue
        
        visited.append(state)
        # visit child nodes
        successors = problem.getSuccessors(state)
        for child_state, child_action, _ in successors:
            # store state, action and cost = f + g
            # f - cumulative cost from the beginning up to this point
            # g - heuristic
            if child_state not in visited:
                # add child nodes
                child_action = actions + [child_action]
                cost = problem.getCostOfActions(child_action)
                frontier.push((child_state, child_action, 0), cost + heuristic(child_state, problem))



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
