import pygame
import base_gui

IMAGE_PATH = 'images/'


class Image(base_gui.BaseGui):
    def __init__(self, image, screen, rect):
        base_gui.BaseGui.__init__(self)
        self.image_name = image
        try:
            self.image = pygame.image.load(f'{IMAGE_PATH}{self.image_name}')
        except:
            self.error['image_not_found'] = f'Image {image} not found in {IMAGE_PATH}'
            return

        self.screen = screen
        self.rect = rect
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





