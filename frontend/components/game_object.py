from pygame.rect import Rect


class GameObject:

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.bounds = Rect(x, y, w, h)

    def draw(self, surface):
        pass

    def update(self):
        pass

    def scrollUp(self, y_offset):
        self.y -= y_offset
        self.bounds.y -= y_offset

    def scrollDown(self, y_offset):
        self.y += y_offset
        self.bounds.y += y_offset
