import pygame
import base_gui

class DefaultPanel(base_gui.BaseGui):
	def __init__(self, gui, name, x, y, width, height, default_dict=base_gui.load_defaults(), visible=True, active=True):
		base_gui.BaseGui.__init__(self)

		self.visible = visible
		self.active = active
		self.name = name
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.gui = gui
		self.screen = self.gui.screen
		self.error = {}
		self.default_dict = default_dict
		self.background_color = self.default_dict['panel_background_color']
		self.border_color = self.default_dict['panel_border_color']

		self.changed = False  # updated by self.children objects
		self.children = []
		print(self.name, self.x, self.y, self.width, self.height)
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.children.append(PanelColorBlock(self, self.background_color, self.rect))
		self.named_children_dict = {}

	def update_pos(self, x, y):
		self.rect = self.rect.move(x, y)
		self.gui.screen.fill((0, 0, 0))
		for c in self.children:
			c.rect = c.rect.move(x, y)
			if type(c) == base_gui.ButtonOK:
				c.update()

	def display(self):
		if self.is_error():
			self.on_error()
			return

		for child in self.children:
			print(child.rect.bottom)
			child.display()

		#  If border is made a fundamental object then it we don't need to override the display()
		self.border = pygame.draw.rect(self.screen,
									   self.border_color,
									   self.rect,
									   self.default_dict['panel_border'])


	def change_background_color(self, color):
		if self.valid_color(color):
			# self.background is a DefaultColorBlock object

			self.background_color = color
			self.children[0].color = self.background_color
			self.changed = True

	def create_button(self, x, y, some_func, text, kind):
		if kind == 'text':
			self.children.append(buttons.Button(self, x, y, some_func, text, self.default_dict))
		elif kind == 'image':
			self.children.append(buttons.ButtonImage(self, x, y, some_func, text, self.default_dict))
		elif kind == 'toggle':
			self.children.append(buttons.ButtonToggleImage(self, x, y, some_func, text, self.default_dict))
		elif kind == 'ok':
			self.children.append(buttons.ButtonOK(self, x, y, some_func, text, self.default_dict))
		else:
			self.error['create_invalid_button'] = f'Creating invalid button type {kind} in panel {self.name}'


	def create_button_ok(self, text, x, y):
		self.children.append(buttons.ButtonOK(text, self, x, y, [], self.default_dict))

	def create_treeview(self, name, x, y):
		self.children.append(tree_view.TreeView(name, self, x, y, self.default_dict))
		return self.children[-1]

	def create_dropdown_title(self, text, x, y, num_entries_visible, entries_list, function, length):
		# The dropdown list creates its own panel, but looks like a defaultLabel at present found in another panel
		self.children.append(base_gui.DropDown(self, text, x, y, num_entries_visible, entries_list, function, length))

	def create_label(self, text, x, y, justify='left', fontsize=None, label_name=False):
		self.children.append(labels.DefaultLabel(text, self, x, y, justify, self.default_dict, fontsize, label_name))
		if self.children[-1].error:
			del self.children[-1]
		else:
			if label_name:
				self.named_children_dict[label_name] = self.children[-1]

	def create_background_color(self, color, rect):
		self.children.append(pygame.draw.rect(self.screen, color, rect))
		self.changed = True

	def __str__(self):
		return ('Panel object at {}, {} with width {} and height {}'.format(self.x, self.y,
																			self.width, self.height))


class PanelScroll(DefaultPanel):
	def __init__(self, gui, name, x, y, width, height, full_list, view_num, default_dict=base_gui.load_defaults(), visible=True,
				 active=True):
		# DefaultPanel.__init__(self, gui, name, x, y, width, height, default_dict=load_defaults(), visible=True,
		# 					  active=True)
		DefaultPanel.__init__(self, gui, name, x, y, width, height)

		self.full_list = full_list
		self.view_num = view_num
		self.scrollbar = None
		self.scrollbar_changed = False

	def create_scrollbar(self, lowest_thumb_y, max_entries, visible_entries, orientation='vertical'):
		#  lowest_thumb_y is the lowest point the scrollbar thumb.y can be in the panel
		if orientation == 'vertical':
			# Change to a horizontal and vertical
			# TODO Add max_v
			print(f'Creating scrollbar in panel {lowest_thumb_y}, {self.height}, {self.height * (self.height / lowest_thumb_y)}')
			self.scrollbar = (scrollbars.Scrollbar(self, lowest_thumb_y, max_entries, visible_entries))
			self.children.append(self.scrollbar)

	def get_output_list(self):
		first_index = self.scrollbar.get_element()
		return self.full_list[first_index: first_index + self.view_num]


class PanelDropDownScroll(PanelScroll):
	def __init__(self, gui, name, x, y, width, height, full_list, view_num, dropdown, default_dict=base_gui.load_defaults(),
				 visible=True, active=True):
		PanelScroll.__init__(self, gui, name, x, y, width, height, full_list, view_num)
		#  As the name implies, this is created and controlled by a drop down label from another panel.
		self.dropdown = dropdown
		self.active_label = None
		self.highlight = None    # On mouseover
		self.old_highlight = True

	def display(self):
		self.dropdown.populate_list()
		super().display()


	def create_label(self, text, x, y, justify='left', fontsize=None, label_name=False):
		self.children.append(labels.DropDownListLabel(text, self, x, y, justify, self.default_dict, fontsize, label_name))
		if self.children[-1].error:
			del self.children[-1]
		else:
			if label_name:
				self.named_children_dict[label_name] = self.children[-1]

class PanelDynamicScrollbar(DefaultPanel):
	def __str__(self, gui, name, x, y, width, height, default_dict=base_gui.load_defaults(), visible=True, active=True):
		DefaultPanel.__init__(self, gui, name, x, y, width, height, default_dict=base_gui.load_defaults(), visible=True, active=True)
		pass
		self.scrollbar = False

	def check_for_scrollbar(self):
		#  Need to compare check self.scrollbar.% movement then show
		pass

	def union_all(self):
		output = self.children[0]
		for child in self.children:
			try:
				output = output.union(child.rect)
			except AttributeError:
				for kid in child.children:
					try:
						output = output.union(kid.rect)
					except AttributeError:
						self.error['child_child_rect'] = f'{child} has no rect, {child.kid} has no rect, panel.union_all()'
				self.error['child_rect'] = f'{child} has no rect, panel.union_all()'
		return output

	def display(self):
		#  Need to check the to_display Rect against the panel.rect.  If the scrollbar is need it is created in this method
		#  if one exists and is no longer required, delete it.
		self.check_for_scrollbar()
		if self.scrollbar:
			pass



######################################
#
# Imports

from color_blocks import PanelColorBlock
import labels, buttons, tree_view, scrollbars