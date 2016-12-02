from snake import Snake
from constants import *
from heapq import *
import pygame
from node import Node
from functools import reduce

class Area:
    totalAreas = []
    def __init__(self,minX,maxX,minY,maxY,obstacles,mapsize):
        self.borders = [ (minX,maxX), (minY,maxY) ]
        self.gateways = {}
        #Upper gateway
        temp = []
        for x in range(minX,maxX+1):
            if (x,minY) not in obstacles and (x, (minY - 1)%mapsize[1]) not in obstacles and x != maxX:
                temp += [(x,minY)]
            elif temp == []:
                pass
            elif len(temp) > 5:
                self.gateways[temp[0]] = up
                self.gateways[temp[-1]] = up
                temp = []
            else:
                self.gateways[temp[len(temp)//2]] = up
                temp = []

        #Lower gateway
        temp = []
        for x in range(minX,maxX+1):
            if (x,maxY) not in obstacles and (x, (maxY + 1)%mapsize[1]) not in obstacles and x != maxX:
                temp += [(x,maxY)]
            elif temp == []:
                pass
            elif len(temp) > 5:
                self.gateways[temp[0]] = down
                self.gateways[temp[-1]] = down
                temp = []
            else:
                self.gateways[temp[len(temp)//2]] = down
                temp = []

        #Left gateway
        temp = []
        for y in range(minY,maxY+1):
            if (minX,y) not in obstacles and ((minX - 1)%mapsize[0], y) not in obstacles and y != maxY:
                temp += [(minX,y)]
            elif temp == []:
                pass
            elif len(temp) > 5:
                self.gateways[temp[0]] = left
                self.gateways[temp[-1]] = left
                temp = []
            else:
                self.gateways[temp[len(temp)//2]] = left
                temp = []

        #Right gateway
        temp == []
        for y in range(minY,maxY+1):
            if (maxX,y) not in obstacles and ((maxX + 1)%mapsize[0], y) not in obstacles and y != maxY:
                temp += [(maxX,y)]
            elif temp == []:
                pass
            elif len(temp) > 5:
                self.gateways[temp[0]] = right
                self.gateways[temp[-1]] = right
                temp = []
            else:
                self.gateways[temp[len(temp)//2]] = right
                temp = []

        for x in range(minX,maxX+1):
            for y in range(minY,maxY+1):
                Area.totalAreas += [(x,y)]

        self.dists = {(x,y):abs(x[0]-y[0])+abs(x[1]-y[1]) for x in self.gateways.keys() for y in self.gateways.keys() if x!=y}


    def __str__(self):
        return "Borders: "+str(self.borders)+" Gateways: "+str(self.gateways) + "\n"

    def __lt__(self, other):
        return self.borders[0][0] <= other.borders[0][0] if self.borders[0][0] != other.borders[0][0] else self.borders[1][0] <= other.borders[1][0]

    def isIn(self,pos):
        return pos[0] in range(self.borders[0][0],self.borders[0][1]+1) and pos[1] in range(self.borders[1][0],self.borders[1][1]+1)


class student(Snake):
    def __init__(self, body=[(0,0)] , direction=(1,0),name="Pizza Boy aka Robot"):
        super().__init__(body,direction,name=name)
        self.node = None
        self.areas = [];


    def update(self,points=None, mapsize=None, count=None, agent_time=None):
        self.agent_time = agent_time
        self.nOpponents = len(points) - 1
        self.mapsize = mapsize
        if self.nOpponents == 0:
            self.opponentPoints = 0
        else:
            self.opponentPoints = [x[1] for x in points if x[0] != self.name][0]

    def updateDirection(self,maze):
        ratio = 5
        self.obstacles = maze.obstacles[:]

        if self.areas == []:
            mapsizex4 = self.mapsize[0]//ratio
            mapsizey4 = self.mapsize[1]//ratio
            remx = self.mapsize[0]%ratio
            remy = self.mapsize[1]%ratio
            for y in range(0,self.mapsize[1]):
                for x in range(0,self.mapsize[0]):
                    if (x,y) not in Area.totalAreas and (x,y) not in self.obstacles:
                        xloopstart = x
                        xloopend = -1
                        for x2 in range(xloopstart, self.mapsize[0]):
                            if (x2,y) in self.obstacles:
                                xloopend = x2-1
                                break
                        xloopend = xloopend if xloopend != -1 else self.mapsize[0]-1
                        yloopstart = y
                        yloopend = -1
                        breakPoint = False
                        for y2 in range(yloopstart,self.mapsize[1]):
                            for x2 in range(xloopstart, xloopend + 1):
                                if (x2,y2) in self.obstacles or (x2,y2) in Area.totalAreas:
                                    yloopend = y2 - 1
                                    breakPoint = True
                                    breakPoint
                            if breakPoint == True:
                                break
                        yloopend = yloopend if yloopend != -1 else self.mapsize[1] - 1
                        self.areas += [Area(xloopstart,xloopend,yloopstart,yloopend,self.obstacles,self.mapsize)]
                        print(self.areas[-1])
                        input()

            for x in range(0,self.mapsize[0]):
                for y in range(0,self.mapsize[1]):
                    if (x,y) not in Area.totalAreas + self.obstacles:
                        print((x,y))


        """
            for x in range(0,ratio):
                for y in range(0,ratio):
                    self.areas += [ Area(x*mapsizex4,(x+1)*mapsizex4-1,y*mapsizey4,(y+1)*mapsizey4-1,maze.obstacles,self.mapsize) ]
                if remx != 0:
                    self.areas += [ Area(self.mapsize[0]-remx,self.mapsize[0]-1,x*mapsizey4,(x+1)*mapsizey4-1,maze.obstacles,self.mapsize) ]
                if remy != 0:
                    self.areas += [ Area(x*mapsizex4,(x+1)*mapsizex4-1,self.mapsize[1]-remy,self.mapsize[1]-1,maze.obstacles,self.mapsize) ]

            if remx!= 0 and remy != 0:
                self.areas += [ Area(self.mapsize[0]-remx,self.mapsize[0]-1,self.mapsize[1]-remy,self.mapsize[1]-1,maze.obstacles,self.mapsize) ]

            self.areas.sort() #///////////////REMOVER DEPOIS///////////////////////////////////

        goal = None

        for x in self.areas:
            if x.isIn(maze.foodpos) and x.isIn(self.body[0]):
                goal = maze.foodpos
                break
            if x.isIn(self.body[0]):
                headSquare = x

        if goal == None:
            goal = self.highLevelSearch(self.body[0],maze.foodpos).getAction()
        """
        input()


        goal = maze.foodpos
        opponentAgent = [x for x in maze.playerpos if x not in self.body]
        mazedata = (self.body[:],opponentAgent,maze.obstacles[:],goal) #Search for food
        finalNode = self.aStar(mazedata)
        self.direction = finalNode.getAction()

    def valid_actions(self,mazedata,points,oppPoints):
            validDirections = []
            occupiedPositions = mazedata[2] + mazedata[1][:-1] + mazedata[0]
            directions = (up, down, right, left)
            if self.nOpponents != 0 and points <= oppPoints:
                for x in directions: #Remover casos de colisão caso estejamos a perder
                    occupiedPositions += [((mazedata[1][0][0]+x[0])%self.mapsize[0], (mazedata[1][0][1]+x[1])%self.mapsize[1])]
            for x in directions:
                if ((mazedata[0][0][0]+x[0])%self.mapsize[0], (mazedata[0][0][1]+x[1])%self.mapsize[1]) not in occupiedPositions:
                    validDirections += [x]
            return validDirections

    def distance(self,pos1, pos2):
        return min(abs(pos2[0]-pos1[0]), (self.mapsize[0])-1-abs(pos2[0]-pos1[0]))  +  min(abs(pos2[1]-pos1[1]), self.mapsize[1]-1-abs(pos2[1]-pos1[1]))

    def isGoal(self,mazedata):
        oppActions = [False]
        if self.nOpponents > 0:
            oppMazedata = (mazedata[1],mazedata[0],mazedata[2],mazedata[3])
            oppActions = [self.valid_actions(self.result(oppMazedata,x),self.opponentPoints,self.points) == [] for x in self.valid_actions(oppMazedata,self.opponentPoints,self.points)]
        return mazedata[0][0] == mazedata[3] or any(oppActions)

    def result(self,mazedata, action):
        newX = (mazedata[0][0][0]+action[0]+self.mapsize[0])%(self.mapsize[0])
        newY = (mazedata[0][0][1]+action[1]+self.mapsize[1])%(self.mapsize[1])
        playerpos = [(newX, newY)]
        playerpos += mazedata[0][:-1]
        mazedata = (playerpos,mazedata[1],mazedata[2],mazedata[3])
        return mazedata

    def highLevelSearch(self,head,foodpos):
        node = Node(head, 0, self.distance(head,foodpos), None, None)
        frontier = []
        heappush(frontier, node)
        explored = []
        square = None
        while True:
            if frontier == []:
                return None

            node = heappop(frontier)
            for x in self.areas:
                if x.isIn(node.maze):
                    square = x
                    break
            actions = square.gateways
            if square.isIn(foodpos):
                return node

            if node.maze not in explored:
                explored += [node.maze]

            for x in actions.keys():
                head = (((x[0] + actions[x][0])%self.mapsize[0]), ((x[1] + actions[x][1])%self.mapsize[1]))
                print(square.dists)
                dist = square.dists[head,node.maze] if (head,node.maze) in square.dists else square.dists[node.maze,head]
                child = Node(head, node.costG + dist, self.distance(head,foodpos), head, node)

                if head not in explored and child not in frontier:
                    heappush(frontier,child)

                elif [x for x in frontier if x == child and x.costG > child.costG] != []:
                    frontier.remove(child)
                    heappush(frontier,child)

    def aStar(self, mazedata):
        s = pygame.time.get_ticks()
        actions = self.valid_actions(mazedata,self.points,self.opponentPoints)
        node = Node(mazedata, 0, self.distance(mazedata[0][0],mazedata[3]),actions[0] if actions != [] else self.direction,None)
        frontier = []
        heappush(frontier, node)
        explored = []
        while (pygame.time.get_ticks() - s) < (self.agent_time*0.9):
            if frontier == []:
                return node
            node = heappop(frontier)

            if self.isGoal(node.maze) and self.valid_actions(self.result(mazedata,node.getAction()),self.points,self.opponentPoints) != []:
                return node

            if node.maze[0][0] not in explored:
                explored += [(node.maze[0][0],node.action)]
            for x in self.valid_actions(node.maze,self.points,self.opponentPoints):
                result = self.result(node.maze,x)
                child = Node(result ,node.costG+1,self.distance(result[0][0],result[3]),x,node)

                if (child.maze[0][0],child.action) not in explored and child not in frontier:
                    heappush(frontier,child)

                elif [x for x in frontier if x == child and x.costG > child.costG] != []:
                    frontier.remove(child)
                    heappush(frontier,child)

        return node
