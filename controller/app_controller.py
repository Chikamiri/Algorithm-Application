import pygame
from model.grid import Grid
from model.generators.recursive_backtracker import RecursiveBacktracker
from model.generators.prims import PrimsAlgorithm
from model.solvers.bfs import BFS
from model.solvers.dfs import DFS
from model.solvers.astar import AStar
from model.solvers.dijkstra import Dijkstra
from model.solvers.wall_follower import WallFollower
from model.benchmark_service import BenchmarkService
from view.renderer import Renderer

class AppController:
    def __init__(self, rows=30, cols=40):
        pygame.init()
        self.rows = rows
        self.cols = cols
        
        # Fixed Window Size
        self.WINDOW_WIDTH = 1280
        self.WINDOW_HEIGHT = 720
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Maze Algorithm Visualizer")
        
        # Speed control
        self.target_fps = 60
        self.steps_per_frame = 1
        
        self.clock = pygame.time.Clock()
        self.renderer = Renderer(self.screen)
        
        self.grid = Grid(rows, cols)
        
        self.generators = {
            pygame.K_1: RecursiveBacktracker(),
            pygame.K_2: PrimsAlgorithm()
        }
        
        self.solvers = {
            pygame.K_3: BFS(),
            pygame.K_4: DFS(),
            pygame.K_5: AStar(),
            pygame.K_6: Dijkstra(),
            pygame.K_7: WallFollower()
        }
        
        self.current_algo_gen = None
        self.current_algo_name = "None"
        self.running = True
        self.paused = False
        self.elapsed_time = 0.0
        self.total_steps = 0
        self.computation_time = 0.0 # CPU Time in ms
        
        # Benchmark State
        self.benchmark_service = BenchmarkService()
        self.state = "NORMAL" # NORMAL, BENCHMARKING, BENCHMARK_RESULTS
        self.benchmark_iterations = 5
        
        self.update_grid_endpoints()

    def update_grid_endpoints(self):
        self.start_cell = self.grid.get_cell(0, 0)
        self.end_cell = self.grid.get_cell(self.cols - 1, self.rows - 1)
        self.start_cell.is_entry = True
        self.end_cell.is_exit = True

    def reset_grid(self):
        # Ensure minimum size
        self.rows = max(5, self.rows)
        self.cols = max(5, self.cols)
        
        self.grid = Grid(self.rows, self.cols)
        self.update_grid_endpoints()
        self.current_algo_gen = None
        self.current_algo_name = "None"
        self.elapsed_time = 0.0
        self.total_steps = 0
        self.computation_time = 0.0

    def run(self):
        import time # Ensure time is available
        while self.running:
            # Time delta in seconds
            dt = self.clock.tick(self.target_fps) / 1000.0
            
            self.handle_events()
            
            if self.state == "NORMAL":
                if not self.paused and self.current_algo_gen:
                    self.elapsed_time += dt
                    try:
                        # Measure CPU Time for the steps taken in this frame
                        start_comp = time.perf_counter_ns()
                        for _ in range(self.steps_per_frame):
                            next(self.current_algo_gen)
                            self.total_steps += 1
                        end_comp = time.perf_counter_ns()
                        self.computation_time += (end_comp - start_comp) / 1_000_000 # to ms
                    except StopIteration:
                        self.current_algo_gen = None
                
                self.renderer.draw_grid(self.grid)
                if self.grid.current:
                    self.renderer.draw_current(self.grid.current)
                
                # Calculate Stats
                visited_count = 0
                path_len = 0
                frontier_count = 0
                
                total_cells = self.rows * self.cols
                
                is_solver = self.current_algo_name in ["BFS", "DFS", "AStar", "Dijkstra", "WallFollower"]
                
                if is_solver:
                    visited_count = sum(1 for col in self.grid.cells for cell in col if cell.visited_by_solver)
                    path_len = sum(1 for col in self.grid.cells for cell in col if cell.is_path)
                    frontier_count = sum(1 for col in self.grid.cells for cell in col if cell.in_frontier)
                else:
                    # Generator or None (show generator visited)
                    visited_count = sum(1 for col in self.grid.cells for cell in col if cell.visited)
                
                coverage = (visited_count / total_cells) * 100 if total_cells > 0 else 0
                
                stats = {
                    "visited": visited_count, 
                    "path": path_len,
                    "total": total_cells,
                    "coverage": coverage,
                    "frontier": frontier_count,
                    "time": self.elapsed_time,
                    "comp_time": self.computation_time,
                    "steps": self.total_steps
                }

                speed_info = f"{self.steps_per_frame} steps/frame"
                self.renderer.draw_info(self.current_algo_name, speed_info, (self.cols, self.rows), stats)
                
                if self.paused:
                    self.renderer.draw_pause_overlay()
            
            elif self.state == "BENCHMARKING":
                if not self.benchmark_service.is_running:
                    if self.benchmark_service.error:
                        # Stay in this state to show error
                        self.renderer.draw_benchmark_progress(self.benchmark_service.progress, self.benchmark_service.status_message)
                    elif self.benchmark_service.progress > 0:
                        # Success
                        self.state = "BENCHMARK_RESULTS"
                else:
                    self.renderer.draw_benchmark_progress(self.benchmark_service.progress, self.benchmark_service.status_message)

            elif self.state == "BENCHMARK_RESULTS":
                self.renderer.draw_benchmark_results(self.benchmark_service.get_averages(), self.benchmark_iterations)

            pygame.display.flip()
            
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                # Global Keys
                if event.key == pygame.K_b:
                    if self.state == "NORMAL":
                        self.state = "BENCHMARK_RESULTS" # Jump to results view (initially empty)
                    else:
                        self.state = "NORMAL"

                # State Specific Handling
                if self.state == "NORMAL":
                    mods = pygame.key.get_mods()
                    is_shift = mods & pygame.KMOD_SHIFT
                    
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_r:
                        self.reset_grid()
                    
                    # Speed Control
                    elif event.key == pygame.K_LEFTBRACKET: # [
                        decrement = 5 if is_shift else 1
                        self.steps_per_frame = max(1, self.steps_per_frame - decrement)
                    elif event.key == pygame.K_RIGHTBRACKET: # ]
                        increment = 5 if is_shift else 1
                        self.steps_per_frame = min(100, self.steps_per_frame + increment)
                        
                    # Size Control (Independent Width/Height)
                    elif event.key == pygame.K_LEFT:
                        self.cols -= 5
                        self.reset_grid()
                    elif event.key == pygame.K_RIGHT:
                        self.cols += 5
                        self.reset_grid()
                    elif event.key == pygame.K_UP:
                        self.rows -= 5
                        self.reset_grid()
                    elif event.key == pygame.K_DOWN:
                        self.rows += 5
                        self.reset_grid()
                    
                    # Presets
                    elif event.key == pygame.K_F1:
                        self.rows, self.cols = 15, 15
                        self.reset_grid()
                    elif event.key == pygame.K_F2:
                        self.rows, self.cols = 30, 40
                        self.reset_grid()
                    elif event.key == pygame.K_F3:
                        self.rows, self.cols = 50, 70
                        self.reset_grid()
                        
                    elif event.key in self.generators:
                        self.reset_grid()
                        algo = self.generators[event.key]
                        self.current_algo_name = algo.__class__.__name__
                        self.current_algo_gen = algo.generate(self.grid)
                    elif event.key in self.solvers:
                        self.grid.reset_visited()
                        self.elapsed_time = 0.0 # Reset time for solver
                        self.total_steps = 0
                        self.computation_time = 0.0
                        algo = self.solvers[event.key]
                        self.current_algo_name = algo.__class__.__name__
                        self.current_algo_gen = algo.solve(self.grid, self.start_cell, self.end_cell)

                elif self.state == "BENCHMARK_RESULTS":
                    mods = pygame.key.get_mods()
                    is_shift = mods & pygame.KMOD_SHIFT
                    step = 5 if is_shift else 1
                    
                    if event.key == pygame.K_RETURN:
                        self.state = "BENCHMARKING"
                        self.benchmark_service.start_benchmark(self.rows, self.cols, self.benchmark_iterations)
                    elif event.key == pygame.K_UP:
                        self.benchmark_iterations = min(100, self.benchmark_iterations + step)
                    elif event.key == pygame.K_DOWN:
                        self.benchmark_iterations = max(1, self.benchmark_iterations - step)
