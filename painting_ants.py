import pygame as pg
from collections import deque
from random import choice, randrange


class Ant:
    def __init__(self, app, pos, color):
        self.app = app
        self.color = color
        self.x, self.y = pos
        self.increments = deque([(1, 0), (0, 1), (-1, 0), (0, -1)])

    def run(self):
        value = self.app.grid[self.y][self.x]
        self.app.grid[self.y][self.x] = not value

        SIZE = self.app.CELL_SIZE
        center = self.x * SIZE, self.y * SIZE
        if value:
            pg.draw.circle(self.app.screen, self.color, center, SIZE)

        self.increments.rotate(1) if value else self.increments.rotate(-1)
        dx, dy = self.increments[0]
        self.x = (self.x + dx) % self.app.COLS
        self.y = (self.y + dy) % self.app.ROWS


class App:
    def __init__(self, WIDTH=1600, HEIGHT=900, CELL_SIZE=6):
        pg.init()
        self.screen = pg.display.set_mode([WIDTH, HEIGHT])
        self.clock = pg.time.Clock()

        self.CELL_SIZE = CELL_SIZE
        self.ROWS, self.COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
        self.grid = [[0 for col in range(self.COLS)] for row in range(self.ROWS)]

        colors1 = [(50, 30, i) for i in range(256)]
        colors2 = [(150, i, 120) for i in range(256)]
        ants1 = [Ant(self, [self.COLS // 3, self.ROWS // 2],
                     choice(colors1)) for i in range(400)]
        ants2 = [Ant(self, [self.COLS - self.COLS // 3, self.ROWS // 2],
                     choice(colors2)) for i in range(400)]
        self.ants = ants1 + ants2

    @staticmethod
    def get_color():
        channel = lambda: randrange(30, 220)
        return channel(), channel(), channel()

    def run(self):
        while True:
            [ant.run() for ant in self.ants]

            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.flip()
            self.clock.tick()


if __name__ == '__main__':
    app = App()
    app.run()