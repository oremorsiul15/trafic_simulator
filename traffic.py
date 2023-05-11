import pygame
import time
from stoplight import Stoplight
import pickle
import os
from functools import reduce  # Required in Python 3
import operator
import numpy as np

from traffic_path import Path

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

        self.map = pygame.display.set_mode((1200, 912))
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
            self.paths: list[Path] = project_data["paths"]
            self.stoplights = project_data["stoplights"]
            for p in self.paths:
                p.cars = []
                p.rate = 20
            self.reset_surfaces()
            print("Project loaded")
        else:
            print("No saved project found")

    def load_project(self, name):
        if os.path.exists(name):
            with open(name, "rb") as f:
                project_data = pickle.load(f)
            self.paths: list[Path] = project_data["paths"]
            self.stoplights = project_data["stoplights"]
            for p in self.paths:
                p.cars = []
                p.rate = 20
            self.reset_surfaces()
            # print("Project loaded")
        else:
            print("No saved project found")

    def reset_surfaces(self):
        for path in self.paths:
            path.surface = self.map
        for stoplight in self.stoplights:
            stoplight.surface = self.map

    def handle_input(self):
        # this secction is only for manual testing
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
                    self.action([True]*len(self.stoplights))
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
                f"[{i}] path: {len(self.paths[i].points)} points and {len(self.paths[i].cars)} cars {'(OVERFLOW)' if self.paths[i].on_overflow else ''}", True, BLACK)
            self.map.blit(self.p_txt, (10, self.map.get_height()-20-(25*i)))

    def action(self, toggle: list[bool]):
        for i in range(len(toggle)):
            if toggle[i]:
                self.stoplights[i].toggle()

    def get_observation(self):
        return [s.state for s in self.stoplights] + [int(p.on_overflow) for p in self.paths] + [int(self.collided)]

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

    def close(self):
        self.running = False

    def run(self):
        while (self.running):
            self.handle_input()
            self.update()
            self.draw()
            time.sleep(1/30)


if __name__ == "__main__":
    game = Game()
    game.init()
    game.run()
