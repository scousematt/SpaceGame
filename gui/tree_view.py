import pygame
import random
import base_gui, labels


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

    def display(self):
        pass

    def __str__(self):
        return f'parent {self.parent} iid is {self.iid} show {self.show_children}'

class TreeView(base_gui.BaseGui):
    def __init__(self, name, panel, x, y, default_dict):
        base_gui.BaseGui.__init__(self)
        self.parent = panel
        self.name = name
        self.x = x
        self.y = y
        self.original_y = self.y
        self.default_dict = default_dict
        self.screen = self.parent.screen
        self.iids = ['000000']
        self.nodes = {'000000' : Node('000000', 'Root', 0, '000000', True)}
        #self.root_node = self.add_node('000000', 0, '')
        self.root = self.nodes['000000'].iid

        # Temporary while testing the order
        self.packer = '  '


    def add_node(self, dad, text, location='end', iid='', show_children=True):
        if iid == '':
            iid = self.generate_iid()

        node = Node(dad, text, self.nodes[dad].generation + 1, iid, show_children)
        self.nodes[iid] = node
        if location == 'end' or location > len(self.nodes[dad].children):
            self.nodes[dad].children.append(node)
        else:
            self.iid_dict[dad].children.insert_node(location)
        self.parent.changed = True

        return iid


    def generate_iid(self):
        letters = '0123456789abcdef'
        sample_iid = '000000'
        while sample_iid in self.iids:
            sample_iid = ''.join(random.choices(letters, k=6))

        self.iids.append(sample_iid)
        return sample_iid

    def display_children(self, node_iid):
        node = self.nodes[node_iid]
        print(f'{self.packer * (self.nodes[node.iid].generation) + node.text}')
        x = self.x + 25 * self.nodes[node.iid].generation
        text = node.text
        print(node.children)
        if len(node.children) > 0 and node.show_children:
            text = f'- {node.text}'
        elif len(node.children) > 0:
            text = f'+ {node.text}'
        else:
            text = f'   {node.text}'
        self.parent.children.append(labels.DefaultLabel(text, self.parent, x, self.y ))
        self.y += 25

        if not node.show_children:
            print('Not showing children')
            return


        for child in node.children:
            self.display_children(child.iid)
            # Build up the self.panel.children


    def display(self):
        self.y = self.original_y
        self.display_children(self.root)

    def __str__(self):
        return f'Treeview name {self.name}'

