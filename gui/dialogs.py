import pygame
import base_gui, panels


def make_standard(gui, name, default_dict):
        #  Just adding a single ok button
        _buttonx = default_dict['dialog_width'] / 2 - default_dict['button_width'] / 2
        gui.panel_dict[name].create_button_ok(_buttonx, gui.panel_dict[name].end_of_text_y)

def make_standard_image(gui, name, title, text, default_dict, visible, active, image):
    pass

dialog_type_dict = {'standard': make_standard}

def make_dialog(dialog_type, gui, name, title, text, default_dict, visible, active, image):
    gui.panel_dict[name] = panels.PanelDialog(gui, name, title, text, default_dict, visible, active, image)
    gui.panels.append(gui.panel_dict[name])
    dialog_type_dict[dialog_type](gui, name, default_dict)


class DefaultDialog():
    '''
|   This is a builder class that calculates a lot of variables for a panel object.
   '''
    def __init__(self, gui, title, text, default_dict=base_gui.load_defaults()):

        self.gui = gui
        self.title = title
        self.text = text
        self.default_dict = default_dict

        self.set_panel_sizes()
        self.set_active()

    def set_active(self):
        #  The dialog is the only thing on the screen which can be clicked on.
        for p in self.gui.panels:
            p.active = False

    def close_dialog(self):
        print(f'close dialog for dialog {self.name} len of dialogs {len(self.gui.dialog_dict)}')
        self.gui.number_dialogs -= 1
        self.gui.hide_panel(self.name)
        del self.gui.dialog_dict[self.name]
        self.gui.panels.remove(self.gui.panel_dict[self.name])
        #  Make the last dialog the active one.
        if len(self.gui.dialog_dict) > 0:
            _key = list(self.gui.dialog_dict)[-1]
            self.gui.dialog_dict[_key].active = True
        else:
            for panel in self.gui.panels:
                if panel.visible:
                    panel.active = True

    def set_panel_sizes(self):
        #  A seperate method so that class children can calculate differently - images etc.
        #  Text sizes.
        self.formatted_text = base_gui.format_text(self.text, self.default_dict['msg_chars_on_line'])
        self.end_of_text_y = (2 * self.default_dict['msg_text_y']) + \
                             (self.default_dict['msg_label_fontsize'] + 5) * len(self.formatted_text)


        #  Panel sizes.
        self.gui.number_dialogs += 1
        self.x = self.default_dict['dialog_x'] + self.gui.number_dialogs * self.default_dict['dialog_multiple_offset']
        self.y = self.default_dict['dialog_y'] + self.gui.number_dialogs * self.default_dict['dialog_multiple_offset']
        self.height = self.end_of_text_y + self.default_dict['button_height'] + self.default_dict['msg_text_y']
        self.width = self.default_dict['dialog_width']

        #  Set up Title
        self.title_rect = pygame.Rect(self.x + self.default_dict['panel_border'],
                                      self.y + self.default_dict['panel_border'],
                                      self.width - self.default_dict['panel_border'] * 2,
                                      self.default_dict['msg_title_height'])






