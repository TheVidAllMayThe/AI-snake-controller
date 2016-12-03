import copy

class Node:
    def __init__(self,maze,costG,costH,action,parent):
        self.maze = maze
        self.costG = costG
        self.costH = costH
        self.costF = costG + costH
        self.action = action
        self.parent = parent
        self.depth = 0 if parent == None else parent.depth + 1

    def __eq__(self,other):
        if other == None:
            return None
        return self.maze == other.maze

    def __lt__(self,other):
        return self.costF < other.costF

    def getAction(self):
        node = self
        action = self.action
        while node.parent != None:
            action = node.action
            node = node.parent
        return action


class HiNode:
    def __init__(self,place,costG,costH,parent):
        self.place = place
        self.costG = costG
        self.costH = costH
        self.costF = costG + costH
        self.parent = parent
        self.depth = 0 if parent == None else parent.depth + 1

    def __eq__(self,other):
        if other == None:
            return None
        return self.place == other.place

    def __lt__(self,other):
        return self.costF < other.costF

    def getPlace(self):
        if self.parent == None:
            return self.place
        elif self.parent.parent == None:
            return self.place
        return self.parent.getPlace()
