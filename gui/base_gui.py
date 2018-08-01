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


class BaseGui:
	def __init__(self):
		self.error = {}
		self.visible = False
		
	def is_error(self):
		if len(self.error) > 0:
			return True
		else:
			return False
			
			
	def on_error(self):
		print('Errors detected in {}'.format(self))
		for value in self.error:
			print('{} : {}'.format(value, self.error[value]))
			
	def valid_color(self, color):
		if type(color) == tuple and len(color) == 3:
			for i in color:
				if i < 0 or i > 255:
					self.error['invalid_color'] = color
					return False
			return True
		self.error['invalid_color'] = color
		return False


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
		# Set the correct background color rather than panel defaults
		self.panel.change_background_color(self.default_dict['msg_background_color'])

		# Create background for title
		self.title_background = DefaultColorBlock(self.panel, self.default_dict['msg_title_background_color'],
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


class DefaultLabel(BaseGui):

	def __init__(self, text, parent, x, y, justify='left', default_dict=load_defaults(), fontsize=None, label_name=None):
		BaseGui.__init__(self)
		self.default_dict = default_dict
		self.parent = parent
		self.text = text
		if isinstance(self.text, int):
			#here we can test to see if we want colored numbers (red , green) or brackets around -ve
			str(self.text)

		self.name = label_name

		self.x = x + self.parent.x
		self.y = y + self.parent.y
		self.default_dict = default_dict
		self.justify = justify    #left or right, on centre y
		self.text_color = self.default_dict['label_color']
		self.fontname = self.default_dict['label_font']

		if fontsize == None:
			self.fontsize = self.default_dict['label_fontsize']
		else:
			self.fontsize = return_correct_type(fontsize)

		try:
			# Check to see if a font object has already been created
			self.font = self.parent.gui.font_dict[''.join([self.fontname, str(self.fontsize)])]
		except KeyError:
			self.font = pygame.font.Font(self.fontname, self.fontsize)
			self.parent.gui.font_dict[''.join([self.fontname, str(self.fontsize)])] = self.font
		except:
			try:
				#A dropdown list is the parent, rather than a panel
				self.font = self.parent.parent.gui.font_dict[''.join([self.fontname, str(self.fontsize)])]
			except KeyError:
				self.font = pygame.font.Font(self.fontname, self.fontsize)
				self.parent.parent.gui.font_dict[''.join([self.fontname, str(self.fontsize)])] = self.font

			except:
				self.error['font'] = True
		if not self.is_error():
			self.change_text(self.text)
		

			
				
	def change_text(self, new_text):
		self.text = new_text
		if type(self.text) == int:
			#here we can test to see if we want colored numbers (red , green) or brackets around -ve
			self.text  = str(self.text)
		self.text_surface = self.font.render(	self.text,
												True, 
												self.text_color)
		self.rect = self.text_surface.get_rect()

		if self.justify == 'left':
			self.rect.topleft = self.x, self.y
		elif self.justify == 'right':
			self.rect.topright = self.x, self.y
		else:
			self.rect.topleft = self.parent.x + (self.parent.width - self.rect.width) / 2, self.y
		#Check to see if label is within panel
		if not self.parent.rect.contains(self.rect):
			if self.parent.rect.left > self.rect.left or self.parent.rect.right > self.rect.right:
				self.error['out_of_panel_horizontal'] = self
			elif self.parent.rect.top > self.rect.top or self.parent.rect.bottom > self.rect.bottom:
				self.error['out_of_panel_vertical'] = self

		self.parent.changed = True


		
	def change_color(self, color):
		if self.valid_color(color):
			self.text_color = color
			self.change_text(self.text) # recaulate the text surface
		self.parent.changed = True
	
	def display(self):
		if self.is_error():
			self.on_error()
			return
		self.parent.screen.blit(self.text_surface, self.rect)

	def __str__(self):
		if self.justify == 'right':
			return('Label "{}" from Panel "{}" right justified x is rhs'.format(self.text, self.parent.name))
		else:
			return ('Label "{}" from Panel "{}"'.format(self.text, self.parent.name))

class DefaultColorBlock(BaseGui):

	def __init__(self, panel, color, rect, drag_with_mouse=False):
		# This is for things internal to panels where a block of color is needed, things like message box title background
		# it is essentially a colored pygame.rect
		BaseGui.__init__(self)
		self.panel = panel
		self.color = color
		self.rect = pygame.Rect(rect)
		self.drag_with_mouse = drag_with_mouse
		self.add_to_children()

	def add_to_children(self):
		self.panel.children.insert(1, self)

	def display(self):
		pygame.draw.rect(self.panel.screen,
						 self.color,
						 self.rect)

class ScrollbarColorBlock(DefaultColorBlock):
	def __init__(self, panel, color, rect, parent, drag_with_mouse=False):
		DefaultColorBlock.__init__(self, panel, color, rect, drag_with_mouse=False)
		self.parent = parent
		self.line_width = self.parent.line_width
		self.color = color
		self.rect = rect
		self.highlight_color = (self.color[0] + 50, self.color[1] + 50, self.color[2] + 50)
		self.shadow_color = (self.color[0] - 50, self.color[1] - 50, self.color[2] - 50)

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

class DropList(BaseGui):
	def __init__(self, parent, text, x, y, num_visible_entries, entries_list, function):
		BaseGui.__init__(self)
		self.default_dict = load_defaults()
		self.parent = parent
		self.text = text
		self.x = x
		self.y = y
		self.entries_list = entries_list
		self.num_visible_entries = num_visible_entries
		self.max_height = len(entries_list) * self.default_dict['dropdown_line_height'] + 2 * self.default_dict['dropdown_line_header']
		self.function = function

		self.justify = 'left'
		self.default_dict = load_defaults()
		self.fontsize = self.default_dict['label_fontsize']
		self.children = []
		self.children.append(DefaultLabel(self.text, self.parent, x, y, self.justify, default_dict=self.default_dict, fontsize=self.fontsize, label_name='drop_list'))
		self.height = self.default_dict['dropdown_line_height'] * self.num_visible_entries + self.default_dict['dropdown_line_header']
		self.display_list_visible = False
		self.list_index = 0

	def display(self):
		# This should display only the label
		for element in self.children:
			element.display()

	def display_list(self):
		# The label has been clicked so we need a panel to open, populated and with a scrollbar if necessary
		panel_name = 'Drop Down'

		new_index = 0
		#x = self.x + self.parent.x + self.default_dict['dropdown_x_offset']
		y = self.y + self.parent.y + self.default_dict['dropdown_y_offset']
		print(self.display_list_visible)

		try:
			new_index = self.panel.children[3].list_element
		except:
			self.list_index = 0
		if new_index != self.list_index:
			self.list_index = new_index
			self.display_list_visible = False

		print('list index', self.list_index)
		if not self.display_list_visible:
			print('display list false')
			self.parent.gui.create_scroll_panel(panel_name, self.x + self.parent.x - self.default_dict['dropdown_label_left_margin'],
										y + self.parent.y, self.default_dict['dropdown_width'], self.height,
										self.entries_list, self.num_visible_entries)
			print(self.parent.gui.panel_dict)
			self.panel = self.parent.gui.panel_dict[panel_name]
			self.parent.gui.create_scrollbar(panel_name, self.max_height, len(self.entries_list), self.num_visible_entries, 'vertical')


			y = self.default_dict['dropdown_line_header']

			for entry in self.entries_list[self.list_index: self.list_index + self.num_visible_entries]:
				self.parent.gui.create_label(panel_name, entry, self.default_dict['dropdown_label_left_margin'], y)
				y += self.default_dict['dropdown_line_height']
		self.display_list_visible = True



	def on_click(self, name):
		# When an element from the drop down list is clicked
		self.function(name)
		self.parent.gui.hide_panel('Drop Down')
		self.parent.gui.dropdown_active = None
		self.display_list_visible = False
		self.parent.gui.panel_dict['Drop Down'].children = []

class PanelColorBlock(DefaultColorBlock):

	def __init__(self, panel, color, rect, drag_with_mouse=False):
		DefaultColorBlock.__init__(self, panel, color, rect, drag_with_mouse=False)

	def add_to_children(self):
		self.panel.children.insert(0, self)

class DefaultButton(BaseGui):
	def __init__(self, text, panel, x, y, function_list, default_dict=load_defaults()):
		BaseGui.__init__(self)
		
		
		self.text = text
		self.panel = panel
		
		#self.error = error
		self.x = x + panel.x
		self.y = y + panel.y

		
		self.default_dict = default_dict
		
		self.button_color = default_dict['button_color']
		self.button_shadow_color = default_dict['button_shadow_color']
		self.button_highlight_color = default_dict['button_highlight_color']
		self.text_color = default_dict['button_text_color']
		
		#Fonts
		self.fontname = default_dict['button_font']
		self.fontsize = default_dict['button_fontsize']
		try:
			self.font = pygame.font.Font(self.fontname, self.fontsize)
		except:
			self.error['font'] = True

		self.width = default_dict['button_width']
		self.height = default_dict['button_height']
				
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

		self.offset = default_dict['button_highlight_offset']
		
		# This is the rect that contains the whole button
		self.shadow_rect = self.rect.inflate(self.offset * 2, self.offset * 2)
		
	
		self.create_highlight_coords()	
		self.change_text(text)

		self.panel.changed = True
		self.function_list = function_list
		if self.function_list == []:
			self.function_list = [self.close_panel]
		self.function_index = 0
		print(self.function_list)
		self.on_click_method = self.function_list[self.function_index]
	

	def update(self):
		self.text_rect.center = ((self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2))
		self.create_highlight_coords()
		self.shadow_rect = self.rect.inflate(self.offset * 2, self.offset * 2)

	def on_click(self):
		#
		# Note. A button can change things in other panels. self.panel.changed ??
		#
		# External function requires self, internal do not.
		try:
			return_method =  self.on_click_method(self)
		except TypeError:
			return_method = self.on_click_method()
		self.function_index += 1
		if self.function_index == len(self.function_list):
			self.function_index = 0
		self.on_click_method = self.function_list[self.function_index]
		return return_method

	def close_panel(self):
		self.panel.screen.fill((0,0,0))
		self.panel.visible = False
		self.panel.active = False
		for panel in self.panel.gui.panels:
			if panel.visible:
				panel.active = True

	def check_text_size(self):
		if self.text_rect.width > self.width:
			self.error['text_width'] = True
		if self.text_rect.height > self.height:
			self.error['text_height'] = True

	def change_text(self, new_text):
		# TODO text should be a label, so it can update position correctly
		self.text = new_text
		self.text_surface = self.font.render(	new_text, 
												True, 
												self.text_color)
		self.text_rect = self.text_surface.get_rect()
		self.check_text_size()

		self.text_rect.center = ((self.x + self.width//2, self.y + self.height//2))
		if not self.panel.rect.contains(self.text_rect):
			self.error['out_of_bounds'] = self
		self.display()

	def create_highlight_coords(self):
		
		self.highlight_coords = [(self.rect.x - self.offset, self.rect.y - self.offset),
							(self.rect.x + self.rect.w + self.offset, self.rect.y - self.offset),
							(self.rect.x + self.rect.w, self.rect.y),
							(self.rect.x, self.rect.y),
							(self.rect.x, self.rect.y + self.rect.h),
							(self.rect.x - self.offset, self.rect.y + self.rect.h + self.offset)]
	
	def display(self):
		if self.is_error():
			self.on_error()
			return()
		pygame.draw.rect(	self.panel.screen,
							self.button_shadow_color,
							self.shadow_rect)
		
		pygame.draw.polygon(	self.panel.screen,
								self.button_highlight_color,
								self.highlight_coords)
									
		pygame.draw.rect(	self.panel.screen,
							self.button_color,
							self.rect)
		
		self.panel.screen.blit(self.text_surface, self.text_rect)
		
	
	def __str__(self):
		return('Button object at {}, {} with text "{}"'.format(self.x - self.panel.x,
															self.y - self.panel.y,
															self.text))
	

class ButtonOK(DefaultButton):

	def __init__(self, text, panel, x, y, function_list=[], default_dict=load_defaults()):
		DefaultButton.__init__(self, text, panel, x, y, function_list=[])
		self.width = panel.width - (2 * self.default_dict['msg_text_x'])
		self.text = 'OK'
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

		self.offset = default_dict['button_highlight_offset']

		# This is the rect that contains the whole button
		self.shadow_rect = self.rect.inflate(self.offset * 2, self.offset * 2)

		self.create_highlight_coords()
		self.change_text(text)

class Scrollbar(BaseGui):
	def __init__(self, panel, button_max_height, max_entries, visible_entries, default_dict=load_defaults()):
		BaseGui.__init__(self)
		self.panel = panel
		self.button_height = (panel.height * (panel.height / button_max_height)) // 1
		self.button_max_height = button_max_height
		self.max_entries = max_entries
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

		self.children.append(DefaultColorBlock(self.panel, self.default_dict['scrollbar_color'], self.rect))
		self.children.append(ScrollbarColorBlock(self.panel,  self.default_dict['scrollbar_button_color'],
		 											self.button_rect, self, drag_with_mouse=True))
		#Created
		self.panel.changed = True

	def display(self):
		for child in self.children:
			#print(child.rect)
			child.display()

	def get_element(self):
		# This will return the index of the first line to be visible
		traverse = self.height - self.button_height
		step = (traverse / (self.max_entries - self.visible_entries)) // 1
		cur_pos = self.children[1].rect.y - self.panel.rect.top
		print('traverse', traverse, 'step', step, 'cur_pos', cur_pos)
		return int(cur_pos // step)

	def update_pos(self, x, y):
		max_y = self.y + self.height - self.button_height
		self.children[1].rect.y += y
		if self.children[1].rect.y < self.y:
			self.children[1].rect.y = self.y
		elif self.children[1].rect.y > self.y + self.height - self.button_height:
			self.children[1].rect.y = self.y + self.height - self.button_height
		self.panel.changed = True
		self.panel.visible = True
		self.list_element = self.get_element()
		print('before')

class DefaultPanel(BaseGui):

	def __init__(self, gui, name, x, y, width, height, default_dict=load_defaults(), visible=True, active=True):
		BaseGui.__init__(self)

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
		
		self.changed = False # updated by self.children objects
		self.children = []
		print(self.name, self.x, self.y, self.width, self.height)
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.background = PanelColorBlock(self, self.background_color, self.rect)
		self.named_children_dict = {}

	def update_pos(self, x, y):
		self.rect = self.rect.move(x, y)
		self.gui.screen.fill((0,0,0))
		for c in self.children:
			c.rect = c.rect.move(x, y)
			if type(c) == ButtonOK:
				c.update()

	def display(self):
		if self.is_error():
			self.on_error()
			return

		for child in self.children:
			child.display()

		self.border = pygame.draw.rect(self.screen,
								   self.border_color,
								   self.rect,
								   self.default_dict['panel_border'])


	def change_background_color(self, color):
		if self.valid_color(color):
			# self.background is a DefaultColorBlock object
			self.background.color = color
			self.changed = True

	def create_button(self, text, x, y, some_func):
		self.children.append(DefaultButton(text, self, x, y, some_func, self.default_dict))

	def create_button_ok(self, text, x, y):
		self.children.append(ButtonOK(text, self, x, y, [], self.default_dict))

	def create_scrollbar(self, max_height, max_entries, visible_entries, orientation='vertical'):
		if orientation == 'vertical':
			#Change to a horizontal and vertical
			# TODO Add max_v
			print(max_height, self.height, self.height * (self.height / max_height))
			self.children.append(Scrollbar(self, max_height, max_entries, visible_entries))

	def create_dropdown(self, text, x, y, num_entries_visible, entries_list, function):
		self.children.append(DropList(self, text, x, y, num_entries_visible, entries_list, function))

	def create_label(self, text, x, y, justify='left', fontsize=None, label_name=False):
		self.children.append(DefaultLabel(text, self, x, y, justify, self.default_dict, fontsize, label_name))
		if self.children[-1].error:
			del self.children[-1]
		else:
			if label_name:
				self.named_children_dict[label_name] = self.children[-1]

	def create_background_color(self, color, rect):
		self.children.append(pygame.draw.rect(self.screen, color, rect))
		self.changed = True

	def __str__(self):
		return('Panel object at {}, {} with width {} and height {}'.format(self.x, self.y,
																		self.width, self.height))

class PanelScroll(DefaultPanel):
	def __init__(self, gui, name, x, y, width, height, full_list, view_num, default_dict=load_defaults(), visible=True, active=True):
		# DefaultPanel.__init__(self, gui, name, x, y, width, height, default_dict=load_defaults(), visible=True,
		# 					  active=True)
		DefaultPanel.__init__(self, gui, name, x, y, width, height)


		self.full_list = full_list
		self.view_num = view_num

	def get_output_list(self, first_index):
		return self.full_list[first_index: first_index + self.view_num]



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
		self.buttons = [DefaultButton, ButtonOK]
		self.lmb_pressed = False
		self.mouse_x = 0
		self.mouse_y = 0
		self.element_moving = False
		self.dropdown_active = None


	def show_panel(self, panel_name):
		# Think this is replaced by the panel_dict
		for panel in self.panels:
			if panel.name == panel_name:
				panel.visible = True

	def hide_panel(self, name_of_panel):

		for panel_name, panel in self.panel_dict.items():
			if panel.name == name_of_panel:
				panel.visible = False
				panel.active = False
			if panel.visible == True:
				panel.changed = True

		self.display()

	def display(self):
		for panel_name, panel in self.panel_dict.items():
			# TODO check to see if panel is changed
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
						if (type(element) in self.buttons)and element.rect.collidepoint(pos):
							element.on_click()
						elif type(element) == DefaultColorBlock:
							if element.drag_with_mouse and element.rect.collidepoint(pos):
								self.lmb_pressed = True
								self.mouse_x = pos[0]
								self.mouse_y = pos[1]
								self.element_moving = panel
						elif type(element) == ScrollbarColorBlock and element.rect.collidepoint(pos):
							self.lmb_pressed = True
							self.mouse_x = pos[0]
							self.mouse_y = pos[1]
							# we want the scrollbar to update itself, not a scrollbar element
							self.element_moving = element.parent
						elif type(element) == DropList and element.children[0].rect.collidepoint(pos):
							self.lmb_pressed = True
							self.dropdown_active = element
						elif panel.name == 'Drop Down':
							if type(element) == DefaultLabel and element.rect.collidepoint(pos):
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
			print('change of {}, {}'.format(x_diff, y_diff))
			self.element_moving.update_pos(x_diff, y_diff)
			self.element_moving = False

	def on_mousemove_dropdown(self, pos):
		panel = self.panel_dict['Drop Down']
		if panel.rect.collidepoint(pos):
			#We are over drop down panel with the mouse
			for child in panel.children:
				if type(child) is DefaultLabel and child.rect.collidepoint(pos):
					child.change_color(child.default_dict['label_highlight_color'])
				elif type(child) is DefaultLabel:
					child.change_color(child.default_dict['label_color'])


	def panels_inactivate(self):
		for panel in self.panels_on_screen:
			panel.active = False

	def panels_activate(self):
		for panel in self.panels_on_screen:
			if panel.visible:
				panel.active = True


	def create_scroll_panel(self, name, x, y, width, height, full_list, num_visible, dict=None, visible=True, active=True, scrollable=False):
		self.panel_dict[name] = (PanelScroll(self, name, x, y, width, height, full_list, num_visible, visible=True, active=True))

	def create_panel(self, name, x, y, width, height, dict=None, visible=True, active=True, scrollable=False):
		if dict == None:
			dict = self.default_dict
		self.panel_dict[name] = DefaultPanel(self, name, x, y, width, height, dict, visible, active)

		self.panels.append(self.panel_dict[name])
		if visible:
			self.panels_on_screen.append(self.panel_dict[name])

	def create_button(self, name, text, x, y, functions):
		panel = self.panel_dict[name]
		if self.is_error() == False:
			panel.create_button(text, x, y, functions)

	def create_button_ok(self, panel, x, y):
		if self.is_error() == False:
			panel.create_button_ok('OK', x, y)

	def create_scrollbar(self, panel_name, max_height, num_entries, visible_entries, orientation='vertical'):
		if not orientation in ['vertical', 'horizontal']:
			self.error['scrollbar_orientation'] = 'Scrollbar in panel {}'.format(panel_name)
		panel = self.panel_dict[panel_name]
		if self.is_error() == False:
			panel.create_scrollbar(max_height, num_entries, visible_entries, orientation)

	def create_dropdown(self, panel_name, text, x, y, num_entries_visible, entries_list, function):
		panel = self.panel_dict[panel_name]
		if self.is_error() == False:
			panel.create_dropdown(text, x, y, num_entries_visible, entries_list, function)

	def create_label(self, panel_name, text, x, y, justify='left', fontsize=None, label_name=False):
		panel = self.panel_dict[panel_name]
		if self.is_error() == False:
			panel.create_label(text, x, y, justify, fontsize, label_name)

	def change_label_text(self, panel_name, label_name, text):
		panel = self.panel_dict[panel_name]
		label = panel.named_children_dict[label_name]
		label.change_text(text)

	def get_panel_by_name(self, name):
		for panel in self.panels:
			if name == panel.name:
				return(panel)

		self.error['invalid_panel_name'] = '{} not found in GuiManger.panels'.format(name)
		print(self.error)

	def create_message_box(self, name, title, text, gui_defaults):
		MessageBox(name, title, text, self)