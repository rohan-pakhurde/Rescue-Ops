import heapq, time
import random
import pygame

x = 50
y = 50
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

##import easygui
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)
BLUE     = ( 0,   0,   255)
YELLOW   = ( 255, 255, 153)
ORANGE   = ( 255, 165, 0)

# Agent Strength Levels
MIN_STRENGTH = 0
MAX_STRENGTH = 100
MAX_STRENGH_DIFF = (MAX_STRENGTH - MIN_STRENGTH)

NUM_ENEMY = 3
NUM_SWAT = 3
NUM_HOSTAGE = 5

TRUE = 1
FALSE = 0

SHOT = 1
NOTSHOT = 0

# Duel Matrix - duelMatrix[i][j] = 1 means that Swat[i] is duelling with Enemy[j];
# 0 => no duel between those two
# Row i gives all Enemies that Swat[i] is duelling with
# Col i gives all Swats that Enemy[i] is duelling with
duelMatrix = [[0 for x in range(NUM_SWAT)] for x in range(NUM_ENEMY)]

AGENT_ENEMY = 2
AGENT_SWAT = 1

# Note: x is along width, y is along height
CELL_WIDTH = 25
CELL_HEIGHT = 25
MAX_HEIGHT = 21
MAX_WIDTH = 21
margin = 1
##size = [708, 708]
size = [(MAX_WIDTH*(CELL_WIDTH+1))+1+350, (MAX_HEIGHT*(CELL_HEIGHT+1))+1]
screen = pygame.display.set_mode(size)

class Grid_Cell(object):
    def __init__(self, x, y, blocked):
        self.blocked = blocked
        self.path = False
        self.x = x
        self.y = y
        self.next = None
        self.g = 0
        self.f = 0
        self.agenttype = None
        self.agentid = -1
        #self.strength = 0
    def __lt__(self, other):
        return self.f < other.f

class Agent(object):
    def __init__(self, agent_id, agent_type, xOffset, yOffset):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.moveTo = []
        self.message = ''
        #Defining strength levels
        if 1 == agent_id:
            self.strength = 10
        elif 2 == agent_id:
            self.strength = 50
        elif 3 == agent_id:
            self.strength = 70
    
class Gridworld(object):
    def __init__(self):
        self.gameOn = False
        
        self.open = []
        heapq.heapify(self.open)
        self.close = set()
        self.grids = []
        self.grid_height = MAX_HEIGHT
        self.grid_width = MAX_WIDTH
        self.font = pygame.font.SysFont('Arial', 14)
        
        self.swatAgents = []
        self.swatPos = []
        self.swatLastVisited = []
        
        self.enemyAgents = []
        self.enemyPos = []
        self.enemyLastVisited = []
        
        self.hostagePos = []
        self.rescue_hostage = []
        
        self.messages = []
        ##Lists of duelling agent objects. duellingSwatList[i] duels with duellingEnemyList[i]
        self.duellingSwatList = []
        self.duellingEnemyList = []
        # self.killed = FALSE

        pygame.display.set_caption("Rescue Op Simulation")
        self.font1 = pygame.font.SysFont('Arial', 9)

    def init_grid(self):
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                blocked = False
                if x%2==1 and y%2==1:
                    blocked = True
                self.grids.append(Grid_Cell(x, y, blocked))
##        self.ENEMY_START_POS = self.get_grid(random.randint(1,20), random.randint(1,30))
        self.ENEMY_START_POS = self.get_gridCell(0, 0)
        """
        self.ENEMY_START_POS0 = self.get_gridCell(0, 0)
        self.ENEMY_START_POS1 = self.get_gridCell(0, 0)
        self.ENEMY_START_POS2 = self.get_gridCell(0, 0)
        self.ENEMY_START_POS0.agenttype = AGENT_ENEMY
        self.ENEMY_START_POS1.agenttype = AGENT_ENEMY
        self.ENEMY_START_POS2.agenttype = AGENT_ENEMY
        self.ENEMY_START_POS0.agentid = 0
        self.ENEMY_START_POS1.agentid = 1
        self.ENEMY_START_POS2.agentid = 2
        self.ENEMY_START_POS0.strength = 10
        self.ENEMY_START_POS1.strength = 50
        self.ENEMY_START_POS2.strength = 70
        """
