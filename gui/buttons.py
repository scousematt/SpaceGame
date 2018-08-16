import pygame
import base_gui, color_blocks, labels, fundamentals


class DefaultButton(base_gui.BaseGui):
    def __init__(self, panel, x, y, function_list, default_dict):
        #
        #  When writing documentation, note that the function list is a list of names, if the () is
        #  included, the function will execute.
        #
        base_gui.BaseGui.__init__(self)
        self.parent = panel
        self.x = x + panel.x
        self.y = y + panel.y
        self.children = []

        self.default_dict = default_dict


        self.rect = pygame.Rect(self.x, self.y, self.default_dict['button_width'], self.default_dict['button_height'])
        self.children.append(color_blocks.Triangles2ColorBlock(self.parent,
                                                              self.default_dict['button_highlight_color'],
                                                              self.rect.inflate(self.default_dict['button_highlight_offset'] * 2,
                                                                                self.default_dict['button_highlight_offset'] * 2),
                                                              self.default_dict['button_shadow_color']))
        self.children.append(color_blocks.DefaultColorBlock(self.parent,
                                                           self.default_dict['button_color'],
                                                           self.rect))

        self.parent.changed = True
        self.function_list = function_list
        if self.function_list == []:
            self.function_list = [self.close_panel]
        self.function_index = 0
        print(self.function_list)
        self.on_click_method = self.function_list[self.function_index]

        #  Return for __str__.
        self.str = f'Button {type(self)} in panel {self.parent.name}'

    def on_click(self):
        try:
            return_method =  self.on_click_method(self)
        except TypeError:
            return_method = self.on_click_method()
        self.function_index += 1
        if self.function_index == len(self.function_list):
            self.function_index = 0
        self.on_click_method = self.function_list[self.function_index]
        return return_method


class Button(DefaultButton):
    def __init__(self, panel, x, y, function_list, text, default_dict=base_gui.load_defaults()):
        DefaultButton.__init__(self, panel, x, y, function_list, default_dict=base_gui.load_defaults())


        self.text = text


        button_dict = {'label_color': (200,200,200), #self.default_dict['button_text_color'],
                       'label_font': self.default_dict['button_font'],
                       'label_fontsize': self.default_dict['button_fontsize']}
        self.children.append(labels.DefaultLabel(self.text, self, self.rect.x, self.rect.y,
                                                 justify='center', default_dict=button_dict))





    # def update(self):
    #     self.text_rect.center = ((self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2))
    #     self.create_highlight_coords()
    #     self.shadow_rect = self.rect.inflate(self.offset * 2, self.offset * 2)



class ButtonOK(DefaultButton):

    def __init__(self, text, panel, x, y, function_list=[], default_dict=base_gui.load_defaults()):
        DefaultButton.__init__(self, text, panel, x, y, function_list=[])
        self.width = panel.width - (2 * self.default_dict['msg_text_x'])
        self.text = 'OK'
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.offset = default_dict['button_highlight_offset']

        # This is the rect that contains the whole button
        self.shadow_rect = self.rect.inflate(self.offset * 2, self.offset * 2)

        self.create_highlight_coords()
        self.change_text(text)


class ButtonImage(DefaultButton):
    def __init__(self, panel, x, y, function_list, image, default_dict=base_gui.load_defaults()):
        DefaultButton.__init__(self, panel, x, y, function_list, default_dict)
        # TODO All images are assumed to be square

        #  If the image is in a button, the button already corrects for the panel x, y. The correction in
        #  image is therefore redundant.

        self.x -= panel.x
        self.y -= panel.y


        #  Center the image in the button.
        x_ = self.x + 0.5 * (self.default_dict['button_width'] - self.default_dict['button_height'])


        #  This rect is for the image size not mouse click detection.
        self.image_rect = pygame.Rect(x_, self.y, self.default_dict['button_height'], self.default_dict['button_height'])
        # Resize image to fit in button
        self.image = image

        self.setup()
        print(f'Button rect {self.rect}, image rect {self.children[-1].rect}')

    def get_image_index(self):
        idx = [i for i, val in enumerate(self.children) if type(val) == fundamentals.Image]
        print(f'iundex is {idx}')
        return idx[0]

    def setup(self):
        self.children.append(fundamentals.Image(self.image, self.parent, self.image_rect))

class ButtonToggleImage(ButtonImage):
    def __init__(self, panel, x, y, function_list, image, default_dict=base_gui.load_defaults()):
        ButtonImage.__init__(self, panel, x, y, function_list, image)
        #self.update()

    def setup(self):
        self.cur_image = 0
        self.images = []
        for image in self.image:
            self.images.append(fundamentals.Image(image, self.parent, self.image_rect))
        self.children.append(self.images[0])

    def display(self):
        # remove the image
        del self.children[self.get_image_index()]
        # replace the image
        self.children.append(self.images[self.cur_image])
        super().display()


    def on_click(self):
        try:
            return_method =  self.on_click_method(self)
        except TypeError:
            return_method = self.on_click_method()
        self.cur_image += 1
        if self.cur_image == len(self.images):
            self.cur_image = 0

        self.function_index += 1
        if self.function_index == len(self.function_list):
            self.function_index = 0

        self.on_click_method = self.function_list[self.function_index]
        print(f'The cur_image is now {self.cur_image}, image is {self.images[self.cur_image]}')
        self.display()
        return return_method