import pygame
import base_gui
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
gui.create_button('Toolbar', '30 day', 10, 10, [g.update30])
gui.create_panel('Data', 100, 100, 600, 400) #Note panel is not changed until it has something in it
gui.create_label('Data','Name', 10,10)
gui.create_label('Data',g.settlement_names[0], 300,10, label_name='name')
gui.create_label('Data','Population', 10, 40)
gui.create_label('Data',g.settlements[g.settlement_names[0]].pop_int, 300, 40, label_name='pop')
gui.create_dropdown('Toolbar', 'Select Planet', 200, 10, 3, g.settlement_names, g.display_settlement )

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


