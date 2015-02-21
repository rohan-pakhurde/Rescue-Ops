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
        self.start = self.swat
        self.end = self.enemy
        self.playerAt = self.swat

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
        
##    def display_grid(self):
##        pygame.display.set_caption("Rescue Op Simulation")
##        screen.fill(BLACK)
##        done = False
##        while done == False:
##            for event in pygame.event.get(): 
##                if event.type == pygame.QUIT: 
##                    done = True
##                elif event.type == pygame.MOUSEBUTTONDOWN:
##                    done = True
##                for grid in self.grids:
##                    color = BLACK
##                    if grid.blocked == False:
##                        color = WHITE
##                    #--
##                    if grid.visited == True and grid.blocked == False:
##                        color = BLUE
##                    #--
##                    if grid.path == True:
##                        color = GREEN
##                    #--
##                    if grid == self.enemy:
##                        color = YELLOW
##                    if grid == self.swat:
##                        color = YELLOW
##                    #--
##                    pygame.draw.rect(screen, color,
##                         [(margin+width)*grid.x+margin, (margin+height)*grid.y+margin,
##                          width, height])
####            pygame.draw.circle(screen, RED,
####                [(margin+width)*(self.enemy.x+margin), (margin+height)*(self.enemy.y+margin)],5, 0)
####            pygame.display.flip()
##            for ind in range(4):
##                self.agentAt = self.get_grid(random.randint(1,20), random.randint(1,28))
##                pygame.draw.circle(screen, RED,
##                    [(self.agentAt.x * width)+(self.agentAt.x * margin)+int(width/2)+1,(self.agentAt.y * height)+ (self.agentAt.y * margin)+int(height/2)+1],2, 0)            
##            pygame.display.flip()
####            time.sleep(0.5)
            
    def display_grid(self):
        pygame.display.set_caption("Rescue Op Simulation")
        screen.fill(BLACK)
        done = False
        for count in range(20):
            self.enemyAt = self.get_grid(random.randrange(0,self.grid_width-1,2), random.randrange(0,self.grid_height-1,2))        

            self.swatAt = self.get_grid(random.randrange(0,self.grid_width-1,2), random.randrange(0,self.grid_height-1,2))        

            if (self.enemyAt.x == self.swatAt.x):
                self.enemyAt.path = True
                self.swatAt.path = True
                diff = self.enemyAt.y - self.swatAt.y
                while diff!=0:
                    self.markGrid = self.get_grid(self.swatAt.x , self.swatAt.y+diff)
                    self.markGrid.path = True
                    if diff > 0:
                        diff = diff-1
                    else:
                        diff = diff+1

            if (self.enemyAt.y == self.swatAt.y):
                self.enemyAt.path = True
                self.swatAt.path = True
                diff = self.enemyAt.x - self.swatAt.x
                while diff!=0:
                    self.markGrid = self.get_grid(self.swatAt.x+diff , self.swatAt.y)
                    self.markGrid.path = True
                    if diff > 0:
                        diff = diff-1
                    else:
                        diff = diff+1
            
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
                    grid.path = False
                #--
                if grid == self.enemy:
                    color = YELLOW
                if grid == self.swat:
                    color = YELLOW
                #--
                pygame.draw.rect(screen, color,
                     [(margin+width)*grid.x+margin, (margin+height)*grid.y+margin,
                      width, height])
    ##            pygame.draw.circle(screen, RED,
    ##                [(margin+width)*(self.enemy.x+margin), (margin+height)*(self.enemy.y+margin)],5, 0)
    ##            pygame.display.flip()
            pygame.draw.circle(screen, RED,
                [(self.enemyAt.x * width)+(self.enemyAt.x * margin)+int(width/2)+1,(self.enemyAt.y * height)+ (self.enemyAt.y * margin)+int(height/2)+1],4, 0)

            pygame.draw.circle(screen, RED,
                [(self.swatAt.x * width)+(self.swatAt.x * margin)+int(width/2)+1,(self.swatAt.y * height)+ (self.swatAt.y * margin)+int(height/2)+1],4, 0)
            
            pygame.display.flip()
            time.sleep(2)

def main():
    pygame.init()
    a = Gridworld()
    a.init_grid()
    a.filename = 'Mazes\\'+str(1)+'.txt'
##        a.create_file()
    a.display_grid()
    pygame.quit()
    
if __name__ == '__main__':
    main()
