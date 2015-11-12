import pygame, random, copy, time
import numpy as np
import pylab as pl
from mpl_toolkits.mplot3d import axes3d
import matplotlib.colors as colors
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#from matplotlib.pylab import *
# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
PURPLE   = ( 255,   0, 255)
YELLOW   = ( 255, 255,   0)
ORANGE   = ( 255, 155,   3)
GREY     = ( 188, 188, 188)
# This sets the width and height of each grid location
width  = 15
height = 15

# This sets the margin between each cell
margin = 0
grid_x=50
grid_y=50

grid = []
road_grid = []
searchorder=[1,2,3,4] #Initial vision
road_distribution=1.0
arrest_map =[[0 for i in range(int(grid_x))] for i in range(int(grid_y))] # Create a 2 dimensional array.
for row in range(grid_x):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    road_grid.append([])
    for column in range(grid_y):
        if row%3==0 or column%5==0:
            if random.random()>road_distribution:
                grid[row].append(1)
                road_grid[row].append(1)
            else:
                grid[row].append(0)
                road_grid[row].append(0)
        else:
            grid[row].append(1) # Append a cell
            road_grid[row].append(1)

def get_start_coords(type_class,number_of_clusters=4,clusters=False, variance=2*grid_x**0.5):
    while True:
        if type_class=="h":
            if clusters == True:
                if number_of_clusters == 1:
                    __randx = int(np.round(random.gauss(np.round((grid_x/2) , 0), variance),0))%grid_x
                    __randy = int(np.round(random.gauss(np.round((grid_y/2) , 0), variance),0))%grid_y
                if number_of_clusters == 2:
                    prob = random.randint(0,  1)
                    if prob == 0:
                        __randx = int(np.round(random.gauss(np.round((3*grid_x/4) , 0), variance),0))%grid_x
                        __randy = int(np.round(random.gauss(np.round((3*grid_y/4) , 0), variance),0))%grid_y
                    else:
                        __randx = int(np.round(random.gauss(np.round((grid_x/4) , 0), variance),0))%grid_x
                        __randy = int(np.round(random.gauss(np.round((grid_y/4) , 0), variance),0))%grid_y
                if number_of_clusters == 3:
                    prob = random.randint(0,  2)
                    if prob == 0:
                        __randx = int(np.round(random.gauss(np.round((3*grid_x/4) , 0), variance),0))%grid_x
                        __randy = int(np.round(random.gauss(np.round((3*grid_y/4) , 0), variance),0))%grid_y
                    if prob ==1:
                        __randx = int(np.round(random.gauss(np.round((grid_x/4) , 0), variance),0))%grid_x
                        __randy = int(np.round(random.gauss(np.round((grid_y/4) , 0), variance),0))%grid_y
                    if prob ==2:
                        __randx = int(np.round(random.gauss(np.round((3*grid_x/4) , 0), variance),0))%grid_x
                        __randy = int(np.round(random.gauss(np.round((grid_y/4) , 0), variance),0))%grid_y
                if number_of_clusters == 4:
                    prob = random.randint(0,  3)
                    if prob == 0:
                        __randx = int(np.round(random.gauss(np.round((3*grid_x/4) , 0), variance),0))%grid_x
                        __randy = int(np.round(random.gauss(np.round((3*grid_y/4) , 0), variance),0))%grid_y
                    if prob ==1:
                        __randx = int(np.round(random.gauss(np.round((grid_x/4) , 0), variance),0))%grid_x
                        __randy = int(np.round(random.gauss(np.round((grid_y/4) , 0), variance),0))%grid_y
                    if prob ==2:
                        __randx = int(np.round(random.gauss(np.round((3*grid_x/4) , 0), variance),0))%grid_x
                        __randy = int(np.round(random.gauss(np.round((grid_y/4) , 0), variance),0))%grid_y
                    if prob ==3:
                        __randx = int(np.round(random.gauss(np.round((grid_x/4) , 0), variance),0))%grid_x
                        __randy = int(np.round(random.gauss(np.round((3*grid_y/4) , 0), variance),0))%grid_y
            if clusters ==False:
                __randx=random.randint(0,grid_x-1)
                __randy=random.randint(0,grid_y-1)

            if __randx%3!=0 and __randy%5!=0 and grid[__randx][__randy]==1:
                return __randx,__randy

        if type_class == "p":
        #if clusters == False:
            __randx=random.randint(0,grid_x-1)
            __randy=random.randint(0,grid_y-1)
            if road_grid[__randx][__randy]==0:
                    return __randx,__randy

