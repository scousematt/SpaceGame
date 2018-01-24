import pygame

pygame.init()
screen = pygame.display.set_mode((800,600))

import base_gui


		
gui_defaults = base_gui.load_defaults()	
my_panel = base_gui.DefaultPanel(150,150,510, 400, screen, gui_defaults)
panels = []
active_panel = None
panels.append(my_panel)


def message_box(title, text, screen, gui_defaults):
	'''
	Need to determine the size of the box in order to create a panel large enough

	Bottons will be stacked vertically
	:param text:
	:param buttons:
	:return:
	'''

	panel = base_gui.DefaultPanel(150,20, 500, 500, screen, gui_defaults)
	paragraphs = text.split('\n')
	formatted_text = []
	for paragraph in paragraphs:
		words = paragraph.split(' ')
		line = '   '
		for word in words:
			if len(line) + len(word) + 7 < gui_defaults['msg_chars_on_line']:
				line += word + ' '
			else:
				formatted_text.append(line)
				line = word + ' '
		formatted_text.append(line)
	

	#Write the text to the panel as labels

	panel.create_background_color(gui_defaults['msg_title_background_color'],
										(panel.x + gui_defaults['panel_border'],
										panel.y + gui_defaults['panel_border'],
										panel.width - gui_defaults['panel_border'] * 2, gui_defaults['msg_title_height']))
	panel.create_label('This is the heading here',
						gui_defaults['msg_title_x'],
						gui_defaults['msg_title_y'],
						justify='center')
	for i, line in enumerate(formatted_text):
		panel.create_label(line,
						   gui_defaults['msg_text_x'],
						   gui_defaults['msg_text_y'] + i*(gui_defaults['msg_label_fontsize'] + 5),
						   fontsize=gui_defaults['msg_label_fontsize'])
	
def some_func(button):
	button.panel.change_background_color((23,0,100))
	button.change_text('test1')
	
def another_func(button):
	button.panel.change_background_color((23,200,200))
	button.change_text('test2')
	
def func3(button):
	button.panel.change_background_color((23,200,100))
	button.change_text('test3')
	
my_panel.create_label('sdfsdfs a label', 10,10)
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

title = 'This is a message box'
text = '''Don't let NPCs steal the player's thunder. Having an NPC accompany the players is not uncommon because it provides a good in-character avenue for the characters to ask questions or get information. \nJust make sure the NPC is not some super powerful badass who one shots all the enemies. Then the players will just feel like side kicks instead of heroes. Ideally, combat NPCs should take a supporting role. Nobody likes an NPC stealing their kills, but everyone likes an NPC who buffs and heals them'''
message_box(title, text, screen, gui_defaults)

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



















