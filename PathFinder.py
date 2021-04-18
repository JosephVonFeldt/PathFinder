import pygame
import sys
from random import randint

width = 600
height = 600

columns = 100
rows = 100

box_width = width / columns
box_height = height / rows

default_color = (120,120,120)
wall_color = (0, 0, 0)
seen_color = (200, 0, 0)
new_color = (0, 200, 00)
path_color = (200, 0, 200)
startEND_color = (220, 220, 220)

pygame.init()
pygame.display.set_caption("PATHFINDER")
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

    def __repr__(self):
        return str((self.x,self.y, self.wall))
    def __hash__(self):
        return hash((self.x,self.y))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __gt__(self, other):
        return (self.x,self.y)>(other.x,other.y)

    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

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
    def make_wall(self):
        self.wall = True
        self.color(wall_color)

    def remove_wall(self):
        self.wall = False
        self.color(default_color)
        
    def get_available_neighbors(self):
        available_neighbors = []
        for n in self.neighbors:
            if not n.wall:
                available_neighbors.append(n)
        return available_neighbors
    

def wall(grid, pos, start, end):
    n = grid[int(pos[0]//box_width)][int(pos[1]//box_height)]
    if not n == start and not n == end:
        n.make_wall()

def unwall(grid, pos, start, end):
    n = grid[int(pos[0]//box_width)][int(pos[1]//box_height)]
    if not n == start and not n == end:
        n.remove_wall()
    
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
            checkClose()
    return grid

def checkClose():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        

def checkEnd():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                main()

def readEvents(grid, start, end ):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    wall(grid,pygame.mouse.get_pos(),start,end)
                if event.button == 2:
                    unwall(grid,pygame.mouse.get_pos(),start,end)
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0]:
                wall(grid,pygame.mouse.get_pos(),start,end)
            if mouse_buttons[2]:
                unwall(grid,pygame.mouse.get_pos(),start,end)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return None
                if event.key == pygame.K_SPACE:
                    return "DJ"

            
def dijkstra(grid, start, end):
    known_pathes = {start:[start]}
    current_neighbors = [start]
    while end not in known_pathes:
        new_neighbors = []
        for n in current_neighbors:
            checkClose()
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
    if end not in known_pathes:
        return None
    for n in known_pathes[end][1:-1]:
        n.color(path_color)
    return known_pathes[end]

def sort_by_dist(node_list, end):
    distances = [n.distance(end) for n in node_list]
    return [n for distance, n in sorted(zip(distances,node_list))]
    
def psuedoAStar(grid, start, end):
    known_pathes = {start:[start]}
    current_neighbors = [start]
    
    while end not in known_pathes:
        new_neighbors = []
        for n in current_neighbors[:4]:
            checkClose()
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
        current_neighbors = current_neighbors[4:]+new_neighbors
        current_neighbors = sort_by_dist(current_neighbors, end)
        if k == end:
                        break
        
    if end not in known_pathes:
        return None
    for n in known_pathes[end][1:-1]:
        n.color(path_color)
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
    alg = readEvents(grid, start, end)
    if alg == "DJ":
        path = dijkstra(grid, start, end )
    else:
        path = psuedoAStar(grid,start,end)
    while True:
        checkEnd()
        
main()
    

    
    
