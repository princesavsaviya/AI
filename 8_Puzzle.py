# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 16:57:24 2025

@author: princ
"""

import numpy as np
import heapq as hq
import itertools

counter = itertools.count()


def create_node(state,g):
    return {'state':state,
            'g':g}

def get_blank_space(node):
    return np.argwhere(node['state']==0)[0]

def queuing_function(nodes,node):
    n = node['state'].shape[0]
    row,column = get_blank_space(node)

    if row + 1 < n:
        temp = np.copy(node['state'])
        temp[row, column], temp[row+1, column] = temp[row+1, column], temp[row, column]
        temp_node = create_node(temp, node['g']+1)
        hq.heappush(nodes, (temp_node['g'], next(counter),temp_node))
    if row - 1 >= 0:
        temp = np.copy(node['state'])        
        temp[row, column], temp[row-1, column] = temp[row-1, column], temp[row, column]
        temp_node = create_node(temp, node['g']+1)
        hq.heappush(nodes, (temp_node['g'], next(counter),temp_node))
        
    if column + 1 < n:
        temp = np.copy(node['state'])
        temp[row, column], temp[row, column+1] = temp[row, column+1], temp[row, column]
        temp_node = create_node(temp, node['g']+1)
        hq.heappush(nodes, (temp_node['g'], next(counter),temp_node))
    if column - 1 >= 0:
        temp = np.copy(node['state'])
        temp[row, column], temp[row, column-1] = temp[row, column-1], temp[row, column]
        temp_node = create_node(temp, node['g']+1)
        hq.heappush(nodes, (temp_node['g'], next(counter),temp_node))
    return nodes

        
def general_solution(init_state,goal_state):
    
    init_node = create_node(init_state, 0)
    
    nodes = []
    hq.heappush(nodes, (init_node['g'], next(counter), init_node))
    visited = set()
    
    while nodes:
        
        _, count,node = hq.heappop(nodes)
        
        node_tuple = tuple(node['state'].flatten())
        if node_tuple in visited:
            continue
        visited.add(node_tuple)
        
        if np.array_equal(node['state'], goal_state):
            print()
            print("State Generated :: ", count)
            print()
            print("Ans :: ")
            return node['state']
        
        nodes = queuing_function(nodes, node)
    return "failure"

init_state = np.array([1,6,7,5,0,3,4,8,2]).reshape((3,3))
goal_state = np.array([1,2,3,4,5,6,7,8,0]).reshape((3,3))

print(general_solution(init_state, goal_state))

    


"""
for solving Error :: https://stackoverflow.com/questions/10218953/tie-breaking-in-a-priority-queue-using-python
"""