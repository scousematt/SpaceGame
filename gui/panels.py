import pygame
import base_gui
from color_blocks import PanelColorBlock, BlockWithBorder
import labels, buttons, tree_view, scrollbars, dialogs

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
		#  Elements of the object that will be displayed no matter the internal movement of the children. This is where images for corners
		#  and title bars, [x], etc would be.
		self.static_children = []
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.static_children.append(PanelColorBlock(self, self.background_color, self.rect))
		self.static_children.append(BlockWithBorder(self, self.border_color, self.rect, self.default_dict['panel_border'] ))
		#  What is this used for?
		self.named_children_dict = {}

		self.str = f'{self.name} {type(self)} at {self.x}, {self.y}'


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
		print('We are in defaultpanel display')

		for static in self.static_children:
			static.display()
		for child in self.children:
			child.display()

		# #  If border is made a fundamental object then it we don't need to override the display()
		# self.border = pygame.draw.rect(self.screen,
		# 							   self.border_color,
		# 							   self.rect,
		# 							   self.default_dict['panel_border'])


	def change_background_color(self, color):
		if self.valid_color(color):
			# self.background is a DefaultColorBlock object

			self.background_color = color
			for static in self.static_children:
				if isinstance(static, PanelColorBlock):
					static.color = self.background_color
					self.changed = True
					return

			self.error['no_panel_block'] = f'Change background in panel {self.name} cannot find PanelColorBlock'

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
			print(f'Creating scrollbar in panel {self.name}, panel height {self.height}, height of thumb {self.height * (self.height / lowest_thumb_y)}')
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
	def __init__(self, gui, name, x, y, width, height, default_dict=base_gui.load_defaults(), visible=True, active=True):
		DefaultPanel.__init__(self, gui, name, x, y, width, height)
		self.scrollbar = False
		#  While self.rect is the panel dimension, need a value for the overall height of the contents regardless of what is displayed.
		self.total_y = self.rect.height
		#  Displayed rect is the show output from total_rect, initially set to the panel rect
		self.display_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h) #  Making sure that the 2 rects are not same in memory.
		self.old_display_rect_y = self.display_rect.y
		self.change_y = 0
		self.total_change_y = 0
		self.lowest_y = 0
		self.str = f'DynamicScrollbar'

	def check_for_scrollbar(self):
		#  Need to compare check self.scrollbar.% movement then show
		#if not self.display_rect.contains(self.total_rect):
		if self.total_y > self.display_rect.height:
			#  The contents are larger than the panel.
			if not self.scrollbar:
				self.scrollbar = scrollbars.DefaultScrollbar(self)
				#  The scrollbar will be present in the same place no matter the content, so add to static_children.
				#  if added to static children, it will not be examined in the gui loop.
				self.static_children.append(self.scrollbar)
			self.scrollbar.update()
		else:
			if self.scrollbar:
				self.static_children.remove(self.scrollbar)
			self.scrollbar = None
			self.display_rect.top = self.rect.top
		#  If scrollbar exists then

	def set_display_rect(self, y=False, bottom=False, top=False):
		#  What if more than one is true? Altering display_rect elsewhere could make maintainence difficult.
		self.old_display_rect_y = self.display_rect.y
		if y:
			self.display_rect.y = y
		elif bottom:
			self.display_rect.bottom = bottom
		else:
			self.display_rect.top += top
		self.change_y = self.old_display_rect_y - self.display_rect.y

	def display(self):
		y_change = self.old_display_rect_y - self.display_rect.y
		self.total_change_y += y_change
		_lowest = 10000
		_total_y_list = []
		_min_y = 100000
		_max_y = 0
		for child in self.children:
			child.update(y_change)
			_min_y = min(_min_y, child.rect.y)
			_max_y = max(_max_y, child.rect.bottom)
			if child.y - self.rect.y < _lowest:
				#  Find the closest child to the top of the frame
				_lowest = child.y - self.rect.y
		#  Now that all the interior elements have been updated, recalculate the self.total_rect.
		if len(self.children)> 0:
			#  TODO is display being run without the children created?
			self.total_y = abs(_max_y) - abs(_min_y) + _lowest

		print(self.total_y)
		self.check_for_scrollbar()



		if self.is_error():
			self.on_error()
			return
		for static in self.static_children:
			static.display()
		for child in self.children:
			child.display()


class PanelDialog(DefaultPanel, dialogs.DefaultDialog):
	def __init__(self, gui, name, title, text, default_dict=base_gui.load_defaults(), visible=True, active=True):
		dialogs.DefaultDialog.__init__(self, gui, title, text, default_dict=base_gui.load_defaults())
		DefaultPanel.__init__(self, gui, name, self.x, self.y, self.width, self.height, default_dict=base_gui.load_defaults(), visible=True, active=True)

		self.static_children.append(PanelColorBlock(self, self.default_dict['msg_title_background_color'], self.title_rect))
		self.static_children.append(labels.DefaultLabel(self.title, self,
														self.default_dict['msg_title_x'],
														self.default_dict['msg_title_y'], justify='centerx'))

		#  Add the main text
		for i, line in enumerate(self.formatted_text):
			self.create_label(line,
								self.default_dict['msg_text_x'],
								self.default_dict['msg_text_y'] + i * (self.default_dict['msg_label_fontsize'] + 5),
								fontsize=self.default_dict['msg_label_fontsize'])
