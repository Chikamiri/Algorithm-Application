from typing import Generator, List
from ..interfaces import ISolver
from ..grid import Grid
from ..cell import Cell

class DFS(ISolver):
    def solve(self, grid: Grid, start_cell: Cell, end_cell: Cell, visualize: bool = True) -> Generator[int, None, dict]:
        stack = [start_cell]
        came_from = {start_cell: None}
        
        visited_count = 0
        max_frontier = 1
        
        if visualize:
            start_cell.in_frontier = True
        
        found = False
        while stack:
            max_frontier = max(max_frontier, len(stack))
            current = stack.pop()
            visited_count += 1
            
            if visualize:
                current.in_frontier = False
                current.visited_by_solver = True
            
            if current == end_cell:
                found = True
                break
                
            for neighbor in grid.get_accessible_neighbors(current):
                if neighbor not in came_from:
                    came_from[neighbor] = current
                    if visualize:
                        neighbor.in_frontier = True
                    stack.append(neighbor)
            
            if visualize:
                yield len(stack)
            
        # Reconstruct path
        path = []
        if found:
            temp = end_cell
            while temp:
                path.append(temp)
                if visualize:
                    temp.is_path = True
                temp = came_from[temp]
            path.reverse()
            
        return {
            "path": path,
            "visited_count": visited_count,
            "peak_frontier": max_frontier
        }
