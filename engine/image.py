import engine.tile

class Image(object):

    def __init__(self, tiles):
        self.__tiles = tiles

    @property
    def tiles(self):
        return self.__tiles

    def getTileAtPos(x, y):
        return self.__tiles[y][x]

    @staticmethod
    def stringToImage(str):
        tiles = [[]]
        str = str.splitlines()
        for index, line in enumerate(str):
            for char in line:
                tiles[index].append(engine.tile.Tile(char))
            tiles.append([])

        return Image(tiles)
