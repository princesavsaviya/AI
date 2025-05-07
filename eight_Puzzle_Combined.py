# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 16:57:24 2025

@author: prince
"""

import numpy as np
import heapq as hq
import itertools

counter = itertools.count()

def zero_heuristic(state,goal_state,n):
    "Heuristic function to calculate the distance between the current state and goal state."
    return 0

def manhattan_heuristic(state,goal_state,n):
    distance = 0
    for i in range(n):
        for j in range(n):
            row,column = np.argwhere(goal_state==state[i][j])[0]
            distance = distance + np.abs(row-i) + np.abs(column - j)
    
    return distance

def misplaced_tile_heuristic(state,goal_state,n):
    misplaced_values = (state!=goal_state).sum()
    return misplaced_values


def create_node(state,g,h):
    "Create a Dictionary to store state and value of g(n)."
    
    return {'state':state,
            'g':g,
            'h':h,
            'f':h+g}

def get_blank_space(node):
    "Get the Index of the Blank Space(0)."
    
    return np.argwhere(node['state']==0)[0]

def get_valid_moves(row,column,n):
    "Get the valid moves from 4 available moves."
    
    possible_moves = ((1,0),(-1,0),(0,1),(0,-1))
    valid_moves = []
    for move in possible_moves:
        if 0<=row+move[0]<n and 0<=column+move[1]<n:
            valid_moves.append(move)
    return valid_moves

def queuing_function(nodes,node,goal_state,h_func):
    "Generate the states using valid moves and append it to the priority queue."
    
    n = node['state'].shape[0]
    row,column = get_blank_space(node)

    valid_moves = get_valid_moves(row, column, n)

    # Create the States from the valid moves calculated using the get_valid_moves function and update the nodes 
    for move in valid_moves:
        temp = np.copy(node['state'])
        temp[row, column], temp[row+move[0], column+move[1]] = temp[row+move[0], column+move[1]], temp[row, column]
        h = h_func(temp, goal_state,n)
        temp_node = create_node(temp, node['g']+1,h)
        hq.heappush(nodes, (temp_node['f'], next(counter),temp_node)) # universal counter is used as tie breaker for the same temp_node
        
    return nodes

        
def general_search(init_state,goal_state,h_func):
    "Perform search using the A* Algorithm"
    
    n = init_state.shape[0]
    h = h_func(init_state, goal_state,n)
    init_node = create_node(init_state, 0,h)
    
    expanded_nodes = 0 # To keep track of the number of states generated
    nodes = [] # Priority Queue
    hq.heappush(nodes, (init_node['f'], next(counter), init_node))
    visited = set() # To keep track of already visited nodes
    max_nodes = 0 # To keep track of the maximum number of nodes in the queue
    while nodes:
        
        g, count,node = hq.heappop(nodes) # get the node with least g value
        expanded_nodes += 1 # Increment the number of states generated
        g = node['g']
        node_tuple = tuple(node['state'].flatten())
        if node_tuple in visited:
            continue
        visited.add(node_tuple)
        
        if np.array_equal(node['state'], goal_state):
            print()
            print("State Generated :: ", expanded_nodes)
            print()
            print("Depth of Solution :: ",g)
            print()
            print("Max Nodes in Queue :: ", max_nodes)
            print()
            print("Ans :: ")
            return (node['state'],g,expanded_nodes,max_nodes)
        
        nodes = queuing_function(nodes, node,goal_state,h_func)
        max_nodes = max(max_nodes, len(nodes))
    return "failure"

if __name__ == "__main__":
    # Default Puzzle
    init_state = np.array([1,6,7,5,0,3,4,8,2]).reshape((3,3))
    goal_state = np.array([1,2,3,4,5,6,7,8,0]).reshape((3,3))


    search_type = int(input("Enter 1 to use Misplaced Tile Heuristic \nEnter 2 to use Manhattan Distance Heuristic \nEnter 3 to use Uniform Cost Search :: "))
    while search_type not in [1,2,3]:
        print("Invalid Input, try again!")
        search_type = int(input("Enter 1 to use Misplaced Tile Heuristic \nEnter 2 to use Manhattan Distance Heuristic \nEnter 3 to use Uniform Cost Search :: "))
    if search_type == 1:
        h_func = misplaced_tile_heuristic
    elif search_type == 2:
        n = init_state.shape[0]
        h_func = manhattan_heuristic
    else:
        h_func = zero_heuristic

    game_mode = int(input("Enter 1 to use default Puzzle \nEnter 2 to use custom Puzzle :: "))

    if game_mode == 2:
        n = int(input("Enter n for nxn Puzzle Board :: "))
        l = []
        i=0
        while i<n:
            row = list(map(int,input(f"Enter Values of Row{i+1} with space between :: ").split()))
            if len(row)!=n:
                print("Entered Value greater or less then n, try again!")
                continue
            else:
                l.append(row)
                i+=1
        
        init_state = np.array(l)
        goal_state = np.array([i for i in range(1,n*n)]+[0]).reshape((n,n)) # Generate Goal state based on "n"
        if len(np.argwhere(init_state==0))!=1:
            print("There are no blank space or more than 1 blank space, try again!")
        else:
            print("Initial State :: \n", init_state)
            print(general_search(init_state, goal_state,h_func)[0])
    else:
        print(general_search(init_state, goal_state,h_func)[0])






    


"""
for solving Error :: https://stackoverflow.com/questions/10218953/tie-breaking-in-a-priority-queue-using-python
for generation example states :: https://sliding.toys/mystic-square/8-puzzle/
"""