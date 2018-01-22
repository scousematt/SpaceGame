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


class Errors:
	def __init__(self):
		self.error = {}
		
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


class DefaultLabel(Errors):
	def __init__(self, text, panel, x, y, justify='left', default_dict=load_defaults()):
		Errors.__init__(self)
		
		self.default_dict = default_dict
		self.panel = panel
		self.text = text
		
		self.x = x + self.panel.x
		self.y = y + self.panel.y
		self.default_dict = default_dict
		self.justify = justify    #left or right, on centre y
		self.text_color = self.default_dict['label_color']
		self.fontname = self.default_dict['label_font']
		self.fontsize = self.default_dict['label_fontsize']
		try:
			self.font = pygame.font.Font(self.fontname, self.fontsize)
		except:
			self.error['font'] = True
		print(self.error)
		self.change_text(self.text)
		

			
				
	def change_text(self, new_text):
		self.text = new_text
		self.text_surface = self.font.render(	new_text, 
												True, 
												self.text_color)
		self.text_rect = self.text_surface.get_rect()

		if self.justify == 'left':
			self.text_rect.topleft = self.x, self.y 
		else:
			self.text_rect.topright = self.x, self.y
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
	

class DefaultButton(Errors):
	def __init__(self, text, panel, x, y, function_list, default_dict=load_defaults()):
		Errors.__init__(self)
		
		
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
		self.function_index = 0
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
	
class DefaultPanel(Errors):
	def __init__(self, x, y, width, height, screen, default_dict=load_defaults()):
		Errors.__init__(self)
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.screen = screen
		self.error = {}
		
		self.default_dict = default_dict
		self.background_color = self.default_dict['panel_background_color']
		self.border_color = self.default_dict['panel_border_color']
		
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.display()
		self.changed = False

							
		self.children = []

	def display(self):
		if self.is_error():
			self.on_error()
			return
		self.background = pygame.draw.rect(	self.screen,
							self.background_color,
							self.rect)
		self.border = pygame.draw.rect(	self.screen, 
							self.border_color,
							self.rect,
							4)
		

	def change_background_color(self, color):
		if self.valid_color(color):
			self.background_color = color
		self.display()
		#Note, display overwrites all the children
		for child in self.children:
			child.display()

	def create_button(self, text, x, y, some_func):
		self.children.append(DefaultButton(text, self, x, y, some_func, self.default_dict))

	def create_label(self, text, x, y, justify='left'):
		self.children.append(DefaultLabel(text, self, x, y, justify, self.default_dict))

	def __str__(self):
		return('Panel object at {}, {} with width {} and height {}'.format(self.x, self.y,
																		self.width, self.height))
