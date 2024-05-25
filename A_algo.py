# in any pathfinding algo we have edes and nodes
# nodes -> point (eg: vertex of a triangle)
# edges -> sides or the paths (eg: sides of the triangle)

# weighted edge : it means the the edges which contain shortest path other than others
# un-weighted edge: it also contains the path but the path is not optimal
#
# it is also a brute force algo which check each possible path
# This algo contain hurestic function which guide us reaching our optimal path
# -> In this we only consider the path which we contain optimal path
# -> In this most of the data is considered in a priority queue
#
# -> we use manhattendistance formula
# --->  F(n) = G(n)+H(n)
# F(n) is it give some rough estimate how much distance we are behind the destination
# G(n) is current shortest distance from start node to current node
# H(n) is Heuristic function
#
# --> if any node has lower F(n) then it has shortest path than other we priotised that particular node
# --> the prioritized of any node is particularly depends up on the F(n)

import pygame as pg
from queue import PriorityQueue

width = 800
win = pg.display.set_mode((width,width))    # It is generally buliding a window of given size
pg.display.set_caption("shaik's Visualization")


white = (255,255,255)
red = (255,0,0)
green = (0,0,255)
blue = (0,255,0)
yellow = (255,255,0)
black = (0,0,0)
purple = (128,0,128)
orange = (255,165,0)
grey = (128,128,128)
turquoise = (64,224,208)

class Spot:                 # to keep track of the color (eg: black spot means a barrier)
    def __init__(self,row,col, width,total_rows):
        self.row = row
        self.col = col
        self.x = row * width        # to know the spot current position
        self.y = col * width
        self.color = white          # initially they are in white color
        self.neighbours = []        # to know the spot neighbours
        self.width = width
        self.total_rows = total_rows
    def get_position(self):           # getting the position of the spot
        return self.row, self.col
    def is_closed(self):            # it tells us have we looked at the spot
        return self.color == red    # it will return return red if we already visited it
    def is_open(self):
        return self.color == green
    def is_barrier(self):
        return self.color == black
    def is_start(self):
        return self.color == orange
    def is_end(self):
        return self.color == turquoise
    def reset(self):
        self.color = white
    def get_width(self,width):
        return width
    def make_start(self):
        self.color = orange
    def make_closed(self):           # we are making or set the color for different functionality
        self.color = red
    def make_open(self):
        self.color = green
    def make_barrier(self):
        self.color = black
    def make_end(self):
        self.color = turquoise
    def make_path(self):
        self.color = purple
    def draw(self,win):             # it is an individual spot position (eg: if spot at 16x17 pos we can't define a square because sizes are different)
        pg.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))
    def update_neighbours(self,grid):
        self.neighbours = []
        if self.row < self.total_rows-1 and not grid[self.row+1][self.col].is_barrier():    # here we are going down the rows and check whether the down row is an barrier or not
            self.neighbours.append(grid[self.row+1][self.col])

        if self.row > 0 and not grid[self.row-1][self.col].is_barrier():
            self.neighbours.append(grid[self.row-1][self.col])

        if self.col < self.total_rows-1 and not grid[self.row][self.col+1].is_barrier():    # right
            self.neighbours.append(grid[self.row][self.col+1])

        if self.col > 0 and not grid[self.row][self.col-1].is_barrier():                    # here we are check whetehr my spot is at row which is greater than zero and the right spot is a barrier or not
            self.neighbours.append(grid[self.row][self.col-1])

    def __it__(self,other):
        return False


def h(p1,p2):       # we are estimating the distance from end point using manhatten distance or taxi cab dist( because dist measured in a straight line)
    x1,y1 = p1
    x2,y2 = p2
    return abs(x1-x2)+abs(y1-y2)

