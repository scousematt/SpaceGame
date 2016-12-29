import math
import random
import sys
import pygame
from pygame.locals import *

import itertools, operator
import pdb




from OpenGL.GL import *
from OpenGL.GLU import *


class Icosphere:
	def __init__(self):
		self.s = 2.5
		self.t = self.s * (1.0 + math.sqrt(5.0)) / 2.0
		#Note the 1 is the same 1 as in the vertexes.append
		self.t_magnitude = (self.s**2 + self.t**2) ** 0.5
		self.vertexes = []
		self.triangles = []
		self.hex_list = []
		self.hex_temp = []
		self.hex_centres = []
		self.hexes = 12
		#rotate
		self.angle = 3
		self.r_x = 3
		self.r_y = 3
		#vertex buffer 
		self.vertexes_bytes = 0
		
		self.recursions = 2
		
		self.color = []
		
		self.generate()
		
		
	def generate(self):
		self.vertexes.append([-self.s,  self.t, 0])
		self.vertexes.append([ self.s,  self.t, 0])
		self.vertexes.append([-self.s, -self.t, 0])
		self.vertexes.append([ self.s, -self.t, 0])

		self.vertexes.append([ 0, -self.s,  self.t])
		self.vertexes.append([ 0,  self.s,  self.t])
		self.vertexes.append([ 0, -self.s, -self.t])
		self.vertexes.append([ 0,  self.s, -self.t])

		self.vertexes.append([ self.t, 0, -self.s])
		self.vertexes.append([ self.t, 0,  self.s])
		self.vertexes.append([-self.t, 0, -self.s])
		self.vertexes.append([-self.t, 0,  self.s])

		#create 20 triangles from the above vertexes
		
		#5 faces around point 0
		self.triangles.append([0, 11,  5])
		self.triangles.append([0,  5,  1])
		self.triangles.append([0,  1 , 7])		
		self.triangles.append([0,  7, 10])		
		self.triangles.append([0, 10, 11])

		#5 adjacent faces
		self.triangles.append([ 1,  5,  9])
		self.triangles.append([ 5, 11,  4])
		self.triangles.append([11, 10,  2])		
		self.triangles.append([10,  7,  6])		
		self.triangles.append([ 7,  1,  8])
		
		#5 faces around point 3
		self.triangles.append([ 3,  9,  4])
		self.triangles.append([ 3,  4,  2])
		self.triangles.append([ 3,  2,  6])		
		self.triangles.append([ 3,  6,  8])		
		self.triangles.append([ 3,  8,  9])
		
		#5 adjacent faces
		self.triangles.append([ 4, 9,  5])
		self.triangles.append([ 2, 4, 11])		
		self.triangles.append([ 6, 2, 10])		
		self.triangles.append([ 8, 6,  7])			
		self.triangles.append([ 9, 8,  1])

	def divide_tri(self, tri, weight):
		'''
		tri is a single element of self.triangle consisting of 
		3 vertex indexes
		weight dictates wether the number of subdivisions:
			1 is half
			4/3 is thirds
		'''
		tris = []
		a = self.midpoint(tri[0], tri[1], weight)
		b = self.midpoint(tri[0], tri[2], weight)
		c = self.midpoint(tri[1], tri[2], weight)

		a_id = self.add_vertexes(a)
		b_id = self.add_vertexes(b)
		c_id = self.add_vertexes(c)
		
		if weight == 2:
			a1 = self.midpoint(tri[0], tri[1], -weight)
			b1 = self.midpoint(tri[0], tri[2], -weight)
			c1 = self.midpoint(tri[1], tri[2], -weight)
			#midpoint is halfway between c and b so weight = 1
			d  = self.midpoint(c_id, b_id, 1)
			a1_id = self.add_vertexes(a1)
			b1_id = self.add_vertexes(b1)
			c1_id = self.add_vertexes(c1)
			d_id  = self.add_vertexes(d)
			tris.append([tri[0], a_id, b_id])  #1
			tris.append([a_id, a1_id, d_id])   #2
			tris.append([d_id, b_id, a_id])    #3
			tris.append([b_id, d_id, b1_id])   #4
			tris.append([a1_id, tri[1], c_id]) #5
			tris.append([c_id, d_id, a1_id])   #6
			tris.append([d_id, c_id, c1_id])   #7
			tris.append([c1_id, b1_id, d_id])  #8
			tris.append([b1_id, c1_id, tri[2]])#9
			#Add the hex centres to self.hex_centres
			self.hex_centres.append(tri[0])
			self.hex_centres.append(tri[1])
			self.hex_centres.append(tri[2])
			self.hex_centres.append(d_id)
			
		else:
			tris.append([tri[0], a_id, b_id])
			tris.append([tri[1], c_id, a_id])
			tris.append([tri[2], b_id, c_id])
			tris.append([  a_id, c_id, b_id])
		#~ for t in tris:
			#~ if len(set(t)) < 3:
				#~ print(tri, tris)
				#~ print(self.vertexes[tri[0]], self.vertexes[tri[1]])
				#~ print(self.midpoint(tri[0], tri[1], 2), 
						#~ self.midpoint(tri[0], tri[1], -2)) 
				#~ pdb.set_trace()
				
		return tris

	def refine(self):
		tris = []
		x = 0
		count = 0
		if self.recursions > 0:
			#Initial pass with 12 polys we need to create 2 vertexes per edge
			#After this every triangle has been converted into 9
			#There should be 180 triangle - working
			while x < self.recursions:
				for triangle in self.triangles:
					count += 1
					tris += self.divide_tri(triangle, weight=2)
					print("{} triangles".format(count))
				self.triangles = tris
				tris = []
				count = 0
				print("Count reset")
				x += 1
			#pdb.set_trace()
			print("Finished initial recursion")
			#print((self.triangles))


			
	def identify_hexes(self):
		self.hex_centres = list(set(self.hex_centres))
		triangles_in_hex = []
		for centre_vertex in self.hex_centres:
			self.color.append((random.random(), random.random(), random.random()))
			for triangle in self.triangles:
				if centre_vertex in triangle:
					#The triangle has a vertex that is a hex centre
					triangles_in_hex.append(triangle)
			self.hex_list.append(triangles_in_hex)
			triangles_in_hex = []
		


	def add_vertexes(self, v):
		#print(v)
		if v in self.vertexes:
			return self.vertexes.index(v)
		else:
			self.vertexes.append(v)
			return len(self.vertexes) - 1

	def rotate(self):
		glLoadIdentity() #resets the view
		glTranslate(0, 0, -10) #moves the view
		glRotatef(self.angle, self.r_x, self.r_y, 0)
		self.angle += 1.5
		self.r_x = self.r_x + 0.8 - random.random()
		self.r_y = self.r_y + 1 - random.random()
		
				
	def render_old_GL(self):
		glBegin(GL_TRIANGLES)
		x=0
		for single_hex in self.hex_list:
			glColor3fv(self.color[x])
			for triangle in single_hex:
				for vertex in triangle:
					glVertex3fv(self.vertexes[vertex])
			x += 1
		glEnd()
		
	def render(self):
		glBegin(GL_TRIANGLES)
		for surface in self.hex_list:
			for vertex in surface:
				pass
		
		
	def midpoint(self, v1, v2, weight):
		#print(v1, v2)
		v1 = self.vertexes[v1]
		v2 = self.vertexes[v2]
		if weight == 1:
			v = ([(v1 + v2) / 2 for (v1, v2) in zip(v1, v2)])
		elif weight < 0:
			#the vertexes 2/3 along each edge
			v = ([((2 * v2 / 3) +  v1 / 3) for (v1, v2) in zip(v1, v2)])
		else:
			#vertexes 1/3 along each edge
			v = ([((2 * v1 / 3) + v2 / 3) for (v1, v2) in zip(v1, v2)])
			
		magnitude = sum([v[i]**2 for i in range(3)]) ** 0.5
		return [round(v[i] * self.t_magnitude / magnitude, 8) for i in range(3)]

def main():
	pygame.init()
	display = (800, 600)
	pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
	glMatrixMode(GL_PROJECTION)
	glEnable(GL_CULL_FACE)
	glCullFace(GL_BACK)
	gluPerspective(45, (display[0]/display[1]), 0.1, 150.0)
	glMatrixMode(GL_MODELVIEW)
	ico = Icosphere()
	ico.refine()
	ico.identify_hexes()

	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		ico.rotate()
		ico.render_old_GL()
		
		#glLoadIdentity()
		#glTranslatef(0.0, 0.0, -45.0)
		pygame.display.flip()




if __name__ == "__main__":
	main()

