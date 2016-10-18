from snake import Snake
from constants import *
from heapq import *
from node import Node
from functools import reduce

class StudentAgent(Snake):
	def __init__(self, body=[(0,0)] , direction=(1,0)):
		super().__init__(body,direction,name="Student")

	def update(self,points=None, mapsize=None, count=None):
		self.mapsize = mapsize


	def updateDirection(self,maze):
		studentAgent = self.body
		opponentsAgents = [x for x in maze.playerpos if x != self.body]
		obstacles = maze.obstacles
		foodpos = maze.foodpos
		mazedata = (studentAgent,opponentsAgents,obstacles,foodpos)
		self.direction = self.aStar(mazedata)

	def valid_actions(self,mazedata):
		validDirections = []
		occupiedPositions = reduce(lambda x,y:[x]+[y], mazedata[1]) + mazedata[2] + mazedata[0]
		directions = (up, down, right, left)

		for x in directions:
			if ((mazedata[0][0][0]+x[0])%self.mapsize[0],(mazedata[0][0][1] + x[1])%self.mapsize[1]) not in occupiedPositions:
				validDirections += [x]
		return validDirections


	def distance(self,pos1, pos2):
		return min(abs(pos2[0]-pos1[0]), self.mapsize[0]-1-abs(pos2[0]-pos1[0]))  +  min(abs(pos2[1]-pos1[1]), self.mapsize[1]-1-abs(pos2[1]-pos1[1]))

	def isGoal(mypos, target):
		return mypos == target

	def result(self,mazedata, action):
		playerpos = [((mazedata[0][0][0] + action[0]) % self.mapsize[0],(mazedata[0][0][1] + action[1]) % self.mapsize[1])]
		playerpos += mazedata[:-1]
		return (playerpos,mazedata[1],mazedata[2],mazedata[3])

	def aStar(self, mazedata):
		node = Node(mazedata, 0, self.distance(mazedata[0][0],mazedata[3]),None,None)
		frontier = []
		heappush(frontier, node)
		explored = []
		while True:


			if frontier == []:
				return None
			node = heappop(frontier)

			if StudentAgent.isGoal(node.maze[0][0],node.maze[3]):
				return node.getAction()

			if node.maze not in explored:
				explored += [node.maze]
			for x in self.valid_actions(node.maze):
				result = self.result(node.maze,x)
				child = Node(result ,node.costG+1,self.distance(result[0][0],result[3]),x,node)

				if child.maze not in explored and child not in frontier:
					heappush(frontier,child)

				elif [x for x in frontier if x == child and x.costG > child.costG] != []:
					frontier.remove(child)
					#heapify(frontier)
					heappush(frontier,child)
