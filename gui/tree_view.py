import pygame
import random
import base_gui, labels, fundamentals, buttons, scrollbars


class Node(base_gui.BaseGui):
    def __init__(self, parent, text, generation, iid, show_children):
        base_gui.BaseGui.__init__(self)
        # All variables are going to be iid's
        # The node will actually contain the data to be displayed, color block, text images etc
        self.children = []
        self.parent = parent
        self.generation = generation
        self.text = text
        self.iid = iid
        self.show_children = show_children
        self.str = f'parent {self.parent} iid is {self.iid} show {self.show_children}'


    def toggle_show(self):
        if self.show_children:
            self.show_children = False
        else:
            self.show_children = True


    def display(self):
        pass


class TreeView(base_gui.BaseGui):
    def __init__(self, name, panel, x, y, default_dict):
        base_gui.BaseGui.__init__(self)
        self.parent = panel
        self.name = name

        self.x = x
        self.y = y
        self.original_y = self.y
        self.original_x = self.x
        self.default_dict = default_dict
        # self.default_dict['button_width'] = self.default_dict['label_fontsize'] - 2
        # self.default_dict['button_height'] = self.default_dict['label_fontsize'] - 2
        # self.default_dict['button_highlight_offset'] = 1
        self.screen = self.parent.screen
        #  Make a rect which will hold the outputted leaves
        self.rect = None

        #  Setup a rect to suit plus and minus images.
        self.control_rect = pygame.Rect(self.x,
                                        self.y,
                                        self.default_dict['label_fontsize'],
                                        self.default_dict['label_fontsize'])
        #  This is a blank, the same size as the image.
        self.element_height = self.default_dict['label_fontsize']
        #  Setup the first node, the treeview root.
        self.iids = ['000000']
        self.nodes = {'000000' : Node('000000', 'Root', 0, '000000', True)}
        self.root = self.nodes['000000'].iid

        #  Temporary while testing the order


        #  Set the panel to active so that it is examined in the gui loop
        self.parent.active = True
        self.str = f'Treeview {self.name} in panel {self.parent.name}'
        #  Cumulative changes to the y as scrollbar is manipulated
        self.total_offset = 0
        #  Run to set up the self.rect so that it is populated for self.parent.display().
        self.recalculate_output(self.root)

    def add_node(self, parent, text, location='end', iid='', show_children=True):
        if iid == '':
            iid = self.generate_iid()

        node = Node(parent, text, self.nodes[parent].generation + 1, iid, show_children)
        self.nodes[iid] = node
        if location == 'end' or location > len(self.nodes[parent].children):
            self.nodes[parent].children.append(node)
        else:
            self.iid_dict[parent].children.insert_node(location)
        self.parent.changed = True

        return iid


    def generate_iid(self):
        letters = '0123456789abcdef'
        sample_iid = '000000'
        while sample_iid in self.iids:
            sample_iid = ''.join(random.choices(letters, k=6))

        self.iids.append(sample_iid)
        return sample_iid

    def recalculate_output(self, node_iid):
        node = self.nodes[node_iid]
        x = self.x + self.element_height + node.generation * self.default_dict['treeview_column_spacing']
        #  We need a rect for the image.
        self.control_rect.topleft = (x, self.y)
        if len(node.children) > 0 and node.show_children:
            #     def __init__(self, panel, x, y, function_list, image, default_dict=base_gui.load_defaults()):
            self.children.append(buttons.ButtonTreeviewImage(self.parent, x, self.y,[node.toggle_show],
                                                            self.default_dict['treeview_minus'],
                                                            default_dict=self.default_dict))
        elif len(node.children) > 0:
            self.children.append(buttons.ButtonTreeviewImage(self.parent, x, self.y,[node.toggle_show],
                                                            self.default_dict['treeview_plus'],
                                                            default_dict=self.default_dict))
        x += self.element_height
        self.children.append(labels.DefaultLabel(node.text, self.parent, x + self.default_dict['treeview_packer'], self.y))
        #  Added the label increment the y position.
        self.y += self.element_height
        if node_iid == self.root:
            #  Initialise self.rect
            self.rect = self.children[-1].rect
        else:
            self.rect = self.rect.union(self.children[-1].rect)


        #  If there are no visible children then return to the next sibling of its generation
        if not node.show_children:
            return

        #  If we can see the children, iterate through them
        for child in node.children:
            self.recalculate_output(child.iid)


    def update(self, y_change):
        self.children = []
        # self.original_y += y_change
        self.y = self.original_y
        self.recalculate_output(self.root)
        self.total_offset += y_change
        self.rect.y += self.total_offset

    def display(self):
        display_rect = self.parent.display_rect
        offset = display_rect.y - self.parent.rect.y
        for child in self.children:
            if display_rect.contains(child.rect):
                child.update(-offset)
                child.display()



