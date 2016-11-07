from snake import Snake
from constants import *
from heapq import *
from node import Node
from functools import reduce

class StudentAgent(Snake):
    def __init__(self, body=[(0,0)] , direction=(1,0)):
        super().__init__(body,direction,name="HouseCleaning")
        self.oldPoints = 0

    def update(self,points=None, mapsize=None, count=None):
            self.nOpponents = len(points) - 1
            self.mapsize = mapsize
            if self.nOpponents == 0:
                self.opponentPoints = 0
            else:
                self.opponentPoints = [ x[1] for x in points if x[0] != self.name ][0]

    def updateDirection(self,maze):
        if self.oldPoints > self.points:
            print("fuck")
        self.oldPoints = self.points
        studentAgent = self.body
        opponentsAgents = [x for x in maze.playerpos if x not in self.body]
        obstacles = maze.obstacles
        foodpos = maze.foodpos
        mazedata = (studentAgent,opponentsAgents,obstacles,foodpos) #Search for food
        oppMazedata = (opponentsAgents,studentAgent,obstacles,foodpos)
        if self.nOpponents > 0 and foodpos in [self.result(oppMazedata,x)[0][0] for x in self.valid_actions(oppMazedata)]:
            actions = self.valid_actions(mazedata)
            if actions != []:
                self.direction = actions[0]
        else:
            finalnode = self.aStar(mazedata)
            self.direction = finalnode.getAction()
            

    def valid_actions(self,mazedata):
            validDirections = []
            occupiedPositions = mazedata[2] + mazedata[1][:-1] + mazedata[0]
            directions = (up, down, right, left)
            if self.nOpponents != 0 and self.points < self.opponentPoints:
                for x in directions: #Remover casos de colisão caso estejamos a perder
                    newX = (mazedata[1][0][0]+x[0])%(self.mapsize[0]+1)
                    newY = (mazedata[1][0][1]+x[1])%(self.mapsize[1]+1)
                    occupiedPositions += [(newX, newY)]
            for x in directions:
                newX = (mazedata[0][0][0]+x[0])%(self.mapsize[0]+1)
                newY = (mazedata[0][0][1]+x[1])%(self.mapsize[1]+1)
                if (newX, newY) not in occupiedPositions:
                    validDirections += [x]
            return validDirections

    def distance(self,pos1, pos2):
        return 10*min(abs(pos2[0]-pos1[0]), (self.mapsize[0])-1-abs(pos2[0]-pos1[0]))  +  min(abs(pos2[1]-pos1[1]), self.mapsize[1]-1-abs(pos2[1]-pos1[1]))

    def isGoal(self,mazedata):
        blocksWay = False
        if self.nOpponents > 0:
            oppMazedata = (mazedata[1],mazedata[0],mazedata[2],mazedata[3])
            blocksWay = any([self.valid_actions(self.result(oppMazedata, x)) == [] for x in self.valid_actions(oppMazedata)])
        return mazedata[0][0] == mazedata[3] or blocksWay

    def result(self,mazedata, action):
        newX = (mazedata[0][0][0]+action[0])%(self.mapsize[0]+1)
        newY = (mazedata[0][0][1]+action[1])%(self.mapsize[1]+1)
        playerpos = [(newX, newY)]
        playerpos += mazedata[0][:-1]
        return (playerpos,mazedata[1],mazedata[2],mazedata[3])

    def aStar(self, mazedata):

        node = Node(mazedata, 0, self.distance(mazedata[0][0],mazedata[3]),self.direction,None)
        frontier = []
        heappush(frontier, node)
        explored = []
        depth = 0
        while depth < 40:
            depth += 1
            if frontier == []:
                return node

            node = heappop(frontier)

            if self.isGoal(node.maze):
                return node

            if node.maze[0][0] not in explored:
                explored += [node.maze[0][0]]
            for x in self.valid_actions(node.maze):
                result = self.result(node.maze,x)
                child = Node(result ,node.costG+1,self.distance(result[0][0],result[3]),x,node)

                if child.maze[0][0] not in explored and child not in frontier:
                    heappush(frontier,child)

                elif [x for x in frontier if x == child and x.costG > child.costG] != []:
                    frontier.remove(child)
                    heappush(frontier,child)
        return node
