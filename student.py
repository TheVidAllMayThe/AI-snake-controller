from snake import Snake
from constants import *
from heapq import *
from node import Node
from functools import reduce
import time
class StudentAgent(Snake):
	def __init__(self, body=[(0,0)] , direction=(1,0)):
		super().__init__(body,direction,name="Student")

	def update(self,points=None, mapsize=None, count=None):
            self.nOpponents = len(points) - 1
            self.mapsize = mapsize
            if self.nOpponents == 0:
                self.opponentPoints = 0
            else:
                self.opponentPoints = [ x[1] for x in points if x[0] != self.name ][0]

	def updateDirection(self,maze):
		studentAgent = self.body
		opponentsAgents = [x for x in maze.playerpos if x not in self.body]
		obstacles = maze.obstacles
		foodpos = maze.foodpos
		mazedata = (studentAgent,opponentsAgents,obstacles,foodpos)
		self.direction = self.aStar(mazedata)

	def valid_actions(self,mazedata):
            validDirections = []
            occupiedPositions = mazedata[2] + mazedata[1] + mazedata[0]
            directions = (up, down, right, left)
            if self.points <= self.opponentPoints:
                for x in directions:
                    occupiedPositions += [((mazedata[1][0][0]+x[0])%self.mapsize[0], (mazedata[1][0][1]+x[1])%self.mapsize[1])]
            for x in directions:
                if ((mazedata[0][0][0]+x[0])%self.mapsize[0],(mazedata[0][0][1] + x[1])%self.mapsize[1]) not in occupiedPositions:
                    validDirections += [x]
            return validDirections


	def distance(self,pos1, pos2):
		return 1.5*min(abs(pos2[0]-pos1[0]), self.mapsize[0]-1-abs(pos2[0]-pos1[0]))  +  min(abs(pos2[1]-pos1[1]), self.mapsize[1]-1-abs(pos2[1]-pos1[1]))

	def isGoal(mypos, target):
		return mypos == target

	def result(self,mazedata, action):
		playerpos = [((mazedata[0][0][0] + action[0]) % self.mapsize[0],(mazedata[0][0][1] + action[1]) % self.mapsize[1])]
		playerpos += mazedata[0][:-1]
		return (playerpos,mazedata[1],mazedata[2],mazedata[3])

	def aStar(self, mazedata):

		node = Node(mazedata, 0, self.distance(mazedata[0][0],mazedata[3]),None,None)
		frontier = []
		heappush(frontier, node)
		explored = []
		count = 0

		while True:
			count += 1
			#print(count)
			if frontier == []:
				return None
			node = heappop(frontier)

			if StudentAgent.isGoal(node.maze[0][0],node.maze[3]):
				return node.getAction()

			if node.maze[0][0] not in explored:
				explored += [node.maze[0][0]]
			#print(self.valid_actions(node.maze))
			for x in self.valid_actions(node.maze):
                                result = self.result(node.maze,x)
                                child = Node(result ,node.costG+1,self.distance(result[0][0],result[3]),x,node)

                                if child.maze[0][0] not in explored and child not in frontier:
                                                heappush(frontier,child)

                                elif [x for x in frontier if x == child and x.costG > child.costG] != []:
                                                frontier.remove(child)
                                                heappush(frontier,child)

		return node.getAction()
