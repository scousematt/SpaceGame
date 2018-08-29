import pygame
import base_gui

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
        #  Text sizes.
        self.formatted_text = base_gui.format_text(self.text, self.default_dict['msg_chars_on_line'])
        self.end_of_text_y = (2 * self.default_dict['msg_text_y']) + \
                                (self.default_dict['msg_label_fontsize'] + 5) * len(self.formatted_text)

        #  Panel sizes.
        dialogs_shown = len([dialog for dialog in self.gui.dialogs if dialog.visible])
        self.x = self.default_dict['dialog_x'] + dialogs_shown * self.default_dict['dialog_multiple_offset']
        self.y = self.default_dict['dialog_y'] + dialogs_shown * self.default_dict['dialog_multiple_offset']
        self.height = self.end_of_text_y + self.default_dict['button_height'] + self.default_dict['msg_text_y']

        #  Set up Title
        self.title_rect = pygame.Rect(self.x + self.default_dict['panel_border'],
                                      self.y + self.default_dict['panel_border'],
                                      self.width - self.default_dict['panel_border'] * 2,
                                      self.default_dict['msg_title_height'])



    def set_panel_sizes(self):
        #  A seperate method so that class children can calculate differently - images etc.
        #  Text sizes.
        self.formatted_text = base_gui.format_text(self.text, self.default_dict['msg_chars_on_line'])
        end_of_text_y = (2 * self.default_dict['msg_text_y']) + \
                                (self.default_dict['msg_label_fontsize'] + 5) * len(self.formatted_text)

        #  Panel sizes.
        dialogs_shown = len([dialog for dialog in self.gui.dialogs if dialog.visible])
        self.x = self.default_dict['dialog_x'] + dialogs_shown * self.default_dict['dialog_multiple_offset']
        self.y = self.default_dict['dialog_y'] + dialogs_shown * self.default_dict['dialog_multiple_offset']
        self.height = end_of_text_y + self.default_dict['button_height'] + self.default_dict['msg_text_y']
        self.width = self.default_dict['dialog_width']





