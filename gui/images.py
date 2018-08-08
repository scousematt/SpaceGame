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