import pygame
import base_gui


class DefaultLabel(base_gui.BaseGui):
    def __init__(self, text, parent, x, y, justify='left', default_dict=base_gui.load_defaults(), fontsize=None,
                 label_name=None):
        base_gui.BaseGui.__init__(self)
        self.default_dict = default_dict
        self.parent = parent
        self.text = text
        if isinstance(self.text, int):
            # here we can test to see if we want colored numbers (red , green) or brackets around -ve
            str(self.text)

        self.name = label_name

        self.x = x + self.parent.x
        self.y = y + self.parent.y
        self.default_dict = default_dict
        self.justify = justify  # left or right, on centre y
        self.text_color = self.default_dict['label_color']
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
                # A dropdown list is the parent, rather than a panel
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
            # here we can test to see if we want colored numbers (red , green) or brackets around -ve
            self.text = str(self.text)
        self.text_surface = self.font.render(self.text,
                                             True,
                                             self.text_color)
        self.rect = self.text_surface.get_rect()

        if self.justify == 'left':
            self.rect.topleft = self.x, self.y
        elif self.justify == 'right':
            self.rect.topright = self.x, self.y
        else:
            self.rect.topleft = self.parent.x + (self.parent.width - self.rect.width) / 2, self.y
        # Check to see if label is within panel
        if not self.parent.rect.contains(self.rect):
            if self.parent.rect.left > self.rect.left or self.parent.rect.right > self.rect.right:
                self.error['out_of_panel_horizontal'] = self
            elif self.parent.rect.top > self.rect.top or self.parent.rect.bottom > self.rect.bottom:
                self.error['out_of_panel_vertical'] = self

        self.parent.changed = True

    def change_color(self, color):
        if self.valid_color(color):
            self.text_color = color
            self.change_text(self.text)  # recaulate the text surface
        self.parent.changed = True

    def display(self):
        if self.is_error():
            self.on_error()
            return
        self.parent.screen.blit(self.text_surface, self.rect)

    def __str__(self):
        if self.justify == 'right':
            return ('Label "{}" from Panel "{}" right justified x is rhs'.format(self.text, self.parent.name))
        else:
            return ('Label "{}" from Panel "{}"'.format(self.text, self.parent.name))


class DropDownLabel(DefaultLabel):
    # This is the drop down title label
    def __init__(self, text, parent, x, y, justify='left', default_dict=base_gui.load_defaults(), fontsize=None,
                 label_name=None):
        DefaultLabel.__init__(self, text, parent, x, y, justify='left', default_dict=base_gui.load_defaults(), fontsize=None,
                 label_name=None)

        self.background_rect = self.rect.inflate(24,2)
        self.background_rect.x += 10
        self.image = pygame.image.load('images/dropdown.png')
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.children = []
        self.children.append(DropDownColorBlock(self.parent,
                                           self.default_dict['dropdown_label_back_color'],
                                       self.background_rect))


    def display(self):
        if self.is_error():
            self.on_error()
            return
        for child in self.children:
            child.display()
        self.parent.screen.blit(self.text_surface, self.rect)
        self.parent.screen.blit(self.image, (self.background_rect.right - 20, self.background_rect.top + 2))


#######################
#
# Imports

from color_block import DropDownColorBlock
