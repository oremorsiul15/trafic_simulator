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
        p1 = interpolate.splev(self.u+0.01, self.path)
        self.pos = (float(p[0]), float(p[1]))
        self.ref = None
        self.direction = (float(p1[0]), float(p1[1]))

    def move(self, next_car_pos, state):
        # if next_car_pos is not None:
        #     self.ref = next_car_pos.pos
        #     distance = get_distance(self.pos, self.ref)
        #     speed = (self.speed if (distance > 30) and (
        #         self.u < next_car_pos.u) else 1)
        #     # print(self.pos, next_car_pos.pos, distance, speed)
        #     # print(state/2 *speed, speed)
        #     self.u = (self.u + state/2 * speed)
        # else:
        self.u = (self.u + state/2 * self.speed)
        p = interpolate.splev(self.u, self.path)
        p1 = interpolate.splev(self.u+0.01, self.path)
        self.pos = (float(p[0]), float(p[1]))
        self.direction = (float(p1[0]), float(p1[1]))

    def draw(self, map):
        if self.ref is not None:
            x = math.floor((self.ref[0]-5)/20)*20
            y = math.floor((self.ref[1]-5)/20)*20
            pygame.draw.rect(map, (123, 123, 123), pygame.Rect(x, y, 20, 20))

        pygame.draw.circle(map, (100, 255, 100), self.pos, 10)
        pygame.draw.circle(map, (200, 255 if self.ref is None else 8, 100), (float(self.ref[0]), float(
            self.ref[1])) if self.ref is not None else self.pos, 5)
        pygame.draw.line(map, (0, 0, 0), self.pos, self.direction)
