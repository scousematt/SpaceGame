import pygame
import base_gui, buttons, fundamentals, tree_view

OBJECTS_WITH_TEXT_NOT_PANEL = (buttons.DefaultButton, buttons.Button, base_gui.DropDown, tree_view.TreeView)

class DefaultLabel(base_gui.BaseGui):
	def __init__(self, text, parent, x, y, justify='left', default_dict=base_gui.load_defaults(), fontsize=None,
				 label_name=None):
		base_gui.BaseGui.__init__(self)
		self.default_dict = default_dict
		self.parent = parent
		self.text = '' # We establish self.text in the method self.change_text(text)
		self.rect = None
		self.x = x
		self.y = y

		if isinstance(text, (int, float)):
			# here we can test to see if we want colored numbers (red , green) or brackets around -ve
			text = f'{text}'

		self.name = label_name

		#  Set the label to screen coordinates.
		self.set_screen_coords()

		self.default_dict = default_dict
		self.justify = justify  #  Left, right, on centre y.

		self.text_color = self.default_dict['label_color']
		# Set the screen based on the parent type


		#  Setup output for __str__.
		self.str = f'{type(self)} {self.text} from Parent {self.parent}, Justify {self.justify}'

		#  Move all of this somewhere else, it shouldn't be in the __init__, confusing.
		if isinstance(self.parent, OBJECTS_WITH_TEXT_NOT_PANEL):
			self.screen = self.parent.parent.screen
		else:
			self.screen = self.parent.screen

		self.fontname = self.default_dict['label_font']

		if fontsize == None:
			self.fontsize = self.default_dict['label_fontsize']
		else:
			self.fontsize = base_gui.return_correct_type(fontsize)

		try:
			# Check to see if a font object has already been created
			self.font = self.parent.gui.font_dict[''.join([self.fontname, str(self.fontsize)])]
		except KeyError:
			self.font = pygame.font.Font(self.fontname, self.fontsize)
			self.parent.gui.font_dict[''.join([self.fontname, str(self.fontsize)])] = self.font
		except:
			try:
				# A dropdown list is the parent, rather than a panel, same with buttons
				self.font = self.parent.parent.gui.font_dict[''.join([self.fontname, str(self.fontsize)])]
			except KeyError:
				self.font = pygame.font.Font(self.fontname, self.fontsize)
				self.parent.parent.gui.font_dict[''.join([self.fontname, str(self.fontsize)])] = self.font

			except:
				self.error['font'] = True
		if not self.is_error():
			self.change_text(text)


	def set_screen_coords(self):
		self.x = self.x + self.parent.x
		self.y = self.y + self.parent.y

	def get_text_surface(self):
		# The update will check that there is only one text surface
		list_text_surface_indexes = [i for i, val in enumerate(self.children) if type(val) == fundamentals.TextSurface]
		# TODO Combine all the surface rects here to allow for other fonts and sizes?
		return self.children[list_text_surface_indexes[0]]

	def update_text_surface(self):
		child = [i for i, val in enumerate(self.children) if type(val) == fundamentals.TextSurface]
		if len(child) > 1:
			self.error['label_multiple_texts'] = f'Label {self.text} has multiple TextSurface objects'
		elif len(child) == 1:
			self.children.pop(child[0])
		self.children.append(fundamentals.TextSurface(self.screen, self.text, self.font, self.text_color, self.coords, self.justify))
		self.set_rect()

	def update(self, y_change):
		#  The panel upon scrollbar movement will change the self.rect.y
		for child in self.children:
			child.rect.y += y_change
			child.update_text()
		self.rect = self.rect.move(0,y_change)

	def update_xy(self, x, y):
		for child in self.children:
			child.rect = child.rect.move(x,y)
		self.rect = self.rect.move(x,y)

	def display(self):
		for child in self.children:
			if child.rect.y > self.parent.rect.y:
				child.display()


	def set_rect(self):
		#  From the last element, get the rect.
		self.rect = self.children[-1].rect

	def change_text(self, new_text):
		if isinstance(new_text, (int, float)):
			# here we can test to see if we want colored numbers (red , green) or brackets around -ve

			new_text = f'{new_text}'
		elif isinstance(new_text, str) == False:
			# We have sent something other than an int or a str to be text.
			self.error['label_change_text_not_str'] = f'Label text should be str, is {type(new_text)}'
			return

		if self.text == new_text:
			# Do nothing, nothing has changed
			return

		self.text = new_text
		#  Position self.coords to suit the justification before the text_surface is created
		self.justify_text()

		self.parent.changed = True
		#  Update the TextSurface. Most pointless comment in the world.
		self.update_text_surface()

	def justify_text(self):
		if self.justify == 'left':
			self.coords = (self.x, self.y)
		elif self.justify == 'right':
			self.coords = (self.x, self.y)
		elif self.justify == 'centerx':
			self.coords = (self.parent.rect.centerx, self.y)
		else:
			self.coords = self.parent.rect.center


	def change_color(self, color):
		# TODO Determine if the new color is valid or not and prepare an error
		self.text_color = color
		self.update_text_surface()
		self.parent.changed = True

