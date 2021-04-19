import pygame
import sys
from random import randint


#Variables used to create grid and visualization
width = 600
height = 600

columns = 50
rows = 50

box_width = width / columns
box_height = height / rows

default_color = (120,120,120)
wall_color = (0, 0, 0)
seen_color = (0, 0, 200)
new_color = (0, 200, 0)
path_color = (200, 0, 200)
start_color = (220, 220, 220)
end_color = (200, 0, 0)

pygame.init()
pygame.display.set_caption("PATHFINDER")
screen = pygame.display.set_mode((width,height))

class node:
    """
    Node class:

    Attributes:
        x - x position
        y - y position
        wall - True if node cannot be used in path
        neighbors - list of nodes that this node neighbors
    Methods:
        add_neighbor:
            Description:
                adds other to self.neighbors and self to other.neighbors
            arguments:
                self
                other - node
            returns:
                None
        distance:
            arguments:
                self
                other - node
            returns:
                distance - Taxi Cab distance between self and other's cordinates
        color:
            Description:
                Colors location on grid with corresponding cordonates
            arguments:
                self
                color - (optional) color in RGB tuple format
            returns:
                None
        switch:
            Description:
                reverses value of self.wall
            arguments:
                self
            returns:
                None
            make_wall:
        remove_wall:
            Description:
                Makes self.wall False
            arguments:
                self
            returns:
                None
        get_available_neighbors:
            arguments:
                self
            returns:
                available_neighbors - all neighbors where self.wall == False (The Neighbors that can be used to create a path)
        
        __repr__
        __hash__
        __eq__
        __gt__
        

    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wall = False
        self.neighbors = []

    def add_neighbor(self, other):
        """
        Description:
            adds other to self.neighbors and self to other.neighbors
        arguments:
            self
            other - node
        returns:
            None
        """
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
        """
        arguments:
            self
            other - node
        returns:
            distance - Taxi Cab distance between self and other's cordinates
        """
        return abs(self.x - other.x) + abs(self.y - other.y)

    def color(self, color = default_color):
        """
        Description:
            Colors location on grid with corresponding cordonates
        arguments:
            self
            color - (optional) color in RGB tuple format
        returns:
            None
        """
        rect = (self.x*box_width, self.y*box_height,box_width, box_height)
        pygame.draw.rect(screen, color, rect)
        pygame.display.update()

    def switch(self):
        """
        Description:
            reverses value of self.wall
        arguments:
            self
        returns:
            None
        """
        self.wall = not self.wall
        if self.wall:
            self.color(wall_color)
        else:
            self.color(default_color)
    def make_wall(self):
        """
        Description:
            Makes self.wall True
        arguments:
            self
        returns:
            None
        """
        self.wall = True
        self.color(wall_color)

    def remove_wall(self):
        """
        Description:
            Makes self.wall False
        arguments:
            self
        returns:
            None
        """
        self.wall = False
        self.color(default_color)
        
    def get_available_neighbors(self):
        """
        arguments:
            self
        returns:
            available_neighbors - all neighbors where self.wall == False (The Neighbors that can be used to create a path)
        """
        available_neighbors = []
        for n in self.neighbors:
            if not n.wall:
                available_neighbors.append(n)
        return available_neighbors
    

def wall(grid, pos, start, end):
    """
    Description:
        Turns node at given postion into a wall if node is not start or end
    arguments:
        grid - grid of nodes used to find path
        pos - tuple with mouse postion
        start - start node
        end - end node
    returns:
        None
    """
    n = grid[int(pos[0]//box_width)][int(pos[1]//box_height)]
    if not n == start and not n == end:
        n.make_wall()

def unwall(grid, pos, start, end):
    """
    Description:
        Turns node at given postion into not a wall if node is not start or end
    arguments:
        grid - grid of nodes used to find path
        pos - tuple with mouse postion
        start - start node
        end - end node
    returns:
        None
    """
    n = grid[int(pos[0]//box_width)][int(pos[1]//box_height)]
    if not n == start and not n == end:
        n.remove_wall()
    
def create_grid(cols = columns, rws = rows):
    """
    arguments:
        cols - number of columns(Defaulted to variable given at beginning of file)
        rws - number of rows(Defaulted to variable given at beginning of file)
    returns:
        grid - grid of nodes used to find path with specified number of rows and columns
               All nodes are neighbors to vertically and horizantally adjacent nodes
    """
    grid = []
    for x in range(cols):
        grid.append([])
        for y in range(rows):
            grid[x].append(node(x,y))
            grid[x][y].color() #Drawing each individual node is slow. If performance is an issue color entire grid at once
            if x>0:
                grid[x][y].add_neighbor(grid[x-1][y])
            if y>0:
                grid[x][y].add_neighbor(grid[x][y-1])
            checkClose()
    return grid

def checkClose():
    """
    Description:
        Closes window if X button is clicked
    arguments:
        none
    returns:
        none
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        

