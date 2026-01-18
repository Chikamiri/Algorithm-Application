from typing import Generator, List
from ..interfaces import ISolver
from ..grid import Grid
from ..cell import Cell

class DFS(ISolver):
    def solve(self, grid: Grid, start_cell: Cell, end_cell: Cell) -> Generator[None, None, List[Cell]]:
        stack = [start_cell]
        came_from = {start_cell: None}
        
        start_cell.visited_by_solver = True
        start_cell.in_frontier = True
        
        found = False
        while stack:
            current = stack.pop()
            current.in_frontier = False
            
            if current == end_cell:
                found = True
                break
                
            # For DFS, order matters for visual representation of "standard" DFS
            # but any neighbor works for finding a path.
            for neighbor in grid.get_accessible_neighbors(current):
                if not neighbor.visited_by_solver:
                    neighbor.visited_by_solver = True
                    neighbor.in_frontier = True
                    came_from[neighbor] = current
                    stack.append(neighbor)
            
            yield # Update visualization
            
        # Reconstruct path
        path = []
        if found:
            temp = end_cell
            while temp:
                path.append(temp)
                temp.is_path = True
                temp = came_from[temp]
            path.reverse()
            
        return path
