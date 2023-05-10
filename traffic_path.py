import pygame
import numpy as np
from scipy import interpolate
import random
from stoplight import Stoplight
import math


from car import Car


class Path:
    def __init__(self, surface) -> None:
        self.points = []
        self.smooth = []
        self.cars: list[Car] = []
        self.rate = 5
        self.k = 3
        self.speed = 10
        self.path_limit = 10
        self.surface = surface
        self.color = (random.randint(100, 255), random.randint(
            100, 255), random.randint(100, 255))
        self.path = None
        self.tick = self.rate

        w, h = surface.get_size()
        self.collision_matrix = np.zeros((w//20, h//20), dtype=np.uint8)

    def add_point(self, pos):
        self.points.append(pos)
        if (len(self.points) > self.k):
            (x, y), self.path = b_spline(self.points, self.k)
            self.smooth = list(zip(x, y))
        self.cars = []

    def add_car(self):
        l = curve_lengh(self.smooth)
        if (self.path is not None):
            self.cars.append(Car(self.speed, self.path, l))

    def remove_point(self):
        self.points.pop()
        self.cars = []
        if (len(self.points) > self.k):
            (x, y), self.path = b_spline(self.points, self.k)
            self.smooth = list(zip(x, y))

    def colliding(self, pos, stoplights: list[Stoplight]):
        x1, y1 = pos
        for s in stoplights:
            x2, y2 = s.pos
            if (x1 >= x2-15 and x1 <= x2 + 15) and (y1 >= y2-15 and y1 <= y2 + 15):
                return s.state
        return 2

    def update(self, stoplights: list[Stoplight]):
        for c in self.cars:
            if c.u >= 1:
                self.cars.remove(c)

        self.tick -= 1
        if self.tick < 1:
            self.tick = self.rate
            self.add_car()

        l = len(self.cars)

        self.collision_matrix = self.collision_matrix * 0

        for i in range(l):
            if (i >= 1):
                self.cars[i].move(self.cars[i-1],
                                  2 if len(stoplights) < 1 else self.colliding(self.cars[i].pos, stoplights))
            else:
                self.cars[i].move(None,
                                  2 if len(stoplights) < 1 else self.colliding(self.cars[i].pos, stoplights))
            x, y = self.cars[i].pos
            self.collision_matrix[int(
                math.floor((x-5) / 20))][int(math.floor((y-5)/20))] = 1

    def draw(self):
        for point in self.points:
            pygame.draw.circle(self.surface, (0, 0, 0), point, 5, 0)
        for smoothie in self.smooth:
            pygame.draw.circle(self.surface, self.color, smoothie, 2, 0)
        l = len(self.cars)
        for i in range(l):
            self.cars[i].draw(self.surface)

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["surface"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.surface = pygame.Surface((0, 0))


def curve_lengh(points):
    l = 0
    for i in range(1, len(points)):
        point1 = np.array(points[i-1])
        point2 = np.array(points[i])

        l += np.linalg.norm(point1 - point2)

    return l


def b_spline(waypoints, k):
    x, y = zip(*waypoints)
    tck, _ = interpolate.splprep([x, y], k=k, s=0)
    u = np.linspace(0, 1, num=10000)
    smooth = interpolate.splev(u, tck)
    return (smooth, tck)
