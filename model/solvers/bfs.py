from collections import deque
from typing import Generator, List
from ..interfaces import ISolver
from ..grid import Grid
from ..cell import Cell

class BFS(ISolver):
    def solve(self, grid: Grid, start_cell: Cell, end_cell: Cell, visualize: bool = True) -> Generator[int, None, dict]:
        queue = deque([start_cell])
        came_from = {start_cell: None}
        
        visited_count = 0
        max_frontier = 1
        
        if visualize:
            start_cell.in_frontier = True
        
        while queue:
            max_frontier = max(max_frontier, len(queue))
            current = queue.popleft()
            visited_count += 1
            
            if visualize:
                current.in_frontier = False
                current.visited_by_solver = True
            
            if current == end_cell:
                break
                
            for neighbor in grid.get_accessible_neighbors(current):
                if neighbor not in came_from:
                    came_from[neighbor] = current
                    if visualize:
                        neighbor.in_frontier = True
                    queue.append(neighbor)
            
            if visualize:
                yield len(queue)
            
        # Reconstruct path
        path = []
        if end_cell in came_from:
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