##        print('enemy at: %d,%d' % (self.ENEMY_START_POS.x, self.ENEMY_START_POS.y))
##        self.SWAT_START_POS = self.get_grid(random.randint(1,20), random.randint(1,30))
        self.SWAT_START_POS = self.get_gridCell(self.grid_width-1, self.grid_height-1)

        self.swatAgents = [Agent(1,1,int(CELL_WIDTH/4),int(CELL_HEIGHT/4)),
                           Agent(2,1,3*int(CELL_WIDTH/4),int(CELL_HEIGHT/4)),
                           Agent(3,1,int(CELL_WIDTH/4),3*int(CELL_HEIGHT/4))]
        self.swatPos = [self.SWAT_START_POS, self.SWAT_START_POS, self.SWAT_START_POS]
        """
        self.SWAT_START_POS0 = self.get_gridCell(MAX_WIDTH - 1, MAX_HEIGHT - 1)
        self.SWAT_START_POS1 = self.get_gridCell(MAX_WIDTH - 1, MAX_HEIGHT - 1)
        self.SWAT_START_POS2 = self.get_gridCell(MAX_WIDTH - 1, MAX_HEIGHT - 1)
        self.SWAT_START_POS0.agenttype = AGENT_SWAT
        self.SWAT_START_POS1.agenttype = AGENT_SWAT
        self.SWAT_START_POS2.agenttype = AGENT_SWAT
        self.SWAT_START_POS0.agentid = 0
        self.SWAT_START_POS1.agentid = 1
        self.SWAT_START_POS2.agentid = 2
        self.SWAT_START_POS0.strength = 10
        self.SWAT_START_POS1.strength = 50
        self.SWAT_START_POS2.strength = 70
        """
        
        self.enemyAgents = [Agent(1, AGENT_ENEMY, 0 * int(CELL_WIDTH / 4) + 1, 0 * int(CELL_HEIGHT / 4) + 1),
                            Agent(2, AGENT_ENEMY, 2 * int(CELL_WIDTH / 4) + 1, 0 * int(CELL_HEIGHT / 4) + 1),
                            Agent(3, AGENT_ENEMY, 0 * int(CELL_WIDTH / 4) + 1, 2 * int(CELL_HEIGHT / 4) + 1)]
        self.enemyPos = [self.ENEMY_START_POS, self.ENEMY_START_POS, self.ENEMY_START_POS]

        for hst_ind in range(5):
            self.hostagePos.append(self.get_gridCell(random.randrange(1,self.grid_width-1,2), random.randrange(1,(self.grid_height-1)/2,2)))
            self.rescue_hostage.append(None)

        self.swatLastVisited = [None, None, None]
        self.enemyLastVisited = [None, None, None]

    def get_gridCell(self, x, y):
        return self.grids[x * self.grid_height + y]

    def distBetween(self, pos1, pos2):
        Xdiff = pos1.x-pos2.x
        Ydiff = pos1.y-pos2.y
        return abs(Xdiff)+abs(Ydiff)

    def expand_gridCell(self, grid):
        grids = []
        if grid.x < self.grid_width-1:
            grids.append(self.get_gridCell(grid.x+1, grid.y))
        if grid.y > 0:
            grids.append(self.get_gridCell(grid.x, grid.y-1))
        if grid.x > 0:
            grids.append(self.get_gridCell(grid.x-1, grid.y))
        if grid.y < self.grid_height-1:
            grids.append(self.get_gridCell(grid.x, grid.y+1))
        return grids

    def display_path(self, start, end):
        grid = end
        while grid.next is not start:
            grid = grid.next
            self.get_gridCell(grid.x, grid.y).path = True
##            grid.path = True
##            print('path: grid: %d,%d' % (grid.x, grid.y))

    def update_gridCell(self, exp, grid, end):
        exp.g = grid.g + 1
##        exp.h = self.distBetween(exp, end)
        exp.next = grid
        exp.f = exp.g + self.distBetween(exp, end)

    def generate_Path(self, start, end):
        end.blocked = False
        self.open = []
        self.close = set()
