import pygame
from random import randint

width = 600
height = 600

columns = 60
rows = 60

box_width = width / columns
box_height = height / rows

default_color = (120,120,120)
wall_color = (0, 0, 0)
seen_color = (200, 0, 0)
new_color = (0, 200, 00)
path_color = (200, 0, 200)
startEND_color = (220, 220, 220)

screen = pygame.display.set_mode((width,height))

class node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wall = False
        self.neighbors = []

    def add_neighbor(self, other):
        self.neighbors.append(other)
        other.neighbors.append(self)

    def __hash__(self):
        return hash((self.x,self.y))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def color(self, color = default_color):
        rect = (self.x*box_width, self.y*box_height,box_width, box_height)
        pygame.draw.rect(screen, color, rect)
        pygame.display.update()

    def switch(self):
        self.wall = not self.wall
        if self.wall:
            self.color(wall_color)
        else:
            self.color(default_color)

    def get_available_neighbors(self):
        available_neighbors = []
        for n in self.neighbors:
            if not n.wall:
                available_neighbors.append(n)
        return available_neighbors
    


def create_grid(cols = columns, rws = rows):
    grid = []
    for x in range(cols):
        grid.append([])
        for y in range(rows):
            grid[x].append(node(x,y))
            grid[x][y].color()
            if x>0:
                grid[x][y].add_neighbor(grid[x-1][y])
            if y>0:
                grid[x][y].add_neighbor(grid[x][y-1])
    return grid


def dijkstra(grid, start, end):
    known_pathes = {start:[start]}
    current_neighbors = [start]
    new_neighbors = []
    while end not in known_pathes:
        for n in current_neighbors:
            if n != start:
                n.color(seen_color)
            for k in n.get_available_neighbors():
                if k not in known_pathes:
                    known_pathes[k] = known_pathes[n].copy()
                    known_pathes[k].append(k)
                    if k == end:
                        break
                    new_neighbors.append(k)
                    k.color(new_color)
            if k == end:
                        break
        if k == end:
                        break
        current_neighbors = new_neighbors
    for node in known_pathes[end][1:-1]:
        node.color(path_color)
    return known_pathes[end]

def rand_cords(cols = columns, rws = rows):
    return randint(0,cols-1),randint(0,rws-1)
def main():
    grid = create_grid()
    start_x, start_y = rand_cords()
    end_x, end_y = rand_cords()
    while start_x == end_x or start_y == end_y:
        end_x, end_y = rand_cords()

    grid[start_x][start_y].color(startEND_color)
    grid[end_x][end_y].color(startEND_color)
    start = grid[start_x][start_y]
    end = grid[end_x][end_y]
    path = dijkstra(grid, start, end )


main()
    

    
    
