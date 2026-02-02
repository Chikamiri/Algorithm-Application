import heapq
from typing import Generator, List
from ..interfaces import ISolver
from ..grid import Grid
from ..cell import Cell

class AStar(ISolver):
    def heuristic(self, a: Cell, b: Cell) -> int:
        """Manhattan distance heuristic."""
        return abs(a.x - b.x) + abs(a.y - b.y)

    def solve(self, grid: Grid, start_cell: Cell, end_cell: Cell, visualize: bool = True) -> Generator[int, None, dict]:
        # Priority queue stores (priority, count, cell)
        count = 0
        frontier = [(0, count, start_cell)]
        came_from = {start_cell: None}
        g_score = {start_cell: 0}
        
        visited_count = 0
        max_frontier = 1
        
        if visualize:
            start_cell.in_frontier = True
        
        while frontier:
            max_frontier = max(max_frontier, len(frontier))
            _, _, current = heapq.heappop(frontier)
            visited_count += 1
            
            if visualize:
                current.in_frontier = False
                current.visited_by_solver = True
            
            if current == end_cell:
                break
                
            for neighbor in grid.get_accessible_neighbors(current):
                new_g_score = g_score[current] + 1
                
                if neighbor not in g_score or new_g_score < g_score[neighbor]:
                    g_score[neighbor] = new_g_score
                    priority = new_g_score + self.heuristic(neighbor, end_cell)
                    count += 1
                    heapq.heappush(frontier, (priority, count, neighbor))
                    came_from[neighbor] = current
                    if visualize:
                        neighbor.in_frontier = True
            
            if visualize:
                yield len(frontier)
            
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
