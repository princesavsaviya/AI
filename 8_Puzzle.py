# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 16:57:24 2025

@author: prince
"""

import numpy as np
import heapq as hq
import itertools

counter = itertools.count()


def create_node(state,g):
    "Create a Dictionary to store state and value of g(n)."
    
    return {'state':state,
            'g':g}

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

def queuing_function(nodes,node):
    "Generate the states using valid moves and append it to the priority queue."
    
    n = node['state'].shape[0]
    row,column = get_blank_space(node)

    valid_moves = get_valid_moves(row, column, n)

    # Create the States from the valid moves calculated using the get_valid_moves function and update the nodes 
    # Since it is uniform Cost search it will add 1 as the cost to move to next state.
    for move in valid_moves:
        temp = np.copy(node['state'])
        temp[row, column], temp[row+move[0], column+move[1]] = temp[row+move[0], column+move[1]], temp[row, column]
        temp_node = create_node(temp, node['g']+1)
        hq.heappush(nodes, (temp_node['g'], next(counter),temp_node)) # universal counter is used as tie breaker for the same temp_node
        
    return nodes

        
def general_search(init_state,goal_state):
    "Perform search using the A* Algorithm"
    
    init_node = create_node(init_state, 0)
    
    nodes = [] # Priority Queue
    hq.heappush(nodes, (init_node['g'], next(counter), init_node))
    visited = set() # To keep track of already visited nodes
    
    while nodes:
        
        g, count,node = hq.heappop(nodes) # get the node with least g value
        
        node_tuple = tuple(node['state'].flatten())
        if node_tuple in visited:
            continue
        visited.add(node_tuple)
        
        if np.array_equal(node['state'], goal_state):
            print()
            print("State Generated :: ", count)
            print()
            print("Depth of Solution :: ",g)
            print()
            print("Ans :: ")
            return node['state']
        
        nodes = queuing_function(nodes, node)
    return "failure"

# Default Puzzle
init_state = np.array([1,6,7,5,0,3,4,8,2]).reshape((3,3))
goal_state = np.array([1,2,3,4,5,6,7,8,0]).reshape((3,3))


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
        print(general_search(init_state, goal_state))
else:
    print(general_search(init_state, goal_state))






    


"""
for solving Error :: https://stackoverflow.com/questions/10218953/tie-breaking-in-a-priority-queue-using-python
for generation example states :: https://sliding.toys/mystic-square/8-puzzle/
"""