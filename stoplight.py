import pygame

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

    def toggle(self):
        self.state = 2 if self.state == 0 else self.state -1

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
                                        self.state == self.YELLOW  else 0,
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
