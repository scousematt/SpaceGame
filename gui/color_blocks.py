import pygame
import base_gui


class DefaultColorBlock(base_gui.BaseGui):
	def __init__(self, panel, color, rect, default_dict=base_gui.load_defaults()):
		# This is for things internal to panels where a block of color is needed, things like message box title background
		# it is essentially a colored pygame.rect
		base_gui.BaseGui.__init__(self)
		self.parent = panel
		self.color = color
		self.rect = rect
		self.default_dict = default_dict
		self.str = f'{type(self)} with color {self.color}'

	def display(self):
		pygame.draw.rect(self.parent.screen,
						 self.color,
						 self.rect)

	def update(self, y_change):
		self.rect.y += y_change

	def update_xy(self, x, y):
		self.rect = self.rect.move(x,y)


class Triangles2ColorBlock(DefaultColorBlock):
	def __init__(self, panel, color, rect, color2):
		DefaultColorBlock.__init__(self, panel, color, rect)
		self.color2 = color2

	def display(self):
		pygame.draw.polygon(self.parent.screen,
							self.color,
							[[self.rect.right, self.rect.top],
							 [self.rect.left, self.rect.top],
							 [self.rect.left, self.rect.bottom]])

		pygame.draw.polygon(self.parent.screen,
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

		self.highlight_color = (self.color[0] + 50, self.color[1] + 50, self.color[2] + 50)
		self.shadow_color = (self.color[0] - 50, self.color[1] - 50, self.color[2] - 50)

	def display(self):
		pygame.draw.polygon(self.parent.screen,
						 self.highlight_color,
						  [ self.rect.bottomleft, self.rect.topleft, self.rect.topright],
						  0
						 )
		pygame.draw.polygon(self.parent.screen,
						self.shadow_color,
						[self.rect.topright, self.rect.bottomright, [self.rect.left + 2, self.rect.bottom],
						 [self.rect.right - 2, self.rect.top]],
						0
						)
		pygame.draw.rect(self.parent.screen,
						 self.color,
						 self.rect.inflate(-self.default_dict['scrollbar_button_highlight_width'],
										   -self.default_dict['scrollbar_button_highlight_width']))


class BlockWithBorder(PanelColorBlock):
	def __init__(self, panel, color, rect, border_thickness, default_dict=base_gui.load_defaults(), drag_with_mouse=False):
		PanelColorBlock.__init__(self, panel, color, rect, drag_with_mouse=False)
		self.border_thickness = border_thickness


	def display(self):
		pygame.draw.rect(self.parent.screen,
						   self.color,
						   self.rect,
						   self.border_thickness)

class DropDownColorBlock(DefaultColorBlock):
	def __init__(self, panel, color, rect):
		DefaultColorBlock.__init__(self, panel, color, rect )

