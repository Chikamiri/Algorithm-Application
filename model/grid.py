import random
from typing import List, Optional
from .cell import Cell

class Grid:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.cells = [[Cell(c, r) for r in range(rows)] for c in range(cols)]
        self.current = self.cells[0][0] # Pointer for visualization (e.g., current generator head)
    
    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return self.cells[x][y]
        return None

    def get_neighbors(self, cell: Cell) -> List[Cell]:
        """Returns all valid neighbors (top, right, bottom, left) regardless of walls."""
        neighbors = []
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)] # Top, Right, Bottom, Left
        
        for dx, dy in directions:
            neighbor = self.get_cell(cell.x + dx, cell.y + dy)
            if neighbor:
                neighbors.append(neighbor)
        return neighbors

    def get_unvisited_neighbors(self, cell: Cell) -> List[Cell]:
        """Returns neighbors that haven't been visited by the generator yet."""
        neighbors = self.get_neighbors(cell)
        return [n for n in neighbors if not n.visited]
    
    def get_accessible_neighbors(self, cell: Cell) -> List[Cell]:
        """Returns neighbors that are NOT blocked by walls."""
        neighbors = self.get_neighbors(cell)
        accessible = []
        for n in neighbors:
            if not cell.check_walls(n):
                accessible.append(n)
        return accessible

    def remove_wall(self, a: Cell, b: Cell):
        x = a.x - b.x
        y = a.y - b.y
        
        if x == 1:
            a.walls['left'] = False
            b.walls['right'] = False
        elif x == -1:
            a.walls['right'] = False
            b.walls['left'] = False
        elif y == 1:
            a.walls['top'] = False
            b.walls['bottom'] = False
        elif y == -1:
            a.walls['bottom'] = False
            b.walls['top'] = False

    def reset_visited(self):
        """Resets solver state for all cells."""
        for col in self.cells:
            for cell in col:
                cell.visited = False
                cell.visited_by_solver = False
                cell.in_frontier = False
                cell.is_path = False
