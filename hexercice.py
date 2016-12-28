#-----------------------------------------------------------------------------------------
import random
from sys import argv
import math
from hexgui import GUI
from UnionFind import UnionFind
from time import sleep

from queue import Queue

from socket import socket, SOL_SOCKET, SO_REUSEADDR

import hexvars as hv
from hexutils import sendcmd, recvcmd, PlateauToTablierCoord, TablierToPlateauCoord, CellulesVoisines, CoupValide, Gagnant, JouerUnCoup

#package utilisé pour le mot aléatoire
from uuid import uuid4

#package utilisé pour la fonction f(a,b,c)
from hashlib import sha256

#package utilisé pour choisir aléatoirement pile ou face (0 = pile 1 = face)
from random import randint


#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# A priori, il n'y a rien à éditer ici !
class Bravo(Exception):
	pass

class Oups(Exception):
	pass

class Aurevoir(Exception):
	#0 = état initial;
	#1 = fermeture de connexion initiée et attente de la confirmation de l'autre joueur;
	#2 = "bravo" ou "oups" reçu, le socket n'est plus en écoute pour fermer la connexion
	etat = 0
#-----------------------------------------------------------------------------------------




#-----------------------------------------------------------------------------------------


def CoupJoueur(gui, i, j):
	""" le joueur joue sur la cellule (i,j) """
	if CoupValide(i,j) and hv.monTour :
		sendcmd("joue",PlateauToTablierCoord(i,j))
		JouerUnCoup (gui,i,j,hv.numJoueur)
		hv.monTour = False
	elif not CoupValide(i,j) :
		print ("Cette case n'est pas libre !")
	elif not hv.monTour :
		print ("Ce n'est pas votre tour !")
	
	# To do ! Vous devez programmer cette fonction.


def CoupAdversaire(gui):
	""" traite les commandes et coups de l'adversaire """

	if hv.numJoueur == 1 :
		numAdv = 2
	else :
		numAdv = 1

	(cmd,coo) = recvcmd ("bravo","oups","aurevoir","joue")
	if (cmd == "bravo") :
		raise Bravo
	if (cmd == "oups") :
		raise Oups
	if (cmd == "aurevoir") :
		raise Aurevoir
	if (cmd == "joue") :
		(i,j) = TablierToPlateauCoord (coo)
		if CoupValide (i,j) and not hv.monTour :
			if (JouerUnCoup (gui,i,j,numAdv)) :
				sendcmd("bravo","")
			
			hv.monTour = True
		else :
			sendcmd("oups","")
	# To do ! Vous devez programmer cette fonction.




#-----------------------------------------------------------------------------------------
# A priori, il n'y a rien à éditer ici !
def PartieHex(gui):
	
	try:
		while(True):
			CoupAdversaire(gui)

	# Les exceptions gérent la fin de partie
	except Oups:
		Aurevoir.etat = 2
		QuitterPartie(gui)

	except Bravo:
		Aurevoir.etat = 2
		QuitterPartie(gui)
	
	except Aurevoir:
		Aurevoir.Messages.put( ("<<<", "aurevoir") )
		if Aurevoir.etat == 0:
			QuitterPartie(gui)


def QuitterPartie(gui):

	if (Aurevoir.etat == 0) or (Aurevoir.etat == 2):
		sendcmd('aurevoir', '')
		if Aurevoir.etat == 0:
			Aurevoir.etat = 1
			if Aurevoir.Messages.get() == ("<<<", "aurevoir"): pass
			else: exit(0)

		elif Aurevoir.etat == 2:
			Aurevoir.etat = 1
			if recvcmd('aurevoir') == ("aurevoir", ""): pass
			else: exit(0)
		
		hv.gs.close()
		print("--- La connexion est fermée.")
		sleep(2)
		gui.tk.quit()
		print("--- Le programme est quitté.")
	else:
		print("--- En attente de la réponse de l'autre joueur pour quitter. Patientez.")
#-----------------------------------------------------------------------------------------





