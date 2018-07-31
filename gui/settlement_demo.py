import pygame
import base_gui


pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Put active panel name in here')


gui_defaults = base_gui.load_defaults()

gui = base_gui.GuiManager(screen, gui_defaults)





class Settlement():
    def __init__(self, name, pop):
        self.name = name
        self.pop = pop
        self.pop_int = int(self.pop)

    def update30(self):
        self.update(30)
        print('Got to update30')
        # todo move this is a game class that can update every settlement and only change display on current view
        self.display()

    def update(self, time):
        self.pop += time * self.pop * 2.78 ** -10.5
        self.pop_int = int(self.pop)

    def display(self):
        #Note that this will always be shown in the smae panel
        gui.change_label_text('Data', 'pop', self.pop_int)

#button,Main,rrt,200,250,some_func:another_func:func3

s = Settlement('Welling Town', 2594)
gui.create_panel('Toolbar', 100, 0, 600, 98)
gui.create_button('Toolbar', '30 day', 10, 10, [s.update30])
gui.create_panel('Data', 100, 100, 600, 400) #Note panel is not changed until it has something in it
gui.create_label('Data','Name', 10,10)
gui.create_label('Data',s.name, 300,10)
gui.create_label('Data','Population', 10, 40)
gui.create_label('Data',s.pop_int, 300, 40, label_name='pop')
gui.create_dropdown('Toolbar', 'Select Planet', 200, 10, ['Welling Town', 'Friedrich Strasse','Furlong'] )

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

        elif event.type == pygame.QUIT:
            done = True

        gui.display()
        pygame.display.flip()


