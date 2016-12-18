from snake import Snake
from constants import *
from heapq import *
import pygame
from node import *
import random
import math
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
        self.areas = []

        for x in range(minX, maxX+1):
            for y in range(minY, maxY+1):
                self.areas += [(x, y)]

        Area.totalAreas += self.areas

        r = [50, 100, 150, 200, 255]
        g = [40, 90, 140, 190, 245]
        b = [60, 110, 160, 210, 235]

        self.colour = (r[random.randint(0, 4)], g[random.randint(0, 4)], b[random.randint(0, 4)])

    def __eq__(self, other):
        if self is None:
            if other is None:
                return True
            else:
                return False
        else:
            if other is None:
                return False
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

        current_neighbour1 = None
        count1 = 0
        current_neighbour2 = None
        count2 = 0

        for y in range(self.minY, self.maxY+1):
            neighbour = self.getNeighbour(areas, ((self.minX-1) % self.mapsize[0], y))

            if neighbour is not None and neighbour not in self.neighbours:
                self.neighbours.add(neighbour)
                self.gateways.add(((self.minX, y), left))

                if current_neighbour1 is not None:
                    self.gateways.add(((self.minX, y-1), left))

                current_neighbour1 = neighbour
                count1 = 0

            if neighbour is None:
                if current_neighbour1 is not None:
                    self.gateways.add(((self.minX, y-1), left))
                current_neighbour1 = None
                count1 = 0

            elif neighbour == current_neighbour1:
                count1 += 1
                if count1 % 4 == 0:
                    if ((self.minX - 1) % self.mapsize[0], y) not in self.obstacles:
                        self.gateways.add(((self.minX, y), left))
                    elif ((self.minX - 1) % self.mapsize[0], y-1) not in self.obstacles:
                        self.gateways.add(((self.minX, y - 1), left))
                    elif ((self.minX - 1) % self.mapsize[0], y + 1) not in self.obstacles:
                        self.gateways.add(((self.minX, y + 1), left))

            neighbour = self.getNeighbour(areas, ((self.maxX+1) % self.mapsize[0], y))

            if neighbour is not None and neighbour not in self.neighbours:
                self.neighbours.add(neighbour)
                self.gateways.add(((self.maxX, y), right))

                if current_neighbour2 is not None:
                    self.gateways.add(((self.maxX, y-1), right))

                current_neighbour2 = neighbour
                count2 = 0

            if neighbour is None:
                if current_neighbour2 is not None:
                    self.gateways.add(((self.maxX, y - 1), right))
                current_neighbour2 = None
                count2 = 0

            elif neighbour == current_neighbour2:
                count2 += 1
                if count2 % 4 == 0:
                    if ((self.maxX + 1) % self.mapsize[0], y) not in self.obstacles:
                        self.gateways.add(((self.maxX, y), right))
                    elif ((self.maxX + 1) % self.mapsize[0], y - 1) not in self.obstacles:
                        self.gateways.add(((self.maxX, y - 1), right))
                    elif ((self.maxX + 1) % self.mapsize[0], y + 1) not in self.obstacles:
                        self.gateways.add(((self.maxX, y + 1), right))

        current_neighbour1 = None
        count1 = 0
        current_neighbour2 = None
        count2 = 0

        for x in range(self.minX, self.maxX+1):
            neighbour = self.getNeighbour(areas, (x, (self.minY-1) % self.mapsize[1]))

            if neighbour is not None and neighbour not in self.neighbours:
                self.neighbours.add(neighbour)
                self.gateways.add(((x, self.minY), up))

                if current_neighbour1 is not None:
                    self.gateways.add(((x-1, self.minY), up))

                current_neighbour1 = neighbour
                count1 = 0

            if neighbour is None:
                if current_neighbour1 is not None:
                    self.gateways.add(((x-1, self.minY), up))
                current_neighbour1 = None
                count1 = 0

            elif neighbour == current_neighbour1:
                count1 += 1
                if count1 % 4 == 0:
                    if (x, (self.minY - 1) % self.mapsize[1]) not in self.obstacles:
                        self.gateways.add(((x, self.minY), up))
                    elif (x - 1, (self.minY - 1) % self.mapsize[1]) not in self.obstacles:
                        self.gateways.add(((x - 1, self.minY), up))
                    elif (x + 1, (self.minY - 1) % self.mapsize[1]) not in self.obstacles:
                        self.gateways.add(((x + 1, self.minY), up))


            neighbour = self.getNeighbour(areas, (x, (self.maxY+1) % self.mapsize[1]))

            if neighbour is not None and neighbour not in self.neighbours:
                self.neighbours.add(neighbour)
                self.gateways.add(((x, self.maxY), down))
                if current_neighbour2 is not None:
                    self.gateways.add(((x - 1, self.maxY), down))
                current_neighbour2 = neighbour
                count2 = 0

            if neighbour is None:
                if current_neighbour2 is not None:
                    self.gateways.add(((x - 1, self.maxY), down))
                current_neighbour2 = None
                count2 = 0

            elif neighbour == current_neighbour2:
                count2 += 1
                if count2 % 4 == 0:
                    if (x, (self.maxY + 1) % self.mapsize[1]) not in self.obstacles:
                        self.gateways.add(((x, self.maxY), down))
                    elif (x - 1, (self.maxY + 1) % self.mapsize[1]) not in self.obstacles:
                        self.gateways.add(((x - 1, self.maxY), down))
                    elif (x + 1, (self.maxY + 1) % self.mapsize[1]) not in self.obstacles:
                        self.gateways.add(((x + 1, self.maxY), down))

    def __str__(self):
        neighbours = "["
        for x in self.neighbours:
            neighbours += " ((" + str(x.minX) + "," + str(x.maxX) + ")" + "(" + str(x.minY) + "," + str(x.maxY) + ")) "
        neighbours += "]"
        return "Borders: "+str(self.borders)+" Gateways: "+str(self.gateways) + "\n" + "Neighbours: " + neighbours

    def __lt__(self, other):
        return self.borders[0][0] <= other.borders[0][0] if self.borders[0][0] != other.borders[0][0] else self.borders[1][0] <= other.borders[1][0]

    def isIn(self, pos):
        return pos[0] in range(self.borders[0][0],self.borders[0][1]+1) and pos[1] in range(self.borders[1][0],self.borders[1][1]+1)


