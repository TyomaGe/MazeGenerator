from random import random
from drawer import MazeDrawer
from shaper import MazeShaper


if __name__ == "__main__":
    seed = random()
    shaper = MazeShaper(50, 50, seed)
    maze = shaper.generate(gaps_chance=0.1)
    drawer = MazeDrawer(maze, cell_size=15)
    drawer.draw()
