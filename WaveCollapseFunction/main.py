import random
import pygame

pygame.init()

allids = [x for x in range(1,7)]

height = 0
width = 0
commands = []
remaining = 0

ImgPath = ['', ]
Names = ['',]
Allows = [[[],[],[],[]]]#up, right, down, left

result = []
class Tile():
    
    def __init__(self):
        self.id = 0
        self.poss = set(allids)
        self.entropy = len(self.poss)
        self.N = set(allids)
        self.E = set(allids)
        self.S = set(allids)
        self.W = set(allids)
        self.pN = set(allids)
        self.pE = set(allids)
        self.pS = set(allids)
        self.pW = set(allids)
        self.collapsed = False
    
    def recalculate(self):
        if not self.collapsed:
            self.entropy = len(self.poss)
            for i in self.poss:
                self.N |= set(Allows[i][0])
                self.E |= set(Allows[i][1])
                self.S |= set(Allows[i][2])
                self.W |= set(Allows[i][3])
        if(self.N==self.pN & self.E==self.pE & self.W==self.pW & self.S==self.pS):
            return False
        return True

def read(filename):
    f = [x.strip() for x in open(filename, 'r').readlines() if x[0] not in ['\n','#']]
    mode = ''
    global height, width
    for line in f:
        if line[0] == '[':
            if line == "[tiles]":
                mode = 't'
            elif line == "[commands]":
                mode = 'c'
            elif line == "[size]":
                mode = 's'
        
        elif mode == 't':
            temp = [x.strip(' []') for x in line.split(',')]
            Names.append(temp[0])
            ImgPath.append(temp[2])
            if len(temp) == 4:
                print('temp3')
                print(temp[3])
                temp[3] = [int(x) for x in temp[3].split() if x]
                Allows.append([temp[3]]*4)
            else:
                for i in range(3,8):
                    temp[i] = [int(x) for x in temp[i].split(' ') if x]
                Allows.append([temp[3]+temp[4], temp[3]+temp[5], temp[3]+temp[6], temp[3]+temp[7]])
                
        elif mode == 'c':
            temp = [int(x.strip('\n')) for x in line.split(',')]
            commands.append([temp[0], temp[1], temp[2]])
            
        elif mode == 's':
     
            temp = line.split(',')
            width = int(temp[0])
            height = int(temp[1])

def collapse(x, y, _id):
    global remaining, result
    print(f"collapsed {x},{y} to {_id}")
    result[x][y].entropy = 69420
    result[x][y].N = set(Allows[_id][0])
    result[x][y].E = set(Allows[_id][1])
    result[x][y].S = set(Allows[_id][2])
    result[x][y].W = set(Allows[_id][3])
    result[x][y].collapsed = True
    result[x][y].id = _id
    remaining -= 1

def calc_poss(x, y):
    global result
    curr = result[x][y]
    if result[x-1][y] != 0:
        curr.poss&=set(result[x-1][y].E)
    if result[x+1][y] != 0:
        curr.poss&=set(result[x+1][y].W)
    if result[x][y-1] != 0:
        curr.poss&=set(result[x][y-1].S)
    if result[x][y+1] != 0:
        curr.poss&=set(result[x][y+1].N)
    moai = curr.recalculate()
    result[x][y] = curr
    return moai

def WaveCollapseFunction():
    global result, remaining
    result = [[Tile() for y in range(0, width)] for x in range(0,height)]
    for i in result:
        i.insert(0,0)
        i.append(0)
    result.insert(0,[0]*(width+2))
    result.append([0]*(width+2))
    remaining = width*height
    for x, y, target in commands:
        collapse(x, y, target)
        
    while(remaining):
        failed = True
        suma = 1
        while(suma>0):
            suma = 0
            
            for i in range(1,height+1):
                for j in range(1,width+1):
                    if result[i][j].collapsed == False:
                        suma += calc_poss(i,j)
        
        mini = 2137420
        indx = [-1,-1]
        ones = []
        miis = []
        for xindx, i in enumerate(result):
            if i:    
                for yindx, j in enumerate(i):
                    if j:
                        if j.entropy == 1:
                            ones.append((xindx, yindx))
                        if j.entropy<mini:
                            miis = [(xindx,yindx)]
                            mini = j.entropy
                        elif j.entropy==mini:
                            miis.append((xindx,yindx))
        if ones:
            for x,y in ones:
                collapse(x, y, next(iter(result[x][y].poss)))
        else:
            temp = random.choice(miis)
            #set to list inefficient
            if len(result[temp[0]][temp[1]].poss) != 0:
                collapse(temp[0], temp[1], random.choice(list(result[temp[0]][temp[1]].poss)))
            else:
                failed = False
                print(f'collapse failed(empty poss) x:{temp[0]} y:{temp[1]}')
                break
    idres = [[y.id for y in x if y!=0] for x in result if x[1]!=0]
    return idres,failed

def display(idlist, failed):
    height =  len(idlist)
    width = len(idlist[0])
    imglist = [pygame.transform.scale(pygame.image.load(x), (48,48)) for x in ImgPath[1:]]
    
    screen = pygame.display.set_mode((height*48, width*48))
    for x,i in enumerate(idlist):
        for y,j in enumerate(i):
            screen.blit(imglist[j-1],(x*48,y*48))
    pygame.display.update()
    run = True
    if failed == True:
        while run:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    run = False
if __name__ == '__main__':
    read("pipes-coding-train.txt")
    for i in range(10):
        a = WaveCollapseFunction()
        display(a[0],a[1])

#input()