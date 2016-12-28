from mttkinter import Tk, PhotoImage, Label, NSEW, Canvas
import time
from queue import Queue, Empty
from threading import Event, Thread
import math

from functools import partial

class GUI:

	def changeCellColor(self, i,j, color):
		""" change the color of cell (i,j) to color """
		self.canvas.itemconfigure(self.cells[i,j],fill=color)


	def clickOnCell(self, event, coordinate=None):
		""" being called whenever a cell is clicked """
		(i,j) = coordinate
		self.clickOnCellAlgo(self,i,j)

	def dacell(self,i,j):
		return (self.BoardSize+1)*1.5*self.TileRadius + i*1.5*self.TileRadius - j*1.5*self.TileRadius, 2*self.TileRadius + i*math.sqrt(3)/2*self.TileRadius + j*math.sqrt(3)/2*self.TileRadius

	def __init__(self, taille, couleurs, numJoueur, PartieHex, CoupJoueur, QuitterPartie):
		
		self.tk = Tk()

		# define the algorithms to execute
		self.mainAlgo = PartieHex
		self.clickOnCellAlgo = CoupJoueur
		self.quitterAlgo = QuitterPartie
		
		# <--- VARIABLES ---
		self.BoardSize = taille
		self.TileRadius = 20
		self.Letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
		offsetX = (self.BoardSize+1)*1.5*self.TileRadius
		offsetY = 2*self.TileRadius
		# --- VARIABLES --->
		
		self.canvas = Canvas(self.tk, height=self.BoardSize*2*self.TileRadius+15, width=2*(self.BoardSize+1)*1.5*self.TileRadius, background="black")
		self.cells = {}
		
		
		# <--- DRAWING THE BOARD ---
		self.canvas.create_polygon([self.dacell(-1.5,self.BoardSize+0.5),self.dacell(-1.5,-1.5),self.dacell(self.BoardSize+0.5,self.BoardSize+0.5),self.dacell(self.BoardSize+0.5,-1.5)], fill="red",outline="black",width=1)
		self.canvas.create_polygon([self.dacell(-1.5,self.BoardSize+0.5),self.dacell(self.BoardSize+0.5,self.BoardSize+0.5),self.dacell(-1.5,-1.5),self.dacell(self.BoardSize+0.5,-1.5)], fill="blue",outline="black",width=1)
		
		# Drawing the board and binding a click event to each cell
		for i in range(self.BoardSize):
			for j in range(self.BoardSize):
				self.cells[i,j] = self.DrawTile(offsetX + i*1.5*self.TileRadius - j*1.5*self.TileRadius, offsetY + i*math.sqrt(3)/2*self.TileRadius + j*math.sqrt(3)/2*self.TileRadius, "#EEEEEE")
				
				self.canvas.tag_bind(self.cells[i,j],'<Button>',partial(self.clickOnCell, coordinate=(i,j) ))
				#self.canvas.tag_bind(self.cells[0,0],'<Button>',cliquerQuitter)


		# Drawing the labels around the board
		for i in range(self.BoardSize):
			j = self.BoardSize
			self.canvas.create_text(offsetX + i*1.5*self.TileRadius - j*1.5*self.TileRadius, offsetY + i*math.sqrt(3)/2*self.TileRadius + j*math.sqrt(3)/2*self.TileRadius, text="{0}".format(i+1), fill="white")
			j = -1
			self.canvas.create_text(offsetX + i*1.5*self.TileRadius - j*1.5*self.TileRadius, offsetY + i*math.sqrt(3)/2*self.TileRadius + j*math.sqrt(3)/2*self.TileRadius, text="{0}".format(i+1), fill="white")
		for j in range(self.BoardSize):
			i = -1
			self.canvas.create_text(offsetX + i*1.5*self.TileRadius - j*1.5*self.TileRadius, offsetY + i*math.sqrt(3)/2*self.TileRadius + j*math.sqrt(3)/2*self.TileRadius, text="{0}".format( self.Letters[:self.BoardSize][self.BoardSize-j-1] ), fill="white")
			i = self.BoardSize
			self.canvas.create_text(offsetX + i*1.5*self.TileRadius - j*1.5*self.TileRadius, offsetY + i*math.sqrt(3)/2*self.TileRadius + j*math.sqrt(3)/2*self.TileRadius, text="{0}".format( self.Letters[:self.BoardSize][self.BoardSize-j-1] ), fill="white")

		self.canvas.pack()
		
		Label(self.tk,text="hex game 1.0" + " - player's color:" + couleurs[numJoueur]).pack()
		# --- DRAWING THE BOARD --->


				


        # <--- PRESS q TO QUIT; LAUNCH quitter as a THREAD ---
		def quitter():
			self.quitterAlgo(self)

		def cliquerQuitter(event):
			th = Thread(target=quitter)
			th.daemon = True
			self.tk.after(100, th.start)

		self.tk.bind("q", cliquerQuitter)
		# --- PRESS q TO QUIT; LAUNCH quitter as a THREAD --->


		# <--- LAUNCH mainAlgo as a THREAD ---
		def run():
			self.mainAlgo(self)
		
		if self.mainAlgo:
			th = Thread(target=run)
			th.daemon = True
			self.tk.after(100, th.start)
		# --- LAUNCH mainAlgo as a THREAD --->
		
		
		self.tk.mainloop()


	def DrawTile(self, x, y, color):
		""" create a cell centered on (x,y) and filled with the given color """
		r = self.TileRadius
		points = [(x - r  , y),
		          (x - r/2, y - r*math.sqrt(3)/2),
		          (x + r/2, y - r*math.sqrt(3)/2),
		          (x + r  , y),
		          (x + r/2, y + r*math.sqrt(3)/2),
		          (x - r/2, y + r*math.sqrt(3)/2)]
		tile = self.canvas.create_polygon(points, outline="black", fill=color, width=1)

		return tile





	
	