##        print('from: grid: %d,%d to grid: %d,%d' % (start.x, start.y, end.x, end.y))
        heapq.heappush(self.open, (start.f, start))
        while len(self.open):
            f, grid = heapq.heappop(self.open)
            self.close.add(grid)
            if grid is end:
                self.display_path(start, end)
                break
            exp_grids = self.expand_gridCell(grid)
            for exp_grid in exp_grids:
                if not exp_grid.blocked and exp_grid not in self.close:
                    if (exp_grid.f, exp_grid) in self.open:
                        if exp_grid.g > grid.g + 10:
                            self.update_gridCell(exp_grid, grid, end)
                    else:
                        self.update_gridCell(exp_grid, grid, end)
                        heapq.heappush(self.open, (exp_grid.f, exp_grid))
        end.blocked = True

    def pathCorrection(self, start, end):
        grid = end
        prevCell = None
        currCell = None
        nextCell = None

        currCell = grid
        nextCell = currCell.next
        currCell.next = prevCell
        prevCell = currCell
        grid = nextCell

        currCell = grid
        nextCell = currCell.next
        currCell.next = None
        prevCell = currCell
        grid = nextCell
        
        while grid is not None:
            currCell = grid
            nextCell = currCell.next
            currCell.next = prevCell
            prevCell = currCell
            grid = nextCell

    def assignPath(self, start, end, ind, agentType):
        grid = end
        currCell = None
        nextCell = None
        
        while grid is not start:
            currCell = grid
            nextCell = currCell.next
            currCell.next = None
            if agentType == AGENT_SWAT:
                self.swatAgents[ind].moveTo.insert(0,nextCell)
            else:
                self.enemyAgents[ind].moveTo.insert(0,nextCell)
            grid = nextCell

        start.next = None

    def orderHostages(self, mode, ind):
        if (mode==2):
            hostage_dist = []
            for hostage_ind in range(len(self.hostagePos)):
                if(self.hostagePos[hostage_ind] != None):
                    hostage_dist.append(self.distBetween(self.hostagePos[hostage_ind],self.swatPos[ind]))
                else:
                    hostage_dist.append(9999)
                                        
            for hostage_ind in range(len(self.hostagePos)):
                choose_ind = hostage_dist.index(min(hostage_dist))
                temp = self.hostagePos[hostage_ind]
                self.hostagePos[hostage_ind] = self.hostagePos[choose_ind]
                self.hostagePos[choose_ind] = temp
                hostage_dist[hostage_ind] = 9999

    def assign_HostagetoRescue(self, mode, ind):
        hostage_dist = []
        if (self.swatPos.count(self.swatPos[0]) == len(self.swatPos)):
            self.orderHostages(mode, ind)
            return

        if (self.hostagePos[ind] == None):
            for hostage_ind in range(len(self.hostagePos)):
                if(self.hostagePos[hostage_ind] != None and self.swatPos[ind]!=None):
                    hostage_dist.append(self.distBetween(self.hostagePos[hostage_ind],self.swatPos[ind]))
                else:
                    hostage_dist.append(9999)
            choose_ind = hostage_dist.index(min(hostage_dist))
            self.rescue_hostage[ind] = self.hostagePos[choose_ind]
            self.hostagePos[ind] = self.hostagePos[choose_ind]
            self.hostagePos[choose_ind] = None

    def nextMove(self, agentType, agentAt, hostageAt, ind, mode):
