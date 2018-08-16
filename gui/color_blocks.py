import pygame
import base_gui


class DefaultColorBlock(base_gui.BaseGui):

	def __init__(self, panel, color, rect):
		# This is for things internal to panels where a block of color is needed, things like message box title background
		# it is essentially a colored pygame.rect
		base_gui.BaseGui.__init__(self)
		self.panel = panel
		self.color = color
		self.rect = rect
		self.str = f'{type(self)} with color {self.color}'

	def display(self):
		pygame.draw.rect(self.panel.screen,
						 self.color,
						 self.rect)

class Triangles2ColorBlock(DefaultColorBlock):
	def __init__(self, panel, color, rect, color2):
		DefaultColorBlock.__init__(self, panel, color, rect)
		self.panel = panel
		self.color = color
		self.color2 = color2
		self.rect = rect

	def display(self):
		pygame.draw.polygon(self.panel.screen,
							self.color,
							[[self.rect.right, self.rect.top],
							 [self.rect.left, self.rect.top],
							 [self.rect.left, self.rect.bottom]])

		pygame.draw.polygon(self.panel.screen,
							self.color2,
							[[self.rect.right, self.rect.top],
							 [self.rect.left, self.rect.bottom],
							 [self.rect.right, self.rect.bottom]])

class PanelColorBlock(DefaultColorBlock):
	def __init__(self, panel, color, rect, drag_with_mouse=False):
		DefaultColorBlock.__init__(self, panel, color, rect)
		self.drag_with_mouse = drag_with_mouse


class ScrollbarColorBlock(PanelColorBlock):
	def __init__(self, panel, color, rect, parent, drag_with_mouse=False):
		PanelColorBlock.__init__(self, panel, color, rect, drag_with_mouse=False)
		self.parent = parent
		self.line_width = self.parent.line_width
		self.highlight_color = (self.color[0] + 50, self.color[1] + 50, self.color[2] + 50)
		self.shadow_color = (self.color[0] - 50, self.color[1] - 50, self.color[2] - 50)
		print('We are in scrollbar color block')

	def display(self):
		pygame.draw.polygon(self.panel.screen,
						 self.highlight_color,
						  [ self.rect.bottomleft, self.rect.topleft, self.rect.topright],
						  0
						 )
		pygame.draw.polygon(self.panel.screen,
						self.shadow_color,
						[self.rect.topright, self.rect.bottomright, [self.rect.left + 2, self.rect.bottom],
						 [self.rect.right - 2, self.rect.top]],
						0
						)
		pygame.draw.rect(self.panel.screen,
						 self.color,
						 self.rect.inflate(-self.line_width, -self.line_width))


class DropDownColorBlock(DefaultColorBlock):
	def __init__(self, panel, color, rect):
		DefaultColorBlock.__init__(self, panel, color, rect )

		pass
