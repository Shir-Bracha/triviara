import pygame
from components.text_block import TextBlock
from configs.colors import Color


class Button(TextBlock):

    def __init__(self, x, y, w, h, text, onclick_func):
        self.button_image = pygame.image.load("./assets/blue_button_image.png").convert_alpha()

        super().__init__(x, y, w, h, text, self.button_image)

        self.state = 'normal'
        self.onclick_func = onclick_func
        self.HOVERED_BACK_COLOR = Color.WHITE
        self.PRESSED_BACK_COLOR = Color.BLUE

    def update(self):
        if self.state == 'normal':
            self.back_color = self.DEFAULT_BACK_COLOR
        elif self.state == 'hover':
            self.back_color = self.HOVERED_BACK_COLOR
        elif self.state == 'pressed':
            self.back_color = self.PRESSED_BACK_COLOR

    def handleMouseEvent(self, type_of_event, pos, event_button=None):
        if type_of_event == pygame.MOUSEMOTION:
            self.handleMouseMove(pos)
        elif type_of_event == pygame.MOUSEBUTTONDOWN:
            self.handleMouseDown(pos)
        elif type_of_event == pygame.MOUSEBUTTONUP:
            self.handleMouseUp(pos)

    def handleMouseMove(self, pos):
        if self.bounds.collidepoint(pos):
            if self.state != 'pressed':
                self.state = 'hover'
        else:
            self.state = 'normal'

    def handleMouseDown(self, pos):
        if self.bounds.collidepoint(pos):
            self.state = 'pressed'

    def handleMouseUp(self, pos):
            if self.state == 'pressed':
                self.onclick_func()
                self.state = 'hover'