class Robber:
    def __init__(self, start_x, start_y,coprob, speed=25, rob_speed=15,generation=0, vision=6, age=0):
        self.x=start_x
        self.y=start_y
        self.coprob=coprob
        self.money=random.randint(10,150)
        self.money_collected=self.money
        self.speed = speed
        self.robbing=False
        self.rob_counter=0
        self.rob_speed=rob_speed
        self.generation=generation
        self.vision=vision
        self.housefound=False
        self.copseen=False
        self.route=[]
        self.housecoords=[]
        self.age=age
    def move(self):
        global number_of_houses
        global robbers
        global cops
        global civilians
        xB=0
        yB=0
        directions=[]
        field_of_view=[1,1,1,1] #N S E W
        while True:
            while self.housefound==False and self.route==[]:
                position=0
                while position<=self.vision:
                    diffsign=0
                    position+=1
                    for s in searchorder: #randomizes the order of the vision search
                        if s==1:
                            if road_grid[(self.x-position)%grid_x][(self.y)%grid_y]==0 and field_of_view[0]==1:
                                if isinstance( grid[(self.x-position)%grid_x][(self.y+1)%grid_y], int )!=True:
                                    if grid[(self.x-position)%grid_x][(self.y+1)%grid_y].coprob=="hous":
                                        diffsign=1
                                if isinstance( grid[ (self.x-position)%grid_x][self.y-1], int )!=True:
                                    if grid[(self.x-position)%grid_x][self.y-1].coprob=="hous":
                                        diffsign=-1
                                if diffsign==1 or diffsign==-1:
                                    if grid[(self.x-position)%grid_x][(self.y+diffsign)%grid_y].robbed == False and grid[(self.x-position)%grid_x][(self.y+diffsign)%grid_y].beingrobbed == False:
                                        directions=['0' for i in range(position)]
                                        self.housefound= True
                                        if diffsign==1:
                                            directions.append('1')
                                        elif diffsign==-1:
                                            directions.append('3')
                                        xB = (self.x-position)%grid_x
                                        yB = (self.y+diffsign)%grid_y
                                        break
                            else:
                                field_of_view[0]=0
                            diffsign=0
                        elif s==2:
                            if road_grid[(self.x+position)%grid_x][(self.y)%grid_y]==0 and field_of_view[1]==1:
                                if isinstance( grid[(self.x+position)%grid_x][(self.y+1)%grid_y], int )!=True:
                                    if grid[(self.x+position)%grid_x][(self.y+1)%grid_y].coprob=="hous":
                                        diffsign=1
                                if isinstance( grid[ (self.x+position)%grid_x][self.y-1], int )!=True:
                                    if grid[(self.x+position)%grid_x][self.y-1].coprob=="hous":
                                        diffsign=-1
                                if diffsign==1 or diffsign==-1:
                                    if grid[(self.x+position)%grid_x][(self.y+diffsign)%grid_y].robbed == False and grid[(self.x+position)%grid_x][(self.y+diffsign)%grid_y].beingrobbed == False:
                                        directions=['2' for i in range(position)]
                                        self.housefound= True
                                        if diffsign==1:
                                            directions.append('1')
                                        elif diffsign==-1:
                                            directions.append('3')
                                        xB = (self.x+position)%grid_x
                                        yB = (self.y+diffsign)%grid_y
                                        break
                            else:
                                field_of_view[1]=0
                            diffsign=0
                        elif s==3:
                            if road_grid[(self.x)%grid_x][(self.y+position)%grid_y]==0 and field_of_view[2]==1:
                                if isinstance( grid[(self.x+1)%grid_x][(self.y+position)%grid_y], int )!=True:
                                    if grid[(self.x+1)%grid_x][ (self.y+position)%grid_y ].coprob=="hous":
                                        diffsign=1
                                if isinstance( grid[self.x-1][(self.y+position)%grid_y], int )!=True:
                                    if grid[self.x-1][ (self.y+position)%grid_y ].coprob=="hous":
                                        diffsign=-1
                                if diffsign==1 or diffsign==-1:
                                    if grid[(self.x+diffsign)%grid_x][(self.y+position)%grid_y ].robbed == False and grid[(self.x+diffsign)%grid_x][(self.y+position)%grid_y ].beingrobbed == False:
                                        directions=['1' for i in range(position)]
                                        self.housefound = True
                                        if diffsign==1:
                                            directions.append('2')
                                        elif diffsign==-1:
                                            directions.append('0')
                                        xB = (self.x+diffsign)%grid_x
                                        yB = (self.y+position)%grid_y
                                        break
                            else:
                                field_of_view[2]=0
                            diffsign=0
                        elif s==4:
                            if road_grid[(self.x)%grid_x][(self.y-position)%grid_y]==0 and field_of_view[3]==1:
                                if isinstance( grid[(self.x+1)%grid_x][(self.y-position)%grid_y], int )!=True:
                                    if grid[(self.x+1)%grid_x][ (self.y-position)%grid_y ].coprob=="hous":
                                        diffsign=1
                                if isinstance( grid[self.x-1][(self.y-position)%grid_y], int )!=True:
                                    if grid[self.x-1][ (self.y-position)%grid_y ].coprob=="hous":
                                        diffsign=-1
                                if diffsign==1 or diffsign==-1:
                                    if grid[(self.x+diffsign)%grid_x][(self.y-position)%grid_y ].robbed == False and grid[(self.x+diffsign)%grid_x][(self.y-position)%grid_y ].beingrobbed == False:
                                        directions=['3' for i in range(position)]
                                        self.housefound = True
                                        if diffsign==1:
                                            directions.append('2')
                                        elif diffsign==-1:
                                            directions.append('0')
                                        xB = (self.x+diffsign)%grid_x
                                        yB = (self.y-position)%grid_y
                                        break
                            else:
                                field_of_view[3]=0
                break
            if self.housefound==True:
                try:
                    self.route=directions
                    self.housefound=False
                except UnboundLocalError:
                    print "xb error"
            if len(self.route)>1:
                i=self.route[0]
                new_randx=self.x
                new_randy=self.y
                grid[self.x][self.y]=0
                if i=='0':
                    new_randx=(self.x-1)%grid_x
                elif i=='1':
                    new_randy=(self.y+1)%grid_y
                elif i=='2':
                    new_randx=(self.x+1)%grid_x
                elif i=='3':
                    new_randy=(self.y-1)%grid_y
                if isinstance( grid[new_randx][new_randy], int )!=True:
                    robprob=float(self.money)/float(200)
                    if robprob>1:
                        robprob=1
                    if grid[new_randx][new_randy].coprob=="civ" and random.random()<robprob:
                        self.recruit(grid[new_randx][new_randy])
                grid[new_randx][new_randy]=self
                self.x=new_randx
                self.y=new_randy
                self.route=self.route[1:]
                break
            if len(self.route)==1:
                i=self.route[0]
                new_randx=self.x
                new_randy=self.y
                if i=='0':
                    new_randx=(self.x-1)%grid_x
                elif i=='1':
                    new_randy=(self.y+1)%grid_y
                elif i=='2':
                    new_randx=(self.x+1)%grid_x
                elif i=='3':
                    new_randy=(self.y-1)%grid_y
                #check north
                position=0
                while position <=self.vision and self.copseen==False:
                    position+=1
                    if isinstance( grid[(self.x-position)%grid_x ][(self.y)%grid_y], int )!=True:
                        if grid[(self.x-position)%grid_x][(self.y)%grid_y].coprob=="cop": #look along row
                            self.copseen=True
                    if isinstance( grid[(self.x+position)%grid_x ][(self.y)%grid_y], int )!=True:
                        if grid[(self.x+position)%grid_x][(self.y)%grid_y].coprob=="cop": #look along row
                            self.copseen=True
                    if isinstance( grid[(self.x)%grid_x ][(self.y+position)%grid_y], int )!=True:
                        if grid[(self.x)%grid_x][(self.y+position)%grid_y].coprob=="cop": #look along row
                            self.copseen=True
                    if isinstance( grid[(self.x)%grid_x ][(self.y-position)%grid_y], int )!=True:
                        if grid[(self.x)%grid_x][(self.y-position)%grid_y].coprob=="cop": #look along row
                            self.copseen=True
                if self.y%5 == 0 and self.x%3 != 0: #if column
                    for position in range(-self.vision,self.vision):
                        if isinstance( grid[ (self.x+position)%grid_x ][(self.y)%grid_y], int )!=True:
                            if grid[(self.x+position)%grid_x][(self.y)%grid_y].coprob=="cop": #look along row
                                self.copseen=True
                if isinstance( grid[new_randx][new_randy], int )!=True:
                    if grid[new_randx][new_randy].coprob=="hous":
                        if grid[new_randx][new_randy].robbed==False and grid[new_randx][new_randy].beingrobbed==False:
                            if self.copseen==False:
                                self.robbing=True
                                crime_map[int(new_randx%grid_x) ][int(new_randy%grid_y)] += 1
                                self.housecoords=[new_randx,new_randy]
                                grid[new_randx][new_randy].rob(self.rob_speed)
                                self.money+= self.rob_speed**2
                                break
                            else:
                                self.copseen=False
                self.route=[]
                break
            #RANDOM MOVE#
            change=random.choice([[0,1],[1,0],[-1,0],[0,-1]])
            xdiff,ydiff=change[0],change[1]
            new_randx=(self.x+xdiff)%grid_x
            new_randy=(self.y+ydiff)%grid_y
            if road_grid[new_randx][new_randy]==0:
                grid[self.x][self.y]=0
                if isinstance( grid[new_randx][new_randy], int )!=True:
                    robprob=float(self.money)/float(200)
                    if robprob>1:
                        robprob=1
                    if grid[new_randx][new_randy].coprob=="civ" and random.random()<robprob:
                        self.recruit(grid[new_randx][new_randy])
                        grid[new_randx][new_randy]=self
                grid[new_randx][new_randy]=self
                self.x=new_randx
                self.y=new_randy
            elif isinstance( grid[new_randx][new_randy], int )!=True:
                if grid[new_randx][new_randy].coprob=="hous":
                    if grid[new_randx][new_randy].robbed==False and grid[new_randx][new_randy].beingrobbed==False:
                        self.robbing=True
                        crime_map[int(new_randx%grid_x) ][int(new_randy%grid_y)] += 1
                        grid[new_randx][new_randy].rob(self.rob_speed)
                        self.money+= self.rob_speed**2
                    else:
                        break
            break
        return self.x,self.y
    def get_new_genes(self):
        while True:
            new_speed = np.round(random.gauss(self.speed, 1),0)
            new_rob_speed = np.round(random.gauss(self.rob_speed,1),0)
            new_vision = int(np.round(random.gauss(self.vision,1),0))
            if new_speed >= 1 and new_rob_speed >= 1 and new_vision>=1:
                return new_speed, new_rob_speed, new_vision
            else:
                return self.speed,self.rob_speed,self.vision
    def recruit(self,other):
        global robbers
        global civilians
        global evo
        generation=self.generation+1
        if evo==True:
            speed,rob_speed,vision= self.get_new_genes()
            robbers.append(Robber(self.x,self.y,self.coprob, speed, rob_speed,generation, vision)) #clone new robber
        else:
            robbers.append(Robber(self.x,self.y,self.coprob,self.speed,self.rob_speed, generation)) #clone new robber
        civilians.remove(other)
    def die(self):
        global civilians
        global cops
        global robbers
        try:
            robbers.remove(self)
            civilians.append(Civilian(self.x,self.y,"civ"))
        except ValueError:
            print self, "not found in robbers list"
    def incrobcounter(self):
        self.rob_counter+=1
    def __repr__(self):
        return '%s at (%s,%s), money:%s,speed is %s, robbing:%s, rob_counter:%s, rob_speed:%s, housefound:%s, vision:%s, housecoords:%s' % (self.coprob,self.x,self.y,self.money, self.speed,self.robbing,self.rob_counter,self.rob_speed, self.housefound,self.vision, self.housecoords)

