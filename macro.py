from traffic_path import Path
import operator
from functools import reduce  # Required in Python 3
import os
import pickle
import time
from car import Car
from stoplight import Stoplight
import random
import numpy as np
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


class Stoplight:
    def __init__(self, init_pos, surface) -> None:
        self.RED = 0
        self.YELLOW = 1
        self.GREEN = 2

        self.pos = init_pos
        self.state = self.RED

        self.surface = surface

    def move(self, pos):
        self.pos = pos

    def set_state(self, state):
        self.state = state

    def flip(self):
        self.h, self.w = (self.w, self.h)

    def is_touching(self, pos):
        # x1, y1 = pos
        # x2, y2 = self.pos
        # return (x1 >= x2 and x1 <= x2+self.w) and (y1 >= y2 and y1 <= y2+self.h)
        return False

    def draw(self):
        x, y = self.pos
        pygame.draw.rect(self.surface, (255 if self.state == self.RED or
                                        self.state == self.YELLOW else 0,
                                        255 if self.state == self.GREEN or
                                        self.state == self.YELLOW else 0,
                                        0), pygame.Rect(x-15, y-15, 30, 30))
        # pygame.draw.circle(self.surface, (123,123,123), (x-15, y-15),5)
        # pygame.draw.circle(self.surface, (123,123,123), (x+15, y+15),5)

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["surface"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.surface = pygame.Surface((0, 0))


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


BACK_COLOR = (255, 200, 123)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def prod(iterable):
    return reduce(operator.mul, iterable, 1)


class Game:
    def __init__(self) -> None:

        pygame.font.init()
        self.font = pygame.font.Font("Rajdhani-Regular.ttf", 16)
        self.instructions1 = self.font.render(
            "Press A to add path", True, BLACK)
        self.instructions2 = self.font.render(
            "Press R to remove path", True, BLACK)
        self.instructions3 = self.font.render(
            "Click to add point", True, BLACK)
        self.instructions4 = self.font.render(
            "Press Ctrl + Z to undo", True, BLACK)
        self.instructions5 = self.font.render(
            "Press Ctrl + S to save project", True, BLACK)
        self.instructions6 = self.font.render(
            "Press Ctrl + L to load project", True, BLACK)

    def init(self):
        pygame.init()
        pygame.display.set_caption("traffic simulation")

        self.map = pygame.display.set_mode((900, 612))
        self.map.fill(BACK_COLOR)
        self.running = True
        self.paths: list[Path] = []
        self.stoplights: list[Stoplight] = []

        self.collided = False

    def save_project(self):
        with open("project.pickle", "wb") as f:
            pickle.dump(
                {"paths": self.paths, "stoplights": self.stoplights}, f)
        print("Project saved")

    def load_project(self):
        if os.path.exists("project.pickle"):
            with open("project.pickle", "rb") as f:
                project_data = pickle.load(f)
            self.paths = project_data["paths"]
            self.stoplights = project_data["stoplights"]
            self.reset_surfaces()
            print("Project loaded")
        else:
            print("No saved project found")

    def reset_surfaces(self):
        for path in self.paths:
            path.surface = self.map
        for stoplight in self.stoplights:
            stoplight.surface = self.map

    def set_stoplights(self, state):
        for s in self.stoplights:
            s.state = state

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if event.button == pygame.BUTTON_LEFT:
                    stoplight = [
                        s for s in self.stoplights if s.is_touching(pos)]
                    if len(stoplight) > 0:
                        stoplight[0].move(pos)
                    else:
                        if len(self.paths) > 0:
                            self.paths[-1].add_point(pos)

                elif event.button == pygame.BUTTON_RIGHT:
                    self.stoplights.append(Stoplight(pos, self.map))
                    print("new stoplight")

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.paths.append(Path(self.map))
                    print('path added')
                elif event.key == pygame.K_r:
                    if len(self.paths) > 0:
                        self.paths.pop()
                elif event.key == pygame.K_g:
                    self.set_stoplights((self.stoplights[0].state + 1) % 3)
                    print('toggle state')
                elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    if len(self.paths) > 0:
                        if len(self.paths[-1].points) > 0:
                            self.paths[-1].remove_point()
                        else:
                            self.paths.pop()
                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.save_project()
                elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.load_project()

    def update(self):
        for p in self.paths:
            p.update(self.stoplights)
        c_mat = np.array([m.collision_matrix for m in self.paths])
        self.collided = (np.sum(c_mat, axis=0)//2).sum() > 0

    def draw_path_count_txt(self):
        for i in range(len(self.paths)):
            self.p_txt = self.font.render(
                f"[{i}] path: {len(self.paths[i].points)} points and {len(self.paths[i].cars)} cars", True, BLACK)
            self.map.blit(self.p_txt, (10, self.map.get_height()-20-(25*i)))

    def collision(self):
        pass

    def draw(self):
        self.map.fill(BACK_COLOR if (not self.collided) else (255, 100, 100))

        for p in self.paths:
            p.draw()

        for s in self.stoplights:
            s.draw()

        self.map.blit(self.instructions1, (10, 5+(25*0)))
        self.map.blit(self.instructions2, (10, 5+(25*1)))
        self.map.blit(self.instructions3, (10, 5+(25*2)))
        self.map.blit(self.instructions4, (10, 5+(25*3)))
        self.map.blit(self.instructions5, (10, 5+(25*4)))
        self.map.blit(self.instructions6, (10, 5+(25*5)))

        self.draw_path_count_txt()

        pygame.display.update()

    def run(self):
        while (self.running):
            self.handle_input()
            self.update()
            self.draw()
            time.sleep(1/30)


game = Game()
game.init()
game.run()
