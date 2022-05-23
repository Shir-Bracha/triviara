import pygame
from components.game_object import GameObject
from configs.colors import Color


class TextBlock(GameObject):
    """Rectangle with question"""

    def __init__(self, x, y, w, h, text, image=None):
        super().__init__(x, y, w, h)

        if image:
            self.image = pygame.transform.scale(image, (self.w, self.h))
            self.no_fill = 1
        else:
            self.image = None
            self.no_fill = 0

        self.text = text
        self.font = pygame.font.SysFont('David', 22)
        self.DEFAULT_BACK_COLOR = Color.LIGHT_GRAY
        self.back_color = self.DEFAULT_BACK_COLOR

    def draw(self, surface):
        surface_x = self.x
        surface_y = self.y

        pygame.draw.rect(surface, self.back_color, self.bounds, self.no_fill)

        if self.image:
            surface.blit(self.image, self.image.get_rect(center=self.bounds.center))
            center_x, center_y = self.bounds.center
            surface_x = self.x + 5
            surface_y = center_y-((center_y-self.y)/2)

        surface.blit(self.font.render(self.text, False, (0, 0, 0)),
                     (surface_x, surface_y, self.w, self.h))

    def update(self):
        pass