class Cop:
    def __init__(self, start_x, start_y,coprob, speed=5, vision=15, generation=0, arrest_counter=0, age=0,):
        self.x=start_x
        self.y=start_y
        self.coprob=coprob
        self.speed = speed
        self.arrest_count=0
        self.total_arrest_count = 0
        self.house_arrests=0
        self.street_arrests=0
        self.robfound=False
        self.route=[]
        self.vision=vision
        self.age=age
        self.generation=generation
        if arrest_counter==0:
            self.arrest_counter=random.randint(100,1000)
        else:
            self.arrest_counter=arrest_counter/2
    def move(self):
        global robbers
        global streetarrests
        global housearrests
        global searchorder
        while True:
            while self.robfound==False and self.route==[]:
                position=0
                directions=[]
                xB,yB=0,0
                field_of_view=[1,1,1,1] #N S E W
                while position<=self.vision:
                    diffsign=0
                    position+=1
                    for s in searchorder:
                        if s==1:
                            if road_grid[(self.x-position)%grid_x][(self.y)%grid_y]==0 and field_of_view[0]==1:
                                if isinstance( grid[(self.x-position)%grid_x][(self.y+1)%grid_y], int )!=True:
                                    if grid[(self.x-position)%grid_x][(self.y+1)%grid_y].coprob=="hous":
                                        if grid[(self.x-position)%grid_x][(self.y+1)%grid_y].beingrobbed==True:
                                            diffsign=1
                                            # "I see a house to the right"
                                if isinstance( grid[ (self.x-position)%grid_x][self.y-1], int )!=True:
                                    if grid[(self.x-position)%grid_x][self.y-1].coprob=="hous":
                                        if grid[(self.x-position)%grid_x][self.y-1].beingrobbed==True:
                                            diffsign=-1
                                            # "I see a house to the left"
                                if diffsign==1 or diffsign==-1:
                                    if grid[(self.x-position)%grid_x][(self.y+diffsign)%grid_y].beingrobbed == True:
                                        directions=['0' for i in range(position)]
                                        self.robfound= True
                                        if diffsign==1:
                                            directions.append('1')
                                        elif diffsign==-1:
                                            directions.append('3')
                                        xB = (self.x-position)%grid_x
                                        yB = (self.y+diffsign)%grid_y
                                        break
                            else:
                                field_of_view[0]=0
                            diffsign=0
                        elif s==2:
                            if road_grid[(self.x+position)%grid_x][(self.y)%grid_y]==0 and field_of_view[1]==1:
                                # print "i can see south"
                                if isinstance( grid[(self.x+position)%grid_x][(self.y+1)%grid_y], int )!=True:
                                    if grid[(self.x+position)%grid_x][(self.y+1)%grid_y].coprob=="hous":
                                        diffsign=1
                                        #"I see a house to the right"
                                if isinstance( grid[ (self.x+position)%grid_x][self.y-1], int )!=True:
                                    if grid[(self.x+position)%grid_x][self.y-1].coprob=="hous":
                                        diffsign=-1
                                        #"I see a house to the left"
                                if diffsign==1 or diffsign==-1:
                                    if grid[(self.x+position)%grid_x][(self.y+diffsign)%grid_y].beingrobbed == True:
                                        directions=['2' for i in range(position)]
                                        self.robfound= True
                                        if diffsign==1:
                                            directions.append('1')
                                        elif diffsign==-1:
                                            directions.append('3')
                                        xB = (self.x+position)%grid_x
                                        yB = (self.y+diffsign)%grid_y
                                        break
                            else:
                                field_of_view[1]=0
                            diffsign=0
                        elif s==3:
                            if road_grid[(self.x)%grid_x][(self.y+position)%grid_y]==0 and field_of_view[2]==1:
                                if isinstance( grid[(self.x+1)%grid_x][(self.y+position)%grid_y], int )!=True:
                                    if grid[(self.x+1)%grid_x][ (self.y+position)%grid_y ].coprob=="hous":
                                        diffsign=1
                                        # "I see a house south"
                                if isinstance( grid[self.x-1][(self.y+position)%grid_y], int )!=True:
                                    if grid[self.x-1][ (self.y+position)%grid_y ].coprob=="hous":
                                        diffsign=-1
                                        # "I see a house north"
                                if diffsign==1 or diffsign==-1:
                                    if grid[(self.x+diffsign)%grid_x][(self.y+position)%grid_y ].beingrobbed == True:
                                        directions=['1' for i in range(position)]
                                        self.robfound = True
                                        if diffsign==1:
                                            directions.append('2')
                                        elif diffsign==-1:
                                            directions.append('0')
                                        xB = (self.x+diffsign)%grid_x
                                        yB = (self.y+position)%grid_y
                                        #"house spotted at", xB, yB
                                        break
                            else:
                                field_of_view[2]=0
                            diffsign=0
                        elif s==4:
                            if road_grid[(self.x)%grid_x][(self.y-position)%grid_y]==0 and field_of_view[3]==1:
                                if isinstance( grid[(self.x+1)%grid_x][(self.y-position)%grid_y], int )!=True:
                                    if grid[(self.x+1)%grid_x][ (self.y-position)%grid_y ].coprob=="hous":
                                        diffsign=1
                                        #"I see a house south"
                                if isinstance( grid[self.x-1][(self.y-position)%grid_y], int )!=True:
                                    if grid[self.x-1][ (self.y-position)%grid_y ].coprob=="hous":
                                        diffsign=-1
                                        #"I see a house north"
                                if diffsign==1 or diffsign==-1:
                                    if grid[(self.x+diffsign)%grid_x][(self.y-position)%grid_y ].beingrobbed == True:
                                        directions=['3' for i in range(position)]
                                        self.robfound = True
                                        if diffsign==1:
                                            directions.append('2')
                                        elif diffsign==-1:
                                            directions.append('0')
                                        xB = (self.x+diffsign)%grid_x
                                        yB = (self.y-position)%grid_y
                                        # "house spotted at", xB, yB
                                        break
                            else:
                                field_of_view[3]=0
                break
            if self.robfound==True:
                try:
                    self.route=directions
                    self.robfound=False
                except UnboundLocalError:
                    print "xb error"
            if len(self.route)>1:
                i=self.route[0]
                new_randx=self.x
                new_randy=self.y
                if cop_evo==True:
                    if isinstance( grid[new_randx][new_randy], int )!=True:
                        copprob=float(self.arrest_counter**2)/float(2e4)
                        if grid[new_randx][new_randy].coprob=="civ" and random.random() < copprob:
                            self.recruit(grid[new_randx][new_randy])
                grid[self.x][self.y]=0
                if i=='0':
                    new_randx=(self.x-1)%grid_x
                elif i=='1':
                    new_randy=(self.y+1)%grid_y
                elif i=='2':
                    new_randx=(self.x+1)%grid_x
                elif i=='3':
                    new_randy=(self.y-1)%grid_y
                grid[new_randx][new_randy]=self
                self.x=new_randx
                self.y=new_randy
                self.route=self.route[1:]
                break
            if len(self.route)==1:
                i=self.route[0]
                new_randx=self.x
                new_randy=self.y
                if i=='0':
                    new_randx=(self.x-1)%grid_x
                elif i=='1':
                    new_randy=(self.y+1)%grid_y
                elif i=='2':
                    new_randx=(self.x+1)%grid_x
                elif i=='3':
                    new_randy=(self.y-1)%grid_y
                if isinstance( grid[new_randx][new_randy], int )!=True:
                    if grid[new_randx][new_randy].coprob=="hous":
                        if grid[new_randx][new_randy].beingrobbed==True:
                            for rob in robbers:
                                if len(rob.housecoords)>0:
                                    if rob.housecoords[0]==new_randx and rob.housecoords[1]==new_randy:
                                        housearrests+=1
                                        self.arrest_count+=1
                                        self.total_arrest_count+=1
                                        self.house_arrests+=1
                                        self.arrest_counter=1000
                                        arrest_map[int(new_randx%grid_x)][int(new_randy%grid_y)] += 1
                                        rob.die()
                                        grid[new_randx][new_randy].counter=grid[new_randx][new_randy].robtime
                                        self.route=[]
                                        break
                            self.route=[]
                            break
                        else:
                            self.route=[]
                            break

            change=random.choice([[0,1],[1,0],[-1,0],[0,-1]])
            xdiff,ydiff=change[0],change[1]
            new_randx=(self.x+xdiff)%grid_x
            new_randy=(self.y+ydiff)%grid_y
            if road_grid[new_randx][new_randy]==0:
                grid[self.x][self.y]=0
                if cop_evo==True:
                    if isinstance( grid[new_randx][new_randy], int )!=True:
                        copprob=float(self.arrest_counter**2)/float(2e4)
                        if grid[new_randx][new_randy].coprob=="civ" and random.random() < copprob:
                            self.recruit(grid[new_randx][new_randy])
                if isinstance( grid[new_randx][new_randy], int )!=True:
                    arrestprob=self.speed/40
                    if arrestprob>0.5:
                        arrestprob=0.5
                    if grid[new_randx][new_randy].coprob=="rob" and random.random()<arrestprob:
                        # print "arrest at (%s,%s)" % (new_randx,new_randy)
                        self.x=new_randx
                        self.y=new_randy
                        streetarrests+=1
                        self.arrest_count+=1
                        self.total_arrest_count+=1
                        self.street_arrests+=1
                        arrest_map[int(new_randx%grid_x)][int(new_randy%grid_y)] += 1
                        self.arrest_counter=1000
                        grid[new_randx][new_randy].die()
                        grid[new_randx][new_randy]=self
                grid[new_randx][new_randy]=self
                self.x=new_randx
                self.y=new_randy
            elif isinstance( grid[new_randx][new_randy], int )!=True:
                if grid[new_randx][new_randy].coprob=="hous":
                    if grid[new_randx][new_randy].beingrobbed==True:
                        # print 'house robbed at (%s,%s)' % (new_randx, new_randy)
                        for rob in robbers:
                            if len(rob.housecoords)!=0:
                                if rob.x==self.x and rob.y==self.y:
                                    housearrests+=1
                                    self.arrest_count+=1
                                    self.total_arrest_count+=1
                                    self.house_arrests+=1
                                    self.arrest_counter=1000
                                    arrest_map[int(new_randy%grid_y)][int(new_randx%grid_x)] += 1
                                    rob.die()
                    else:
                        break
            break
        return self.x,self.y
    def recruit(self,other):
        global robbers
        global civilians
        global cop_evo

        generation=self.generation+1
        if cop_evo==True:
            speed, vision= self.get_new_genes()
            cops.append(Cop(self.x,self.y,self.coprob, speed, vision, generation, self.arrest_counter)) #clone new cop
        else:
            cops.append(Cop(self.x,self.y,self.coprob,self.speed,self.vision, generation)) #clone new cop
        civilians.remove(other)
    def die(self):
        global civilians
        global cops
        global robbers
        try:
            cops.remove(self)
            civilians.append(Civilian(self.x,self.y,"civ"))
        except ValueError:
            print self, "not found in cops list"
    def get_new_genes(self):
        while True:
            new_speed = np.round(random.gauss(self.speed, 1),0)
            new_vision = int(np.round(random.gauss(self.vision,1),0))
            if new_speed >= 1 and new_vision>=1:
                return new_speed,new_vision
            else:
                return self.speed,self.vision
    def __repr__(self):
        return '%s at (%s,%s), speed:%s, robfound:%s, vision:%s, total arrests:%s, age:%s, arrest_counter:%s' % (self.coprob,self.x,self.y, self.speed,self.robfound,self.vision, self.arrest_count, self.age, self.arrest_counter)

