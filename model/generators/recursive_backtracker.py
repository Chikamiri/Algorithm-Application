import random
from typing import Generator
from ..interfaces import IGenerator
from ..grid import Grid

class RecursiveBacktracker(IGenerator):
    def generate(self, grid: Grid, visualize: bool = True) -> Generator[None, None, None]:
        # Start at the top-left cell (0,0)
        current = grid.get_cell(0, 0)
        if not current:
            return
            
        current.visited = True
        stack = [current]
        
        while stack:
            current = stack[-1]
            if visualize:
                grid.current = current # For visualization
            
            # Step 1: Get unvisited neighbors
            neighbors = grid.get_unvisited_neighbors(current)
            
            if neighbors:
                # Step 2: Choose a random neighbor
                neighbor = random.choice(neighbors)
                
                # Step 3: Remove wall between current and neighbor
                grid.remove_wall(current, neighbor)
                
                # Step 4: Mark neighbor as visited and push to stack
                neighbor.visited = True
                stack.append(neighbor)
                
                # Yield to let the view update
                if visualize:
                    yield
            else:
                # Backtrack
                stack.pop()
                if visualize:
                    yield
        
        if visualize:
            grid.current = None # Reset pointer when done