#-----------------------------------------------------------------------------------------
def initClient(arguments):
	""" initialisation du client """
	
	# programmation réseaux du socket
	s=socket()
	s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

	#listeExtensions est une liste contenant toutes les extensions passées sur la ligne de commande
	listeExtensions = [key for key in arguments if arguments[key]==True]
	
	s.connect((arguments["ip"],arguments["port"]))
	hv.gs = s
	
	#bonjour extension1 extension2 ...
	sendcmd('bonjour', ' '.join(listeExtensions))
	(cmd,args)=recvcmd('bonjour')
	extensionsSupportees = []
	if len(args)>0 :
		extensionsSupportees = [param for param in args.split(' ') if arguments[param]]
	print("--- Extensions supportées par les deux joueurs :", extensionsSupportees)
	
	#joueur NomJoueur
	sendcmd('joueur', arguments["NomJoueur"])
	(cmd,args)=recvcmd('joueur')
	NomAutreJoueur = args
	print("--- L'autre joueur s'appelle %s." % NomAutreJoueur)
	
	#tablier taille1 taille2 ...
	sendcmd('tablier', ' '.join(arguments["tablier"]))
	(cmd,args) = recvcmd('tablier')
	hv.taille = int(args)
	print("--- Le serveur a choisi un tablier de taille %s" % hv.taille)

	if "pileouface" in extensionsSupportees:
		# To do ! Pour supporter l'extension pileouface, vous devez implémenter ce morceau de code
		Mot = str (uuid4())
		sendcmd ('pileouface', Mot)

		(cmd,rep) = recvcmd ('pileouface')
		Server = rep

		ran = randint (0,1)
		if ran == 0 : 
			ran = 'pile'
		else : 	
			ran = 'face'

		sendcmd ('pileouface' , ran)

		(cmd,rep) = recvcmd ('pileouface')
		Client = sha256(' '.join([Mot,rep,ran]).encode('utf8')).hexdigest()

		if Client == Server : 
			hv.monTour = True
		else :
			hv.monTour = False
	else:
		hv.monTour = True
		print("--- C'est moi qui commence.")

	hv.numJoueur = 2
	print("--- J'ai la couleur", hv.couleurs[hv.numJoueur])


def initServeur(arguments):
	""" initialisation du serveur """
	# To do ! Pour programmer le serveur, vous devez implémenter cette fonction
# programmation réseaux du socket
	s=socket()
	s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	
	s.bind (('0.0.0.0', 6666))
	s.listen (1)
	sc, addr = s.accept()
	print ("Connexion de : " , addr)

	#listeExtensions est une liste contenant toutes les extensions passées sur la ligne de commande
	listeExtensions = [key for key in arguments if arguments[key]==True]
	hv.gs = sc
	
	#bonjour extension1 extension2 ...
	(cmd,args)=recvcmd('bonjour')
	sendcmd('bonjour', ' '.join(listeExtensions))
	
	extensionsSupportees = []
	if len(args)>0 :
		extensionsSupportees = [param for param in args.split(' ') if arguments[param]]
	print("--- Extensions supportées par les deux joueurs :", extensionsSupportees)
	
	#joueur NomJoueur
	(cmd,args)=recvcmd('joueur')
	sendcmd('joueur', arguments["NomJoueur"])
	
	NomAutreJoueur = args
	print("--- L'autre joueur s'appelle %s." % NomAutreJoueur)
	
	#tablier taille1 taille2 ...
	(cmd,args) = recvcmd('tablier')
	sendcmd('tablier', ' '.join(arguments["tablier"]))
	
	hv.taille = int(args)
	print("--- Le serveur a choisi un tablier de taille %s" % hv.taille)

	if "pileouface" in extensionsSupportees:
		# To do ! Pour supporter l'extension pileouface, vous devez implémenter ce morceau de code
		Mot = str (uuid4())
		(cmd,args) = recvcmd ('pileouface')
		rep1 = args

		ran = randint (0,1)
		
		if ran == 0 : 
			ran = 'pile'
		else : 	
			ran = 'face'

		Server = sha256(' '.join([rep1, Mot, ran]).encode('utf8')).hexdigest()
		sendcmd ('pileouface' , Server)

		(cmd,args) = recvcmd ('pileouface')
		rep2 = args

		Client = sha256(' '.join([rep1, Mot, rep2]).encode('utf8')).hexdigest()
		sendcmd ('pileouface', Mot)

		if Client == Server : 
			hv.monTour = False
		else :
			hv.monTour = True

	else:
		hv.monTour = False

	hv.numJoueur = 1
	print("--- J'ai la couleur", hv.couleurs[hv.numJoueur])


