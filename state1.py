class State:
    def __init__(self,playerPos,opponentPos,obstacles,foodpos):
        self.playerPos = playerPos
        self.opponentPos = opponentPos
        self.obstacles = obstacles
        self.foodpos = foodpos

    def __eq__(self,other):
        if self.playerPos != other.playerPos:
            return False
        if self.opponentPos != other.opponentPos:
            return False
        if self.obstacles != other.obstacles:
            return False
        if self.foodpos != other.foodpos:
            return False
        return True
