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
		self.s = 2
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
			#print(a, a1)
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
			tris.append([a_id, d_id, b_id])    #3
			tris.append([b_id, d_id, b1_id])   #4
			tris.append([a1_id, tri[1], c_id]) #5
			tris.append([d_id, a1_id, c_id])   #6
			tris.append([d_id, c_id, c1_id])   #7
			tris.append([d_id, c1_id, b1_id])  #8
			tris.append([b1_id, c1_id, tri[2]])#9
		else:
			tris.append([tri[0], a_id, b_id])
			tris.append([tri[1], c_id, a_id])
			tris.append([tri[2], b_id, c_id])
			tris.append([  a_id, c_id, b_id])
		for t in tris:
			if len(set(t)) < 3:
				print(tri, tris)
				print(self.vertexes[tri[0]], self.vertexes[tri[1]])
				print(self.midpoint(tri[0], tri[1], 2), 
						self.midpoint(tri[0], tri[1], -2)) 
				pdb.set_trace()
		return tris

	def refine(self):
		tris = []
		x = 0
		if self.recursions > 0:
			#Initial pass with 12 polys we need to create 2 vertexes per edge
			#After this every triangle has been converted into 9
			#There should be 180 triangle - working
			for tri in self.triangles:
				tris += self.divide_tri(tri, weight=2)
			self.triangles = tris
			tris = []
			#pdb.set_trace()
			print("Finished initial recursion")
			print((self.triangles))
		while x < self.recursions:
			for tri in self.triangles:
				tris += self.divide_tri(tri, weight=1)					
			x += 1
			self.triangles = tris
			tris=[]
			print(len(self.triangles))
			print(x)
		self.hexes = len(self.vertexes) 

			
		#self.set_color_list()
		#~ for vert in self.vertexes:
			#~ self.vertexes_bytes += sys.getsizeof(vert)
			
	def build_hexes(self, vert_hex_centre):
		#build pentagons from first 12 vertexes
		temp_list = []
		self.hex_centres.append(vert_hex_centre)
		for tris in self.triangles:
			if vert_hex_centre in tris:
				temp_list.append(tris)
		self.hex_temp += temp_list 
		
				
	def identify_hexes(self):
		'''
		Take vertexes and triangles, first vertex is centre of pentagon
		find all triangles with 0 in and append a list to hex
		'''
		#take the list of pentagon triangles and for each find a new centre
		for vert in range(12):
			self.build_hexes(vert)
		self.hex_list += self.hex_temp
		print("Hex list")
		print(self.hex_centres)
		#pdb.set_trace()
		self.hex_temp = []
		while len(self.hex_list) < len(self.triangles):
			for tri in self.hex_list:
				#edge is the shared edge between one tri with a centre in
				#self.hex_centres and one new one to be placed in hex_centres
				#and the 2 triangles are found in tris_with_edges
				edge = [tri[i] for i in range(3) if tri[i] not in self.hex_centres]
				if len(edge) < 2:
					print("Edge")
					#print( edge, tri)
					#print(self.triangles)
				else:	
					tris_with_edge = [tri for tri in self.triangles 
								if edge[0] in tri and edge[1] in tri]
				#print(tris_with_edge)	
				if len(self.hex_list) == 1380:
					print( tris_with_edge, edge )			
				verts = list(set(itertools.chain(*tris_with_edge)))
				if len(self.hex_list) < 1380:
					#print(verts)
					#Remove the verts from the shared edge
					verts.pop(verts.index(edge[0]))
					verts.pop(verts.index(edge[1]))
				#take the unique value
				
				new_centre_vert = [verts[i] for i in range(2)
									if verts[i] not in self.hex_centres]
				#Not every edge will have a new_centre_vert
				if len(new_centre_vert) > 0:
					self.build_hexes(new_centre_vert[0])
				#print(self.hex_temp)

			self.hex_list += self.hex_temp
			print(len(self.hex_list))
			self.hex_temp = []
		'''
		self.hex_temp is only the newly added hexes, so we need to generate
		our new list of edges from this rather than self.hex_list so we don't
		iterate over previously processed hexes
		'''	
			


		#print(self.hex_centres)


	def set_color_list(self):
		x = 0
		while x < len(self.hex_centres):
			self.color.append((random.random(), random.random(), random.random()))
			x += 1
		self.color[0] = (1,1,1)
		print(self.color[0])
		
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
		for surface in self.hex_list:
			
			for vertex in surface:
				if x < 55:
					glColor3fv(self.color[x // 5])

				else:
					#glColor3fv(self.color[(x - 54) // 6])
					glColor3fv((1.0,0,0))
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
			v = ([(v1 + v2)/2 for (v1, v2) in zip(v1, v2)])
		elif weight < 0:
			#the vertexes 2/3 along each edge
			v = ([v2 + (2 * (v1 - v2) / 3) for (v1, v2) in zip(v1, v2)])
		else:
			#vertexes 1/3 along each edge
			v = ([v2 + ((v1 - v2) / 3) for (v1, v2) in zip(v1, v2)])
			
		magnitude = sum([v[i]**2 for i in range(3)]) ** 0.5
		return [round(v[i] * self.t_magnitude / magnitude, 7) for i in range(3)]

	def magnitude(self):
		for v in self.vertexes:
			print(sum([v[i]**2 for i in range(3)]) ** 0.5)


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
	#ico.magnitude()
	ico.identify_hexes()
	ico.set_color_list()
	print("mnmmmmm")
	print(ico.t_magnitude)
	#glEnable(GL_VERTEX_ARRAY)
	#vbo_id = 1
	#glBindBuffer(GL_ARRAY_BUFFER, vbo_id)
	#num_verts = len(ico.vertexes)
	
	#glBufferData(GL_ARRAY_BUFFER, ico.vertexes_bytes, ico.vertexes, GL_STREAM_DRAW)
	#glBindBuffer(GL_ARRAY_BUFFER, vbo_id)
	#print(ico.vertexes_bytes)
	
	
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
				
#~ ico = Icosphere()
#~ ico.render()
#~ print(ico.vertexes[0][1])
#~ print(ico.triangles)
#~ ico.refine()
#~ print(ico.triangles)
