import pygame
import base_gui, color_blocks

class Scrollbar(base_gui.BaseGui):
	def __init__(self, parent, lowest_thumb_y, total_number_entries, visible_entries, default_dict=base_gui.load_defaults()):
		base_gui.BaseGui.__init__(self)
		#
		#  A scrollbar is an object contained in a panel that displays an active bar on the right and eventually on the
		#  bottom of a panel with a thumb that the left mouse button can drag. This will change the displayed contents of the
		#  panel.
		#
		#  The scrollbar will keep track of the thumbs position and therefore the view Rect to be displayed, rather than
		#  the actual Rect of the panel.
		#
		#  A panel should dynamically create a scrollbar if its contents do not fit.
		#
		#  When a scrollbar is displayed (via self.parent.display() ) it needs to be the first thing in the children list.
		#
		#  Test for uniqueness with (isinstance(item, scrollbars.Scrollbar) for item in self.children)
		#  Make sure no more scrollbars can be made.

		self.parent = parent
		self.button_height = (parent.height * (parent.height / lowest_thumb_y)) // 1
		self.lowest_thumb_y = lowest_thumb_y
		#  Total number entries is used to find the number of pixels each line occupies to return the correct top visible element.
		self.total_number_entries = total_number_entries
		self.visible_entries = visible_entries
		self.default_dict = default_dict
		self.height = parent.height# - 2 * self.default_dict['scrollbar_top_margin']
		self.width = self.default_dict['scrollbar_width']
		self.x = self.parent.rect.right - self.width - self.default_dict['scrollbar_margin_right']
		self.y = self.parent.rect.top #+ self.default_dict['scrollbar_top_margin']
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.button_rect = pygame.Rect(self.x, self.y, self.width, self.button_height)
		self.line_width = self.default_dict['scrollbar_button_highlight_width']
		self.list_element = 0 # from the list to be displayed in parent


		self.children.append(color_blocks.DefaultColorBlock(self.parent, self.default_dict['scrollbar_color'], self.rect))
		self.children.append(color_blocks.ScrollbarColorBlock(self.parent,  self.default_dict['scrollbar_button_color'],
													self.button_rect, self, drag_with_mouse=True))

		#  A scrollbar consists of 2 troughs and a thumb according to wikipedia.
		#  If we want an image on the thumb we are going to have to make a fundamentals object.
		self.thumb = self.children[-1]

		#Created
		self.parent.changed = True
		self.parent.scrollbar = self

		#  __str__ return
		self.str = f'Scrollbar object from parent {self.parent.name}'

	def get_element(self):
		# This will return the index of the first line to be visible and doesnt work
		traverse = self.height - self.button_height
		step = (traverse / (self.total_number_entries - self.visible_entries)) // 1
		#  The top of the ScrollbarColorBlock.
		cur_pos = self.thumb.rect.y - self.parent.rect.top
		return int(cur_pos // step)

	def update_pos(self, x, y):
		self.thumb.rect.y += y
		if self.thumb.rect.y < self.y:
			self.thumb.rect.y = self.y
		elif self.thumb.rect.y > self.y + self.height - self.button_height:
			self.thumb.rect.y = self.y + self.height - self.button_height
		self.parent.changed = True
		self.parent.scrollbar_changed = True
		self.parent.visible = True
		self.list_element = self.get_element()