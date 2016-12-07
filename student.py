from snake import Snake
from constants import *
from heapq import *
import pygame
from node import *
from functools import reduce
import time


class Area:
    totalAreas = []

    def __init__(self, minX, maxX, minY, maxY, obstacles, mapsize):
        self.minY = minY
        self.maxY = maxY
        self.minX = minX
        self.maxX = maxX
        self.borders = [ (minX,maxX), (minY,maxY) ]
        self.neighbours = set()
        self.gateways = set()
        self.obstacles = obstacles
        self.mapsize = mapsize

        for x in range(minX, maxX+1):
            for y in range(minY, maxY+1):
                Area.totalAreas += [(x, y)]

    def __eq__(self, other):
        return self.borders == other.borders

    def __hash__(self):
        return hash(tuple(self.borders))

    def getNeighbour(self, areas, coord):
        if coord in self.obstacles:
            return None

        for area in areas:
            if area.isIn(coord):
                return area


    def getneighbours(self, areas):

        current_neighbour = None
        count = 0

        for y in range(self.minY,self.maxY+1):
            neighbour = self.getNeighbour(areas, ((self.minX-1) % self.mapsize[0], y))

            if neighbour is not None and neighbour not in self.neighbours:
                self.neighbours.add(neighbour)
                self.gateways.add(((self.minX, y), left))

                if current_neighbour is not None:
                    self.gateways.add(((self.minX, y-1), left))

                current_neighbour = neighbour
                count = 0

            if neighbour is None:
                if current_neighbour is not None:
                    self.gateways.add(((self.minX, y-1), left))
                current_neighbour = None
                count = 0

            if neighbour == current_neighbour:
                count += 1
                if count % 4 == 0:
                    if ((self.minX - 1, y), left) not in self.obstacles:
                        self.gateways.add(((self.minX, y), left))
                    elif ((self.minX - 1, y-1), left) not in self.obstacles:
                        self.gateways.add(((self.minX, y - 1), left))
                    elif ((self.minX - 1, y + 1), left) not in self.obstacles:
                        self.gateways.add(((self.minX, y + 1), left))


            neighbour = self.getNeighbour(areas,((self.maxX+1) % self.mapsize[0],y))
            if neighbour is not None and neighbour not in self.neighbours:
                self.neighbours.add(neighbour)
                self.gateways.add(((self.maxX, y), right))

        for x in range(self.minX, self.maxX+1):
            neighbour = self.getNeighbour(areas, (x, (self.minY-1) % self.mapsize[1]))
            if neighbour is not None and neighbour not in self.neighbours:
                self.neighbours.add(neighbour)
                self.gateways.add(((x, self.minY), up))
            neighbour = self.getNeighbour(areas, (x, (self.maxY+1) % self.mapsize[1]))
            if neighbour is not None and neighbour not in self.neighbours:
                self.neighbours.add(neighbour)
                self.gateways.add(((x, self.maxY), down))

    def __str__(self):
        neighbours = "["
        for x in self.neighbours:
            neighbours += " ((" + str(x.minX) + "," + str(x.maxX) + ")" + "(" + str(x.minY) + "," + str(x.maxY) +")) "
        neighbours += "]"
        return "Borders: "+str(self.borders)+" Gateways: "+str(self.gateways) + "\n" + "Neighbours: " + neighbours

    def __lt__(self, other):
        return self.borders[0][0] <= other.borders[0][0] if self.borders[0][0] != other.borders[0][0] else self.borders[1][0] <= other.borders[1][0]

    def isIn(self, pos):
        return pos[0] in range(self.borders[0][0],self.borders[0][1]+1) and pos[1] in range(self.borders[1][0],self.borders[1][1]+1)


