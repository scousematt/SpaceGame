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
		self.rect = self.rect
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
	def __init__(self, parent, text, x, y, entries_list):
		self.parent = parent
		self.text = text
		self.x = x
		self.y = y
		self.entries_list = entries_list
		self.justify = 'left'
		self.default_dict = load_defaults()
		self.fontsize = self.default_dict['label_fontsize']
		self.children = []
		self.children.append(DefaultLabel(self.text, self.parent, x, y, self.justify, default_dict=self.default_dict, fontsize=self.fontsize, label_name='drop_list'))
		self.display_switch = False


	def display(self):
		for element in self.children:
			element.display()
			print(self.display_switch)
			if self.display_switch == True:
				self.display_list()

	def display_list(self):
		print('Clicked on drop list')
		height = 30 * 3 + 15
		x = self.x + self.parent.x - 10
		y = self.y + self.parent.y + 30
		self.parent.gui.create_panel('Drop Down', self.x + self.parent.x - 10, y + self.parent.y, 190, height)
		y = 10
		for entry in self.entries_list:
			self.parent.gui.create_label('Drop Down',entry, 10, y)
			print(entry)
			y += 25
		self.parent.gui.dropdown_active = None

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
	def __init__(self, panel, max_v, default_dict=load_defaults()):
		BaseGui.__init__(self)
		self.panel = panel
		self.max_v = max_v    # The total height of the rect_data that scrollbar is controlling the views of
		self.default_dict = default_dict
		self.height = panel.height - 2 * self.default_dict['scrollbar_top_margin']
		self.width = self.default_dict['scrollbar_width']
		self.x = self.panel.rect.right - self.width - self.default_dict['scrollbar_margin_right']
		self.y = self.panel.rect.top + self.default_dict['scrollbar_top_margin']
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.button_rect = pygame.Rect(self.x, self.y, self.width, self.default_dict['scrollbar_button_height'])
		self.line_width = self.default_dict['scrollbar_button_highlight_width']
		self.children=[]

		self.children.append(DefaultColorBlock(self.panel, self.default_dict['scrollbar_color'], self.rect))
		self.children.append(ScrollbarColorBlock(self.panel,  self.default_dict['scrollbar_button_color'],
		 											self.button_rect, self, drag_with_mouse=True))
		#Created
		self.panel.changed = True

	def display(self):
		for child in self.children:
			child.display()

	def update_pos(self, x, y):
		self.children[1].rect.y += y
		if self.children[1].rect.y < self.rect.y:
			self.children[1].rect.y = self.rect.y
		elif self.children[1].rect.bottom > self.rect.bottom:
			self.children[1].rect.bottom = self.rect.bottom
		self.panel.changed = True

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

	def create_scrollbar(self, orientation):
		if orientation == 'vertical':
			#Change to a horizontal and vertical
			# TODO Add max_v
			self.children.append(Scrollbar(self, 100))

	def create_dropdown(self, text, x, y, entries_list):
		self.children.append(DropList(self, text, x, y, entries_list))

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
	def __init__(self, gui, name, x, y, width, height, default_dict=load_defaults(), visible=True, active=True):
		DefaultPanel.__init__(self, gui, name, x, y, width, height, default_dict=load_defaults(), visible=True,
							  active=True)
		#
		#
		# There will be 3 rects, the normal rect which is the position on the screen,
		# a view_rect which is the same size as the rect, and a data rect which is calculated when the
		# whole panel is built. Also data rect will be changed via update. So we need a boolean to check
		self.updated = False
		# We need a way of building the complete data panel and then running the update. So something in gui.panel needs
		# a list of functions [create_label, etd] to which we can append self.update on the end.
		self.rect_view = self.rect
		self.rect_data = pygame.Rect()
		# The rect_view will be moved to the correct part of rect_data and then moved to rect and copied over
		# Add scrollbar need height of data_rect
		self.scrollbar = False

	# Note, the width available is now reduced by the size of the scrollbar

	def update(self):
		if self.updated:
			# The data panel has changed? But this happens off screen so it's already changed in the data.
			# I suppose we use this opportunity to change the scrollbar, if stuff has been added after rect_view the scrollbar block
			# Needs making smaller and moving, converse for items deleted.
			for element in self.element_list:
				# create_label(self, text, x, y, justify='left', fontsize=None, label_name=False)
				# [ [func_name, and then what?? some form of label_dict????
				element()
		self.updated = True


	def create_label(self, text, x, y, justify='left', fontsize=None, label_name=False):
		self.children.append(DefaultLabel(text, self, x, y, justify, self.default_dict, fontsize, label_name))
		if self.children[-1].error['out_of_panel_vertical']:
			# We are in need of a scrollbar and the panel displayed is only an part of the full panel
			# TODO Anything above the panel top is still wrong - change label
			self.rect.bottom = self.children[-1].bottom + self.default_dict['panel_border']
			if not self.scrollbar:
				self.gui.create_scrollbar(self.name, self.rect.height)
		elif self.children[-1].error['out_of_panel_horizontal']:
			pass
		if label_name:
			self.named_children_dict[label_name] = self.children[-1]
		self.updated = False

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

	def hide_panel(self, panel_name):
		# Think this is replaced with the panel_dict
		for panel in self.panels:
			if panel.name == panel_name:
				panel.visible = False

	def display(self):
		for panel_name, panel in self.panel_dict.items():
			# TODO check to see if panel is changed
			if panel.visible == True and panel.changed:
				panel.display()
				panel.changed = False

	def on_lmb_click(self, pos):
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
							self.mouse_y = pos[1]
							# we want the scrollbar to update itself, not a scrollbar element
							self.element_moving = element.parent
						elif type(element) == DropList and element.children[0].rect.collidepoint(pos):
							self.lmb_pressed = True
							print('Pressed')
							element.display_switch = True
							self.dropdown_active = element
						elif type(element) == DefaultLabel and element.parent.name == 'Drop Down' and element.rect.collidepoint(pos):
							print(element.text)
		if self.dropdown_active:
			self.dropdown_active.display_list()


	def on_lmb_up(self, pos):
		self.lmb_pressed = False
		if self.element_moving:

			x_diff = pos[0] - self.mouse_x
			y_diff = pos[1] - self.mouse_y
			print('change of {}, {}'.format(x_diff, y_diff))
			self.element_moving.update_pos(x_diff, y_diff)
			self. element_moving = False

	def panels_inactivate(self):
		for panel in self.panels_on_screen:
			panel.active = False

	def panels_activate(self):
		for panel in self.panels_on_screen:
			if panel.visible:
				panel.active = True

	def create_panel(self, name, x, y, width, height, dict=None, visible=True, active=True, scrollable=False):
		if dict == None:
			dict = self.default_dict
			if scrollable:
				self.panel_dict[name] = PanelScroll(self, name, x, y, width, height, dict, visible, active)
			else:
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

	def create_scrollbar(self, panel_name, orientation='vertical'):
		if not orientation in ['vertical', 'horizontal']:
			self.error['scrollbar_orientation'] = 'Scrollbar in panel {}'.format(panel)
		panel = self.panel_dict[panel_name]
		if self.is_error() == False:
			panel.create_scrollbar(orientation)

	def create_dropdown(self, panel_name, text, x, y, entries_list):
		panel = self.panel_dict[panel_name]
		if self.is_error() == False:
			panel.create_dropdown(text, x, y, entries_list)

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