import numpy as np
from eight_Puzzle_Combined import zero_heuristic,manhattan_heuristic,misplaced_tile_heuristic,general_search
import matplotlib.pyplot as plt
import time

Problems = [np.array([1,2,3,4,5,6,7,8,0]).reshape((3,3)),
            np.array([1,2,3,4,5,6,0,7,8]).reshape((3,3)),
            np.array([1,2,3,5,0,6,4,7,8]).reshape((3,3)),
            np.array([1,3,6,5,0,2,4,7,8]).reshape((3,3)),
            np.array([1,3,6,5,0,7,4,8,2]).reshape((3,3)),
            np.array([1,6,7,5,0,3,4,8,2]).reshape((3,3)),
            np.array([7,1,2,4,8,5,6,3,0]).reshape((3,3)),
            np.array([0,7,2,4,6,1,3,5,8]).reshape((3,3))]

goal_state = np.array([1,2,3,4,5,6,7,8,0]).reshape((3,3))

h_funcs = [zero_heuristic,manhattan_heuristic,misplaced_tile_heuristic]
search_types = ["Uniform Cost Search","Manhattan Distance Heuristic","Misplaced Tile Heuristic"]

all_depths = []
all_states = []
all_times = []
all_nodes = []

for idx, h in enumerate(h_funcs):
    depths = []
    states = []
    times = []
    nodes = []
    print(f"\n=== {search_types[idx]} ===")
    for problem in Problems:
        print("Initial State:\n", problem)
        start_time = time.time()
        _, g, expanded_nodes,max_nodes = general_search(problem, goal_state, h)
        end_time = time.time()
        depths.append(g)
        states.append(expanded_nodes)
        times.append(end_time - start_time)
        nodes.append(max_nodes)
    all_depths.append(depths)
    all_states.append(states)
    all_times.append(times)
    all_nodes.append(nodes)

all_states = np.log10(np.array(all_states))
all_times = np.log10(np.array(all_times))
all_nodes = np.log10(np.array(all_nodes))

fig, ax = plt.subplots(figsize=(10, 5))
for i, (depths, states) in enumerate(zip(all_depths, all_states)):
    ax.plot(depths, states, label=search_types[i], marker='o')
ax.set_xlabel('Depth of Solution')
ax.set_ylabel('Expanded Nodes (log scale base 10)')
ax.set_title('Expanded Nodes vs Depth (Log Scale base 10)')
ax.grid(True)
ax.legend()

plt.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(10, 5))
for i, (depths, times) in enumerate(zip(all_depths, all_times)):
    ax.plot(depths, times, label=search_types[i], marker='o')
ax.set_xlabel('Depth of Solution')
ax.set_ylabel('Time (seconds) (log scale base 10)')
ax.set_title('Time vs Depth (Log Scale base 10)')
ax.grid(True)
ax.legend()

plt.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(10, 5))
for i, (depths, nodes) in enumerate(zip(all_depths, all_nodes)):
    ax.plot(depths, nodes, label=search_types[i], marker='o')
ax.set_xlabel('Depth of Solution')
ax.set_ylabel('Max Nodes in Queue (log scale base 10)')
ax.set_title('Max Nodes in Queue vs Depth (Log Scale base 10)')
ax.grid(True)
ax.legend()

plt.tight_layout()
plt.show()