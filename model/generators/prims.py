import random
from typing import Generator
from ..interfaces import IGenerator
from ..grid import Grid

class PrimsAlgorithm(IGenerator):
    def generate(self, grid: Grid, visualize: bool = True) -> Generator[None, None, None]:
        # Start at a random cell
        start_x = random.randint(0, grid.cols - 1)
        start_y = random.randint(0, grid.rows - 1)
        start_cell = grid.get_cell(start_x, start_y)
        
        start_cell.visited = True
        if visualize:
            grid.current = start_cell
        
        # Frontier cells: unvisited cells that have at least one visited neighbor
        # Use a list for random selection and a set for fast lookup
        initial_frontier = grid.get_unvisited_neighbors(start_cell)
        frontier_list = list(initial_frontier)
        frontier_set = set(initial_frontier)
        
        while frontier_list:
            # Pick a random cell from the frontier list (O(1))
            # We swap the chosen element with the last one and pop to keep it O(1)
            idx = random.randint(0, len(frontier_list) - 1)
            current = frontier_list[idx]
            
            # Efficient removal from list
            frontier_list[idx] = frontier_list[-1]
            frontier_list.pop()
            
            # Remove from set
            if current in frontier_set:
                frontier_set.remove(current)
            else:
                # Should not happen if logic is correct, but safe to continue
                continue

            if current.visited:
                continue

            # Mark current as visited BEFORE carving (Correctness fix)
            current.visited = True

            if visualize:
                grid.current = current
            
            # Find all visited neighbors of this cell
            neighbors = grid.get_neighbors(current)
            visited_neighbors = [n for n in neighbors if n.visited]
            
            if visited_neighbors:
                # Pick a random visited neighbor and remove the wall
                neighbor = random.choice(visited_neighbors)
                grid.remove_wall(current, neighbor)
            
            # Add its unvisited neighbors to the frontier
            new_neighbors = grid.get_unvisited_neighbors(current)
            for n in new_neighbors:
                if n not in frontier_set:
                    frontier_set.add(n)
                    frontier_list.append(n)
            
            if visualize:
                yield # Update visualization
            
        if visualize:
            grid.current = None
