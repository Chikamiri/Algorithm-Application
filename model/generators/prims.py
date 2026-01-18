import random
from typing import Generator
from ..interfaces import IGenerator
from ..grid import Grid

class PrimsAlgorithm(IGenerator):
    def generate(self, grid: Grid) -> Generator[None, None, None]:
        # Start at a random cell
        start_x = random.randint(0, grid.cols - 1)
        start_y = random.randint(0, grid.rows - 1)
        start_cell = grid.get_cell(start_x, start_y)
        
        start_cell.visited = True
        grid.current = start_cell
        
        # Frontier cells: unvisited cells that have at least one visited neighbor
        frontier = set(grid.get_unvisited_neighbors(start_cell))
        
        while frontier:
            # Pick a random cell from the frontier
            current = random.choice(list(frontier))
            grid.current = current
            
            # Find all visited neighbors of this cell
            neighbors = grid.get_neighbors(current)
            visited_neighbors = [n for n in neighbors if n.visited]
            
            if visited_neighbors:
                # Pick a random visited neighbor and remove the wall
                neighbor = random.choice(visited_neighbors)
                grid.remove_wall(current, neighbor)
            
            # Mark current as visited
            current.visited = True
            
            # Add its unvisited neighbors to the frontier
            new_neighbors = grid.get_unvisited_neighbors(current)
            for n in new_neighbors:
                frontier.add(n)
            
            # Remove current from frontier
            frontier.remove(current)
            
            yield # Update visualization
            
        grid.current = None