class Civilian:
    def __init__(self, start_x, start_y,coprob, speed=10):
        self.x=start_x
        self.y=start_y
        self.money=100
        self.coprob=coprob
        self.speed = speed
        self.cop_counter=0
    def move(self):
        change=random.choice([[0,1],[1,0],[-1,0],[0,-1]])
        for i in change:
            xdiff,ydiff=change[0],change[1]
            new_randx=(self.x+xdiff)%grid_x
            new_randy=(self.y+ydiff)%grid_y
            if road_grid[new_randx][new_randy]==0:
                grid[self.x][self.y]=0
                grid[new_randx][new_randy]=self
                self.x=new_randx
                self.y=new_randy
                break
        return self.x,self.y
    def get_new_genes(self):
        pass
    def __repr__(self):
        return '%s at (%s,%s), speed is %s' % (self.coprob,self.x,self.y, self.speed)

class House:
    def __init__(self, start_x, start_y, robbed):
        self.x=start_x
        self.y=start_y
        self.robbed=False
        self.beingrobbed=False
        self.counter=0
        self.coprob="hous"
        self.robtime=0
        grid[self.x][self.y]=self
    def rob(self,robtime):
        self.counter=0
        self.robtime=robtime
        self.beingrobbed=True
        return self.beingrobbed
    def revive(self):
        self.counter=0
        self.robbed=False
        grid[self.x][self.y]=self
    def inccounter(self):
        self.counter+=1
    def __repr__(self):
        return 'house at (%s,%s), Robbed:%s, beingrobbed:%s' % (self.x,self.y, self.robbed,self.beingrobbed)

