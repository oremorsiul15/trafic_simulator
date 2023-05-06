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
        p = interpolate.splev(self.u, self.path)
        self.pos = (float(p[0]), float(p[1]))
        self.ref = None

    def move(self, next_car_pos, state):
        self.ref = next_car_pos
        if next_car_pos is not None:
            distance = get_distance(self.pos, next_car_pos)
            speed =  (1 if distance > 30 else 1/((distance-30)**2+1))
            # print(state/2 *speed, speed)
            self.u = (self.u + state/2 *speed)%1
        else:
            self.u = (self.u + state/2 * self.speed)%1
        p = interpolate.splev(self.u, self.path)
        self.pos = (float(p[0]), float(p[1]))
        

    def draw(self, map):
        pygame.draw.circle(map, (100,255,100), self.pos, 10)
        pygame.draw.circle(map, (200,255,100), (float(self.ref[0]), float(self.ref[1])) if self.ref is not None else self.pos, 5)