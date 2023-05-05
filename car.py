import pygame
from scipy import interpolate
import math

def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return math.sqrt((x1-x2)**2 + (y1 - y2)**2)

class Car:
    def __init__(self, speed, path, l) -> None:
        self.u = 0
        self.speed = speed/l
        self.path = path
        self.pos = interpolate.splev(self.u, self.path)

    def move(self, next_car_pos):
        if next_car_pos is not None:
            distance = get_distance(self.pos, next_car_pos)
            self.u = (self.u + (1 if distance > 30 else 1/(distance + 10)) * self.speed)%1
        else:
            self.u = (self.u + 1 * self.speed)%1
        self.pos = interpolate.splev(self.u, self.path)
        self.pos = (float(self.pos[0]), float(self.pos[1]))
        

    def draw(self, map):
        pygame.draw.circle(map, (100,255,100), self.pos, 10, 0)