##        if (swatAt.next == None) :
##            self.generate_Path(swatAt, hostageAt)
##            self.pathCorrection(swatAt, hostageAt)
##        nextCell = swatAt.next
##        swatAt.next = None

        if agentType == AGENT_SWAT:
            if (len(self.swatAgents[ind].moveTo) == 0):
                self.generate_Path(agentAt, hostageAt)
                self.assignPath(agentAt, hostageAt, ind, agentType)
            
            nextCell = self.swatAgents[ind].moveTo[0]
            del self.swatAgents[ind].moveTo[0]
        else:
            if (len(self.enemyAgents[ind].moveTo) == 0):
                self.generate_Path(agentAt, hostageAt)
                self.assignPath(agentAt, hostageAt, ind, agentType)
            
            nextCell = self.enemyAgents[ind].moveTo[0]
            del self.enemyAgents[ind].moveTo[0]
        return nextCell
        
    def take_action(self, agentType, mode, x, y, ind):

        if agentType == AGENT_SWAT:
            rescued = False
            for hst_ind in range(len(self.hostagePos)):
                if (x-1 >= 0 and self.hostagePos[hst_ind] == self.get_gridCell(x-1,y) or
                    y-1 >= 0 and self.hostagePos[hst_ind] == self.get_gridCell(x,y-1) or
                    x+1 <= self.grid_width-1 and self.hostagePos[hst_ind] == self.get_gridCell(x+1,y) or
                    y+1 <= self.grid_height-1 and self.hostagePos[hst_ind] == self.get_gridCell(x,y+1)):
                    ##self.hostagePos.remove(self.hostagePos[hst_ind])
                    self.swatAgents[ind].message += 'S%d : AT: < %d , %d > -- HostageAt < %d , %d >' % (ind,x,y,self.hostagePos[hst_ind].x,self.hostagePos[hst_ind].y)
                    self.hostagePos[hst_ind] = None
                    ##self.swatPos[hst_ind].next = None
                    rescued = True
                    if rescued :
                        if (self.hostagePos.count(None) == len(self.hostagePos)):
                            self.gameEnd('SWAT WINS !!!')
                        return self.get_gridCell(x,y)
        if mode == 1:
            choice = random.randint(1,100)
            if choice <= 25:
                if (x-1 < 0):
                    cell = self.get_gridCell(x,y)
                else:
                    cell = self.get_gridCell(x-1,y)
            elif choice <= 50:
                if (y-1 < 0):
                    cell = self.get_gridCell(x,y)
                else:
                    cell = self.get_gridCell(x,y-1)
            elif choice <= 75:
                if (x+1 > self.grid_width-1):
                    cell = self.get_gridCell(x,y)
                else:
                    cell = self.get_gridCell(x+1,y)
            else:
                if (y+1 > self.grid_height-1):
                    cell = self.get_gridCell(x,y)
                else:
                    cell = self.get_gridCell(x,y+1)
            if cell.blocked == True or cell == self.get_gridCell(x,y):
                cell =  self.take_action(agentType, mode, x, y, ind)
                
            if agentType == AGENT_SWAT:
                if(self.swatLastVisited[ind] == cell):
                    cell = self.take_action(agentType, mode, x, yf, ind)
                self.swatLastVisited[ind] = self.get_gridCell(x,y)
            else:
                if(self.enemyLastVisited[ind] == cell):
                    cell = self.take_action(agentType, mode, x, y, ind)
                self.enemyLastVisited[ind] = self.get_gridCell(x,y)
        
        elif mode == 2:
            ##if (self.swatPos[ind].next == None):
            ##if (self.hostagePos[ind] == None):
            self.assign_HostagetoRescue(mode,ind)
            ##cell = self.get_gridCell(x,y)
            ##return cell
            if agentType == AGENT_SWAT:
                cell = self.nextMove(agentType, self.swatPos[ind], self.hostagePos[ind], ind, mode)
                #self.swatAgents[ind].message
            else:
                cell = self.nextMove(agentType, self.enemyPos[ind], self.hostagePos[ind], ind, mode)
        if agentType == AGENT_SWAT:
            self.swatAgents[ind].message += 'S%d : AT: < %d , %d >' % (ind,cell.x,cell.y)
        else:
            self.enemyAgents[ind].message += 'T%d : AT: < %d , %d >' % (ind,cell.x,cell.y)
        return cell

    def update_agentPos(self):
        for swat_ind in range(len(self.swatPos)):
            if self.swatPos[swat_ind]!=None:
                self.swatPos[swat_ind] = self.take_action(self.swatAgents[swat_ind].agent_type, 2, self.swatPos[swat_ind].x, self.swatPos[swat_ind].y, swat_ind)
                ##self.generate_Path(self.swatPos[swat_ind],self.hostagePos[swat_ind])

        for enemy_ind in range(len(self.enemyPos)):
            if self.enemyPos[enemy_ind]!=None:
                self.enemyPos[enemy_ind] = self.take_action(self.enemyAgents[enemy_ind].agent_type, 2, self.enemyPos[enemy_ind].x, self.enemyPos[enemy_ind].y, enemy_ind)

    def check_LOS(self):
        #Recycle duelMatrix
        for i in range(NUM_SWAT):
            for j in range(NUM_ENEMY):
                duelMatrix[i][j] = 0

        from collections import defaultdict
        VertLOSSwatDict     = defaultdict(list) # Uses x as the key. Holds list of swats in a col.
        VertLOSEnemyDict    = defaultdict(list) # Uses x as the key. Holds list of enemies in a col.
        HoriLOSSwatDict     = defaultdict(list) # Uses y as the key. Holds list of swats in a row.
        HoriLOSEnemyDict    = defaultdict(list) # Uses y as the key. Holds list of enemies in a row.
        RowDuelDict         = defaultdict(list)
        ColDuelDict         = defaultdict(list)
        #xLOSList = []
        #xSwatList = [[0 for x in range(NUM_SWAT)] for x in range(NUM_SWAT)]

        for swatindex, swat in enumerate(self.swatPos):
            #xSwatList[swatindex].append(swatindex)
            if swat != None:
                VertLOSSwatDict[swat.x].append(swatindex)
                HoriLOSSwatDict[swat.y].append(swatindex)

        for enemyindex, enemy in enumerate(self.enemyPos):
            if enemy != None:
                VertLOSEnemyDict[enemy.x].append(enemyindex)
                HoriLOSEnemyDict[enemy.y].append(enemyindex)

        for x in VertLOSSwatDict.keys():
            if x in VertLOSEnemyDict.keys():
            #if VertLOSEnemyDict.has_key(): #Removed in Python 3.x
                # Swats and enemies found in same column. Build a list.
                for swatindex in VertLOSSwatDict[x]:
                    self.swatPos[swatindex].agenttype = AGENT_SWAT
                    self.swatPos[swatindex].agentid = swatindex
                    ColDuelDict[x].append(self.swatPos[swatindex])
                for enemyindex in VertLOSEnemyDict[x]:
                    self.enemyPos[enemyindex].agenttype = AGENT_ENEMY
                    self.enemyPos[enemyindex].agentid = enemyindex
                    ColDuelDict[x].append(self.enemyPos[enemyindex])

        for y in HoriLOSSwatDict.keys():
            if y in HoriLOSEnemyDict.keys():
                # Swats and enemies found in same row. Build a list.
                for swatindex in HoriLOSSwatDict[y]:
                    self.swatPos[swatindex].agenttype = AGENT_SWAT
                    self.swatPos[swatindex].agentid = swatindex
                    RowDuelDict[y].append(self.swatPos[swatindex])
                for enemyindex in HoriLOSEnemyDict[y]:
                    self.enemyPos[enemyindex].agenttype = AGENT_ENEMY
                    self.enemyPos[enemyindex].agentid = enemyindex
                    RowDuelDict[y].append(self.enemyPos[enemyindex])

        # Got row/column-wise lists of dueling agents
        for tempColList in ColDuelDict.values():
            #tempColList = ColDuelDict[index]
            tempColList.sort(key = lambda tempIter: tempIter.y)
            for tempColListIndex in range(len(tempColList) - 1):
                #if tempColList[tempColListIndex].y == tempColList[tempColListIndex+1].y:
                    #Agents in same cell case
                    #duelMatrixVal = 1000
                #else:
                duelMatrixVal = 1
                if tempColList[tempColListIndex].agenttype == AGENT_SWAT and \
                   tempColList[tempColListIndex+1].agenttype == AGENT_ENEMY:
                    duelMatrix[tempColList[tempColListIndex].agentid][tempColList[tempColListIndex+1].agentid] \
                        = duelMatrixVal
                elif tempColList[tempColListIndex].agenttype == AGENT_ENEMY and \
                     tempColList[tempColListIndex+1].agenttype == AGENT_SWAT:
                    duelMatrix[tempColList[tempColListIndex+1].agentid][tempColList[tempColListIndex].agentid] \
                        = duelMatrixVal

        for tempRowList in RowDuelDict.values():
            #tempRowList = RowDuelDict[index]
            tempRowList.sort(key = lambda tempIter: tempIter.x)
            for tempRowListIndex in range(len(tempRowList) - 1):
                #if tempRowList[tempRowListIndex].x == tempRowList[tempRowListIndex+1].x:
                    #Agents in same cell case
                    #duelMatrixVal = 1000
                #else:
                duelMatrixVal = 1
                if tempRowList[tempRowListIndex].agenttype == AGENT_SWAT and \
                   tempRowList[tempRowListIndex+1].agenttype == AGENT_ENEMY:
                    duelMatrix[tempRowList[tempRowListIndex].agentid][tempRowList[tempRowListIndex+1].agentid] \
                        = duelMatrixVal
                elif tempRowList[tempRowListIndex].agenttype == AGENT_ENEMY and \
                     tempRowList[tempRowListIndex+1].agenttype == AGENT_SWAT:
                    duelMatrix[tempRowList[tempRowListIndex+1].agentid][tempRowList[tempRowListIndex].agentid] \
                        = duelMatrixVal

        #Same cell post processing

        #1. Among swats themselves - those in same cell must have same LOS
        for swatindex, swat in enumerate(self.swatPos):
            if self.swatPos[swatindex].x == self.swatPos[(swatindex+1)%NUM_SWAT].x and \
               self.swatPos[swatindex].y == self.swatPos[(swatindex+1)%NUM_SWAT].y:
                #Two swats in the same cell - equate their LOS
                for enemyindex in range(NUM_ENEMY):
                    if duelMatrix[swatindex][enemyindex] == 1 or duelMatrix[(swatindex+1)%NUM_SWAT][enemyindex] == 1:
                        duelMatrix[swatindex][enemyindex] = duelMatrix[(swatindex+1)%NUM_SWAT][enemyindex] = 1

        #2. Among enemies themselves - those in same cell must have same LOS
        for enemyindex, enemy in enumerate(self.enemyPos):
            if self.enemyPos[enemyindex].x == self.enemyPos[(enemyindex+1)%NUM_ENEMY].x and \
               self.enemyPos[enemyindex].y == self.enemyPos[(enemyindex+1)%NUM_ENEMY].y:
                #Two enemies in the same cell - equate their LOS
                for swatindex in range(NUM_SWAT):
                    if duelMatrix[swatindex][enemyindex] == 1 or duelMatrix[swatindex][(enemyindex+1)%NUM_ENEMY] == 1:
                        duelMatrix[swatindex][enemyindex] = duelMatrix[swatindex][(enemyindex+1)%NUM_ENEMY] = 1

        #3. Between swats and enemies - should be done after above two cases as 1000 can overwrite 1 but not vice versa
        for swatindex, swat in enumerate(self.swatPos):
            for enemyindex, enemy in enumerate(self.enemyPos):
                if swat.x == enemy.x and swat.y == enemy.y:
                    duelMatrix[swatindex][enemyindex] = 1 #1000

    def duel(self):
        for swatindex in range(NUM_SWAT):
            for enemyindex in range(NUM_ENEMY):
                 if duelMatrix[swatindex][enemyindex] == 1:
                     self.shoot(swatindex, enemyindex)

    def shoot(self, swatindex, enemyindex):
        rand_num = random.randint(1, 100)
        if rand_num <= self.swatAgents[swatindex].strength:
            self.enemyPos[enemyindex] = None

        rand_num = random.randint(1, 100)
        if rand_num <= self.enemyAgents[enemyindex].strength:
            self.swatPos[swatindex] = None


    def gameStart(self):
        monitor = True
        while monitor == True:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    monitor = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.gameOn = True
                    monitor = False

    def gameEnd(self,msg):
        print ('In game end')
        monitor = True
        self.font = pygame.font.SysFont('Arial', 30)
        pygame.draw.rect(screen, YELLOW,
                         [abs(((MAX_WIDTH*(CELL_WIDTH+1))+1)/4),
                          abs(((MAX_HEIGHT*(CELL_HEIGHT+1))+1)/4),
                          300, 100])
