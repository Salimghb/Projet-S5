def __init__():
	global taille, plateau, gs, monTour, numJoueur, uf, couleurs

	# taille			# contient la taille du plateau
	# plateau			# plateau de jeu où l'on stocke le joueur (0, 1 ou 2) associé à chaque cellule
	# gs				# socket connectée à l'autre joueur
	# monTour			# booléen True ssi c'est à mon tour de jouer
	# numJoueur			# contient mon numéro (1 ou 2) de joueur
	# uf				# structure Union-Find pour déterminer les cellules connectées
	# couleurs			# contient les couleurs utilisées sur le plateau de l'interface graphique

	taille = None
	plateau = None
	gs = None
	monTour = None
	numJoueur = None
	uf = None
	couleurs = None

