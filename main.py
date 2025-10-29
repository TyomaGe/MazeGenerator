from random import random
from drawer import MazeDrawer
from maze import MazeGenerator


if __name__ == "__main__":
    seed = random()
    maze_generator = MazeGenerator()
    maze = maze_generator.generate(10, 10, seed=seed, shortcut_coef=0.0)
    drawer = MazeDrawer(maze, cell_size=30)
    drawer.draw()
