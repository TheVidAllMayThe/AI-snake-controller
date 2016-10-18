import copy

class State:
    def __init__(self,maze,p):
        self.obstacles = maze.obstacles
        self.player = p.body 
        self.opponent = [ pos for pos in maze.playerpos if pos != self.player[0] ]
        self.foodpos = maze.foodpos
        self.mapsize = p.mapsize
        self.playerDead = False
        self.opponentDead = False
        self.playerPoints = [ points[1] for points in p.lpoints if points[0] == p.name ][0] 
        self.opponentPoints = [ points[1] for points in p.lpoints if points[0] != p.name][0]

    #Given an action of the player returns the resulting state
    def playerResult(self,action):
        assert not self.playerDead, "playerResult when player is dead"
        newState = copy.deepcopy(self)
        #updates the snake...
        head=newState.player[0]#head of snake
        head=(head[0]+action[0],head[1]+action[1])
        #wrap the snake around the window
        headx=self.mapsize[0] if head[0]<0 else 0 if head[0]>self.mapsize[0] else head[0]
        heady=self.mapsize[1] if head[1]<0 else 0 if head[1]>self.mapsize[1] else head[1]
        head=(headx,heady)
        #update the body and see if the snake is dead
        if head in self.player:
            newState.playerDead = True
            return newState
        
        if head in self.opponent:
            if head == self.opponent[0]:
                newState.opponentDead = True
            newState.playerDead = True
            return newState

        if head in self.obstacles:#hit an obstacle
            newState.playerDead = True
            return newState

        elif head == self.foodpos:
            #the snake ate the food
            #self.foodpos=0,0
            newState.player.append((newState.player[0]))
            newState.playerPoints += 10
        #the snake hasnot collided....move along
        newState.player=[head]+newState.player[:-1]

        return newState

    #Given an action of the opponent returns the resulting state
    def opponentResult(self,action):
        assert not self.opponentDead, "opponentResult when opponent is dead"
        newState = copy.deepcopy(self)
        #updates the snake...
        head=newState.opponent[0]#head of snake
        head=(head[0]+action[0],head[1]+action[1])
        #wrap the snake around the window
        headx=self.mapsize[0] if head[0]<0 else 0 if head[0]>self.mapsize[0] else head[0]
        heady=self.mapsize[1] if head[1]<0 else 0 if head[1]>self.mapsize[1] else head[1]
        head=(headx,heady)
        #update the body and see if the snake is dead
        if head in self.opponent:
            newState.opponentDead = True
            return newState
        
        if head in self.player:
            if head == self.player[0]:
                newState.playerDead = True
            newState.opponentDead = True
            return newState

        if head in self.obstacles:#hit an obstacle
            newState.opponentDead = True
            return newState
        elif head == self.foodpos:
            #the snake ate the food
            #self.foodpos=0,0
            newState.opponent.append((newState.opponent[0]))
            newState.opponentPoints += 10
        #the snake hasnot collided....move along
        newState.opponent=[head]+newState.opponent[:-1]
        return newState
