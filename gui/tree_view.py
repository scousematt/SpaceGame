import pygame
import random
import base_gui


class Node(base_gui.BaseGui):
    def __init__(self, parent, text, generation, iid, show_children):
        # All variables are going to be iid's
        # The node will actually contain the data to be displayed, color block, text images etc
        self.children = []
        self.parent = parent
        self.generation = generation
        self.text = text
        self.iid = iid
        self.show_children = show_children

    def __str__(self):
        return f'parent {self.parent} iid is {self.iid} show {self.show_children}'

class Treeview(base_gui.BaseGui):
    def __init__(self):

        self.iids = ['000000']
        self.nodes = {'000000' : Node('000000', 'Root', 0, '000000', True)}
        #self.root_node = self.add_node('000000', 0, '')
        self.root = self.nodes['000000'].iid

        # Temporary while testing the order
        self.packer = '  '


    def add_node(self, parent, text, location='end', iid='', show_children=True):
        if iid == '':
            iid = self.generate_iid()

        node = Node(parent, text, self.nodes[parent].generation + 1, iid, show_children)
        self.nodes[iid] = node
        if location == 'end' or location > len(self.nodes[parent].children):
            self.nodes[parent].children.append(node)
        else:
            self.iid_dict[parent].children.insert_node(location)

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


        if not node.show_children:
            print('Not showing children')
            return


        for child in node.children:
            self.display_children(child.iid)
            # print(f'{self.packer * (self.nodes[child.iid].generation) + child.text}')
            # #print(node)
            # for grandchild in child.children:
            #     self.display_children(grandchild.iid)

    def display(self):
        self.display_children(self.root)



########
# testing

t = Treeview()
g10 = t.add_node(t.root, 'Alan')
g11 = t.add_node(t.root, 'Andy')
g12 = t.add_node(t.root, 'Arnold', show_children=False)
g1020 = t.add_node(g10, 'Bert')
g1021 = t.add_node(g10, 'Bill')
g2020 = t.add_node(g1020, 'Carl')
g1201 = t.add_node(g12, 'Bessie')
t.display()
