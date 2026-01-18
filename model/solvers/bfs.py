from collections import deque
from typing import Generator, List
from ..interfaces import ISolver
from ..grid import Grid
from ..cell import Cell

class BFS(ISolver):
    def solve(self, grid: Grid, start_cell: Cell, end_cell: Cell) -> Generator[None, None, List[Cell]]:
        queue = deque([start_cell])
        came_from = {start_cell: None} # To reconstruct path
        
        start_cell.visited_by_solver = True
        start_cell.in_frontier = True
        
        while queue:
            current = queue.popleft()
            current.in_frontier = False # No longer in frontier, it's processed
            
            if current == end_cell:
                break
                
            for neighbor in grid.get_accessible_neighbors(current):
                if not neighbor.visited_by_solver:
                    neighbor.visited_by_solver = True
                    neighbor.in_frontier = True
                    came_from[neighbor] = current
                    queue.append(neighbor)
            
            yield # Update visualization
            
        # Reconstruct path
        path = []
        if end_cell in came_from:
            temp = end_cell
            while temp:
                path.append(temp)
                temp.is_path = True # Mark for visualization
                temp = came_from[temp]
            path.reverse()
        
        return path