##        screen.blit(self.font.size(400,200))
        screen.blit(self.font.render(msg, True, RED, YELLOW),
                    (((MAX_WIDTH*(CELL_WIDTH+1))+1)/3,
                    ((MAX_HEIGHT*(CELL_HEIGHT+1))+1)/3))
        pygame.display.flip()
        time.sleep(1)
        while monitor == True:
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.gameOn = False
                    monitor = False
                    pygame.quit()
            
    def display_grid(self):
        #font = pygame.font.SysFont('Arial', 8)
        #pygame.display.set_caption("Rescue Op Simulation")
        screen.fill(BLACK)
        done = False
        for count in range(100):
####            Display GridWorld
            screen.fill(BLACK)
            for grid in self.grids:
                color = BLACK
                if grid.blocked == False:
                    color = WHITE
                #--
                if grid.path == True:
                    color = GREEN
                    grid.path = False
                #--
                if grid == self.ENEMY_START_POS:
                    color = YELLOW
                if grid == self.SWAT_START_POS:
                    color = YELLOW
                #--
                pygame.draw.rect(screen, color,
                     [(margin+CELL_WIDTH)*grid.x+margin, (margin+CELL_HEIGHT)*grid.y+margin,
                      CELL_WIDTH, CELL_HEIGHT])
            
