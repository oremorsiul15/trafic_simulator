import pygame
import numpy as np
from scipy import interpolate
import random


from car import Car
class Path:
    def __init__(self, surface) -> None:
        self.points = []
        self.smooth = []
        self.cars:list[Car] = []
        self.rate = 5
        self.k = 3
        self.speed = 10
        self.path_limit = 10
        self.surface = surface
        self.color = (random.randint(100, 255),random.randint(100, 255),random.randint(100, 255))
    
    def add_point(self, pos):
        self.points.append(pos)
        if(len(self.points)>self.k):
            (x, y), path = b_spline(self.points, self.k)
            self.smooth = list(zip(x,y))
            l = curve_lengh(self.smooth)
            # self.cars = []
            self.cars.append(Car(self.speed,path, l))

    def remove_point(self):
        self.points.pop()
        self.cars = []
        if(len(self.points)>self.k):
            (x, y), path = b_spline(self.points, self.k)
            self.smooth = list(zip(x,y))
            l = curve_lengh(self.smooth)
            self.cars = []
            self.cars.append(Car(self.speed,path, l))

    def update(self):
        l = len(self.cars)
        for i in range(l):
            self.cars[i].move((None if i == l-1 else self.cars[i+1].pos))

    def draw(self):
        for point in self.points:
            pygame.draw.circle(self.surface, (0,0,0), point, 5, 0)
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
    tck, _= interpolate.splprep([x,y], k=k, s=0)
    u = np.linspace(0,1, num=10000)
    smooth=interpolate.splev(u, tck)
    return (smooth, tck)