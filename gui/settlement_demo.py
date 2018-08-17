import pygame
import base_gui, event_loop_methods
import game

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Put active panel name in here')


gui_defaults = base_gui.load_defaults()

gui = base_gui.GuiManager(screen, gui_defaults)





g = game.Game(gui, 'Data')
g.add_settlement('Welling Town', 2594,)
g.add_settlement('Plantain', 2583)
g.add_settlement('Fire Creek', 3002)
g.add_settlement('Ford Wilson', 1300)
g.add_settlement('Chess Line', 1845)
g.add_settlement('Withering Wild', 2015)

#button,Main,rrt,200,250,some_func:another_func:func3

gui.create_panel('Toolbar', 100, 0, 600, 98)
gui.create_button('Toolbar', 10, 10, [g.update], ['plus.png', 'minus.png'], kind='toggle')
gui.create_panel('Data', 100, 100, 600, 400) #Note panel is not changed until it has something in it
gui.create_label('Data','Name', 10,10)
gui.create_label('Data',g.settlement_names[0], 300,10, label_name='name')
gui.create_label('Data','Population', 10, 40)
gui.create_label('Data',g.settlements[g.settlement_names[0]].pop_int, 300, 40, label_name='pop')
#  panel created, initial text, x, y, number entries visible at once, entry list, function, length of text displayed.
gui.create_dropdown_title('Toolbar', 'Select Planet', 200, 10, 3, g.settlement_names, g.display_settlement, length=20 )
gui.create_dropdown_title('Toolbar', 'Time', 500, 10, 5, g.time_increments, g.set_time_increment)

gui.create_panel('Tree', 200, 130, 400, 250)

t = gui.create_treeview('Tree', 'Testing', 10, 10)


########
# testing

g10 = t.add_node(t.root, 'Alan')
g11 = t.add_node(t.root, 'Andy')
g12 = t.add_node(t.root, 'Arnold', show_children=False)
g1020 = t.add_node(g10, 'Bert')
g1021 = t.add_node(g10, 'Bill')
g2020 = t.add_node(g1020, 'Carl')
g1201 = t.add_node(g12, 'Bessie')
g1202 = t.add_node(g12, 'Bertha')
g1203 = t.add_node(g12, 'Barbara')
g1204 = t.add_node(g12, 'Brenda')
g1205 = t.add_node(g12, 'Beth')
g1206 = t.add_node(g12, 'Brook')
g1207 = t.add_node(g12, 'Blanche')
g1208 = t.add_node(g12, 'Briana')


t.display()




# TODO We have a drop box that we can click on, now it needs to refresh the information in 'Data' and redraw it. Also make the
# drop list panel the only active panel, which will disappear when clicking is done elsewhere, and of course the scrollbar.


done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Find out which panel we are in
            gui.on_lmb_click(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            gui.on_lmb_up(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            if gui.dropdown_active:
                gui.on_mousemove_dropdown(event.pos)

        elif event.type == pygame.QUIT:
            done = True

        gui.display()
        pygame.display.flip()


