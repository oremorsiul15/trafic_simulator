import math
import numpy as np
n = 10
grid = np.zeros((10,10), dtype=np.int64)

pos  = (2,3)

apple = (8, 7)

def distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return math.sqrt((x1-x2)**2 + (y1 - y2)**2)

def get_shortest_distance(pos1, target, obstacles):
    x1, y1 = pos1
    x2, y2 = target
    dis = 90000
    result = (0,0)
    for i in range(x1 -1, x1 + 2):
        for j in range(y1 -1, y1 + 2):
            if (i, j) != pos1 and ((i, j) not in obstacles):
                d = distance(apple, (i, j))
                print((i, j), d)
                if d < dis:
                    dis = d
                    result = (i, j)

    return result

def find_path(pos, apple, obstacles,  path):  
    if pos == apple:
        return path
    
    shortest_pos = get_shortest_distance(pos, apple, obstacles)
    print(shortest_pos)
    path.append(shortest_pos)
    find_path(shortest_pos, apple, obstacles, path)

# -------------------------------display---------------------------------------------
x1, y1 = pos
x2, y2 = apple
obstacles = [(3, 3), (6, 6), (9, 1), (4, 5)]
path = []
find_path(pos, apple, obstacles, path)
grid[x1][y1] = 2

for o in obstacles:
    x, y = o
    grid[x][y] = 7

print(path)
for p in path:
    x, y = p
    grid[x][y] = 1
grid[x2][y2] = 8

def print_grid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            print(str(grid[i][j])+" ", end='')
        print()
print_grid(grid)