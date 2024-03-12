from settings import *

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line)

        n_horiz_tiles = len(self.data[0])
        n_vert_tiles = len(self.data)

        self.width = n_horiz_tiles*32
        self.height = n_vert_tiles*32