##-- Display Enemy Agents
            for enemy_ind in range(len(self.enemyPos)):
                if self.enemyPos[enemy_ind]!=None:
                    #pygame.draw.rect(screen, RED,
                             #[(margin+CELL_WIDTH)*self.enemyPos[enemy_ind].x+margin+self.enemyAgents[enemy_ind].xOffset, (margin+CELL_HEIGHT)*self.enemyPos[enemy_ind].y+margin+self.enemyAgents[enemy_ind].yOffset,
                              #10, 10])

                    pygame.draw.rect(screen, RED,
                                     [(margin + CELL_WIDTH) * self.enemyPos[enemy_ind].x + margin + self.enemyAgents[
                                         enemy_ind].xOffset,
                                      (margin + CELL_HEIGHT) * self.enemyPos[enemy_ind].y + margin + self.enemyAgents[
                                          enemy_ind].yOffset,
                                      10, 10])
                    renderText1 = '%d' % enemy_ind
                    #print(renderText)
                    screen.blit(self.font1.render(renderText1, True, BLACK),
                                ((margin + CELL_WIDTH) * self.enemyPos[enemy_ind].x + margin + 3 + self.enemyAgents[enemy_ind].xOffset,
                                (margin + CELL_HEIGHT) * self.enemyPos[enemy_ind].y + margin + self.enemyAgents[enemy_ind].yOffset))
                    
                    renderText = self.enemyAgents[enemy_ind].message
                    self.enemyAgents[enemy_ind].message = ''
                    screen.blit(self.font.render(renderText, True, RED, WHITE),
                                (MAX_WIDTH*(CELL_WIDTH+1)+1+10,
                                enemy_ind*30))

