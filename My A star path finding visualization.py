import pygame
import math
from queue import PriorityQueue

pygame.init()

win_size = 500
screen = pygame.display.set_mode((win_size,win_size))
pygame.display.set_caption("My A Star Path Finding Visualisation")

grey = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
black = (0,0,0)
purple = (128,0,128)
screen.fill(white)

font = pygame.font.Font("freesansbold.ttf",10)
START = font.render("S",True,black,white)
FINISH = font.render("S",True,black,white)
START_RECT = START.get_rect()
FINISH_RECT = FINISH.get_rect()



total_rows = 25
width = win_size // total_rows #width of the single block

class Spot:
    def __init__(self,row,col):
        self.row = row
        self.col = col
        self.neighbors = []
        self.color = white

    def make_barrier(self):
        self.color = black

    def make_start(self):
        self.color = blue

    def make_end(self):
        self.color = yellow
        
    def make_open(self):
        self.color = green

    def make_closed(self):
        self.color = red

    def make_path(self):
        self.color = purple

    def is_barrier(self):
        return self.color == black

    def draw(self):
        pygame.draw.rect(screen,self.color,(self.row*width,self.col*width,width,width))

    def update_neighbors(self,grid):
        self.neighbors = []
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  #LEFT
            self.neighbors.append(grid[self.row][self.col - 1])
        if self.col < total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  #RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.row < total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  #DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  #UP
            self.neighbors.append(grid[self.row - 1][self.col])

    def __lt__(self,other):
        return False
            
    

def make_grid():
    grid = []
    for i in range(total_rows):
        grid.append([])
        for j in range(total_rows):
            spot = Spot(i,j)
            grid[i].append(spot) #for this loop appending for i row

    return grid

def draw_grid():
    for i in range(total_rows):
        pygame.draw.line(screen,grey,(i*width,0),(i*width,win_size))
        for j in range(total_rows):
            pygame.draw.line(screen,grey,(0,j*width),(win_size,j*width))

def draw():
    for row in grid:
        for spot in row:
            spot.draw()

    draw_grid()
    pygame.display.update()

def clicked_pos(pos):
    x,y = pos
    row = x // width
    col = y // width

    return row,col

def heuristic(start,end):
    x1,y1 = start.row, start.col
    x2,y2 = end.row, end.col
    return abs(x1 - x2) + abs(y1 - y2)

def the_path(came_from,current,draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw,grid,start,end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0,count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = heuristic(start, end)

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            the_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor, end)
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start and current!=end:
            current.make_closed()

    return False


    
    
start = None
end = None

grid = make_grid()

running = True
while running:
    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            row,col = clicked_pos(pos)
            spot = grid[row][col]

            if not start and spot!=end:
                start = spot
                start.make_start()

            elif not end and spot!=start:
                end = spot
                end.make_end()

            elif spot!=start and spot!=end:
                barrier = spot 
                barrier.make_barrier()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                start = None
                end = None
                grid = make_grid()
                screen.fill(white)

            if event.key == pygame.K_SPACE and start and end:
                for row in grid:
                    for spot in row:
                        spot.update_neighbors(grid)

                algorithm(lambda: draw(),grid,start,end)

    pygame.display.update()

pygame.quit()