def init(arguments):	
	# taille			# contient la taille du plateau
	# plateau			# plateau de jeu où l'on stocke le joueur (0, 1 ou 2) associé à chaque cellule
	# gs				# socket connectée à l'autre joueur
	# monTour			# booléen True ssi c'est à mon tour de jouer
	# numJoueur			# contient mon numéro (1 ou 2) de joueur
	# uf				# structure Union-Find pour déterminer les cellules connectées
	# couleurs			# contient les couleurs utilisées sur le plateau de l'interface graphique
	
	hv.couleurs = ['white', 'red', 'blue']
	
	if arguments["ip"]!=None:
		# on est le client
		initClient(arguments)
	else:
		# on est le serveur
		initServeur(arguments)

	# initialisation du plateau et de la structure union-find
	# le plateau est un dictionnaire; il pourrait être un tableau
	hv.plateau = {}
	for i in range(hv.taille):
		for j in range(hv.taille):
			hv.plateau[i,j] = 0
	
	hv.uf = UnionFind()
	hv.uf.union((1, "haut"), *[(-1,i) for i in range(hv.taille)])
	hv.uf.union((1, "bas"), *[(hv.taille,i) for i in range(hv.taille)])
	hv.uf.union((2, "haut"), *[(i,-1) for i in range(hv.taille)])
	hv.uf.union((2, "bas"), *[(i,hv.taille) for i in range(hv.taille)])

	# queue pour gérer les messages de fin de connexion entre thread
	Aurevoir.Messages = Queue()
	
	print("--- Initialisation terminée. La partie commence.")

		


if __name__ == '__main__':
	#hex [client IP|server] NomJoueur [tablier taille1 ... taillek] [option1] [...] [optionk]
	#hex client 127.0.0.1 Alice pileouface
	#hex.py server Alice pileouface gateau tablier 5 11
	port = 6666

	if len(argv)<3 or argv[1] not in ['client','server']:
		print('usage: %s [client IP|server] NomJoueur [extension1] [...] [extensionk] [tablier taille1 taille2 ... taillek]' % (argv[0],))
		print('exemple pour le serveur : %s server Bob pileouface gateau tablier 5 11 17' % (argv[0],))
		print('exemple pour le client  : %s client 127.0.0.1 Alice message gateau tablier 5 11 14' % (argv[0],))
		exit(1)

		
	arguments = {"NomJoueur": None, "tablier": ['11'], "pileouface": False, "gateau":False, "message":False, "ip":None, "port":port}
	for (pos,param) in enumerate(argv):
		if param in ["pileouface", "gateau", "message"]:
			arguments[param] = True
		elif param=="tablier":
			arguments[param] = argv[pos+1:] #[int(e) for e in argv[pos+1:]]

	
	if argv[1] == "client":
		arguments["ip"] = argv[2]
		arguments["NomJoueur"] = argv[3]
		print("--- Connexion à", arguments["ip"], arguments["port"])


	elif argv[1] == "server":
		#initserver()
		arguments["NomJoueur"] = argv[2]
		print("--- Attente sur le port", port)
		
	init(arguments)	
	GUI(hv.taille, hv.couleurs, hv.numJoueur, PartieHex, CoupJoueur, QuitterPartie)
#-----------------------------------------------------------------------------------------
