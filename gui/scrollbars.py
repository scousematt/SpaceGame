import pygame
import base_gui, color_blocks

class Scrollbar(base_gui.BaseGui):
	def __init__(self, panel, lowest_thumb_y, total_number_entries, visible_entries, default_dict=base_gui.load_defaults()):
		base_gui.BaseGui.__init__(self)
		#
		#  This class works when a list of single lines is being displayed. For more complicated lists though, with
		#  images and color blocks, this is inadequate. I could just make a fundamental.line object that could deal with
		#  this:
		#        line is [ [color_block, defaultlabel, image],
		#                  [color_block, defaultlabel, image] ]
		#
		#  This is a static scrollbar. I need a dynamic one that sell adjusts whenever the total_number_entries can change
		#

		self.panel = panel
		self.button_height = (panel.height * (panel.height / lowest_thumb_y)) // 1
		self.lowest_thumb_y = lowest_thumb_y
		#  Total number entries is used to find the number of pixels each line occupies to return the correct top visible element.
		self.total_number_entries = total_number_entries
		self.visible_entries = visible_entries
		self.default_dict = default_dict
		self.height = panel.height# - 2 * self.default_dict['scrollbar_top_margin']
		self.width = self.default_dict['scrollbar_width']
		self.x = self.panel.rect.right - self.width - self.default_dict['scrollbar_margin_right']
		self.y = self.panel.rect.top #+ self.default_dict['scrollbar_top_margin']
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.button_rect = pygame.Rect(self.x, self.y, self.width, self.button_height)
		self.line_width = self.default_dict['scrollbar_button_highlight_width']
		self.list_element = 0 # from the list to be displayed in parent

		self.children=[]

		self.children.append(color_blocks.DefaultColorBlock(self.panel, self.default_dict['scrollbar_color'], self.rect))
		self.children.append(color_blocks.ScrollbarColorBlock(self.panel,  self.default_dict['scrollbar_button_color'],
													self.button_rect, self, drag_with_mouse=True))
		#  A scrollbar consists of 2 throughs and a thumb according to wikipedia
		self.thumb = self.children[-1]

		#Created
		self.panel.changed = True
		self.panel.scrollbar = self

	def display(self):
		for child in self.children:
			#print(child.rect)
			child.display()

	def get_element(self):
		# This will return the index of the first line to be visible and doesnt work
		traverse = self.height - self.button_height
		step = (traverse / (self.total_number_entries - self.visible_entries)) // 1
		#  The top of the ScrollbarColorBlock. Need a better way of identifying it.
		cur_pos = self.thumb.rect.y - self.panel.rect.top
		return int(cur_pos // step)

	def update_pos(self, x, y):
		self.thumb.rect.y += y
		if self.thumb.rect.y < self.y:
			self.thumb.rect.y = self.y
		elif self.thumb.rect.y > self.y + self.height - self.button_height:
			self.thumb.rect.y = self.y + self.height - self.button_height
		self.panel.changed = True
		self.panel.scrollbar_changed = True
		self.panel.visible = True
		self.list_element = self.get_element()