import pygame

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Put active panel name in here')
import base_gui


gui_defaults = base_gui.load_defaults()	

gui = base_gui.GuiManager(screen, gui_defaults)

#Make a panel called 'Main'. The numbers are x, y, width, height
gui.create_panel('Main', 150,150,510,400)



def message_box(name, title, text, screen, gui_defaults):
	'''
	Need to determine the size of the box in order to create a panel large enough

	Bottons will be stacked vertically
	:param text:
	:param buttons:
	:return:
	'''
	#Make existing panels on the screen inactive to the input
	gui.panels_inactivate()
	gui.create_panel(name, 150,20, 500, 500)
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
	panel = gui.panel_dict[name]
	# Create background for title
	title_background = base_gui.DefaultColorBlock(panel, gui_defaults['msg_title_background_color'],
										(panel.x + gui_defaults['panel_border'],
										panel.y + gui_defaults['panel_border'],
										panel.width - gui_defaults['panel_border'] * 2, gui_defaults['msg_title_height']))
	panel.create_label(title,
						gui_defaults['msg_title_x'],
						gui_defaults['msg_title_y'],
						justify='center')
	for i, line in enumerate(formatted_text):
		panel.create_label(line,
						   gui_defaults['msg_text_x'],
						   gui_defaults['msg_text_y'] + i*(gui_defaults['msg_label_fontsize'] + 5),
						   fontsize=gui_defaults['msg_label_fontsize'])

	end_of_text_y = (2 * gui_defaults['msg_text_y']) + (gui_defaults['msg_label_fontsize'] + 5) * len(formatted_text)
	gui.create_button_ok(panel, gui_defaults['msg_text_x'], end_of_text_y)

class Game():

	def __init__(self, value):
		self.value = value


game = Game(67)

def some_func(button):
	button.panel.change_background_color((23,0,100))
	button.change_text('test1')
	gui.change_label_text('Info','game_value', game.value)
	game.value += 10


def another_func(button):
	button.panel.change_background_color((23,200,200))
	button.change_text('test2')
	
def func3(button):
	button.panel.change_background_color((23,200,100))
	button.change_text('test3')
	
gui.create_label('Main', 'sdfsdfs a label', 10,10)
gui.create_label('Main', 'Another label', 10, 50)
gui.create_label('Main', 'This is a label', 10,90)
gui.create_label('Main', 'Another label', 10, 130)

gui.create_label('Main', '3415', 280,10, justify='right')
gui.create_label('Main', '1265', 280,50, justify='right', fontsize=14)
gui.create_label('Main', '13', 280,90, justify='right')
gui.create_label('Main', '142323', 280,130, justify='right')

gui.create_panel('Info', 150,10,510,130)
gui.create_label('Info', 'Value is', 10, 10)
gui.create_label('Info', 0, 280, 10, justify='right', label_name='game_value')


gui.create_button('Main', 'rrt', 200, 250, [some_func, another_func, func3])


#my_button = Button('This is text', my_panel, 200, 50)


#Testing out method passing to an object
name = 'Message Box'
title = 'This is a message box'
text = '''Don't let NPCs steal the player's thunder. Having an NPC accompany the players is not uncommon because it provides a good in-character avenue for the characters to ask questions or get information. \nJust make sure the NPC is not some super powerful badass who one shots all the enemies. Then the players will just feel like side kicks instead of heroes. Ideally, combat NPCs should take a supporting role. Nobody likes an NPC stealing their kills, but everyone likes an NPC who buffs and heals them'''
message_box(name, title, text, screen, gui_defaults)

done = False

while not done:
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			#Find out which panel we are in
			gui.on_lmb_click(event.pos)

		elif event.type == pygame.QUIT:
			done = True
			
		gui.display()
		pygame.display.flip()



















