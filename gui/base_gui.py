"""
Here is the basic class that describes buttons, panels, labels, etc.

They will be overwritten if a different look, color etc is required.

"""
import pygame




def return_correct_type(var_in):
	try:
		if int(var_in):
			var_in = int(var_in)
	except ValueError:
		try:
			if var_in[0] == '(':
				#tuple
				r, g, b = var_in[1:-1].split(',')
				var_in = (int(r), int(g), int(b))
		except:
			#a string
			pass
	return var_in
		
def load_defaults():
	with open('defaults.txt','r') as default_file:
		which = {}
		for line in default_file:
			if not line[0] == '#':
				attribute, value = line.strip().split(':')
				value=return_correct_type(value)
				which[attribute]=value
	default_file.close()
	return(which)

def format_text(text, line_length):
	'''

	:param text: String. Raw text input, with line breaks
	:param line_length: Int.
	:return: List. Lines formatted to be under the line length
	'''
	output = []
	paragraphs = text.split('\n')
	for p in paragraphs:
		words = p.split(' ')
		# Indent for start of paragraph
		line = '    '
		for w in words:
			if len(line) + len(w) + 7 < line_length:
				line = ' '.join([line, w])
			else:
				output.append(line)
				# Add a space to the end of the current line
				line = w.ljust(len(w)+1)
		output.append(line)
	return(output)


class BaseGui():
	def __init__(self):
		self.error = {}
		self.visible = False
		self.children=[]
		self.str = 'BaseObject'


	def display(self):
		if self.is_error():
			self.on_error()
			return

		for child in self.children:
			child.display()

	def update(self):
		pass

	def is_error(self):
		if len(self.error) > 0:
			return True
		else:
			return False
			
			
	def on_error(self):
		print(f'Errors detected in {self}')
		for value in self.error:
			print(f'{value} : {self.error[value]}')
			
	def valid_color(self, color):
		if isinstance(color, tuple) and len(color) == 3:
			for i in color:
				if i < 0 or i > 255:
					self.error['invalid_color'] = f'{color} out of bounds (0 - 255)'
					return False
			return True
		self.error['invalid_color'] = f'{color} is not a tuple or has the wrong length'
		return False

	def __str__(self):
		return self.str

class BaseVisibleObject():
	def __init__(self):
		self.x = 0
		self.y = 0
		self.children = []

	def offset_xy(self, x, y):
		self.x += x
		self.y += y




class MessageBox(BaseGui):
	def __init__(self, name, title, text, gui, default_dict=load_defaults()):
		BaseGui.__init__(self)
		self.default_dict = default_dict
		self.title = title
		self.text = text
		self.gui = gui
		self.screen = self.gui.screen
		# Make existing panels on the screen inactive to the input
		self.gui.panels_inactivate()
		formatted_text = format_text(self.text, self.default_dict['msg_chars_on_line'] )
		end_of_text_y = (2 * self.default_dict['msg_text_y']) + (self.default_dict['msg_label_fontsize'] + 5) * len(
																										formatted_text)
		# Create the main panel
		gui.create_panel(name, 150, 20, 500,
						 end_of_text_y + self.default_dict['button_height'] + self.default_dict['msg_text_y'])

		# Get the active panel name
		self.panel = gui.panel_dict[name]
		# Set the correct background color rather than panel default_dict
		self.panel.change_background_color(self.default_dict['msg_background_color'])

		# Create background for title
		self.title_background = color_blocks.DefaultColorBlock(self.panel, self.default_dict['msg_title_background_color'],
													  (self.panel.rect.x + self.default_dict['panel_border'],
													   self.panel.rect.y + self.default_dict['panel_border'],
													   self.panel.rect.width - self.default_dict['panel_border'] * 2,
													   self.default_dict['msg_title_height']))
		# panel.children.append(title_background)
		self.title_background.drag_with_mouse = True
		self.panel.create_label(title,
						   self.default_dict['msg_title_x'],
						   self.default_dict['msg_title_y'],
						   justify='center')
		for i, line in enumerate(formatted_text):
			self.panel.create_label(line,
							   self.default_dict['msg_text_x'],
							   self.default_dict['msg_text_y'] + i * (self.default_dict['msg_label_fontsize'] + 5),
							   fontsize=self.default_dict['msg_label_fontsize'])
		self.gui.create_button_ok(self.panel, self.default_dict['msg_text_x'], end_of_text_y)



