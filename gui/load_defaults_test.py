import pygame

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Put active panel name in here')
import base_gui


gui_defaults = base_gui.load_defaults()	

gui = base_gui.GuiManager(screen, gui_defaults)







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

func_dict = {}
func_dict['some_func'] = some_func
func_dict['another_func'] = another_func
func_dict['func3'] = func3


def test_func_arg(function, *args, **kwargs):
	function(*args, **kwargs)

def test_copy(function, *args, **kwargs):
	print(args)
	function(*args, **kwargs)


with open('gui_data.txt','r') as file:
	which = {}
	for line in file:
		if not line[0] == '#':
			args = line.strip().split(',')
			kw_dict = {}
			gui_type = args.pop(0)
			new_args = []
			for i in args:
				# if there is an '='  we need to not use args and use keywords
				# keywords = {'fontsize' : 12, 'name' : 'fred'}
				list_i = i.split('=')
				if len(list_i) == 1:
					if ':' in i and gui_type == 'button':
						# We the element is a list. Currently only button but lets check
						list_b_name = i.split(':')
						list_b = []
						for b in list_b_name:
							list_b.append(func_dict[b])
						new_args.append(list_b)
					else:
						new_args.append(base_gui.return_correct_type(i))
				else:
					kw_dict[list_i[0]] = base_gui.return_correct_type(list_i[1])
			args = new_args
			if gui_type == 'panel':
				test_func_arg(gui.create_panel, *args, **kw_dict)
			elif gui_type == 'label':
				test_func_arg(gui.create_label, *args, **kw_dict)
			elif gui_type == 'button':
				test_func_arg(gui.create_button, *args, **kw_dict)
			elif gui_type == 'scrollbar':
				test_func_arg(gui.create_scrollbar, *args, **kw_dict)
file.close()

gui.create_label('Main', 'manually added', 10, 200)


arguments = ['Main', 'add function', 210, 160]
keyword_args =  {'justify': 'right'}
#test_copy(gui.create_label, *arguments)
test_func_arg(gui.create_label, *arguments, **keyword_args)


#my_button = Button('This is text', my_panel, 200, 50)


#Testing out method passing to an object
name = 'Message Box'
title = 'This is a message box'
text = '''Don't let NPCs steal the player's thunder. Having an NPC accompany the players is not uncommon because it provides a good in-character avenue for the characters to ask questions or get information. \nJust make sure the NPC is not some super powerful badass who one shots all the enemies. Then the players will just feel like side kicks instead of heroes. Ideally, combat NPCs should take a supporting role. Nobody likes an NPC stealing their kills, but everyone likes an NPC who buffs and heals them'''
#gui.create_message_box(name, title, text, gui_defaults)

done = False

while not done:
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			#Find out which panel we are in
			gui.on_lmb_click(event.pos)
		elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
			gui.on_lmb_up(event.pos)

		elif event.type == pygame.QUIT:
			done = True
			
		gui.display()
		pygame.display.flip()



















