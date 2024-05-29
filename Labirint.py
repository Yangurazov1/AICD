!pip install matplotlib
import matplotlib.pyplot as plt
from itertools import groupby
import random
from dataclasses import dataclass, field


@dataclass
class MazeCell:
    x: int
    y: int
    component: int
    is_open: bool = field(default=False)
    walls: list = field(default_factory=list)
N = 30
LINE_WIDTH = 45

maze = []
parents  = []
ranks = []
used = []

def find(x):
    stack = []

    while x != parents[x]:
      stack.append(x)
      x = parents[x]
    while len(stack) != 0:
      cell_index = stack.pop()
      parents[cell_index] = x

    return x

# объединяет два несвязанных множества в одно, соединяя их корни
def union(x, y):
    x_root = find(x.component)
    y_root = find(y.component)

    parents[y_root] = x_root

# возвращает соседей по часовой стрелке
def find_neighbours(maze_cell):
  x, y = maze_cell.x,  maze_cell.y
  neighbours = []
  if y + 1 < N:
    neighbours.append(maze[x][y + 1])
  if x + 1 < N:
    neighbours.append(maze[x + 1][y])
  if y - 1 >= 0:
    neighbours.append(maze[x][y - 1])
  if x - 1 >= 0:
    neighbours.append(maze[x - 1][y])
  return neighbours

#Проверяет, принадлежит ли весь лабиринт одной компоненте
def all_equal(iterable):
   g = groupby(iterable)
   return next(g, True) and not next(g, False)

def delete_walls(cell, neighbour):
    x, y = neighbour.x - cell.x, neighbour.y - cell.y

    if x > 0:
        cell.walls[1] = False
        neighbour.walls[3] = False
    elif x < 0:
        cell.walls[3] = False
        neighbour.walls[1] = False

    if y > 0:
        cell.walls[2] = False
        neighbour.walls[0] = False
    elif y < 0:
        cell.walls[0] = False
        neighbour.walls[2] = False
def generate_maze(N) -> list[list[MazeCell]]:
    maze = []
    n = 0
    for y in range(N):
        line = []
        for x in range(N):
            maze.append(MazeCell(x, y, n, False, [True, True, True, True]))
            n += 1

    unchoises = maze[:]


    while check_comp(maze):
        cell = rand_choise(unchoises, maze)
        if cell is None: break
        x, y = cell.x, cell.y
        neighbours = get_neigbours(x, y, maze)
        neighbour = rd.choice(neighbours)

        if union(cell, neighbour, maze):
            delete_walls(cell, neighbour)
# Открываем один вход и выход
    maze[0][0].is_open = True
    maze[0][0].walls[0] = False
    maze[-1][-1].is_open = True
    maze[-1][-1].walls[2] = False

    return maze
maze = generate_maze(N)
def draw_maze(maze_):
    for i in range(N):
      for j in range(N):
        cell = maze_[i][j]

        if cell.walls[0]:
          plt.plot([cell.x, cell.x + LINE_WIDTH], [N - cell.y, N - cell.y], 'k-', lw=2)
        if cell.walls[1]:
          plt.plot([cell.x + LINE_WIDTH, cell.x + LINE_WIDTH], [N - cell.y, N - cell.y - LINE_WIDTH], 'k-', lw=2)
        if cell.walls[2]:
          plt.plot([cell.x, cell.x + LINE_WIDTH], [N - cell.y - LINE_WIDTH, N - cell.y - LINE_WIDTH], 'k-', lw=2)
        if cell.walls[3]:
          plt.plot([cell.x, cell.x], [N - cell.y, N - cell.y - LINE_WIDTH], 'k-', lw=2)
fig = plt.figure(figsize=(10, 10))

draw_maze(maze)

plt.show()