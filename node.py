import copy

class Node:
    def __init__(self,maze,costG,costH,action,parent):
        self.maze = maze
        self.costG = costG
        self.costH = costH
        self.costF = costG + costH
        self.action = action
        self.parent = parent

    def __eq__(self,other):
        if other == None:
            return None
        return self.maze == other.maze

    def __lt__(self,other):
        return self.costF < other.costF

    def getAction(self):
        node = self
        while node.parent.parent != None:
           node = node.parent
        return node.action
