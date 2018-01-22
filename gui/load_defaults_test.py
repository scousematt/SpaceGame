import pygame

pygame.init()
screen = pygame.display.set_mode((800,600))

import base_gui


		
gui_defaults = base_gui.load_defaults()	
my_panel = base_gui.DefaultPanel(150,150,510, 400, screen, gui_defaults)
panels = []
active_panel = None
panels.append(my_panel)

	
	
def some_func(button):
	button.panel.change_background_color((23,0,100))
	button.change_text('test1')
	
def another_func(button):
	button.panel.change_background_color((23,200,200))
	button.change_text('test2')
	
def func3(button):
	button.panel.change_background_color((23,200,100))
	button.change_text('test3')
	
my_panel.create_label('This is a label', 10,10)
my_panel.create_label('Another label', 10, 50)
my_panel.create_label('This is a label', 10,90)
my_panel.create_label('Another label', 10, 130)

my_panel.create_label('3451', 280,10, justify='right')
my_panel.create_label('1290', 280, 50, justify='right')
my_panel.create_label('13', 280,90, justify='right')
my_panel.create_label('123313', 280, 130, justify='right')



my_panel.create_button('rrt', 200, 250, [some_func, another_func, func3])


#my_button = Button('This is text', my_panel, 200, 50)


#Testing out method passing to an object



done = False

while not done:
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			#Find out which panel we are in
			for p in panels:
				if p.rect.collidepoint(event.pos):
					active_panel = p
					break
			#Find the element clicked on in the active panel
			if active_panel:
				for element in active_panel.children:
					if type(element) == base_gui.DefaultButton and element.rect.collidepoint(event.pos):
						element.on_click()

			
		
		elif event.type == pygame.QUIT:
			done = True
			
		pygame.display.flip()



















