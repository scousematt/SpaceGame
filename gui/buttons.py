import pygame
import base_gui, color_blocks, labels, fundamentals


class DefaultButton(base_gui.BaseGui):
    def __init__(self, panel, x, y, function_list, default_dict=base_gui.load_defaults()):
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

    def display(self):
        if self.is_error():
            self.on_error()
            return ()
        for child in self.children:
            child.display()

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

    def __str__(self):
        return f'{type(self)} at {self.x}, {self.y}'



class Button(DefaultButton):
    def __init__(self, panel, x, y, function_list, text, default_dict=base_gui.load_defaults()):
        DefaultButton.__init__(self, panel, x, y, function_list, default_dict=base_gui.load_defaults())


        self.text = text


        button_dict = {'label_color': (200,200,200), #self.default_dict['button_text_color'],
                       'label_font': self.default_dict['button_font'],
                       'label_fontsize': self.default_dict['button_fontsize']}
        self.children.append(labels.DefaultLabel(self.text, self, self.rect.x, self.rect.y,
                                                 justify='center', default_dict=button_dict))





    def update(self):
        self.text_rect.center = ((self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2))
        self.create_highlight_coords()
        self.shadow_rect = self.rect.inflate(self.offset * 2, self.offset * 2)



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
        DefaultButton.__init__(self, panel, x, y, function_list)

        # Buttons with icons should be square
        x_ = self.x + 0.5 * (self.default_dict['button_width'] - self.default_dict['button_height'])
        #This rect is for the image size not mouse click detection
        self.image_rect = pygame.Rect(x_, self.y, self.default_dict['button_height'], self.default_dict['button_height'])
        # Resize image to fit in button

        self.children.append(fundamentals.Image('dropdown.png', self.parent.screen, self.image_rect))
