from snake import Snake
from constants import *
from heapq import *
import pygame
from node import *
from functools import reduce

class Area:
    totalAreas = []
    def __init__(self,minX,maxX,minY,maxY,obstacles,mapsize):
        self.minY = minY
        self.maxY = maxY
        self.minX = minX
        self.maxX = maxX
        self.borders = [ (minX,maxX), (minY,maxY) ]
        self.neighbours = {}
        self.gateways = {}
        self.mapsize = mapsize
        self.obstacles = obstacles
        #Upper gateway
        """
        for x in range(minX,maxX+1):
            if x == maxX and (maxX,(minY+up[1])%mapsize[1]) not in obstacles:
                self.gateways[(maxX,minY)] = [up] if (maxX,minY) not in self.gateways else self.gateways[(maxX,minY)] + [up]
            elif (x-minX)%4 == 0:
                if (x,(minY+up[1])%mapsize[1]) not in obstacles:
                    self.gateways[(x,minY)] = [up] if (x,minY) not in self.gateways else self.gateways[(maxX,minY)] + [up]
                elif x-1 > minX and (x-1,(minY+up[1])%mapsize[1])  not in obstacles:
                    self.gateways[(x-1,minY)] = [up] if (x-1,minY) not in self.gateways else self.gateways[(x-1,minY)] + [up]
                elif x+1 < maxX and (x+1,(minY+up[1])%mapsize[1])  not in obstacles:
                    self.gateways[(x+1,minY)] = [up] if (x+1,minY) not in self.gateways else self.gateways[(x+1,minY)] + [up]

        #Lower gateway
        for x in range(minX,maxX+1):
            if x == maxX and (maxX,(maxY + down[1])%mapsize[1])  not in obstacles:
                self.gateways[(maxX,maxY)] = [down] if (maxX,maxY) not in self.gateways else self.gateways[(maxX,maxY)] + [down]
            elif (x-minX)%4 == 0:
                if (x,(maxY + down[1])%mapsize[1]) not in obstacles:
                    self.gateways[(x,maxY)] = [down] if (x,maxY) not in self.gateways else self.gateways[(x,maxY)] + [down]
                elif x-1 > minX and (x-1,(maxY + down[1])%mapsize[1])  not in obstacles:
                    self.gateways[(x-1,maxY)] = [down] if (x-1,maxY) not in self.gateways else self.gateways[(x-1,maxY)] + [down]
                elif x+1 < maxX and (x+1,(maxY + down[1])%mapsize[1])  not in obstacles:
                    self.gateways[(x+1,maxY)] = [down] if (x+1,maxY) not in self.gateways else self.gateways[(x+1,maxY)] + [down]

        #Left gateway
        for y in range(minY,maxY+1):
            if y == maxY and ((maxX+left[0])%mapsize[0],maxY) not in obstacles:
                self.gateways[(maxX,maxY)] = [left] if (maxX,maxY) not in self.gateways else self.gateways[(maxX,maxY)] + [left]
            elif (y-minY)%4 == 0:
                if ((maxX+left[0])%mapsize[0],y) not in obstacles:
                    self.gateways[(maxX,y)] = [left] if (maxX,y) not in self.gateways else self.gateways[(maxX,y)] + [left]
                elif y-1 > minY and ((maxX+left[0])%mapsize[0],y-1) not in obstacles:
                    self.gateways[(maxX,y-1)] = [left] if (maxX,y-1) not in self.gateways else self.gateways[(maxX,y-1)] + [left]
                elif y+1 < maxY and ((maxX+left[0])%mapsize[0],y+1) not in obstacles:
                    self.gateways[(maxX,y+1)] = [left] if (maxX,y+1) not in self.gateways else self.gateways[(minY,y+1)] + [left]

        #Right gateway
        for y in range(minY,maxY+1):
            if y == maxY and ((minX+right[0])%mapsize[0],maxY) not in obstacles:
                self.gateways[(minX,maxY)] = [right] if (minX,maxY) not in self.gateways else self.gateways[(minX,maxY)] + [right]
            elif (y-minY)%4 == 0:
                if ((minX+right[0])%mapsize[0],y) not in obstacles:
                    self.gateways[(minX,y)] = [right] if (minX,y) not in self.gateways else self.gateways[(minX,y)] + [right]
                elif y-1 > minY and ((minX+right[0])%mapsize[0],y-1) not in obstacles:
                    self.gateways[(minX,y-1)] = [right] if (minX,y-1) not in self.gateways else self.gateways[(minX,y-1)] + [right]
                elif y+1 < maxY and ((minX+right[0])%mapsize[0],y+1) not in obstacles:
                    self.gateways[(minX,y+1)] = [right] if (minX,y+1) not in self.gateways else self.gateways[(minY,y+1)] + [right]
        """

        for x in range(minX,maxX+1):
            for y in range(minY,maxY+1):
                Area.totalAreas += [(x,y)]

    def getNeighbour(self, areas, coord):
        if coord in self.obstacles:
            return None

        for area in areas:
            if area.isIn(coord) and area != self:
                return area

        return None


    def getneighbours(self, areas):
        self.neighbours = set([area for x in self.gateways.keys() for y in self.gateways[x] for area in areas if area.isIn((x[0]+y[0],x[1]+y[1]))])

        for y in range(self.minY,self.maxY+1):
            neighbour = self.getNeighbour(areas,((self.minX-1)%self.mapsize[0],y))
            if neighbour != None and neighbour not in self.neighbours:
                self.neighbours.add(neighbour)
                self.gateways[(self.minX,y)] = self.gateways[(self.minX,y)] + [left] if (self.minX,y) in self.gateways else [left]
            neighbour = self.getNeighbour(areas,((self.maxX+1)%self.mapsize[0],y))
            if neighbour != None and neighbour not in self.neighbours:
                self.neighbours.add(neighbour)
                self.gateways[(self.maxX,y)] = self.gateways[(self.maxX,y)] + [right] if (self.maxX,y) in self.gateways else [right]

        for x in range(self.minX,self.maxX+1):
            neighbour = self.getNeighbour(areas,(x,(self.minY-1)%self.mapsize[1]))
            if neighbour != None and neighbour not in self.neighbours:
                self.neighbours.add(neighbour)
                self.gateways[(x,self.minY)] = self.gateways[(x,self.minY)] + [down] if (x,self.minY) in self.gateways else [down]
            neighbour = self.getNeighbour(areas,(x,(self.maxY+1)%self.mapsize[1]))
            if neighbour != None and neighbour not in self.neighbours:
                self.neighbours.add(neighbour)
                self.gateways[(x,self.maxY)] = self.gateways[(x,self.maxY)] + [up] if (x,self.maxY) in self.gateways else [up]


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
            for y in range(0,self.mapsize[1]):
                for x in range(0,self.mapsize[0]):
                    if (x,y) not in Area.totalAreas and (x,y) not in self.obstacles:
                        xloopstart = x
                        xloopend = -1
                        for x2 in range(xloopstart, self.mapsize[0]):
                            if (x2,y) in self.obstacles or (x2,y) in Area.totalAreas:
                                xloopend = x2-1 if x2 != xloopstart else x2
                                break
                        xloopend = xloopend if xloopend != -1 else self.mapsize[0]-1
                        yloopstart = y
                        yloopend = -1
                        for y2 in range(yloopstart,self.mapsize[1]):
                            breakPoint = False
                            for x2 in range(xloopstart, xloopend + 1):
                                if (x2,y2) in self.obstacles or (x2,y2) in Area.totalAreas:
                                    yloopend = y2 - 1 if y2 != yloopstart else y2
                                    breakPoint = True
                                    break
                            if breakPoint == True:
                                break
                        yloopend = yloopend if yloopend != -1 else self.mapsize[1] - 1
                        self.areas += [Area(xloopstart,xloopend,yloopstart,yloopend,self.obstacles,self.mapsize)]
            countgate = 0

            for area in self.areas:
                area.getneighbours(self.areas)

        countgate = 0
        for area in self.areas:
                for x in area.gateways.keys():
                    for y in area.gateways[x]:
                        countgate += len(y)
        print(countgate)

        goal = self.highLevelSearch(self.body[0],maze.foodpos)
        #goal = maze.foodpos
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
        s = pygame.time.get_ticks()
        square = None

        for x in self.areas:
            if x.isIn(head):
                if x.isIn(foodpos):
                    return foodpos
                square = x

        node = HiNode(head, 0, self.distance(head,foodpos), None)

        frontier = []
        heappush(frontier, node)
        explored = []
        first = True
        while True:
            print(square)
            if frontier == []:
                return None

            node = heappop(frontier)

            if not first:
                for x in square.neighbours:
                    if x.isIn(node.place):
                        square = x
                        break

                if square.isIn(foodpos):
                    return node.getPlace()

                first = False

            if node.place not in explored:
                explored += [node.place]

            for y in square.gateways.keys():
                for x in square.gateways[y]:
                    newPlace = ((x[0]+y[0])%self.mapsize[0],(x[1]+y[1])%self.mapsize[1])
                    child = HiNode(newPlace, node.costG + self.distance(node.place, newPlace), self.distance(newPlace,foodpos), node)

                    if newPlace not in explored and child not in frontier:
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
