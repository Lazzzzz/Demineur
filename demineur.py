import pygame
import random

pygame.init()
pygame.font.init()

difficulty = int(input("Choisir difficulter \n 1- Facile \n 2- Moyen \n 3- Difficile\n\nPour recommencer votre partie appuyer sur 'r' \n"))

if difficulty == 1:
	difficulty = 9
	nb_case = 10

elif difficulty == 2:
	difficulty = 6
	nb_case = 20

elif difficulty == 3:
	
	difficulty = 3
	nb_case = 30

LONG = 600
LARG = 600

taille = [LONG, LARG]

taille_case = int(taille[0]/nb_case)

grille = [[0 for x in range(nb_case)] for y in range(nb_case)] 

done = False

mX, mY = pygame.mouse.get_pos()
counter = 0
counter_reveal = 0
a = 0
perdu = False
gagner = False


fenetre = pygame.display.set_mode((taille))
pygame.display.set_caption('demineur')

fenetre.fill((0,0,0))

class Case():
	def __init__(self, j, i):

		r = random.randint(0,difficulty)

		if r == 0:
			self.bombe = True
		else:
			self.bombe = False

		self.reveler = False

		self.nb_bombe_adj = 0

		self.i = i
		self.j = j

		self.font = pygame.font.SysFont("comicsansms", int(taille_case/2))

	def checkAutour(self):
		if self.bombe == False:

			if i - 1 >= 0:
				if grille[i-1][j].bombe == True:
					self.nb_bombe_adj = self.nb_bombe_adj + 1
			
			if i + 1 < len(grille):
				if grille[i+1][j].bombe == True:
					self.nb_bombe_adj = self.nb_bombe_adj + 1
			
			if j - 1 >= 0:		
				if grille[i][j-1].bombe == True:
					self.nb_bombe_adj = self.nb_bombe_adj + 1
			
			if j + 1 < len(grille[i]):	
				if grille[i][j+1].bombe == True:
					self.nb_bombe_adj = self.nb_bombe_adj + 1
				
			if i - 1 >= 0 and j - 1 >= 0:			
				if grille[i-1][j-1].bombe == True:
					self.nb_bombe_adj = self.nb_bombe_adj + 1
			
			if i - 1 >= 0 and j + 1 < len(grille[i]):
				if grille[i-1][j+1].bombe == True:
					self.nb_bombe_adj = self.nb_bombe_adj + 1
			
			if i + 1 < len(grille) and j + 1 < len(grille[i]):
				if grille[i+1][j+1].bombe == True:
					self.nb_bombe_adj = self.nb_bombe_adj + 1
				
			if i + 1 < len(grille) and  j - 1 >= 0:
				if grille[i+1][j-1].bombe == True:
					self.nb_bombe_adj = self.nb_bombe_adj + 1

	def updateAutour(self):
		if self.bombe == False:
			if self.reveler == True:	
				if self.nb_bombe_adj == 0:
					if i - 1 >= 0:
						grille[i-1][j].reveler = True
										
					if i + 1 < len(grille):
						grille[i+1][j].reveler = True
						
					if j - 1 >= 0:		
						grille[i][j-1].reveler = True
							
					if j + 1 < len(grille[i]):	
						grille[i][j+1].reveler = True
										

	def contenu(self, perdu):
		if self.reveler == True:
			if self.bombe == True:
				pygame.draw.rect(fenetre, (22, 20, 19), (self.i + 1, self.j + 1, taille_case -2, taille_case -2))
				pygame.draw.circle(fenetre, (255,0,0), (int(self.i + taille_case/2), int(self.j + taille_case/2)), int(taille_case/4))
				
				for i in range(nb_case):
					for j in range(nb_case):
						grille[i][j].reveler = True
				
			else:

				pygame.draw.rect(fenetre, (22, 20, 19), (self.i + 1, self.j + 1, taille_case -2, taille_case -2))

				if self.nb_bombe_adj != 0:
					t = self.font.render(str(self.nb_bombe_adj), True, (255, 255, 255))
					t_rect = t.get_rect(center=(self.i + taille_case/2, self.j + taille_case/2))

					fenetre.blit(t, t_rect)


	def update(self, perdu):
		
		if mX > self.i and mY > self.j:
			if mX < self.i + taille_case and mY < self.j + taille_case:
				if pygame.mouse.get_pressed()[0]:
					self.reveler = True

		pygame.draw.rect(fenetre, (255, 255, 255) , ((self.i, self.j), (taille_case, taille_case)), 1)	
		
		self.updateAutour()
		self.contenu(perdu)

for i in range(nb_case):
	for j in range(nb_case):
		grille[i][j] = Case(i * taille_case, j * taille_case)
		if grille[i][j].bombe == False:
			counter = counter + 1

for i in range(nb_case):
	for j in range(nb_case):
		grille[i][j].checkAutour()

while not done:
	
	for event in pygame.event.get():
			
		if event.type == pygame.QUIT:
			done = True
		
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_UP or event.key == pygame.K_r:

				grille = None
				grille = [[0 for x in range(nb_case)] for y in range(nb_case)] 

				counter = 0
				counter_reveal = 0
				a = 0
				perdu = False
				gagner = False

				for i in range(nb_case):
					for j in range(nb_case):
						grille[i][j] = Case(i * taille_case, j * taille_case)
						if grille[i][j].bombe == False:
							counter = counter + 1
				
				for i in range(nb_case):
					for j in range(nb_case):
						grille[i][j].checkAutour()

				print("reset")
					
	mX, mY = pygame.mouse.get_pos()

	fenetre.fill((0,0,0))
	
	counter_reveal = a
	a = 0

	for i in range(nb_case):
		for j in range(nb_case):
			grille[i][j].update(perdu)
			
			if grille[i][j].bombe == False:
				if grille[i][j].reveler == True:
					a = a + 1

			if grille[i][j].bombe == True:
				if grille[i][j].reveler == True:
					perdu = True

	if perdu == False:
		if counter_reveal == counter:
			for i in range(nb_case):
				for j in range(nb_case):
					grille[i][j].reveler = True
					
					if gagner == False:

						if difficulty == 1:
							print("vous avez gagner en difficulter facile")

						elif difficulty == 2:
							print("vous avez gagner en difficulter moyen")

						elif difficulty == 3:
							print("vous avez gagner en difficulter Difficile")
					
					gagner = True
	pygame.time.Clock().tick(30)
	pygame.display.flip()

pygame.quit()
