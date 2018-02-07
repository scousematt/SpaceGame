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


class DefaultLabel(BaseGui):
	def __init__(self, text, panel, x, y, justify='left', default_dict=load_defaults(), fontsize=None, name=None):
		BaseGui.__init__(self)
		
		self.default_dict = default_dict
		self.panel = panel
		self.text = text
		if type(self.text) == int:
			#here we can test to see if we want colored numbers (red , green) or brackets around -ve
			str(self.text)

		self.name = name

		self.x = x + self.panel.x
		self.y = y + self.panel.y
		self.default_dict = default_dict
		self.justify = justify    #left or right, on centre y
		self.text_color = self.default_dict['label_color']
		self.fontname = self.default_dict['label_font']
		if fontsize == None:
			self.fontsize = self.default_dict['label_fontsize']
		else:
			self.fontsize = fontsize
		try:
			self.font = pygame.font.Font(self.fontname, self.fontsize)
		except:
			self.error['font'] = True
		self.change_text(self.text)
		

			
				
	def change_text(self, new_text):
		self.text = new_text
		if type(self.text) == int:
			#here we can test to see if we want colored numbers (red , green) or brackets around -ve
			self.text  = str(self.text)
		self.text_surface = self.font.render(	self.text,
												True, 
												self.text_color)
		self.text_rect = self.text_surface.get_rect()

		if self.justify == 'left':
			self.text_rect.topleft = self.x, self.y 
		elif self.justify == 'right':
			self.text_rect.topright = self.x, self.y
		else:
			print(self.panel.x)

			self.text_rect.topleft = self.panel.x + (self.panel.width - self.text_rect.width) / 2, self.y
		#Check to see if label is within panel
		if not self.panel.rect.contains(self.text_rect):
			self.error['out_of_panel'] = self
		self.display()		

		
	def change_color(self, color):
		if self.valid_color(color):
			self.text_color = color
	
	def display(self):
		if self.is_error():
			self.on_error()
			return
		self.panel.screen.blit(self.text_surface, self.text_rect)

class DefaultColorBlock(BaseGui):

	def __init__(self, parent, color, rect):
		# This is for things internal to panels where a block of color is needed, things like message box title background
		# it is essentially a colored pygame.rect
		self.parent = parent
		self.color = color
		self.rect = rect
		self.parent.children.insert(0, self)

	def display(self):
		pygame.draw.rect(self.parent.screen,
						 self.color,
						 self.rect)


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
				
		self.top_rect = pygame.Rect(self.x, self.y, self.width, self.height)

		self.offset = default_dict['button_highlight_offset']
		
		# This is the rect that contains the whole button
		self.rect = self.top_rect.inflate(self.offset * 2, self.offset * 2)
		
	
		self.create_highlight_coords()	
		self.change_text(text)

		self.display()
		self.function_list = function_list
		if self.function_list == []:
			self.function_list = [self.close_panel]
		self.function_index = 0
		print(self.function_list)
		self.on_click_method = self.function_list[self.function_index]
	
		
	def on_click(self):
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
		print('Got to close panel')
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
		
		self.highlight_coords = [(self.top_rect.x - self.offset, self.top_rect.y - self.offset),
							(self.top_rect.x + self.top_rect.w + self.offset, self.top_rect.y - self.offset),
							(self.top_rect.x + self.top_rect.w, self.top_rect.y),
							(self.top_rect.x, self.top_rect.y),
							(self.top_rect.x, self.top_rect.y + self.top_rect.h),
							(self.top_rect.x - self.offset, self.top_rect.y + self.top_rect.h + self.offset)]
	
	def display(self):
		if self.is_error():
			self.on_error()
			return()
		pygame.draw.rect(	self.panel.screen,
							self.button_shadow_color,
							self.rect)
		
		pygame.draw.polygon(	self.panel.screen,
								self.button_highlight_color,
								self.highlight_coords)
									
		pygame.draw.rect(	self.panel.screen,
							self.button_color,
							self.top_rect)
		
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
		self.top_rect = pygame.Rect(self.x, self.y, self.width, self.height)

		self.offset = default_dict['button_highlight_offset']

		# This is the rect that contains the whole button
		self.rect = self.top_rect.inflate(self.offset * 2, self.offset * 2)

		self.create_highlight_coords()
		self.change_text(text)


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
		
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.changed = False
		self.children = []
		self.background = DefaultColorBlock(self, self.background_color, self.rect)
		self.named_children_dict = {}

	def display(self):
		if self.is_error():
			self.on_error()
			return

		#self.background = DefaultColorBlock(self, self.background_color, self.rect)
		# self.background = pygame.draw.rect(	self.screen,
		# 					self.background_color,
		# 					self.rect)
		self.border = pygame.draw.rect(	self.screen, 
							self.border_color,
							self.rect,
							self.default_dict['panel_border'])
		for child in self.children:
			child.display()
		

	def change_background_color(self, color):
		if self.valid_color(color):
			# self.background is a DefaultColorBlock object
			self.background.color = color


	def create_button(self, text, x, y, some_func):
		self.children.append(DefaultButton(text, self, x, y, some_func, self.default_dict))

	def create_button_ok(self, text, x, y):
		self.children.append(ButtonOK(text, self, x, y, [], self.default_dict))


	def create_label(self, text, x, y, justify='left', fontsize=None, label_name=False):
		self.children.append(DefaultLabel(text, self, x, y, justify, self.default_dict, fontsize, label_name))
		if label_name:
			self.named_children_dict[label_name] = self.children[-1]
			print(self.named_children_dict)

	def create_background_color(self, color, rect):
		self.children.append(pygame.draw.rect(self.screen, color, rect))

	def __str__(self):
		return('Panel object at {}, {} with width {} and height {}'.format(self.x, self.y,
																		self.width, self.height))

class GuiManager(BaseGui):

	def __init__(self, screen, default_dict):
		BaseGui.__init__(self)
		self.screen = screen
		self.default_dict = default_dict

		self.error = {}


		self.panels = []
		self.panel_dict = {}
		self.buttons = [DefaultButton, ButtonOK]


	def show_panel(self, panel_name):
		for panel in self.panels:
			if panel.name == panel_name:
				panel.visible = True

	def hide_panel(self, panel_name):
		for panel in self.panels:
			if panel.name == panel_name:
				panel.visible = False

	def display(self):
		for panel_name, panel in self.panel_dict.items():
			if panel.visible == True:
				panel.display()

	def on_lmb_click(self, pos):
		for panel_name, panel in self.panel_dict.items():
			if panel.active and panel.rect.collidepoint(pos):
				for element in panel.children:
					if (type(element) in self.buttons)and element.rect.collidepoint(pos):
						element.on_click()


	def panels_inactivate(self):
		for panel in self.panels:
			panel.active = False

	def panels_activate(self):
		for panel in self.panels:
			if panel.visible:
				panel.active = True

	def create_panel(self, name, x, y, width, height, dict=None, visible=True, active=True):
		if dict == None:
			dict = self.default_dict
		self.panel_dict[name] = DefaultPanel(self, name, x, y, width, height, dict, visible, active)
		self.panels.append(self.panel_dict[name])

	def create_button(self, name, text, x, y, functions):
		panel = self.panel_dict[name]
		if self.is_error() == False:
			panel.create_button(text, x, y, functions)

	def create_button_ok(self, panel, x, y):
		if self.is_error() == False:
			panel.create_button_ok('OK', x, y)



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