class student(Snake):

    def __init__(self, body=[(0, 0)], direction=(1,0), name="Pizza Boy aka Robot"):
        super().__init__(body,direction,name=name)

        self.first = True
        self.node = None
        self.areas = [];
        self.current_players_len = 2
        self.first_search = True
        self.old_square = None
        self.current_square = None
        self.food_pos_square = None
        self.frontier = []
        self.explored = []
        self.first_high_search = True
        self.calculated_path = None
        self.calculated = False
        self.game = None
        self.opponent_agent = [-1]
        self.opponent_agent_old_score = 1
        self.opponent_agent_score_change = False
        self.square_size = None
        self.count = 0

    def update(self,points=None, mapsize=None, count=None, agent_time=None, game=None):
        self.agent_time = agent_time
        self.nOpponents = len(points) - 1
        self.mapsize = mapsize
        if self.nOpponents == 0:
            self.opponentPoints = 0
        else:
            self.opponentPoints = [x[1] for x in points if x[0] != self.name][0]
        self.game = game
        self.square_size = int(0.54 * agent_time + 1.7)

        if not self.first and not self.areas:
            #Fill dead ends
            actions = [up, right, down, left]
            for x,y in [ (x,y) for x in range(0,self.mapsize[0]) for y in range(0,self.mapsize[1]) if (x,y) not in self.obstacles ]:
                l = [ a for a in actions if ((x+a[0])%self.mapsize[0],(y+a[1])%self.mapsize[1]) not in self.obstacles ]
                if len(l) == 1:
                    self.obstacles += [(x,y)]
                    lt = l[:]
                    xt = x
                    yt = y
                    while True:
                        xt,yt = ((xt+lt[0][0])%self.mapsize[0], (yt+lt[0][1])%self.mapsize[1])
                        lt = [ a for a in actions if ((xt+a[0])%self.mapsize[0],(yt+a[1])%self.mapsize[1]) not in self.obstacles ]
                        if len(lt) != 1:
                            break
                        else:
                            self.obstacles += [(xt,yt)]

            for y in range(0, self.mapsize[1]):
                for x in range(0, self.mapsize[0]):
                    if (x,y) not in Area.totalAreas and (x,y) not in self.obstacles:
                        xloopstart = x
                        xloopend = -1
                        xcount = 0
                        for x2 in range(xloopstart, self.mapsize[0]):
                            if (x2,y) in self.obstacles or (x2,y) in Area.totalAreas:
                                xloopend = x2-1 if x2 != xloopstart else x2
                                break
                            if xcount == self.square_size:
                                xloopend = x2
                                break
                            xcount += 1

                        xloopend = xloopend if xloopend != -1 else self.mapsize[0]-1
                        yloopstart = y
                        yloopend = -1
                        ycount = 0
                        for y2 in range(yloopstart,self.mapsize[1]):
                            breakPoint = False
                            for x2 in range(xloopstart, xloopend + 1):
                                if (x2,y2) in self.obstacles or (x2, y2) in Area.totalAreas:
                                    yloopend = y2 - 1 if y2 != yloopstart else y2
                                    breakPoint = True
                                    break
                            if breakPoint:
                                break
                            if ycount == self.square_size:
                                yloopend = y2
                                break
                            ycount += 1
                        yloopend = yloopend if yloopend != -1 else self.mapsize[1] - 1
                        self.areas += [Area(xloopstart, xloopend, yloopstart, yloopend, self.obstacles, self.mapsize)]

            for area in self.areas:
                area.getneighbours(self.areas)

    def updateDirection(self,maze):

        self.obstacles = maze.obstacles[:]
        self.opponent_agent_score_change = False
        self.opponent_agent_old_score = len(self.opponent_agent)
        self.opponent_agent = [x for x in maze.playerpos if x not in self.body]

        if self.opponent_agent_old_score != len(self.opponent_agent):
            self.opponent_agent_score_change = True
            self.opponent_agent_old_score = len(self.opponent_agent)

        if len(self.body) + len(self.opponent_agent) != self.current_players_len:
            self.first_search = True
            self.current_players_len = len(self.body) + len(self.opponent_agent)
            self.frontier = []
            self.explored = []
            self.calculated = False
            self.first_high_search = True

        if self.first_search:
            goal = maze.foodpos

        else:
            goal = self.highLevelSearch(self.body[0], maze.foodpos)

        if self.calculated:
            self.count += 1

        #self.game.surface.fill((0, 0, 0))
        """
        for area in self.areas:
            self.game.paint(area.areas, area.colour)
            self.game.paint([x[0] for x in area.gateways], pygame.Color(255, 255, 0))
        """
        deadends = self.deadEnds(self.body,self.opponent_agent,self.obstacles)
        #self.game.paint(deadends, pygame.Color(255,255,255))
        self.mazedata_without_deadends = (self.body, self.opponent_agent, self.obstacles, goal)
        mazedata = (self.body, self.opponent_agent, self.obstacles+deadends,goal) #Search for food

        action = self.aStar(mazedata)
        """
        if self.calculated:
            self.game.paint(self.calculated_path, pygame.Color(255, 255, 255, 255))
        """
        valid_action = None
        if action is None or (self.body[0][0] + action[0], self.body[0][1] + action[1]) in (self.obstacles + self.body + self.opponent_agent):

            num_valid_actions = 0
            for x in self.valid_actions(self.mazedata_without_deadends, 10, 0):
                valid_actions = self.valid_actions(self.result(self.mazedata_without_deadends, x), 10, 0)
                if len(valid_actions) > num_valid_actions:
                    num_valid_actions = len(valid_actions)
                    valid_action = x
            action = valid_action if valid_action is not None else self.direction
        if action is not None:
            self.direction = action

        elif valid_action is None and self.valid_actions(self.mazedata_without_deadends, 10, 0):
            self.direction = self.valid_actions(self.mazedata_without_deadends, 10, 0)[0]
        self.first = False

    def valid_actions(self, mazedata, points, oppPoints):
            validDirections = []
            occupiedPositions = mazedata[2] + mazedata[1] + mazedata[0]
            directions = (up, left, down, right)
            if self.nOpponents != 0 and points <= oppPoints:
                for x in directions:       #Remover casos de colisão caso estejamos a perder
                    occupiedPositions += [((mazedata[1][0][0]+x[0])%self.mapsize[0], (mazedata[1][0][1]+x[1])%self.mapsize[1])]
            for x in directions:
                if ((mazedata[0][0][0]+x[0])%self.mapsize[0], (mazedata[0][0][1]+x[1])%self.mapsize[1]) not in occupiedPositions:
                    validDirections += [x]
            return validDirections

    def deadEnds(self,snake1,snake2,obstacles):
        s = pygame.time.get_ticks()
        actions = [up,down,left,right]
        deadends = []

        for block in snake1[:-1]:
            for x in [ ( ( block[0] + a[0] ) % self.mapsize[0], ( block[1] + a[1] ) % self.mapsize[1] ) for a in actions if ( ( block[0] + a[0] ) % self.mapsize[0], ( block[1] + a[1] ) % self.mapsize[1] ) not in snake1 + snake2 + obstacles + deadends]:

                if pygame.time.get_ticks() - s > self.agent_time * 0.1:
                    #print("not done")
                    return deadends
                l = [ a for a in actions if ( ( x[0] + a[0] ) % self.mapsize[0], ( x[1] + a[1] ) % self.mapsize[1] ) not in obstacles + deadends + snake1[1:] + snake2]
                if len(l) <= 1:
                    deadends += [x] 
                    lt = l[:]
                    xt = x[0]
                    yt = x[1]
                    if l == []:
                        break
                    while pygame.time.get_ticks() - s > self.agent_time * 0.1:
                        xt,yt = ((xt+lt[0][0]) % self.mapsize[0], (yt+lt[0][1])%self.mapsize[1])
                        lt = [a for a in actions if ((xt + a[0]) % self.mapsize[0], (yt + a[1]) % self.mapsize[1]) not in obstacles + deadends + snake1[1:] + snake2]
                        if len(lt) != 1 or (xt,yt) == snake1[0]:
                            break
                        deadends += [(xt,yt)]

        #print("deadEnds ticks: limit - {}   start - {}   end - {}   diff - {}".format(self.agent_time * 0.05, s, pygame.time.get_ticks(), pygame.time.get_ticks() - s))
        #print("done")
        return deadends


    def distance(self, pos1, pos2):
        return ((min(abs(pos2[0]-pos1[0]), (self.mapsize[0])-1-abs(pos2[0]-pos1[0])))**2  +  (min(abs(pos2[1]-pos1[1]), self.mapsize[1]-1-abs(pos2[1]-pos1[1])))**2)**(1/2)

    def isGoal(self, mazedata):
        oppActions = [False]
        if self.nOpponents > 0:
            oppMazedata = (mazedata[1],mazedata[0],mazedata[2],mazedata[3])
            oppActions = [self.valid_actions(self.result(oppMazedata,x),self.opponentPoints,self.points) == [] for x in self.valid_actions(oppMazedata,self.opponentPoints,self.points)]
        return mazedata[0][0] == mazedata[3] or any(oppActions)

    def result(self, mazedata, action):
        newX = (mazedata[0][0][0]+action[0]+self.mapsize[0])%(self.mapsize[0])
        newY = (mazedata[0][0][1]+action[1]+self.mapsize[1])%(self.mapsize[1])
        playerpos = [(newX, newY)]
        playerpos += mazedata[0][:-1]
        mazedata = (playerpos,mazedata[1],mazedata[2],mazedata[3])
        return mazedata

    def highLevelSearch(self, head, foodpos):
        s = pygame.time.get_ticks()
        square = None
        food_pos_square = None

        for x in self.areas:
            if x.isIn(foodpos):
                food_pos_square = x
            if x.isIn(head):
                square = x

        if food_pos_square == square:
            self.count = 0
            self.food_pos_square = food_pos_square
            self.frontier = []
            self.explored = []
            self.calculated = False
            self.first_high_search = True
            return foodpos

        if self.calculated:
            if self.distance(head, self.calculated_path[0]) >= (((self.square_size+2)**2)*2)**(1/2) or self.count == 50:
                self.count = 0
                self.food_pos_square = food_pos_square
                self.frontier = []
                self.explored = []
                self.calculated = False
                self.first_high_search = True
            if head == self.calculated_path[0]:
                self.count = 0
                self.calculated_path = self.calculated_path[1:]
                if not self.calculated_path:
                    self.count = 0
                    self.food_pos_square = food_pos_square
                    self.frontier = []
                    self.explored = []
                    self.calculated = False
                    self.first_high_search = True

            if self.calculated:
                #print("CalculatedPath HighLevel: limit - {}   start - {}   end - {}   diff - {}".format(self.agent_time * 0.05, s, pygame.time.get_ticks(), pygame.time.get_ticks() - s))
                return self.calculated_path[0]

        if self.first_high_search:
            self.food_pos_square = food_pos_square
            self.node = HiNode((head, (0, 0)), 0, self.distance(head, foodpos), None, square, None, self.mapsize)
            heappush(self.frontier, self.node)
            self.first_high_search = False
        else:
            heappush(self.frontier, self.node)

        while (pygame.time.get_ticks() - s) < (self.agent_time*0.60):

            if not self.frontier:
                return None

            self.node = heappop(self.frontier)

            if self.node.square == self.food_pos_square:
                self.calculated_path = self.node.get_complete_path()
                self.calculated = True
                #print("UncalculatedPath HighLevel: limit - {}   start - {}   end - {}   diff - {}".format(self.agent_time * 0.05, s, pygame.time.get_ticks(), pygame.time.get_ticks() - s))
                return self.calculated_path[0]

            if self.node.gateway not in self.explored:
                self.explored += [self.node.gateway]

            for x in self.node.square.gateways:
                newPlace = ((x[0][0]+x[1][0]) % self.mapsize[0], (x[0][1]+x[1][1]) % self.mapsize[1])

                for neighbour in self.node.square.neighbours:
                    if neighbour.isIn(newPlace):
                        square = neighbour

                child = HiNode(x, self.node.costG + self.distance(self.node.get_gateway_result(), newPlace), self.distance(newPlace, foodpos), self.node, square, self.node.square, self.mapsize)
                if x not in self.explored and child not in self.frontier:
                    heappush(self.frontier, child)


                elif [x for x in self.frontier if x == child and x.costG > child.costG]:
                    self.frontier.remove(child)
                    heappush(self.frontier, child)

        #print("WorstCase HighLevel: limit - {}   start - {}   end - {}   diff - {}".format(self.agent_time * 0.05, s, pygame.time.get_ticks(), pygame.time.get_ticks() - s))
        return self.node.getPlace()

    def aStar(self, mazedata, tail=False):
        s = pygame.time.get_ticks()
        actions = self.valid_actions(mazedata, self.points, self.opponentPoints)
        node = Node(mazedata, 0, self.distance(mazedata[0][0], mazedata[3]), actions[0] if actions != [] else self.direction,None)
        frontier = []
        heappush(frontier, node)
        explored = []
        highest_depth_node = node

        if self.calculated:
            limit = self.agent_time*0.30
        else:
            limit = self.agent_time*0.30 if self.first_search else self.agent_time*0.1
            if tail:
                limit = self.agent_time*0.30 if self.first_search else self.agent_time*0.1

        while (pygame.time.get_ticks() - s) < limit:
            if not frontier:
                if tail:
                    #print("Unsuccessfull tail A* Time: limit - {}   start - {}   end - {}   diff - {}".format(self.agent_time * 0.05, s, pygame.time.get_ticks(), pygame.time.get_ticks() - s))
                    return -1
                valid_action = None
                num_valid_actions = 0
                for x in self.valid_actions(self.mazedata_without_deadends,10,0):
                    valid_actions = self.valid_actions(self.result(self.mazedata_without_deadends, x), 10, 0)
                    if len(valid_actions) > num_valid_actions:
                        num_valid_actions = len(valid_actions)
                        valid_action = x

                #print("Unsuccessfull A* Time: limit - {}   start - {}   end - {}   diff - {}\n".format(self.agent_time * 0.05, s, pygame.time.get_ticks(), pygame.time.get_ticks() - s))
                return valid_action

            node = heappop(frontier)
            if node.depth > highest_depth_node.depth:
                highest_depth_node = node

            if self.isGoal(node.maze):
                if tail:
                    #print("Successfull A* Time tail: limit - {}   start - {}   end - {}   diff - {}".format(self.agent_time * 0.05, s, pygame.time.get_ticks(), pygame.time.get_ticks() - s))
                    return 1
                tail_action = self.valid_actions((node.maze[0][::-1], node.maze[1], node.maze[2], node.maze[3]), 10, 0)

                if not tail_action:
                    break
                else:
                    tail_action = tail_action[0]
                if self.aStar((node.maze[0], node.maze[1], node.maze[2], (node.maze[0][-1][0] + tail_action[0], node.maze[0][-1][1] + tail_action[1])), tail=True) != -1:
                    #print("Successfull A* Time: limit - {}   start - {}   end - {}   diff - {}\n".format(self.agent_time * 0.05, s, pygame.time.get_ticks(), pygame.time.get_ticks() - s))

                    return node.getAction()
                else:
                    valid_action = None
                    num_valid_actions = 0
                    for x in self.valid_actions(self.mazedata_without_deadends, 10, 0):
                        valid_actions = self.valid_actions(self.result(self.mazedata_without_deadends, x), 10, 0)
                        if len(valid_actions) > num_valid_actions:
                            num_valid_actions = len(valid_actions)
                            valid_action = x
                    #print("Undetermined A* Time: limit - {}   start - {}   end - {}   diff - {}\n".format(self.agent_time * 0.05, s, pygame.time.get_ticks(), pygame.time.get_ticks() - s))
                    return valid_action

            if node.maze[0][0] not in explored:
                explored += [(node.maze[0][0], node.action)]
            for x in self.valid_actions(node.maze, self.points, self.opponentPoints):
                result = self.result(node.maze, x)
                child = Node(result, node.costG + 1, self.distance(result[0][0], result[3]), x, node)

                if (child.maze[0][0], child.action) not in explored and child not in frontier:
                    heappush(frontier, child)

                elif [x for x in frontier if x == child and x.costG > child.costG]:
                    frontier.remove(child)
                    heappush(frontier, child)
            """
            self.game.paint([x.maze[0][0] for x in frontier], pygame.Color(0, 155, 0))
            self.game.paint([x[0] for x in explored], pygame.Color(155, 0, 0))
            """
        self.first_search = False
        if tail:
            #print("worst case Tail A* Time tail: limit - {}   start - {}   end - {}   diff - {}".format(self.agent_time * 0.05, s,pygame.time.get_ticks(),pygame.time.get_ticks() - s))
            return 0
        #print("Worst Case A* Time: limit - {}   start - {}   end - {}   diff - {}\n".format(self.agent_time * 0.05, s, pygame.time.get_ticks(),pygame.time.get_ticks() - s))
        return node.getAction()

