import numpy as np
import random
import time
import copy
print("Welcome!!!\n")
time.sleep(1)
sol_maze = []
N = int(input("Enter size of maze: "))
print("\n")
while True:
    maze = np.random.randint(2, size=(N, N))

    def MAZE(maze):
        global sol
        sol = copy.deepcopy(maze)

        if BACKTRACKING_ALGORITHM(maze, 0, 0, sol) == False:
            return False

        return True

    def BACKTRACKING_ALGORITHM(maze, x, y, sol):

        if x == N-1 and y == N-1:
            sol[x][y] = 5
            return True

        if check(maze, x, y) == True:
            sol[x][y] = 5

            if BACKTRACKING_ALGORITHM(maze, x+1, y, sol) == True:
                return True

            if BACKTRACKING_ALGORITHM(maze, x, y+1, sol) == True:
                return True

            sol[x][y] = 0
            return False

    def check(maze, x, y):
        if x >= 0 and x < N and y >= 0 and y < N and maze[x][y] == 1:
            return True

    if MAZE(maze) == False or maze[N-1][N-1] == 0 or maze[0][0] == 0:
        continue

    time.sleep(1)
    for i in maze:
        for j in i:
            print(str(j), end=" ")
        print()
    time.sleep(1)
    print("\nThis is the maze to be solved")
    break


time.sleep(1)
ch = input(("\nEnter y to get solution: "))
print('\n')
if ch == 'y' or ch == 'Y':
    for i in sol:
        for j in i:
            print(str(j), end=" ")
        print()
print("\nThis is the solution maze")