def shortest_path(came_from,current,draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid,start,end):       # here the lambda fxn is defined in a variable draw and we are accessing our lamda function using that draw method
    count = 0
    open_set = PriorityQueue()
    open_set.put((0,count, start))          # our first step of algorithm is to add f(n) of start node                                       # the count is responsable for keeping track of which inserted first (we can break ties using this count) and start is the start spot
    came_from = {}                          # generally it holds the previous node its came from
    g_score = {spot: float("inf") for row in grid for spot in row}      # at start we dont know the distance that's why we are putting inf
    g_score[start] = 0              # the g(n) is zero
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_position(), end.get_position())        # we want make an estimate how far our start node is from the desti and h is an heuristic mehtod

    open_set_hash = {start}             # we need to check whether the value in the priority queue or not
    while not open_set.empty():         # it is my open_set is not empty it means a we are traversing a node and a path exist ( if a open_set is empty then our path is not exist)
        for event in pg.event.get():
            if event.type == pg.QUIT:   # hit x button to quit
                pg.quit()
        current = open_set.get()[2]     # the indexing at 2 because i just want node form the open_set
        open_set_hash.remove(current)

        if current == end:          # if the removed value is the end the we found the path

            return True
        for neighbour in current.neighbours:
            temp_g_score = g_score[current]+1           # here in the grid the distance between neighbours is 1 and the neighrbour of current is at 1 dista
                                                        # so we are adding 1 to the current ( this is the distance of the neighbour)
            if temp_g_score < g_score[neighbour]:       # if we found a better path than g[neigbour] then update the g_score
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_position(),end.get_position())        # F(n) = G(n)+h(n)
                if neighbour not in open_set_hash:
                    count+=1
                    open_set.put((f_score[neighbour],count,neighbour))      # we are considering this neighbour because it has better path and we are updating our open_set
                    open_set_hash.add(neighbour)
                    neighbour.make_open()
        draw()
        if current != start:        # if current is not the start the node then close it
            shortest_path(came_from,end,draw)
            end.make_end()
            current.make_closed()
    return False



def make_grid(rows, width):     # this method will make individual grid
                                # how many rows we want in which width
    grid = []
    gap = width // rows         # it tells what is the width of the each of the cubes will be
    for i in range(rows):
        grid.append([])         # we are creating a grid which hold spot color and all other data in a list
        for j in range(rows):
            spot = Spot(i,j,gap,rows)
            grid[i].append(spot)
    print(grid)
    return grid

def draw_grid(win,rows,width):       # it draws grid from the grid list above method
    gap = width // rows
    for i in range(rows):
        pg.draw.line(win,grey,(0,i * gap),(width,i*gap))        # it will draw a line after rows and their gaps
        for j in range(rows):
            pg.draw.line(win,grey,(j*gap,0),(j*gap,width))             # we are drawing vertical lines after certain gap

def draw(win,grid,rows,width):
    win.fill(white)
    for row in grid:
        for spot in row:
            spot.draw(win)                  # we are calling method to fill all spot with some color
    draw_grid(win,rows,width)
    pg.display.update()                 # take whatever draw and update the screen

def get_clicked_position(pos,rows,width):       # it will return on which spot we are clicked
    gap = width // rows
    y , x = pos
    row = y // gap                       # it will exact location row which row we clicked by remove the gap between the rows
    col = x // gap
    return row,col

def main(win,width):
    rows = 50       # this is our main function in which all the previous are integrated
    grid = make_grid(rows,width)

    start = None
    end = None
    run = True                      # here i am declaring some variable to keep the track of the main function which it is running or started etc
    started = False
    while run:
        draw(win,grid,rows,width)
        for event in pg.event.get():        # it is going through all the event(such as clicking, spot responding etc)
            if event.type == pg.QUIT:       # it will stop running if we clikc the 'q' button
                run = False
            if started:                     # after starting of the algorithm the user clicked anything thing such are make some barriers etc
                continue
            if pg.mouse.get_pressed()[0]:   # by clicking on the left mouse button it will execute
                pos = pg.mouse.get_pos()    # gives us the position of the mouse function
                row, col = get_clicked_position(pos,rows,width)         # it will return at what actuall spot we clicke on
                spot = grid[row][col]       # we can index the row and col
                if not start and spot!=end:         # if we don't have a start spot whenever we clikc the mouse it will considered as a start pos and start and end pos should be different
                    start = spot
                    start.make_start()      # if will give the start spot of color orage
                elif not end and spot!=start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()
            elif pg.mouse.get_pressed()[2]:  # by clicking on the right mouse button it will execute
                pos = pg.mouse.get_pos()
                row, col = get_clicked_position(pos, rows, width)
                spot = grid[row][col]
                spot.reset()            # this condition is generally used to remove barriers or reseting the barriers
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
            if event.type == pg.KEYDOWN:         # whenever we press the keyboard key
                if event.key == pg.K_SPACE and not started:    # the key is space key and my algorithm is not started yet

                    for row in grid:            # a row in grid
                        for x in row:        # our spot in the row
                            x.update_neighbours(grid)     # update all the neighbours
                                                    ## when ever we press space key check the spot and update all the neighbours
                    algorithm(lambda: draw(win,grid,rows,width),grid,start,end)


    pg.quit()
main(win,width)
