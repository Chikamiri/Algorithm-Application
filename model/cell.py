class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False  # Used during generation
        self.is_entry = False
        self.is_exit = False
        
        # Solver states
        self.visited_by_solver = False # Used during solving (part of closed set)
        self.in_frontier = False # Used during solving (part of open set)
        self.is_path = False # Part of the final solution path

    def check_walls(self, other) -> bool:
        """
        Checks if there is a wall between this cell and another neighbor.
        Returns True if there is a wall, False if open.
        """
        x = self.x - other.x
        y = self.y - other.y
        
        if x == 1: # other is to the left
            return self.walls['left']
        elif x == -1: # other is to the right
            return self.walls['right']
        elif y == 1: # other is above
            return self.walls['top']
        elif y == -1: # other is below
            return self.walls['bottom']
        return False
    
    def __repr__(self):
        return f"Cell({self.x}, {self.y})"
