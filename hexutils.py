import hexvars as hv


#-----------------------------------------------------------------------------------------
def sendcmd(cmd,args, affiche=True):	
	if args:
		hv.gs.send(('%s %s\n' % (cmd,args)).encode('utf-8'))
	else:
		hv.gs.send(('%s\n' % (cmd,)).encode('utf-8'))
	if affiche: print(">>>", cmd, args)

def recvcmd(*pot, affiche=True):
	v = hv.gs.recv(1024)
	l = v.decode('utf-8').strip().split(' ',1)
	cmd = l[0]
	if len(l)>1:
		args = l[1]
	else:
		args = ''
	assert cmd in pot
	if affiche: print("<<<", cmd, args)
	return (cmd,args)
#-----------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------
def PlateauToTablierCoord(i, j):
	""" convertit les coordonnées (i,j) du plateau vers des coordonnées ('lettre' nombre) du tablier """

	Lettres = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	l, n = Lettres[:hv.taille][hv.taille-j-1], i+1
	return l+str(n)

def TablierToPlateauCoord(coord):
	""" convertit les coordonnées ('lettre' nombre) du tablier vers des coordonnées (i,j) du plateau """
	
	l, n = coord[0] , int(coord[1:])
	Lettres = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	return ( n-1, hv.taille-1-Lettres[:hv.taille].index(l) )

def CellulesVoisines(i, j, joueur):
	""" retourne la liste des cellules voisines à la cellule (i,j) et appartenant au joueur."""
	
	voisins = [(i-1, j-1), (i, j-1), (i+1, j), (i+1, j+1), (i, j+1), (i-1, j)]
	return [(x,y) for (x,y) in voisins if x>=0 and x<hv.taille and y>=0 and y<hv.taille and hv.plateau[x,y]==joueur] + [(x,y) for (x,y) in voisins if (joueur==1 and (x<0 or x==hv.taille)) or (joueur==2 and (y<0 or y==hv.taille))]
	
def CoupValide(i, j):
	""" vérifie si un coup sur la cellule (i,j) est valide """
	
	if i < 0 or i >= hv.taille or j < 0 or j >= hv.taille or hv.plateau[i,j]!=0:
		return False
	return True

def Gagnant(joueur):
	""" return True if joueur couleur gagne; False otherwise """
	
	if hv.uf[(joueur,"haut")] == hv.uf[(joueur,"bas")]:
		return True
	return False

def JouerUnCoup(gui, i, j, numeroJoueur):
	""" joue la cellule (i,j) pour le joueur numeroJoueur """
		
	hv.plateau[i,j] = numeroJoueur
	gui.changeCellColor(i, j, hv.couleurs[numeroJoueur])
	
	# On utilise une structure UnionFind pour déterminer les cellules connectées
	hv.uf.union((i,j), *CellulesVoisines(i, j, numeroJoueur))

	return Gagnant(numeroJoueur)
#-----------------------------------------------------------------------------------------

