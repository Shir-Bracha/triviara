import pygame.color
import pygame_textinput

from components.text_block import TextBlock
from configs.colors import Color


class TextInput(TextBlock):
	def __init__(self, x, y, w, h, placeholder='', length_restriction=20):
		super().__init__(x, y, w, h, placeholder)

		self.back_color = Color.WHITE
		self.focus = False
		self.length_restriction = length_restriction
		self.placeholder = placeholder
		self.textinput = pygame_textinput.TextInputVisualizer()
		self.textinput.font_color = Color.BLUE
		self.textinput.cursor_color = Color.GREEN
		self.textinput.value = placeholder

	def draw(self, surface):
		pygame.draw.rect(surface, self.back_color, self.bounds)
		surface.blit(self.textinput.surface, (self.x, self.y, self.w, self.h))

	def update(self):
		self.textinput.update([])

	def get_text(self):
		return self.textinput.value

	def handle_mouse_down(self,  type_of_event, pos, event_button=None):
		if type_of_event == pygame.MOUSEBUTTONDOWN:
			if self.bounds.collidepoint(pos):
				self.focus = True
			else:
				self.focus = False

	def handle_key_down_event(self, event):
		if not self.focus:
			return

		if self.placeholder:
			self.textinput.value = ''
			self.text = ''
			self.placeholder = ''

		if len(self.textinput.value) == self.length_restriction and not event.key == pygame.K_BACKSPACE:
			return

		self.textinput.update([event])