##-- Display Swat Agents
            for swat_ind in range(len(self.swatPos)):
                if self.swatPos[swat_ind]!=None:
                    pygame.draw.circle(screen, BLUE,
                                       [(self.swatPos[swat_ind].x * CELL_WIDTH) + (self.swatPos[swat_ind].x * margin) +
                                        self.swatAgents[swat_ind].xOffset + 1,
                                        (self.swatPos[swat_ind].y * CELL_HEIGHT) + (self.swatPos[swat_ind].y * margin) +
                                        self.swatAgents[swat_ind].yOffset + 1], 4, 0)
                    renderText1 = '%d' % swat_ind
                    screen.blit(self.font1.render(renderText1, True, WHITE),
                                ((margin + CELL_WIDTH) * self.swatPos[swat_ind].x + margin + 3 + self.swatAgents[swat_ind].xOffset,
                                (margin + CELL_HEIGHT) * self.swatPos[swat_ind].y + margin + self.swatAgents[swat_ind].yOffset))

                    renderText = self.swatAgents[swat_ind].message
                    self.swatAgents[swat_ind].message = ''
                    screen.blit(self.font.render(renderText, True, BLUE, WHITE),
                                (MAX_WIDTH*(CELL_WIDTH+1)+1+10,
                                (swat_ind+3)*30))

##-- Display Hostages
            for hst_ind in range(len(self.hostagePos)):
                if(self.hostagePos[hst_ind] != None):
                    pygame.draw.circle(screen, ORANGE,
                        [(self.hostagePos[hst_ind].x * CELL_WIDTH)+(self.hostagePos[hst_ind].x * margin)+int(CELL_WIDTH/2)+1,(self.hostagePos[hst_ind].y * CELL_HEIGHT)+ (self.hostagePos[hst_ind].y * margin)+int(CELL_HEIGHT/2)+1],4,0)

                    ##renderText = 'Your text here'
                    #print(renderText)
                    ##screen.blit(self.font.render(renderText, True, WHITE),
                    ##(MAX_WIDTH*(CELL_WIDTH+1))+1+50,50)
            
            
            pygame.display.flip()
            time.sleep(1)

            if(self.gameOn == True):
                self.update_agentPos()
                self.check_LOS()
                self.duel()
            else:
                self.gameStart()

def main():
    pygame.init()
##    maze_number = input("Start Y/N: ")
    a = Gridworld()
    a.init_grid()
    a.display_grid()
    pygame.quit()
    
if __name__ == '__main__':
    main()
