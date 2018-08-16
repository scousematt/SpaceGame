import pygame
import base_gui

IMAGE_PATH = 'images/'


class Image(base_gui.BaseGui):
    def __init__(self, image, parent, rect):
        base_gui.BaseGui.__init__(self)
        self.image_name = image
        try:
            self.image = pygame.image.load(f'{IMAGE_PATH}{self.image_name}')
        except:
            self.error['image_not_found'] = f'Image {image} not found in {IMAGE_PATH}'
            return

        self.parent = parent
        self.screen = self.parent.screen
        self.rect = pygame.Rect(rect.x + self.parent.x, rect.y + self.parent.y, rect.width, rect.height)
        #If the image is to be scaled
        if (rect.width, rect.height) != self.image.get_size():
            self.image = pygame.transform.scale(self.image, (self.rect.w, self.rect.h))


    def display(self):
        if self.is_error():
            self.on_error()
            return ()
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

    def __str__(self):
        return f'{type(self)} {self.image_name}'


class TextSurface(base_gui.BaseGui):
    def __init__(self, screen, text, font, color, coords, justify='left'):
        base_gui.BaseGui.__init__(self)
        self.screen = screen
        self.text = text
        self.font = font
        self.color = color
        self.coords = coords # size of the final location of the text
        self.justify = justify
        self.text_surface = None
        self.rect = None
        self.update(self.font, self.text, self.color, self.justify)


    def update(self, font, text, color, justify):
        self.text_surface = font.render(text, True, color)
        self.rect = self.text_surface.get_rect()
        if justify == 'left':
            self.rect.topleft = self.coords
        elif justify == 'right':
            self.rect.topright = self.coords
        else:
            print(f'Justify :{self.justify}')
            self.rect.center = self.coords


    def display(self):
        self.screen.blit(self.text_surface, self.rect)

class OutputLine(base_gui.BaseGui):
    '''
    #  Not sure about the name yet but this is a group of other elements joined together to aid in scrollbars.
    #  The treeview and potentially the message box are going to be made up of lines. Each of which can contain things
    #  like labels of different fonts and sizes, images, etc.
    Do we want to give each line an x and y and then have each internal element have an offset from this. Would certainly
    make moving the lines contents up and down (and long term, left and right) simpler.

    The problem is that individual comonments are set relative to the screen. We need to store the line minus

    '''
    def __init__(self):
        base_gui.BaseGui.__init__(self)

        #  The coordinates start at 0,0 as there is no offset. When things are moved around inside a panel, the
        #  coordinates will get a value which can then be passed into their children.set_coords.
        #  Sending an offset allows the value of element to be changed while still retaining
        #  total offset.
        #
        #  A few problems - what if an OutputLine.child.element gets changed. What happens when a label has its
        #  text changed.  Potentially we are talking putting everything in a line. Change the

        self.x_offset = 0
        self.y_offset = 0
        #  Current offset.
        self.change_x = 0
        self.change_y = 0
        self.children = []

    def change_offset(self, x, y):
        self.change_x = x
        self.change_y = y
        self.x_offset += x
        self.y_offset += y

    def display(self):
        if self.is_error():
            self.on_error()
            return

        for child in self.children:
            child.offset_xy(self.change_x, self.change_y)
            child.display()