class Town(House):
    def __init__(self,number_of_houses,number_of_clusters,clusters=True):
        self.clusters=clusters
        self.number_of_clusters=number_of_clusters
        self.size=number_of_houses
        self.houses=[]
        self.houses=self.get_houses()
    def get_houses(self):
        for i in self.houses:
            del i
        for x in range(self.size):
            a,b=get_start_coords("h", self.number_of_clusters, self.clusters)
            self.houses.append(House(a,b,False))
        return self.houses

clusters = True
global number_of_clusters
number_of_clusters = 1
randx = 0
randy = 0

def get_stats():
    stat1,stat2,stat3,stat4=[],[],[],[]
    for rob in robbers:
        stat1.append(int(rob.speed))
        stat2.append(int(rob.rob_speed))
        stat3.append(int(rob.generation))
        stat4.append(int(rob.vision))
    return stat1,stat2,stat3,stat4

houses,cops,robbers,civilians,coppers=[],[],[],[],[]
crime_map = [[0 for col in range(int(grid_y) + 1)] for row in range(int(grid_x) +1)]
number_of_cops=50
cop_swap_num=int(number_of_cops*0.05)
number_of_robbers=100
global number_of_houses
number_of_houses=200
global streetarrests
streetarrests=0
global housearrests
housearrests=0
number_of_civs=100
total_genemap_robspeed_movespeed = []
total_genemap_vision_movespeed = []
total_genemap_vision_robspeed = []
total_genemap_cops =[]
total_genemap_rob_generation, total_genemap_cop_generation=[],[]
for x in range(number_of_cops):
    a,b=get_start_coords("p")
    cops.append(Cop(a,b,"cop"))
for x in range(number_of_robbers):
    a,b=get_start_coords("p")
    robbers.append(Robber(a,b,"rob"))
for x in range(number_of_civs):
    a,b=get_start_coords("p")
    civilians.append(Civilian(a,b,"civ"))
num_houses,num_robbers,num_civs,num_housearrests,num_streetarrests,num_cops=[],[],[],[],[],[]

counter=0
Gotham=Town(number_of_houses, number_of_clusters)

evo=True
cop_evo2=True
cop_evo=False
pause=False
plot=True
extinction=False
house_redistribute=False
# Initialize pygame
pygame.init()

# Set the height and width of the screen
size = [width*grid_x, height*grid_y]
screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont("monospace", 25)

# Set title of screen
pygame.display.set_caption("Gotham City")

