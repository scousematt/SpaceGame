
import math
import tkinter as tk
import tkinter.ttk as ttk

RADIUS = 16

def get_points(x, y):
	dc = RADIUS /2 #* math.cos(math.pi / 3)
	ds = RADIUS * math.sin(math.pi / 3)
	v1 = (x - dc, y - ds)
	v2 = (x + dc, y - ds)
	v3 = (x + RADIUS, y)
	v4 = (x + dc, y + ds)
	v5 = (x - dc, y + ds)
	v6 = (x - RADIUS, y)
	return [v1, v2, v3, v4, v5, v6]
	
root = tk.Tk()
can = tk.Canvas(root, width=800, height=800, borderwidth=0)
can.grid()
#top left


def draw_hexes(can, x, y, number_of_hexes):
	number_of_rows = 4 * number_of_hexes + 2
	dy = RADIUS * math.sin(math.pi / 3)
	dx = RADIUS * 1.5
	temp_number_of_hexes = number_of_hexes

	color = 'grey'
	hexes = []
	for j in range(number_of_rows):
		count = 0
		for i in range(temp_number_of_hexes):
			if count == j:
				break
			can.create_polygon(get_points(x + count * 3 * RADIUS, y), 
								outline='black', fill=color)
			hexes.append((j, i))
			count += 1
		if j < number_of_hexes:
			x -= dx
		elif j == number_of_hexes:
			x += dx
			temp_number_of_hexes -= 1 
		elif j > number_of_hexes and j < number_of_hexes * 3 - 3:
			if temp_number_of_hexes < number_of_hexes:
				temp_number_of_hexes = number_of_hexes
				x -= RADIUS * 3
			else:
				temp_number_of_hexes -= 1
				x += RADIUS * 3
			dx *= -1
			x -= dx
		elif j == number_of_hexes * 3 - 3:
			
			if number_of_hexes % 2 == 0:
				temp_number_of_hexes = number_of_hexes
				x -= dx
			else:
				temp_number_of_hexes = number_of_hexes - 1
				x += dx
		else:
			temp_number_of_hexes -= 1
			x += dx
		y += dy
	return hexes
			
x = 400
y = 50
number_of_hexes = 10		
hexes = draw_hexes(can, x, y, number_of_hexes)
#print(hexes)
can.itemconfig(136, fill='red')
		
root.mainloop() 
	
	
