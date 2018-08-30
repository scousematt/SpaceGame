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
        self.x = x + self.parent.rect.x
        self.y = y + self.parent.rect.y

        self.default_dict = default_dict
        #  Populate the button sizes from the default_dict.
        self.setup_sizes()

        self.rect = pygame.Rect(self.x, self.y, self.button_width, self.button_height)
        self.children.append(color_blocks.Triangles2ColorBlock(self.parent,
                                                              self.default_dict['button_highlight_color'],
                                                              self.rect.inflate(self.button_highlight_offset * 2,
                                                                                self.button_highlight_offset * 2),
                                                              self.default_dict['button_shadow_color']))
        self.children.append(color_blocks.DefaultColorBlock(self.parent,
                                                           self.default_dict['button_color'],
                                                           self.rect))

        self.parent.changed = True
        self.function_list = function_list
        if self.function_list == []:
            self.function_list = [self.close_panel]
        self.function_index = 0
        self.on_click_method = self.function_list[self.function_index]

        #  Return for __str__.
        self.str = f'Button {type(self)} in panel {self.parent.name}'

    def close_panel(self):
        self.parent.gui.hide_panel(self.parent.name)

    def setup_sizes(self):
        self.button_width = self.default_dict['button_width']
        self.button_height = self.default_dict['button_height']
        self.button_highlight_offset = self.default_dict['button_highlight_offset']

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

    def update(self, y_change):
        for child in self.children:
            child.update(y_change)

    def update_xy(self, x, y):
        self.rect = self.rect.move(x,y)
        for child in self.children:
            child.update_xy(x,y)



    def display(self):
        for child in self.children:
            #  If scrolled out of panel, don't show it.
            #print(f'button child.rect.y {child.rect.y} parent.rect.y {self.parent.rect.y}')
            if child.rect.y > self.parent.rect.y:
                child.display()
            else:
                print(f'from else button child.rect.y {child.rect} parent.rect.y {self.parent.rect}')

class Button(DefaultButton):
    def __init__(self, panel, x, y, function_list, text, default_dict=base_gui.load_defaults()):
        DefaultButton.__init__(self, panel, x, y, function_list, default_dict=base_gui.load_defaults())


        self.text = text


        button_dict = {'label_color': (200,200,200), #self.default_dict['button_text_color'],
                       'label_font': self.default_dict['button_font'],
                       'label_fontsize': self.default_dict['button_fontsize']}
        self.children.append(labels.ButtonLabel(self.text, self, self.rect.x, self.rect.y,
                                                 justify='center', default_dict=button_dict))




class ButtonOK(Button):
    '''
    Only to be used in dialogs. Not in standard panels.
    '''
    def __init__(self, panel, x, y, default_dict=base_gui.load_defaults()):
        Button.__init__(self, panel, x, y, [], 'OK', default_dict)
        for child in self.children:
            print(child.rect, type(child))
        self.function_list = [self.parent.close_dialog]
        self.on_click_method = self.function_list[0]

    def display(self):
        for child in self.children:
            #  If scrolled out of panel, don't show it.
            #print(f'button child.rect.y {child.rect.y} parent.rect.y {self.parent.rect.y}')
            if child.rect.y > self.parent.rect.y:
                child.display()
            else:
                #  We have asked child.update_xy to run, so lets check out ubttons.ButtonLabel
                print(f'{type(child)} from else button child.rect.y {child.rect} parent.rect.y {self.parent.rect}')

class ButtonImage(DefaultButton):
    def __init__(self, panel, x, y, function_list, image, default_dict=base_gui.load_defaults()):
        DefaultButton.__init__(self, panel, x, y, function_list, default_dict)
        # TODO All images are assumed to be square

        #  Center the image in the button.
        x_ = self.x + 0.5 * (self.button_width - self.button_height)


        #  This rect is for the image size not mouse click detection.
        self.image_rect = pygame.Rect(x_ - self.parent.x, self.y - self.parent.x, self.button_height, self.button_height)
        # Resize image to fit in button
        self.image = image

        self.setup()



    def get_image_index(self):
        idx = [i for i, val in enumerate(self.children) if type(val) == fundamentals.Image]
        return idx[0]

    def setup(self):
        self.children.append(fundamentals.Image(self.image, self.parent, self.image_rect))

    def set_children_rect_y(self):
        for child in self.children:
            if self.rect.y != child.rect.y:
                child.rect.y =  self.rect.y

    def display(self):
        #  The image is relative to the button, not the panel, so adjust here.
        if self.rect.y != self.children[self.get_image_index()].rect.y:
            self.children[self.get_image_index()].rect.y = self.rect.y
            #self.children[self.get_image_index()].rect.y = self.rect.y
        super().display()

class ButtonTreeviewImage(ButtonImage):
    def __init__(self, panel, x, y, function_list, image, default_dict=base_gui.load_defaults()):
        ButtonImage.__init__(self, panel, x, y, function_list, image)

    def setup_sizes(self):
        self.button_width = self.default_dict['treeview_image_width']
        self.button_height = self.default_dict['treeview_image_width']
        self.button_highlight_offset = self.default_dict['treeview_highlight_offset']


class ButtonToggleImage(ButtonImage):
    def __init__(self, panel, x, y, function_list, image, default_dict=base_gui.load_defaults()):
        ButtonImage.__init__(self, panel, x, y, function_list, image)

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
        self.display()
        return return_method