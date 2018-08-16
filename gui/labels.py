import pygame
import base_gui, buttons, fundamentals, tree_view

OBJECTS_WITH_TEXT_NOT_PANEL = (buttons.DefaultButton, base_gui.DropDown, tree_view.TreeView)

class DefaultLabel(base_gui.BaseGui):
	def __init__(self, text, parent, x, y, justify='left', default_dict=base_gui.load_defaults(), fontsize=None,
				 label_name=None):
		base_gui.BaseGui.__init__(self)
		self.default_dict = default_dict
		self.parent = parent
		self.text = '' # We establish self.text in the method self.change_text(text)


		if isinstance(text, (int, float)):
			# here we can test to see if we want colored numbers (red , green) or brackets around -ve
			text = f'{text}'

		self.name = label_name

		#  Set the label to screen coordinates.
		self.x = x + self.parent.x
		self.y = y + self.parent.y
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

	def get_text_surface(self):
		# The update will check that there is only one text surface
		list_text_surface_indexes = [i for i, val in enumerate(self.children) if type(val) == fundamentals.TextSurface]
		# TODO Combine all the surface rects here to allow for other fonts and sizes?
		return self.children[list_text_surface_indexes[0]]

	def update(self):
		child = [i for i, val in enumerate(self.children) if type(val) == fundamentals.TextSurface]
		if len(child) > 1:
			self.error['label_multiple_texts'] = f'Label {self.text} has multiple TextSurface objects'
		elif len(child) == 1:
			self.children.pop(child[0])
		self.children.append(fundamentals.TextSurface(self.screen, self.text, self.font, self.text_color, self.coords, self.justify))

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

		# self.text_surface = self.font.render(self.text,
		# 									 True,
		# 									 self.text_color)
		# self.rect = self.text_surface.get_rect()

		if self.justify == 'left':
			self.coords = (self.x, self.y)
		elif self.justify == 'right':
			self.coords = self.x, self.y
		else:
			print(f'Justify :{self.justify} from labels.DefaultLabel.change_text()')
			self.coords = self.parent.rect.center
		# Check to see if label is within panel
		# if not self.parent.rect.contains(self.rect):
		# 	if self.parent.rect.left > self.rect.left or self.parent.rect.right > self.rect.right:
		# 		self.error['out_of_panel_horizontal'] = self
		# 	elif self.parent.rect.top > self.rect.top or self.parent.rect.bottom > self.rect.bottom:
		# 		self.error['out_of_panel_vertical'] = self
		self.parent.changed = True
		# Update the TextSurface
		self.update()

	def change_color(self, color):
		# TODO Determine if the new color is valid or not and prepare an error
		self.text_color = color
		self.update()
		self.parent.changed = True


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

		self.update()


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