class DropDown(BaseGui):
	def __init__(self, parent, name, x, y, num_visible_entries, entries_list, function, length):
		BaseGui.__init__(self)
		self.default_dict = load_defaults()
		self.parent = parent
		self.name = name
		self.x = x
		self.y = y
		self.entries_list = entries_list
		self.num_visible_entries = num_visible_entries
		#  This is the lowest value of y if every item in the list was displayed
		self.max_height = len(entries_list) * self.default_dict['dropdown_line_height'] + 2 * self.default_dict['dropdown_line_header']
		self.function = function
		self.length = length
		self.set_length_of_text(self.name)

		# Name of down down panel to be displayed.
		self.panel_name = 'Drop Down' #only 1 drop down active at a time, so when a new drop down is activated it overwrites this
		#  The raw panel without any labels in it. Saves using a slice which cannot handle adding images etc to the base panel.
		self.dropdown_panel_empty = []
		self.justify = 'left'
		self.default_dict = load_defaults()
		self.fontsize = self.default_dict['label_fontsize']

		self.children.append(labels.DropDownTitleLabel(self.name, self.parent, x, y, self.justify, default_dict=self.default_dict, fontsize=self.fontsize, label_name='drop_list'))
		self.rect = self.children[-1].rect
		self.height = self.default_dict['dropdown_line_height'] * self.num_visible_entries + self.default_dict['dropdown_line_header']
		self.display_list_visible = False
		self.str = f'Dropdown title label and image: {name}.'

	def set_length_of_text(self, text_):
		if self.length == 0:
			return
		elif self.length < len(text_):
			self.error['dropdown_title_text_length'] = f'Length is {len(self.length)} chars, text_ is {len(text_)}'
		elif self.length >= len(text_):
			self.text = f'{text_:{self.length}}'

	def display_list(self):
		# self.parent.gui.dropdown_active = True # Lets the main event loop know it is looking at mouse over the panel
		#creates new panel_dropdown_scroll object and populates it
		y = self.y + self.parent.y + self.default_dict['dropdown_y_offset']

		if not self.display_list_visible:
			# First time the window opens
			_x = self.x + self.parent.x - self.default_dict['dropdown_label_left_margin']
			_y = y + self.parent.y
			#  Go back to baseGui.create_dropdown_scroll_panel to create a new panel and populate it.
			try:
				self.panel = self.parent.gui.panel_dict[self.panel_name]
			except:
				#  No panel with name 'drop down' exists.
				self.create_panel(_x, _y)
				self.dropdown_panel_empty = self.panel.children
			else:
				if self.panel.children == []:  #  Used a dropdown and it has been set to [] after closing
					self.create_panel(_x, _y)
				self.panel.children = self.dropdown_panel_empty
			self.populate_list()

		self.display_list_visible = True

	def create_panel(self, _x, _y):
		self.parent.gui.create_dropdown_scroll_panel(self.panel_name,
													 _x,
													 _y,
													 self.default_dict['dropdown_width'],
													 self.height,
													 self.entries_list,
													 self.num_visible_entries,
													 self)
		#  Do we need to call this through parent.gui.create_scrollbar, why not just self.children.append(DefaultScrollbar)
		self.parent.gui.create_scrollbar(self.panel_name, self.max_height, len(self.entries_list),
										 self.num_visible_entries, 'vertical')
		#  Populate the base panel.
		self.panel = self.parent.gui.panel_dict[self.panel_name]
		self.dropdown_panel_empty = self.panel.children

	def populate_list(self):
		# Get rid of the labels in the panel and add the new ones
		y = self.default_dict['dropdown_line_header']
		#  Reset the panel to factory defaults without any labels.
		self.panel.children = self.dropdown_panel_empty[:]

		for entry in self.panel.get_output_list():
			# the label created is overwritten in a panel drop down list panel
			self.parent.gui.create_label(self.panel_name, entry, self.default_dict['dropdown_label_left_margin'], y)
			y += self.default_dict['dropdown_line_height']


	def on_click(self, name):
		# When an element from the drop down list is clicked
		self.function(name)
		self.set_length_of_text(name)
		self.children[0].change_text(name)
		self.parent.gui.hide_panel('Drop Down')
		self.parent.gui.dropdown_active = False
		self.display_list_visible = False
		self.parent.gui.panel_dict['Drop Down'].children = []