def checkEnd():
    """
    Description:
        Closes window if X button is clicked.
        Reruns main if ENTER key is pressed.
    arguments:
        none
    returns:
        none
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                main()

def readEvents(grid, start, end ):
    """
    Description:
        While loop that runs until space or ENTER is pressed.
        Closes window if X button is clicked.
        
        Reruns main if ENTER key is pressed.
        
    arguments:
        grid - grid of nodes used to find path
        start - start node
        end - end node
    returns:
        none
    """
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
    """
    Description:
        Starts at start node and visualizes dijkstra's algorithm search for end node  
    arguments:
        grid - grid of nodes used to find path
        start - start node
        end - end node
    returns:
        path - list of nodes creating a path from start to end node (if no path exists, none is returned)
    """
    known_pathes = {start:[start]}
    current_neighbors = [start]
    while end not in known_pathes and len(current_neighbors)>0:
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
    """
    arguments:
        node_list - list of nodes
        end - end node
    returns:
        sorted_node_list - list of nodes sorted by distance from end (closest first)
    """
    distances = [n.distance(end) for n in node_list]
    return [n for distance, n in sorted(zip(distances,node_list))]

def min_path(neighbors, known_pathes):
    """
    arguments:
        neighbors - list of nodes
        known_pathes - dict with nodes as keys and known_pathes to those nodes as values
    returns:
        shortest_known_path - shortest path from known_pathes with a neighbor as a key
    """
    path = []
    for n in neighbors:
        if n in known_pathes:
            if path == [] or len(known_pathes[n])<len(path):
                path = known_pathes[n]
    return path.copy()
  
def psuedoAStar(grid, start, end):
    """
    Description:
        Starts at start node and visualizes search (similar to A* but implementation is admittedly wonky) for end node  
    arguments:
        grid - grid of nodes used to find path
        start - start node
        end - end node
    returns:
        path - list of nodes creating a path from start to end node (if no path exists, none is returned)
    """
    known_pathes = {start:[start]}
    current_neighbors = [start]
    
    while end not in known_pathes and len(current_neighbors)>0:
        new_neighbors = []
        for n in current_neighbors[:2]:
            checkClose()
            if n != start:
                n.color(seen_color)
            for k in n.get_available_neighbors():
                if k not in known_pathes:
                    known_pathes[k] = min_path(k.get_available_neighbors(),known_pathes)
                    known_pathes[k].append(k)
                    if k == end:
                        break
                    new_neighbors.append(k)
                    k.color(new_color)
            if k == end:
                        break
        current_neighbors = current_neighbors[2:]+new_neighbors
        current_neighbors = sort_by_dist(current_neighbors, end)
        if k == end:
                        break
        
    if end not in known_pathes:
        return None
    for n in known_pathes[end][1:-1]:
        n.color(path_color)
    return known_pathes[end]

def rand_cords(cols = columns, rws = rows):
    """
    arguments:
        cols - number of columns(Defaulted to variable given at beginning of file)
        rws - number of rows(Defaulted to variable given at beginning of file)
    returns:
        x - random x value 
        y - random y value
    """
    return randint(0,cols-1),randint(0,rws-1)

def main():
    grid = create_grid()
    start_x, start_y = rand_cords()
    end_x, end_y = rand_cords()
    while start_x == end_x or start_y == end_y: #Makes sure that start and end are not in same row or same column
        end_x, end_y = rand_cords()
    grid[start_x][start_y].color(start_color)
    grid[end_x][end_y].color(end_color)
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
    

    
    
