class Node:
    def __init__(self, maze, costG, costH, action, parent):
        self.maze = maze
        self.costG = costG
        self.costH = costH
        self.costF = costG + costH
        self.action = action
        self.parent = parent
        self.depth = 0 if parent == None else parent.depth + 1

    def __eq__(self, other):
        if other is None:
            return None
        return self.maze == other.maze

    def __lt__(self, other):
        return self.costF < other.costF

    def getAction(self):
        node = self
        action = self.action
        while node.parent is not None:
            action = node.action
            node = node.parent
        return action


class HiNode:
    def __init__(self, gateway, costG, costH, parent, square, mapsize):
        self.gateway = gateway
        self.costG = costG
        self.costH = costH
        self.costF = costG + costH
        self.parent = parent
        self.square = square
        self.mapsize = mapsize
        self.depth = 0 if parent is None else parent.depth + 1

    def __eq__(self, other):
        if other is None:
            return None
        return self.gateway == other.gateway

    def __lt__(self,other):
        return self.costF < other.costF

    def get_gateway_result(self):
        x = self.gateway
        return ((x[0][0]+x[1][0]) % self.mapsize[0], (x[0][1]+x[1][1]) % self.mapsize[1])

    def getPlace(self):
        if self.parent is None:
            return self.get_gateway_result()
        elif self.parent.parent is None:
            return self.get_gateway_result()
        return self.parent.getPlace()