################################################################################
#
# Do imports here


import panels, labels, color_blocks, buttons, tree_view, event_loop_methods, scrollbars


BUTTONS = (buttons.DefaultButton, buttons.Button, buttons.ButtonOK, buttons.ButtonImage)
MOUSE_DEFAULT = 0
MOUSE_DROPDOWN_ACTIVE = 1
MOUSE_SCROLLBAR = 2

class GuiManager(BaseGui):

	def __init__(self, screen, default_dict):
		BaseGui.__init__(self)
		self.screen = screen
		self.default_dict = default_dict

		self.error = {}


		self.panels = []
		self.font_dict = {}
		self.panels_on_screen = []
		self.panel_dict = {}
		self.lmb_pressed = False
		self.mouse_x = 0
		self.mouse_y = 0
		self.element_moving = False
		self.dropdown_active = None
		self.mouse_state = None

		self.initial_setup()

	def initial_setup(self):
		screen_rect = self.screen.get_rect()
		self.create_panel('Main Panel', 0, 0, screen_rect.width, screen_rect.height,
						  default_dict=None, visible=True, active=True, scrollable=False)
		self.panel_dict['Main Panel'].change_background_color( (122,0,0) )#self.default_dict['main_panel_background_color'])
		self.panel_dict['Main Panel'].display()

	def hide_panel(self, panel_name):
		panel = self.panel_dict[panel_name]
		panel.visible = False
		panel.active = False
		redraw_screen = False
		if panel.visible == True:
			panel.changed = True
		for p in self.panels:
			# When removing a panel, check to make sure panels below are re displayed
			if p.visible:
				if p.rect.colliderect(panel.rect):
					p.changed = True
		self.display()

	def display(self):

		for panel_name, panel in self.panel_dict.items():
			if panel.visible == True and panel.changed == True:
				panel.display()
				panel.changed = False

	def on_lmb_click(self, pos):

		dropdown_text = None
		for panel_name, panel in self.panel_dict.items():
			if panel.active and panel.rect.collidepoint(pos):
				for element in panel.children:
					if not self.lmb_pressed:
						#Button is not currently held down
						if not self.dropdown_active:
							#  Drop down active renders the rest of the UI invalid until an option from the dropdown is selected.
							if isinstance(element, BUTTONS)and element.rect.collidepoint(pos):
								event_loop_methods.button_clicked(element)
							elif isinstance(element, tree_view.TreeView):
								event_loop_methods.treeview_clicked(element, pos)
							elif isinstance(element, color_blocks.DefaultColorBlock):
								#  Clicking a title bar to move a window.
								event_loop_methods.move_panel(element, panel, pos, self)
							elif isinstance(element, DropDown) and element.children[0].background_rect.collidepoint(pos):
								self.lmb_pressed = True
								self.dropdown_active = element
							elif isinstance(element, scrollbars.DefaultScrollbar) and element.thumb.rect.collidepoint(pos):
								event_loop_methods.mouse_left_scrollbar(self, element, pos)

						elif isinstance(element, (scrollbars.Scrollbar)) and element.thumb.rect.collidepoint(pos):
							event_loop_methods.mouse_left_scrollbar(self, element, pos)
						elif panel.name == 'Drop Down':
							#  Clicking on an option from the drop down menu.
							if isinstance(element, labels.DefaultLabel) and element.get_text_surface().rect.collidepoint(pos):
								# get drop list and work update on the clicked element
								self.lmb_pressed = True
								self.dropdown_active.on_click(element.text) # that works, the Data panel is updated

		if self.dropdown_active:
			self.dropdown_active.display_list()


	def on_lmb_up(self, pos):
		self.lmb_pressed = False
		if self.element_moving:
			x_diff = pos[0] - self.mouse_x
			y_diff = pos[1] - self.mouse_y
			self.element_moving.update_pos(x_diff, y_diff)
			self.element_moving = False

	def on_mousemove_dropdown(self, pos):
		# Run from main pygame loop
		#This highlights the text when mouseover
		#  This needs moving to the dropdown class.
		panel = self.panel_dict['Drop Down']
		if panel.rect.collidepoint(pos):
			#We are over drop down panel with the mouse
			if self.lmb_pressed:
				panel.scrollbar.update_pos(pos[0] - self.mouse_x, pos[1] - self.mouse_y)
			for child in panel.children:
				if isinstance(child, labels.DropDownListLabel) and child.get_text_surface().rect.collidepoint(pos):
					panel.highlight = child.text
					if panel.highlight != panel.old_highlight:
						panel.changed = True
						panel.old_highlight = panel.highlight
		else:
			panel.changed = True
			panel.highlight = None


	def create_scroll_panel(self, name, x, y, width, height, full_list,
							num_visible, default_dict=None, visible=True, active=True, scrollable=False):
		self.panel_dict[name] = (panels.PanelScroll(self, name, x, y, width, height, full_list, num_visible, visible=True, active=True))

	def create_dropdown_scroll_panel(self, name, x, y, width, height, full_list, num_visible, dropdown, default_dict=None,
									 visible=True, active=True, scrollable=False):
		self.panel_dict[name] = (panels.PanelDropDownScroll(self, name, x, y, width, height, full_list, num_visible, dropdown, visible=True, active=True))


	def create_panel(self, name, x, y, width, height, default_dict=None, visible=True, active=True, scrollable=False):
		if default_dict == None:
			default_dict = self.default_dict
		if name in self.panel_dict:
			self.error['panel_name_exists'] = name
			return
		#self.panel_dict[name] = panels.DefaultPanel(self, name, x, y, width, height, default_dict, visible, active)
		self.panel_dict[name] = panels.PanelDynamicScrollbar(self, name, x, y, width, height, default_dict, visible, active)

		self.panels.append(self.panel_dict[name])
		if visible:
			self.panels_on_screen.append(self.panel_dict[name])

	def create_button(self, panel_name, x, y, functions, text, kind='text'):
		panel = self.panel_dict[panel_name]
		if self.is_error() == False:
			panel.create_button(x, y, functions, text, kind)

	def create_button_ok(self, panel, x, y):
		if self.is_error() == False:
			panel.create_button_ok('OK', x, y)

	def create_scrollbar(self, panel_name, max_height, num_entries, visible_entries, orientation='vertical'):
		if not orientation in ['vertical', 'horizontal']:
			self.error['scrollbar_orientation'] = 'Scrollbar in panel {}'.format(panel_name)
		panel = self.panel_dict[panel_name]
		if self.is_error() == False:
			panel.create_scrollbar(max_height, num_entries, visible_entries, orientation)


	def create_dropdown_title(self, panel_name, text, x, y, num_entries_visible, entries_list, function, length=0):
		# This creates the special label for drop down titles, clicking this will open a new panel with a scrollbar
		panel = self.panel_dict[panel_name]
		if self.is_error() == False:
			panel.create_dropdown_title(text, x, y, num_entries_visible, entries_list, function, length)

	def create_label(self, panel_name, text, x, y, justify='left', fontsize=None, label_name=False):
		panel = self.panel_dict[panel_name]
		if self.is_error() == False:
			panel.create_label(text, x, y, justify, fontsize, label_name)

	def create_dropdown_list_label(self, panel_name, text, x, y, justify='left', fontsize=None, label_name=False):
		panel = self.panel_dict[panel_name]
		if self.is_error() == False:
			panel.create_dropdown_list_label(text, x, y, justify, fontsize, label_name)

	def create_treeview(self, panel_name, name, x, y):
		panel = self.panel_dict[panel_name]
		if not self.is_error():
			return panel.create_treeview(panel, x, y)


	def change_label_text(self, panel_name, label_name, text):
		panel = self.panel_dict[panel_name]
		label = panel.named_children_dict[label_name]
		label.change_text(text)

	def get_panel_by_name(self, name):
		for panel in self.panels:
			if name == panel.name:
				return(panel)

		self.error['unknown_panel_name'] = '{} not found in GuiManger.panels'.format(name)
		print(self.error)

	def create_message_box(self, name, title, text, gui_defaults):
		MessageBox(name, title, text, self)