
from sample_players import DataPlayer
from isolation import Isolation
from enum import IntEnum
from typing import List

from isolation import DebugState

import random
from copy import deepcopy
import math

MTCS_C = 1.0
NUM_ITER = 100


class MCTSNode():
    """
    Definition of a node in the tree of a Monte Carlo Tree Search
    algorithm
    """
    def __init__(self, state: Isolation, parent: 'MCTSNode' = None):
        """
        Constructor
        
        Args:
            state [Isolation]: The current state of the Isolation board
            parent [MCTSNode]: The parent of this node. None denotes the root.
        """
        self._state: Isolation = state
        self._children: List[MCTSNode] = []
        self._children_actions: List[IntEnum] = []
        self._parent: MCTSNode = parent
        self._visits: int = 1
        self._reward: float = 0.0

    def add_child_node(self, state: Isolation, action: IntEnum):
        """
        Method to add a child node given that this
        node is the parent
        
        Args:
            state [Isolation]: The current state of the Isolation board
            action [Action]: The action to make given this current state
        """
        child = MCTSNode(state, self)
        self._children.append(child)
        self._children_actions.append(action)

    def update(self, reward):
        """
        Method to update the cumulative reward and visits
        for this node
        
        Args:
            reward [float]: The reward to add to this node
        """
        self._reward += reward
        self._visits += 1

    def fully_explored(self) -> bool:
        """
        Determine if we have fully explored all possible actions given
        this state
        
        Returns:
            A bool to denote whether we have fully explored all possible
            actions given this state
        """
        return len(self._state.actions()) == len(self._children_actions)

### Functions that define the core MTCS algorithm
def expand(node) -> MCTSNode:
    # choose action a that belongs to untried actions from the current node v
    for action in node._state.actions():
        if action not in node._children_actions:
            # Add new child node v' to current node v
            # by applying the action a
            new_state = node._state.result(action)
            node.add_child_node(new_state, action)
            # Return this node
            return node._children[-1]

def tree_policy(node: MCTSNode) -> MCTSNode:
    """
    Tree Policy for MTCS - Selects a leaf node.
    If we have not fully explored all nodes given the input node, we
    will return a child node we haven't explored.  Otherwise, we will
    return the child node with the best score.
    
    Args:
        node [MCTSNode]: MTCS Node to test

    Returns:
        An MTCS child node subject to the aforementioned
    """
    # while v is nonterminal do
    while not node._state.terminal_test():
        # if v is not fully expanded (fully explored)
        if not node.fully_explored():
            # return expand(node)
            return expand(node)
        # else node <- bestChild(node)
        node = best_child(node)

    return node


def best_child(node: MCTSNode) -> MCTSNode:
    """
    Find the child node with the best score given
    the input node
    
    Args:
        node [MCTSNode]: Current input node

    Returns:
        MCTSNode that is the child with the best score given
        the input node
    """
    
    # return argmax over all children v' of node v
    # Q(v') / N(v') + c * sqrt(2 * ln(N(v)) / ln(N(v')))
    best_score = float("-inf")
    best_node = None
    
    for child in node._children:
        exploitation = child._reward / child._visits
        exploration = math.sqrt(2.0 * math.log(node._visits) / child._visits)
        score = exploitation + MTCS_C * exploration
        if score >= best_score:
            best_node = child
            best_score = score

    return best_node


def default_policy(state: Isolation) -> int:
    """
    Default policy given the current state of the Isolation board.
    Essentially we play the board given this current state until someone
    wins or loses.
    
    Args:
        state [Isolation]: Current state of the input Isolation board

    Returns:
        Reward such that 1 is a winning state and -1 is a losing state
    """
    # Save a copy of the initial input state
    initial_state = deepcopy(state)
    initial_player = initial_state.player()

    # While the current state is is non-terminal    
    while not state.terminal_test():
        # Choose action uniformly at random
        action = random.choice(state.actions())
        # Update the current state based on this action
        state = state.result(action)

    # Recall that the reward is 1 for winner, -1 for loser
    # Get whoever is playing currently given the initial state
    # If we see that at the end of the game, this player has no
    # more moves left, they have lost so the reward is -1
    return -1 if state._has_liberties(initial_player) else 1


def backup(node: MCTSNode, reward: int):
    """
    Backpropagation step for the MTCS algorithm for two players
    
    Args:
        node [MCTSNode]: Leaf node that dictates a game ending
        reward [int]: The reward issued at this game ending
    """
    # while node v is not terminal
    while node is not None:
        # num_visits_at_v += 1
        # total_reward_at_v += reward
        node.update(reward)
        # Move upwards to the parent
        node = node._parent
        # reward = -reward
        reward *= -1

class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """

    def mcts_search(self, state: Isolation):
        """
        Performs a MTCS iteration given an Isolation board
        
        Args:
            state [Isolation]: Input isolation board
        """
        # Create root node v0 with state
        root = MCTSNode(state)
        
        # If the root is terminal, simply do a random choice of the actions
        if root._state.terminal_test():
            return random.choice(state.actions())
        # while within computational budget do
        for i in range(NUM_ITER):
            # Perform tree policy to select best child
            child = tree_policy(root)
            
            # If we don't end up getting a child, skip
            if not child:
                continue
            # Enact default policy to get best reward
            reward = default_policy(child._state)
            
            # Backpropagate
            backup(child, reward)

        # Determine the best action to take given the best child
        idx = root._children.index(best_child(root))
        return root._children_actions[idx]

    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller will be responsible
        for cutting off the function after the search time limit has expired.

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE: 
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        # TODO: Replace the example implementation below with your own search
        #       method by combining techniques from lecture
        #
        # EXAMPLE: choose a random move without any search--this function MUST
        #          call self.queue.put(ACTION) at least once before time expires
        #          (the timer is automatically managed for you)
        
        # If the total move count is less than 2, there's no point in doing a
        # MTCS search it's essentially random chance - don't waste time and just
        # randomly choose an action
        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
        else:
            self.queue.put(self.mcts_search(state))
            
#         print('In get_action(), state received:')
#         debug_board = DebugState.from_state(state)
#         print(debug_board)
