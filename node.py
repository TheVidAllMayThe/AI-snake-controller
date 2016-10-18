class Node:
    def __init__(self,maze,cost,expectedCost,action,parent):
        self.maze = maze
        self.cost = cost
        self.expectedCost = expectedCost
        self.totalCost = cost + expectedCost
        self.action = action  
        self.parent = parent
   
    def __eq__(self,other):
        if other == None:
            return None
        return self.cube == other.cube

    def __lt__(self,other):
        return self.totalCost < other.totalCost

    def getPath(self):
        path = []
        node = self
        while node.parent != None:
           path = [ node.action ] + path
           node = node.parent
        return path