class ButtonLabel(DefaultLabel):
	def __init__(self, text, parent, x, y, justify, default_dict, fontsize=None,
				 label_name=None):
		self.button = parent

		DefaultLabel.__init__(self, text, parent, x, y, justify, default_dict, fontsize=None,
				 label_name=None)
		'''Same as the DefaultLabel except the self.parent.y does not refer to its parent (a button) but the panel in which the button
		resides.'''
		self.parent = self.parent.parent
		self.rect = self.button.rect
		print(f'The label has {len(self.children)} children')
		#self.rect = self.parent.rect

	def set_screen_coords(self):
		#  Button is the child of a panel, we need panel sizes.
		self.x = self.x + self.parent.parent.x
		self.y = self.y + self.parent.parent.y


	def justify_text(self):
		if self.justify == 'left':
			self.coords = (self.x, self.y)
		elif self.justify == 'right':
			self.coords = (self.x, self.y)
		else:

			self.coords = self.parent.rect.center



class DropDownTitleLabel(DefaultLabel):
	# This is the drop down title label
	def __init__(self, text, parent, x, y, justify='left', default_dict=base_gui.load_defaults(),fontsize=None,
				 label_name=None):
		DefaultLabel.__init__(self, text, parent, x, y, justify='left', default_dict=base_gui.load_defaults(), fontsize=None,
				 label_name=None)

		self.background_rect = self.children[0].rect.inflate(24,2)
		self.background_rect.x += 10
		self.children = []
		self.children.append(DropDownColorBlock(self.parent,
										   self.default_dict['dropdown_label_back_color'],
									   self.background_rect))
		#  The image corrects itself and so does the label, the x needs to be reduced by panel.x
		self.image_rect = pygame.Rect(self.background_rect.right - 20 - self.parent.x, self.background_rect.top + 2, 20, 20)
		self.children.append(fundamentals.Image('dropdown.png', self.parent, self.image_rect))

		self.update_text_surface()

	def set_rect(self):
		#  There are more elements in the label so this method overwrites the DefaultLabel to union all the rects in self.children
		self.rect = self.children[0].rect
		for child in self.children:
			self.rect = self.rect.union(child.rect)

class DropDownListLabel(DefaultLabel):
	def __init__(self, text, parent, x, y, justify='left', default_dict=base_gui.load_defaults(), fontsize=None,
				 label_name=None):
		DefaultLabel.__init__(self, text, parent, x, y, justify='left', default_dict=base_gui.load_defaults(), fontsize=None,
				 label_name=None)

		self.highlight = False

	def display(self):
		if self.is_error():
			self.on_error()
			return
		if self.text == self.parent.highlight:
			if self.text_color != self.default_dict['label_highlight_color']:
				self.change_color(self.default_dict['label_highlight_color'])
		elif self.text_color == self.default_dict['label_highlight_color']:
			self.change_color(self.default_dict['label_color'])
		for child in self.children:
			child.display()
		#self.parent.screen.blit(self.text_surface, self.rect)



#######################
#
# Imports

from color_blocks import DropDownColorBlock
