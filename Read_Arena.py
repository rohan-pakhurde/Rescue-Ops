import heapq, time
import random
import pygame

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = ( 0,   0,   255)
YELLOW   = ( 255, 255, 153)
#--
ORANGE = (255, 165, 0)
 
width  = 25
height = 25
margin = 1
##size = [708, 708]
size = [(21*26)+1, (29*26)+1]
screen = pygame.display.set_mode(size)
 
class Grid(object):
    def __init__(self, x, y, blocked):
        self.blocked = blocked
        self.visited = False
        self.path = False
        self.x = x
        self.y = y
        self.parent = None
        self.next = None
        self.g = 0
        self.h = 0
        self.f = 0
    def __lt__(self, other):
        return self.f < other.f
    
class Gridworld(object):
    def __init__(self):
        self.open = []
        heapq.heapify(self.open)
        self.close = set()
        self.grids = []
        self.grid_height = 29
        self.grid_width = 21
        self.filename = ''

    def init_grid(self):
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                blocked = False
##                if random.randint(1,100) < 30:
##                    blocked = True
                if x%2==1 and y%2==1:
                    blocked = True
                self.grids.append(Grid(x, y, blocked))
##        self.enemy = self.get_grid(random.randint(1,20), random.randint(1,30))
        self.enemy = self.get_grid(0, 0)
        print('enemy at: %d,%d' % (self.enemy.x, self.enemy.y))
##        self.swat = self.get_grid(random.randint(1,20), random.randint(1,30))
        self.swat = self.get_grid(20, 28)
##        self.last_visited = self.enemy
        self.enemy.blocked = False
        self.swat.blocked = False
        self.enemy.path = True
        self.swat.path = True

    def get_grid(self, x, y):
        return self.grids[x * self.grid_height + y]

    def create_file(self):
        opfile = open(self.filename,"w")
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                current_grid = self.get_grid(x, y)
                if current_grid is self.enemy:
                    opfile.write('S')
                elif current_grid is self.swat:
                    opfile.write('G')
                elif current_grid.blocked:
                    opfile.write('b')
                else:
                    opfile.write('~')
            opfile.write('\n')
        opfile.close()

    def read_maze(self, filename):
        x=0
        y=0
        text_file = open(filename, "r")
        txt = text_file.readlines()
        for line in txt:
            y=0
            for chars in line:
##                print('x: %d, y: %d' % (x, y))
                grid = self.get_grid(x,y)
                if str(chars) == '~':
                    grid.blocked = False
                elif str(chars) == 'b':
                    grid.blocked = True
                elif str(chars) == 'S':
                    self.enemy = grid
                    self.enemy.path = True
                elif str(chars) == 'G':
                    self.swat = grid
                    self.swat.path = True
                self.grids.append(grid)
                y = y+1
            x = x+1
        text_file.close()
        
    def display_grid(self):
        pygame.display.set_caption("Rescue Op Simulation")
        screen.fill(BLACK)
        done = False
        while done == False:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    done = True
                for grid in self.grids:
                        color = BLACK
                        if grid.blocked == False:
                            color = WHITE
                        #--
                        if grid.visited == True and grid.blocked == False:
                            color = BLUE
                        #--
                        if grid.path == True:
                            color = GREEN
                        #--
                        if grid == self.enemy:
                            color = YELLOW
                        if grid == self.swat:
                            color = YELLOW
                        #--
                        pygame.draw.rect(screen, color,
                             [(margin+width)*grid.x+margin, (margin+height)*grid.y+margin,
                              width, height])        
            pygame.display.flip()
##            time.sleep(0.5)

def main():
    pygame.init()
##    a = Gridworld()
##    a.init_grid()
##    a.filename = 'Mazes\\'+str(n+1)+'.txt'
##    a.create_file()

    filename = 'Mazes\\'+str(1)+'.txt'
    a = Gridworld()
##    a.init_grid()
    a.read_maze(filename)
    a.display_grid()
    pygame.quit()
    
if __name__ == '__main__':
    main()
