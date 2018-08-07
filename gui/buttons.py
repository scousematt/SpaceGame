import pygame
import base_gui, color_block, labels

class DefaultButton(base_gui.BaseGui):
    def __init__(self, text, panel, x, y, function_list, default_dict=base_gui.load_defaults()):
        base_gui.BaseGui.__init__(self)


        self.text = text
        self.parent = panel

        # self.error = error
        self.x = x + panel.x
        self.y = y + panel.y
        self.children = []
        self.default_dict = default_dict

        self.button_color = default_dict['button_color']
        self.button_shadow_color = default_dict['button_shadow_color']
        self.button_highlight_color = default_dict['button_highlight_color']
        self.text_color = default_dict['button_text_color']

        # Fonts
        self.fontname = default_dict['button_font']
        self.fontsize = default_dict['button_fontsize']
        try:
            self.font = pygame.font.Font(self.fontname, self.fontsize)
        except:
            self.error['font'] = True

        self.width = default_dict['button_width']
        self.height = default_dict['button_height']

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.children.append(color_block.Triangles2ColorBlock(self.parent,
                                                              self.default_dict['button_highlight_color'],
                                                              self.rect.inflate(self.default_dict['button_highlight_offset'] * 2,
                                                                                self.default_dict['button_highlight_offset'] * 2),
                                                              self.default_dict['button_shadow_color']))
        self.children.append(color_block.DefaultColorBlock(self.parent,
                                                           self.default_dict['button_color'],
                                                           self.rect))

        button_dict = {'label_color': (200,200,200), #self.default_dict['button_text_color'],
                       'label_font': self.default_dict['button_font'],
                       'label_fontsize': self.default_dict['button_fontsize']}
        self.children.append(labels.DefaultLabel(self.text, self, self.rect.x, self.rect.y,
                                                 justify='center', default_dict=button_dict))


        self.parent.changed = True
        self.function_list = function_list
        if self.function_list == []:
            self.function_list = [self.close_panel]
        self.function_index = 0
        print(self.function_list)
        self.on_click_method = self.function_list[self.function_index]


    def update(self):
        self.text_rect.center = ((self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2))
        self.create_highlight_coords()
        self.shadow_rect = self.rect.inflate(self.offset * 2, self.offset * 2)

    def on_click(self):
        #
        # Note. A button can change things in other panels. self.panel.changed ??
        #
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



    def display(self):
        if self.is_error():
            self.on_error()
            return()
        for child in self.children:
            child.display()
        print(self.children[-1])

        #self.panel.screen.blit(self.text_surface, self.text_rect)


    def __str__(self):
        return('Button object at {}, {} with text "{}"'.format(self.x - self.parent.x,
                                                               self.y - self.parent.y,
                                                               self.text))


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