#Loop until the user clicks the close button.
done = False
counter = 0
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
writing_set=False
# -------- Main Program Loop -----------
while done == False:
    # Gotham.rearrange()

    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                pause=False
            if event.key == pygame.K_d:
                plot=False
                writing_set=False
            if event.key == pygame.K_s:
                dic_Z={}
                graph1,graph2,graph3=[],[],[]
                speed_list,rob_speed_list,generation_list,vision_list=get_stats()
                if speed_list and rob_speed_list and generation_list:
                    max_x=max(speed_list)
                    max_y=max(rob_speed_list)
                    size=(max_x+1,max_y+1)
                    gene_map1=np.zeros(size)
                    max_x=max(speed_list)
                    max_y=max(vision_list)
                    size=(max_x+1,max_y+1)
                    gene_map2=np.zeros(size)
                    max_x=max(rob_speed_list)
                    max_y=max(vision_list)
                    size=(max_x+1,max_y+1)
                    gene_map3=np.zeros(size)
                    for i in range(len(speed_list)):
                        graph1.append('%s,%s' % (speed_list[i],rob_speed_list[i]))
                        graph2.append('%s,%s' % (speed_list[i],vision_list[i]))
                        graph3.append('%s,%s' % (rob_speed_list[i],vision_list[i]))
                        dic_Z1=Counter(graph1)
                        dic_Z2=Counter(graph2)
                        dic_Z3=Counter(graph3)
                    for i in dic_Z1.keys():
                        var=i.split(',')
                        gene_map1[int(var[0])][int(var[1])]=dic_Z1[i]
                    for i in dic_Z2.keys():
                        var=i.split(',')
                        gene_map2[int(var[0])][int(var[1])]=dic_Z2[i]
                    for i in dic_Z3.keys():
                        var=i.split(',')
                        gene_map3[int(var[0])][int(var[1])]=dic_Z3[i]
                    print "ROBBER STATS"
                    print "speed:",np.average(speed_list)
                    print "rob speed:",np.average(rob_speed_list)
                    print "generation:",np.average(generation_list)
                    print "vision:", np.average(vision_list)
                    print "GENE MAP"
                    # print "range:"
                    # print max_s-diff_s, "to", max_s
                    # print max_r-diff_r, "to", max_r
                    fig= pl.figure(1)
                    ax1=fig.add_subplot(131)
                    fig.suptitle("Gene map",fontsize="20")
                    pl.xlabel("Robbing speed",fontsize="18")
                    pl.ylabel("Moving speed",fontsize="18")
                    cax1=ax1.matshow(gene_map1)
                    fig.colorbar(cax1)
                    ax2=fig.add_subplot(132)
                    pl.xlabel("Vision",fontsize="18")
                    pl.ylabel("Moving speed",fontsize="18")
                    cax2=ax2.matshow(gene_map2)
                    fig.colorbar(cax2)
                    ax3=fig.add_subplot(133)
                    pl.xlabel("Vision",fontsize="18")
                    pl.ylabel("Robbing speed",fontsize="18")
                    cax3=ax3.matshow(gene_map3)
                    fig.colorbar(cax3)
                    pl.show()
            if event.key == pygame.K_z:
                fig = pl.figure()
                ax = fig.add_subplot(111, projection='3d')
                # plot points in 3D
                dic_Z={}
                genes,x,y,z,I=[],[],[],[],[]
                speed_list,rob_speed_list,generation_list,vision_list=get_stats()
                if speed_list and rob_speed_list and vision_list:
                    for i in range(len(speed_list)):
                        genes.append('%s,%s,%s' % (speed_list[i],rob_speed_list[i], vision_list[i]))
                        dic_Z=Counter(genes)
                    for i in dic_Z.keys():
                        var=i.split(',')
                        index_x=int(var[0])
                        index_y=int(var[1])
                        index_z=int(var[2])
                        x.append(index_x)
                        y.append(index_y)
                        z.append(index_z)
                        I.append(float(dic_Z[i]))
                cmhot = pl.get_cmap("jet")
                norm_colors=colors.Normalize(min(I),max(I))
                cax=ax.scatter(x,y,z,c=I,cmap=cmhot,norm=norm_colors)
                pl.xlabel("speed")
                pl.ylabel("robbing speed")
                fig.colorbar(cax)
                robgenes_title='robgenes'+str(counter)+'iterations.txt'
                with open(robgenes_title,'w') as f:
                    f.write('GENE DICTIONARY\n')
                    f.write('KEY\tVALUE\n')
                    for i in dic_Z.keys():
                        f.write('%s\t%s\n' % (i,dic_Z[i]))
                pl.show()
            if event.key == pygame.K_c:
                fig = pl.figure()
                ax = fig.add_subplot(111)
                fig.suptitle("Crime map",fontsize="20")
                pl.xlabel("Grid X",fontsize="18")
                pl.ylabel("Grid Y",fontsize="18")
                cax=ax.matshow(crime_map)
                fig.colorbar(cax)
                pl.show()

            if event.key == pygame.K_x:

                pl.figure(1)
                pl.plot([i for i in range(len(num_houses))], num_houses, label="houses")
                pl.plot([i for i in range(len(num_robbers))], num_robbers, label="robbers")
                pl.plot([i for i in range(len(num_civs))], num_civs, label="civilians")
                pl.plot([i for i in range(len(num_cops))], num_cops, label="cops")
                pl.title("Number of elements over iterations", fontsize="24")
                pl.xlabel("Number of iterations", fontsize="20")
                pl.ylabel("Number of element", fontsize="20")
                pl.legend(loc='upper right')

                pl.figure(2)
                pl.plot(range(len(num_housearrests)),num_housearrests, label='House arrests')
                pl.plot(range(len(num_streetarrests)),num_streetarrests, label='Street arrests')
                pl.xlabel("Number of iterations", fontsize="20")
                pl.ylabel("Arrests per 1000 iteration", fontsize="20")
                pl.legend(loc='upper right')
                pop_title='population'+str(counter)+'iterations.txt'
                with open(pop_title,'w') as f:
                    f.write('HOUSES\tROBBERS\tCOPS\tCIVILIANS\n')
                    for i in range(len(num_houses)):
                        f.write('%s\t%s\t%s\t%s\n' % (num_houses[i],num_robbers[i],num_cops[i],num_civs[i]))
                arrest_title='arrests'+str(counter)+'iterations.txt'
                with open(arrest_title,'w') as f:
                    f.write('Iteration\tTotal arrests\tHouse arrests\tStreet arrests\n')
                    for i in range(len(num_housearrests)):
                        f.write('%s\t%s\t%s\t%s\n' % (i*1000,num_housearrests[i]+num_streetarrests[i],num_housearrests[i],num_streetarrests[i]))
                pl.show()
            if event.key == pygame.K_a:
                dic_Z={}
                vision_list,speed_list,generation_list=[],[],[]
                graph=[]
                for cop in cops:
                    vision_list.append(cop.vision)
                    speed_list.append(cop.speed)
                    generation_list.append(cop.generation)
                if vision_list and speed_list:
                    max_x=max(speed_list)
                    max_y=max(vision_list)
                    size=(max_x+1,max_y+1)
                    gene_map=np.zeros(size)
                    for i in range(len(speed_list)):
                        graph.append('%s,%s' % (int(speed_list[i]),int(vision_list[i])))
                        dic_Z=Counter(graph)
                    for i in dic_Z.keys():
                        var=i.split(',')
                        gene_map[int(var[0])][int(var[1])]=dic_Z[i]
                print "cop gen:",np.average(generation_list)
                fig= pl.figure(1)
                ax1=fig.add_subplot(111)
                fig.suptitle("Gene map",fontsize="20")
                pl.xlabel("Vision",fontsize="18")
                pl.ylabel("Speed",fontsize="18")
                cax1=ax1.matshow(gene_map)
                fig.colorbar(cax1)
                copgenes_title='copgenes'+str(counter)+'iterations.txt'
                with open(copgenes_title,'w') as f:
                    f.write('GENE DICTIONARY\n')
                    f.write('KEY\tVALUE\n')
                    for i in dic_Z.keys():
                        f.write('%s\t%s\n' % (i,dic_Z[i]))
                pl.show()
            if event.key == pygame.K_f:
                global number_of_clusters
                global Gotham

                number_of_clusters = 2
                for i in Gotham.houses:
                    grid[i.x][i.y]=1
                    del i
                Gotham=Town(number_of_houses, number_of_clusters)
            if event.key == pygame.K_m:
                fig = pl.figure()
                ax = fig.add_subplot(111)
                fig.suptitle("Arrest map",fontsize="20")
                pl.xlabel("Grid X",fontsize="18")
                pl.ylabel("Grid Y",fontsize="18")
                cax=ax.matshow(arrest_map)
                fig.colorbar(cax)
                pl.show()

            if event.key == pygame.K_b:
                cop_age_list, rob_age_list = [],[]
                arrest_count_list, arrest_list = [],[]
                cop_generations_list, rob_generations_list = [],[]
                arrest_count_avg_list=[]
                money_list=[]
                for cop in cops:
                    cop_age_list.append(cop.age)
                    arrest_count_list.append(cop.arrest_count)
                    arrest_list.append(cop.total_arrest_count)
                    cop_generations_list.append(cop.generation)
                for rob in robbers:
                    rob_age_list.append(rob.age)
                    money_list.append(rob.money)
                    rob_generations_list.append(rob.generation)
                fig = pl.figure()
                ax = fig.add_subplot(131)
                pl.plot(cop_age_list,arrest_count_list, 'bo')
                pl.xlabel("Age", fontsize="20")
                pl.ylabel("Arrests per 1000 iteration", fontsize="20")

                ax = fig.add_subplot(132)
                pl.plot(cop_age_list,arrest_list, 'ro')
                pl.xlabel("Age", fontsize="20")
                pl.ylabel("Arrests", fontsize="20")

                ax = fig.add_subplot(133)
                pl.plot(cop_age_list,cop_generations_list, 'go')
                pl.title("Generation against Age for Cops")
                pl.xlabel("Age", fontsize="20")
                pl.ylabel("Generation", fontsize="20")

                fig2=pl.figure()
                ax = fig2.add_subplot(131)
                pl.plot(rob_age_list,money_list, 'bo')
                pl.xlabel("Age", fontsize="20")
                pl.ylabel("Money", fontsize="20")

                ax = fig2.add_subplot(132)
                pl.plot(rob_generations_list,money_list, 'ro')
                pl.xlabel("Generation", fontsize="20")
                pl.ylabel("Money", fontsize="20")

                ax = fig2.add_subplot(133)
                pl.plot(rob_age_list,rob_generations_list, 'go')
                pl.title("Generation against Age for Robbers")
                pl.xlabel("Age", fontsize="20")
                pl.ylabel("Generation", fontsize="20")
                fig3=pl.figure()
                ax = fig3.add_subplot(131)
                pl.plot(rob_age_list,money_list, 'bo')
                pl.xlabel("Age", fontsize="20")
                pl.ylabel("Money", fontsize="20")

                ax = fig3.add_subplot(132)
                pl.plot(rob_generations_list,money_list, 'ro')
                pl.xlabel("Generation", fontsize="20")
                pl.ylabel("Money", fontsize="20")

                ax = fig3.add_subplot(133)
                pl.plot(rob_age_list,rob_generations_list, 'go')
                pl.title("Generation against Age for Robbers")
                pl.xlabel("Age", fontsize="20")
                pl.ylabel("Generation", fontsize="20")
                pl.show()
            if event.key == pygame.K_q:
                house_arrests,street_arrests=[],[]
                for cop in cops:
                    house_arrests.append(cop.house_arrests)
                    street_arrests.append(cop.street_arrests)
                fig=pl.figure()
                ax=fig.add_subplot(111)
                pl.plot(house_arrests,street_arrests, 'bo')
                pl.xlabel("House arrests", fontsize="20")
                pl.ylabel("Street arrests", fontsize="20")
                ratio_of_arrests=float(sum(house_arrests))/float(sum(street_arrests))
                print ratio_of_arrests
                pl.show()
            if event.key == pygame.K_w:
                pass
            if event.key == pygame.K_v:
                fig = plt.figure()
                plt.ion()
                plt.show()
                for i in range(0, len(total_genemap_cops)):
                    plt.clf()
                    title="Cop Gene map at generation:" + str(np.round(total_genemap_cop_generation[i], 2))
                    pl.xlabel("Vision",fontsize="18")
                    pl.ylabel("Speed",fontsize="18")
                    fig.suptitle(title,fontsize="20")
                    ax = fig.add_subplot(111)
                    cax=ax.matshow(total_genemap_cops[i])
                    fig.colorbar(cax)
                    time.sleep(0.5)
                    plt.draw()
                    time.sleep(0.5)
                plt.close()
                plt.ioff()
            if event.key == pygame.K_l:
                fig = plt.figure()

                plt.ion()
                plt.show()
                for i in range(0, len(total_genemap_vision_movespeed)):
                    plt.clf()
                    ax = fig.add_subplot(111)
                    pl.xlabel("Vision",fontsize="18")
                    pl.ylabel("Moving Speed",fontsize="18")
                    title="Robber Gene map at generation:" + str(np.round(total_genemap_rob_generation[i], 2))
                    fig.suptitle(title,fontsize="20")
                    cax=ax.matshow(total_genemap_vision_movespeed[i])
                    fig.colorbar(cax)
                    time.sleep(0.5)
                    plt.draw()
                    time.sleep(0.5)
                plt.close()
                plt.ioff()
            if event.key == pygame.K_k:
                fig = plt.figure()
                plt.ion()
                plt.show()
                for i in range(0, len(total_genemap_vision_robspeed)):
                    plt.clf()
                    ax = fig.add_subplot(111)
                    pl.xlabel("Vision",fontsize="18")
                    pl.ylabel("Robbing Speed",fontsize="18")
                    title="Robber Gene map at generation:" + str(np.round(total_genemap_rob_generation[i], 2))
                    fig.suptitle(title,fontsize="20")
                    cax=ax.matshow(total_genemap_vision_robspeed[i])
                    fig.colorbar(cax)
                    time.sleep(0.5)
                    plt.draw()
                    time.sleep(0.5)
                plt.close()
                plt.ioff()
            if event.key == pygame.K_j:
                fig = plt.figure()
                plt.ion()
                plt.show()
                for i in range(0, len(total_genemap_robspeed_movespeed)):
                    plt.clf()
                    ax = fig.add_subplot(111)
                    title="Robber Gene map at generation:" + str(np.round(total_genemap_rob_generation[i], 2))
                    fig.suptitle(title,fontsize="20")
                    cax=ax.matshow(total_genemap_robspeed_movespeed[i])
                    pl.xlabel("Robbing Speed",fontsize="18")
                    pl.ylabel("Moving Speed",fontsize="18")
                    fig.colorbar(cax)
                    time.sleep(0.5)
                    plt.draw()
                    time.sleep(0.5)
                plt.close()
                plt.ioff()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (width + margin)
            row = pos[1] // (height + margin)
            # Set that location to zero
            for cop in cops:
                if cop.x==row and cop.y==column:
                    print cop
            for rob in robbers:
                if rob.x==row and rob.y==column:
                    print rob
            for civ in civilians:
                if civ.x==row and civ.y==column:
                    print civ
            for house in Gotham.houses:
                if house.x==row and house.y==column:
                    print house
    while pause==False:
        ###FOR SIMULATION TO RUN 100,000 times###
        # if counter==1000000:
        #     pause=True
        if counter%1000==0 and counter>0:
            global housearrests
            global streetarrests
            global avg_arrests
            global arrest_list
            if cop_evo==True:
                for i in cops:
                    i.arrest_count=0
            print "Iteration number:",counter
            num_housearrests.append(housearrests)
            num_streetarrests.append(streetarrests)
            try:
                avg_housearrests = float(housearrests)/float(len(cops))
            except ZeroDivisionError:
                print "there are 0 cops"
            try:
                avg_streetarrests = float(streetarrests)/float(len(cops))
            except ZeroDivisionError:
                print "there are 0 cops"
            housearrests=0
            streetarrests=0
            if house_redistribute==True:
                for i in Gotham.houses:
                    grid[i.x][i.y]=1
                    del i
                Gotham.get_houses()
            # np.random.shuffle(searchorder)

            if cop_evo2==True:
                cops.sort(key=lambda x: x.arrest_count, reverse=True)
                for i in cops[-cop_swap_num:]:
                    print i.arrest_count
                    del i
                #SHOULD RESET ARRESTS EVERY 1000 ITERATIONSt
                for i in cops:
                    i.arrest_count=0
                cops=cops[:-cop_swap_num]
                new_cops=[]
                for i in cops[:cop_swap_num]:
                    speed, vision=i.get_new_genes()
                    generation=i.generation+1
                    a,b=get_start_coords("p")
                    new_cops.append(Cop(a,b,"cop", speed=speed,vision=vision,generation=generation))
                cops=new_cops+cops
        if counter%2000==0 and counter>0:
            dic_Z={}
            graph1,graph2,graph3=[],[],[]
            speed_list,rob_speed_list,generation_list,vision_list=get_stats()
            if speed_list and rob_speed_list and generation_list:
                max_x=max(speed_list)
                max_y=max(rob_speed_list)
                size=(max_x+1,max_y+1)
                gene_map1=np.zeros(size)
                max_x=max(speed_list)
                max_y=max(vision_list)
                size=(max_x+1,max_y+1)
                gene_map2=np.zeros(size)
                max_x=max(rob_speed_list)
                max_y=max(vision_list)
                size=(max_x+1,max_y+1)
                gene_map3=np.zeros(size)
                for i in range(len(speed_list)):
                    graph1.append('%s,%s' % (speed_list[i],rob_speed_list[i]))
                    graph2.append('%s,%s' % (speed_list[i],vision_list[i]))
                    graph3.append('%s,%s' % (rob_speed_list[i],vision_list[i]))
                    dic_Z1=Counter(graph1)
                    dic_Z2=Counter(graph2)
                    dic_Z3=Counter(graph3)
                for i in dic_Z1.keys():
                    var=i.split(',')
                    gene_map1[int(var[0])][int(var[1])]=dic_Z1[i]
                for i in dic_Z2.keys():
                    var=i.split(',')
                    gene_map2[int(var[0])][int(var[1])]=dic_Z2[i]
                for i in dic_Z3.keys():
                    var=i.split(',')
                    gene_map3[int(var[0])][int(var[1])]=dic_Z3[i]
            try:
                rob_gen_avg=np.average(generation_list)
            except:
                print "there are no robs"
            total_genemap_rob_generation.append(rob_gen_avg)
            total_genemap_robspeed_movespeed.append(gene_map1)
            total_genemap_vision_movespeed.append(gene_map2)
            total_genemap_vision_robspeed.append(gene_map3)

            dic_Z={}
            vision_list,speed_list,generation_list=[],[],[]
            graph=[]
            for cop in cops:
                vision_list.append(cop.vision)
                speed_list.append(cop.speed)
                generation_list.append(cop.generation)
            if vision_list and speed_list:
                max_x=max(speed_list)
                max_y=max(vision_list)
                size=(max_x+1,max_y+1)
                gene_map=np.zeros(size)
                for i in range(len(speed_list)):
                    graph.append('%s,%s' % (int(speed_list[i]),int(vision_list[i])))
                    dic_Z=Counter(graph)
                for i in dic_Z.keys():
                    var=i.split(',')
                    gene_map[int(var[0])][int(var[1])]=dic_Z[i]
            try:
                cop_gen_avg=np.average(generation_list)
            except:
                print "there are no cops"
            total_genemap_cop_generation.append(cop_gen_avg)
            total_genemap_cops.append(gene_map)
        for event in pygame.event.get():
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_p:
                    pause=True
                if event.key == pygame.K_d:
                    plot=True
        for cop in cops:
            cop.age+=1
            cop.arrest_counter-=0.85
            if cop_evo==True:
                if cop.arrest_counter<=0:
                    cop.die()
            if counter%cop.speed == 0:
                cop.move()
        for rob in robbers:
            rob.age+=1
            if rob.robbing==True:
                rob.incrobcounter()
                if rob.rob_counter>rob.rob_speed:
                    rob.robbing=False
                    rob.rob_counter=0
            elif counter%rob.speed == 0:
                rob.move()
                rob.money -= (25/(rob.speed))**2+1
                if rob.money<=0:
                    rob.die()
        for civ in civilians:
            if counter%civ.speed == 0:
                civ.move()
        for house in Gotham.houses:
            if house.beingrobbed==True:
                house.inccounter()
                if house.counter>=house.robtime:
                    house.beingrobbed=False
                    Gotham.size-=1
                    house.robbed=True
            elif house.robbed==True:
                house.inccounter()
                if house.counter>200:
                    Gotham.size+=1
                    house.revive()
        counter+=1
        screen.fill(BLACK)
        robs = len(robbers)
        civs = len(civilians)
        coppers= len(cops)
        if extinction==False:
            if robs==0:
                print "rob extinction after ", counter, "iterations"
                pause=True
                extinction=True
            if coppers==0:
                print "cop extinction after ", counter, "iterations"
                pause=True
                extinction=True
        num_houses.append(Gotham.size)
        num_robbers.append(robs)
        num_civs.append(civs)
        num_cops.append(coppers)
        if plot==True:
            gen_list=[]
            for rob in robbers:
                gen_list.append(rob.generation)
            for row in range(grid_x):
                for column in range(grid_y):
                    if grid[row][column]==1:
                        color = BLUE
                        shape="sq"
                    elif grid[row][column] ==0:
                        color = BLACK
                        shape="sq"
                    elif isinstance( grid[row][column], int )!=True: #should replace with try.
                        if grid[row][column].coprob == "cop":
                            if len(grid[row][column].route)>1:
                                color=BLUE
                            else:
                                color = GREEN
                            shape="c"
                        elif grid[row][column].coprob=="rob":
                            if grid[row][column].robbing==True:
                                color=BLACK
                            elif len(grid[row][column].route)>1:
                                color=ORANGE
                            else:
                                color=RED
                            shape="c"
                        elif grid[row][column].coprob =="hous":
                            if grid[row][column].robbed==True:
                                color=GREY
                                shape="sq"
                            elif grid[row][column].beingrobbed==True:
                                shape="csq"
                            else:
                                color=PURPLE
                                shape="sq"
                        elif grid[row][column].coprob == "civ":
                            color=WHITE
                            shape="c"
                    if shape=="c":
                        pygame.draw.ellipse(screen,
                                    color,
                                    [(margin+width)*column+margin,
                                    (margin+height)*row+margin,
                                    width,height])
                    if shape=="sq":
                        pygame.draw.rect(screen,
                                    color,
                                    [(margin+width)*column+margin,
                                    (margin+height)*row+margin,
                                    width,height])
                    if shape=="csq":
                        pygame.draw.rect(screen,
                                    ORANGE,
                                    [(margin+width)*column+margin,
                                    (margin+height)*row+margin,
                                    width,height])
                        pygame.draw.ellipse(screen,
                                    RED,
                                    [(margin+width)*column+margin,
                                    (margin+height)*row+margin,
                                    width,height])
            try:
                label = myfont.render('Generation:%s' % int(np.average(gen_list)), 1, (255,255,0))
            except ValueError:
                label = myfont.render('Generation:NaN', 1, (255,255,0))
            screen.blit(label, (0, 0))
        pygame.display.flip()

pygame.quit()
pl.show()