class student(Snake):

    def __init__(self, body=[(0, 0)], direction=(1,0),name="Pizza Boy aka Robot"):
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
            #Fill dead ends
            cenas1 = len(self.obstacles)
            actions = [up, right, down, left]
            for x,y in [ (x,y) for x in range(0,self.mapsize[0]) for y in range(0,self.mapsize[1]) if (x,y) not in self.obstacles ]:
                l = [ ((x+a[0])%self.mapsize[0],(y+a[1])%self.mapsize[1]) for a in actions if ((x+a[0])%self.mapsize[0],(y+a[1])%self.mapsize[1]) not in self.obstacles ] 
                if len(l) == 1:
                    self.obstacles += [(x,y)]
                    lt = l[:]
                    xt = x
                    yt = y
                    while True:
                        xt,yt = ((xt+lt[0][0])%self.mapsize[0], (yt+lt[0][1])%self.mapsize[1])
                        lt = [ ((xt+a[0])%self.mapsize[0],(yt+a[1])%self.mapsize[1]) for a in actions if ((xt+a[0])%self.mapsize[0],(yt+a[1])%self.mapsize[1]) not in self.obstacles ] 
                        if len(lt) != 1:
                            break
                        else:
                            self.obstacles += [(xt,yt)]
            print(len(self.obstacles)-cenas1)

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


            for area in self.areas:
                area.getneighbours(self.areas)            

        goal = self.highLevelSearch(self.body[0],maze.foodpos)
        opponentAgent = [x for x in maze.playerpos if x not in self.body]
        mazedata = (self.body[:],opponentAgent,self.obstacles[:],goal) #Search for food
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

    def deadend(self,mazedata):
        actions = self.valid_actions(mazedata,self.points,self.opponentPoints)
        if len(actions) > 1:
            return False
        return all([self.result(mazedata,x) for x in actions])

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
            if x.isIn(foodpos):
                food_pos_square = x
            if x.isIn(head):
                square = x

        if food_pos_square == square:
            return foodpos

        node = HiNode((head, (0, 0)), 0, self.distance(head,foodpos), None, square, self.mapsize)

        frontier = []
        heappush(frontier, node)
        explored = []

        while (pygame.time.get_ticks() - s) < (self.agent_time*0.3):
            if not frontier:
                return None

            node = heappop(frontier)

            if node.square == food_pos_square:
                return node.getPlace()

            if node.get_gateway_result() not in explored:
                explored += [node.gateway]

            for x in node.square.gateways:
                newPlace = ((x[0][0]+x[1][0]) % self.mapsize[0], (x[0][1]+x[1][1]) % self.mapsize[1])

                for neighbour in node.square.neighbours:
                    if neighbour.isIn(newPlace):
                        square = neighbour

                child = HiNode(x, node.costG + self.distance(node.get_gateway_result(),newPlace), self.distance(newPlace, foodpos), node, square, self.mapsize)
                if x not in explored and child not in frontier:
                    heappush(frontier,child)

                elif [x for x in frontier if x == child and x.costG > child.costG]:
                    frontier.remove(child)
                    heappush(frontier,child)
        return foodpos

    def aStar(self, mazedata):
        s = pygame.time.get_ticks()
        actions = self.valid_actions(mazedata,self.points,self.opponentPoints)
        node = Node(mazedata, 0, 2*self.distance(mazedata[0][0],mazedata[3]),actions[0] if actions != [] else self.direction,None)
        frontier = []
        heappush(frontier, node)
        explored = []
        while (pygame.time.get_ticks() - s) < (self.agent_time*0.65):
            if frontier == []:
                return node
            node = heappop(frontier)

            if self.isGoal(node.maze) and self.valid_actions(self.result(mazedata,node.getAction()),self.points,self.opponentPoints) != []:
                return node

            if node.maze[0][0] not in explored:
                explored += [(node.maze[0][0], node.action)]
            for x in self.valid_actions(node.maze, self.points,self.opponentPoints):
                result = self.result(node.maze, x)
                child = Node(result, node.costG + 1, 2*self.distance(result[0][0], result[3]), x, node)


                if (child.maze[0][0], child.action) not in explored and child not in frontier:
                    heappush(frontier, child)


                elif [x for x in frontier if x == child and x.costG > child.costG] != []:
                    frontier.remove(child)
                    heappush(frontier, child)

        return node
