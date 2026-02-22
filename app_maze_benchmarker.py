#Programme réalisé par LIM Dany

########################################################################################################################

#Création de la fenêtre :

from time import*
from math import*
from tkinter import*
from random import*
fenetre=Tk()
fenetre.title("TNSI_LIM_Dany_Labyrinthe")
canevas=Canvas(fenetre,width=640,height=640,bg='#00D5FB')
canevas.place(x=25,y=55)
fenetre.config(width=1020, height=950, bg="#0063C4")

########################################################################################################################

#Importation des class nécessaires pour le projet :

class coord:
    def __init__(self, i, j):
        self.x = i
        self.y = j
    def __add__(self, other): return coord(self.x + other.x, self.y + other.y)
    def __sub__(self, other): return coord(self.x - other.x, self.y - other.y)
    def __mul__(self, other: int): return coord(self.x * other, self.y * other)
    def __eq__(self, other): return other!=None and (self.x == other.x and self.y == other.y)
    def __le__(self, other): return self.x <= other.x and self.y <= other.y
    def __lt__(self, other): return self.x < other.x and self.y < other.y
    def __str__(self): return "( " + str(self.x) + " ; " + str(self.y) + " ) "

class cellule:
    def __init__(self, position=coord(0,0), e = 0):
        self.pos = position
        self.mur = {'n': True, 'e': True, 's': True, 'w': True}
        self.etat = e
        self.des = {'c': None, 'n': None, 'e': None, 's': None, 'w': None}
        self.couleur = "black"
    def supp_mur(self, cell):
        position = news[str(self.pos - cell.pos)] # recherche de la direction
        m_opp = m_oppose[position]
        if cell.mur[position]:
             cell.mur[position] = False
             canevas.delete(cell.des[position])
             cell.des[position]= None
        if self.mur[m_opp]:
             self.mur[m_opp] = False
             canevas.delete(self.des[m_opp])
             self.des[m_opp] = None
    def dessine(self, d):
        Ax, Ay = self.pos.x, self.pos.y
        self.des['c'] = canevas.create_rectangle(d*Ax,d*Ay,d*Ax+d,d*Ay+d, fill=couleur_cellule[self.etat],width=1,outline = couleur_cellule[self.etat])
        for i in range(4):
            suiv = coord(Ax,Ay)+depl['nesw'[(i+1)%4]]
            if self.mur['nesw'[i]]: # Vérifie s’il y a un mur (True) dans la direction testée
                self.des['nesw'[i]] = canevas.create_line(d*Ax,d*Ay, d*suiv.x,d*suiv.y, fill=coul_mur,width=3)
                Ax,Ay = suiv.x, suiv.y
    def set_etat(self, e=1):
        self.etat = e
        canevas.itemconfig(self.des['c'], fill=couleur_cellule[self.etat],outline = couleur_cellule[self.etat],width=3)
    def set_couleur(self,couleur_cell,couleur_mur):
        "set_couleur est la méthode qui permet de changer la couleur des murs et de l'intérieur d'une cellule sans changer l'état de la cellule, qui prend donc en paramètre couleur_cell et couleur_mur, deux str"
        canevas.itemconfig(self.des['c'], fill=couleur_cell,width=3,outline = couleur_mur)
class labyrinthe:
    def __init__(self, t, d):
        self.taille = t # nombre de division
        self.dim = d # taille de chaque cellule1
        self.grille = [[cellule(coord(x,y)) for y in range(self.taille.y)] for x in range(self.taille.x)]
        self.entree = None # cellule d’entrée du labyrinthe
        self.sortie = None # cellule de sortie du labyrinthe

    def Voisine_O(self,cell):
        "Voisine_0 est la méthode qui prend en paramètre un objet de type cellule et qui permet de lui chercher une cellule voisine en vérifiant si l'état de la cellule voisine est 0,nécéssaire pour la création du labyrinthe en DFS"
        liste_cellules_voisines = []
        position_cellule = cell.pos
        #Pour tous les directions possibles (haut,bas,gauche,droite):
        for dep in Ldepl:
            position_voisin = position_cellule + coord(dep[0], dep[1])
            #On vérifie que son voisin possible est bien dans le labyrinthe et non à l'extérieur:
            if position_voisin >= coord(0,0) and position_voisin < coord(self.taille.x,self.taille.y):
                cellule_voisine = self.grille[position_voisin.x][position_voisin.y]
                #Si l'état de la cellule voisine est 0 cela veut dire que c'est une cellule voisine à la cellule visée à comptabiliser:
                if cellule_voisine.etat == 0:
                    liste_cellules_voisines.append(cellule_voisine)
        return liste_cellules_voisines
    def Recherche_Voisine_DFS(self,cell):
        "Recherche_Voisine_DFS est la méthode qui prend en paramètre un objet de type cellule et qui permet de lui chercher une cellule voisine en vérifiant si un mur les sépare,nécéssaire pour la recherche en DFS"
        liste_cellules_voisines_DFS = []
        position_cellule = cell.pos
        #Pour tous les directions possibles (haut,bas,gauche,droite):
        for dep in Ldepl:
            #position_voisin est un voisin éventuellement possible à la cellule
            position_voisin = position_cellule + coord(dep[0], dep[1])
            #On vérifie que son voisin possible est bien dans le labyrinthe et non à l'extérieur:
            if position_voisin >= coord(0, 0) and position_voisin < coord(self.taille.x, self.taille.y):
                cellule_voisine = self.grille[position_voisin.x][position_voisin.y]
                for i in range(4):
                    #Permet d'empecher que les cellules voisines avec un mur entre la cellule ciblée soient comptabilisées:
                    if Ldepl[i] == (dep[0], dep[1]):
                        #Si la cellule n'admet pas de mur vers le point cardinal donné cela veut dire que la cellule derrière le mur du point cardinal donné est une cellule voisine:
                        if cell.mur[direction_cardinaux[i]] == False:
                            liste_cellules_voisines_DFS.append(cellule_voisine)
        return liste_cellules_voisines_DFS

class Pile:
    def __init__(self):
        self.valeurs = []
    def est_vide(self):
        return self.valeurs == []
    def empile(self, valeur):
        self.valeurs.append(valeur)
    def depile(self):
        if self.valeurs: return self.valeurs.pop()
    def __str__(self):
        ch = ''
        for x in self.valeurs:
            ch = "| " + str(x) + " |" + "\n" + ch
        return ch + "⎺⎺⎺⎺⎺\n"

########################################################################################################################

def generation_grille():
    "generation_grille est la fonction qui permet de générer une grille de n*n cellules (qui servira de base pour la création du labyrinthe)"
    global lab, cellule_entree, cellule_sortie,n
    canevas.delete('all')
    n = int(entree_nbr_cellule_basique.get())
    #Mise à jour de l'interface
    texte_creer_labyrinthe_dfs.place(x=720, y=320)
    texte_recreer_grille.place(x=60, y=710)
    bouton_recreer_grille.place(x=75, y=780)
    texte_generation_grille.config(text="Grille du labyrinthe \ngénérée !")
    texte_labyrinthe.place(x=45 - ((645 % n) // 2))
    bouton_creer_labyrinthe_dfs.place(x=750, y=360)
    entree_nbr_cellule_basique.place_forget()
    bouton_valider_nbr_cellule_grille.place_forget()
    texte_creer_labyrinthe_dfs.config(text="Créer un labyrinthe")
    texte_nbr_secondes.place_forget()
    #La condition ci-dessous permet de limiter la taille du labyrinthe à 300x300:
    if n <= 300:
        lab = labyrinthe(coord(n, n), 20)
        for i in range(n):
            for j in range(n):
                lab.grille[i][j].dessine(645//n)
        #Je reconfig la taille du canevas pour que le labyrinthe rentre parfaitement dedans:
        canevas.config(width=640 - (645 % n), height=640 - (645 % n))
        texte_labyrinthe.place(x=45-((645%n)//2))
        #Par défaut, l'entrée est en 0,0 et la sortie en n-1,n-1:
        lab.entree = lab.grille[0][0]
        lab.sortie = lab.grille[n-1][n-1]
    else:
        print("Vous ne pouvez pas créer un labyrinthe de plus de 300x300 cellules !")

def generation_labyrinthe_methode_DFS():
    "generation_labyrinthe_methode_DFS est la fonction qui permet de générer un labyrinthe avec la méthode DFS"
    global labyrinthe_genere
    #bouton_creer_labyrinthe_dfs.place_forget() permet d'empecher la création de 2 labyrinthes en simultané
    bouton_creer_labyrinthe_dfs.place_forget()
    parcours = Pile()
    #Méthode DFS:
    parcours.empile(lab.grille[0][0])
    #On lance le chrono pour savoir le temps mis pour trouver un chemin
    temps_depart = time()
    while not parcours.est_vide():
        cellule_actuelle = parcours.depile()
        #cellule_actuelle.etat = cellule_actuelle.etat + 1 permet de rendre plus foncé la couleur des cellules en fonction de combien de fois on est déja passé sur cette cellule
        cellule_actuelle.etat = cellule_actuelle.etat + 1
        cellule_actuelle.set_etat(cellule_actuelle.etat)
        liste_voisine = lab.Voisine_O(cellule_actuelle)
        if liste_voisine != [] :
            prochaine_cellule = choice(liste_voisine)
            cellule_actuelle.supp_mur(prochaine_cellule)
            parcours.empile(cellule_actuelle)
            parcours.empile(prochaine_cellule)
            fenetre.update()
        else:
            #La condition ci-desosus permet implicitement de vérifier si la grille a déja été crée car si cela n'avait pas été le cas, lab.entree et lab.sortie serait égal à None :
            if lab.entree != None and lab.sortie != None:
                #Affichage de la cellule d'entrée:
                cellule_entree = lab.grille[0][0]
                cellule_entree.set_couleur("#22427C","#22427C")
                #Affichage de la cellule de sortie:
                cellule_sortie = lab.grille[n - 1][n - 1]
                cellule_sortie.set_couleur("#22427C","#22427C")
                #Mise à jour de l'interface:
                texte_replacer_entree_sortie.place(x=400, y=710)
                bouton_replacer_entree_sortie.place(x=410, y=780)
    #On sort de la boucle donc la recherche est finie : fin du chrono
    temps_fin = time()
    #Différence entre le temps de départ et le temps de fin pour avoir le temps écoulé:
    temps_ecoule = temps_fin - temps_depart
    print("Labyrinthe complètement généré, vous pouvez placer désormais placer une entrée et une sortie.")
    #Le labyrinthe vient d'être généré donc True, cela servira lorsque l'utilisateur voudra placer une entrée et une sortie, on vérifira alors que le labyrinthe a bien été généré
    labyrinthe_genere = True
    #Mise à jour de l'interface:
    texte_nbr_secondes.config(text="Le labyrinthe a été généré en " + str(temps_ecoule) + "s \nvia la méthode de génération DFS !")
    texte_nbr_secondes.place(x=100, y=850)
    texte_creer_labyrinthe_dfs.place(x=700, y=320)
    texte_creer_labyrinthe_dfs.config(text="Labyrinthe complètement généré !\n Vous pouvez placer une entrée \net une sortie ! (bleu foncé)",font=('Courier',11,""))
    #Je config les boutons qui servent à rechercher un chemin avec leur fonction attitré,cela évite que l'utilisateur puisse rechercher un chemin alors que le labyrinthe n'est pas bien généré;
    #ce qui causerait des problèmes
    bouton_recherche_methode_main_droite.config(command = recherche_methode_main_droite)
    bouton_recherche_methode_DFS.config(command=recherche_methode_DFS)
    bouton_recherche_methode_Dijkstra.config(command = recherche_methode_dijkstra)

########################################################################################################################

#Création des fonctions pour gérer le clic de l'utilisateur, placer des entrées et sorties et récréer la grille

def gestion_clic(event):
    "gestion_clic est la fonction qui permet de placer une nouvelle entrée et une nouvelle sortie dans le labyrinthe qui prend en paramètre un event,le clic de l'utilisateur"
    global cellule_entree, cellule_sortie,sortie_placee,entree_placee
    #Je recupère la position du clic de l'utilisateur
    x,y = event.x, event.y
    #Mon Canevas fait du 640 par 640 donc la taille d'une cellule est égale à la longueur du coté de mon Canevas divisé par le nombre de cellules n présente sur ce côté:
    n = int(entree_nbr_cellule_basique.get())
    taille_cellule = 640 // n
    i,j = x // taille_cellule, y // taille_cellule
    #Condition qui vérifie d'abord si le labyrinthe a bien été généré:
    if labyrinthe_genere == True:
        #Toutes ces conditions servent à faire en sorte que lorsque l'utilisateur replace ses entrées et sorties,la cellule qui était anciennement l'entrée/la sortie ait une couleur correspondante au type de recherche effectuée
        if entree_placee == False and recherche_main_droite == True :
            ##22427C correspond au bleu foncé (sortie et entrée)
            ##77B5FE correspond à la couleur bleu ciel lors de la recherche main droite
            lab.entree.set_couleur("#77B5FE","#77B5FE")
            lab.entree = lab.grille[i][j]
            lab.grille[i][j].set_couleur("#22427C","#22427C")
            entree_placee = True
        elif sortie_placee == False and recherche_main_droite == True:
            lab.sortie.set_couleur("#77B5FE","#77B5FE")
            lab.sortie = lab.grille[i][j]
            lab.grille[i][j].set_couleur("#22427C","#22427C")
            sortie_placee = True

        elif entree_placee == False and recherche_DFS == True:
            #green correspond à la couleur verte lors de la recherche DFS
            lab.entree.set_couleur("green", "green")
            lab.entree = lab.grille[i][j]
            lab.grille[i][j].set_couleur("#22427C","#22427C")
            entree_placee = True
        elif sortie_placee == False and recherche_DFS == True:
            lab.sortie.set_couleur("green", "green")
            lab.sortie = lab.grille[i][j]
            lab.grille[i][j].set_couleur("#22427C","#22427C")
            sortie_placee = True

        elif entree_placee == False and recherche_DFS == False and recherche_main_droite == False and recherche_dijkstra == False:
            ##6ACDE5 correspond à la couleur bleu clair des cellules du labyrinthe initialement crée
            lab.entree.set_couleur("#6ACDE5", "#6ACDE5")
            lab.entree = lab.grille[i][j]
            lab.grille[i][j].set_couleur("#22427C", "#22427C")
            entree_placee = True
        elif sortie_placee == False and recherche_DFS == False and recherche_main_droite == False and recherche_dijkstra == False:
            lab.sortie.set_couleur("#6ACDE5", "#6ACDE5")
            lab.sortie = lab.grille[i][j]
            lab.grille[i][j].set_couleur("#22427C", "#22427C")
            sortie_placee = True

        elif entree_placee == False and recherche_dijkstra == True:
            ##8A2BE2 correspond à la couleur violet lors de la recherche Dijkstra
            lab.entree.set_couleur("#8A2BE2", "#8A2BE2")
            lab.entree = lab.grille[i][j]
            lab.grille[i][j].set_couleur("#22427C", "#22427C")
            entree_placee = True
        elif sortie_placee == False and recherche_dijkstra == True:
            lab.sortie.set_couleur("#8A2BE2", "#8A2BE2")
            lab.sortie = lab.grille[i][j]
            lab.grille[i][j].set_couleur("#22427C", "#22427C")
            sortie_placee = True

        #La condition ci-dessous empêche l'utilisateur de poser plus d'une entrée et sortie
        if entree_placee == True and sortie_placee == True:
            print("L'entrée et la sortie ont été placé ! ")
            texte_replacer_entree_sortie.place(x=400, y=710)
            bouton_replacer_entree_sortie.place(x=410, y=780)

canevas.bind('<Button-1>', gestion_clic)

def replacer_entree_sortie():
    "replacer_entree_sortie est la fonction qui permet de replacer une nouvelle entrée et une nouvelle sortie dans le labyrinthe"
    global entree_placee,sortie_placee
    nouvelle_entree = lab.entree
    nouvelle_sortie = lab.sortie
    #Les conditions ci-dessous servent à recolorier les nouvelles entrées/sorties en bleu foncé
    if recherche_main_droite == True:
        nouvelle_entree.set_couleur("#22427C","#22427C")
        nouvelle_sortie.set_couleur("#22427C","#22427C")
    elif recherche_DFS == True:
        nouvelle_sortie.set_couleur("#22427C","#22427C")
        nouvelle_entree.set_couleur("#22427C", "#22427C")
    elif recherche_dijkstra == True:
        nouvelle_sortie.set_couleur("#22427C", "#22427C")
        nouvelle_entree.set_couleur("#22427C", "#22427C")
    entree_placee = False
    sortie_placee = False
    print("Vous pouvez désormais placer une nouvelle entrée et une nouvelle sortie.")



def recreer_grille():
    "recreer_grille est la fonction qui permet de regénérer une nouvelle grille pour le labyrinthe"
    global labyrinthe_genere
    #Mise à jour de l'interface:
    canevas.delete('all')
    texte_generation_grille.place(x=715, y=120)
    entree_nbr_cellule_basique.place(x=770, y=180)
    bouton_valider_nbr_cellule_grille.place(x=750, y=210)
    texte_recreer_grille.place_forget()
    bouton_recreer_grille.place_forget()
    bouton_replacer_entree_sortie.place_forget()
    texte_replacer_entree_sortie.place_forget()
    texte_nbr_secondes.place_forget()
    texte_creer_labyrinthe_dfs.config(text="Créer un labyrinthe",font = ("Courier",15,""))
    texte_creer_labyrinthe_dfs.place(x=720,y=320)
    texte_generation_grille.config(text = "Générer une grille \nde nxn cellules",font = ("Courier",15,""))
    #Initialisation à false puisque le labyrinthe vient d'être supprimé
    labyrinthe_genere = False
    #On enlève la possibilité pour l'utilisateur d'utiliser les méthodes de recherche lorsque le labyrinthe est supprimé pour éviter les problèmes :
    bouton_recherche_methode_Dijkstra.config(command = "")
    bouton_recherche_methode_DFS.config(command = "")
    bouton_recherche_methode_main_droite.config(command = "")

########################################################################################################################

#Création des fonctions de recherche de chemin demandés

def recherche_methode_main_droite():
    "recherche_methode_main_droite est la fonction qui permet de parcourir le labyrinthe en suivant le bord droit (main droite)"
    global recherche_main_droite,recherche_DFS,recherche_dijkstra
    #Mise à jour de l'interface:
    bouton_recreer_grille.place_forget()
    bouton_replacer_entree_sortie.place_forget()
    texte_nbr_secondes.place_forget()
    n = int(entree_nbr_cellule_basique.get())
    #Pour y voir plus clair lors du parcours,on reset la couleur des cellules mais pas leurs murs pour garder les murs supprimés du labyrinthe intacts:
    for i in range(n):
        for j in range(n):
            lab.grille[i][j].set_etat(0)
            lab.grille[i][j].set_couleur("light blue","light blue")
            lab.grille[2][2].set_couleur("light blue","light blue")
    #On lance le chrono pour savoir le temps mis pour trouver un chemin
    temps_depart = time()
    #Méthode main droite:
    cellule_actuelle = lab.entree
    cellule_actuelle.set_etat(2)
    cellule_actuelle.set_couleur("#77B5FE","#77B5FE")
    cellule_sortie = lab.sortie
    #On choisit le nord comme direction de base
    direction = "n"
    while cellule_actuelle.pos != cellule_sortie.pos:
        x, y = cellule_actuelle.pos.x, cellule_actuelle.pos.y
        #La condition ci-desosus permet de vérifier si la cellule a un mur dans la direction donnée :
        if cellule_actuelle.mur[direction] == False :
            fenetre.update()
            #On va chercher la cellule voisine qui se trouve après le mur:
            prochaine_cellule = lab.grille[x + mouvement_cardinaux[direction][0]][y + mouvement_cardinaux[direction][1]]
            #On change son état et sa couleur:
            prochaine_cellule.set_etat(2)
            prochaine_cellule.set_couleur("#77B5FE","#77B5FE")
            #Et on avance petit à petit dans le labyrinthe grâce à l'égalité ci-dessous :
            cellule_actuelle = prochaine_cellule
            fenetre.update()
            #La condition ci-dessous vérifie que l'on peut tourner sur la droite (sens horaire):
            if prochaine_cellule.mur[sens_horaire[direction]] == False:
                #Le sens horaire sur la droite:
                direction = sens_horaire[direction]
        else:
            #Le sens anti horaire pour suivre le coté droit:
            direction = sens_anti_horaire[direction]
    #On sort de la boucle donc la recherche est finie : fin du chrono
    temps_fin = time()
    #Différence entre le temps de départ et le temps de fin pour avoir le temps écoulé:
    temps_ecoule = temps_fin - temps_depart
    #Initialisation des variables boolénnes à False/True et mise à jour de l'interface:
    recherche_DFS = False
    recherche_main_droite = True
    recherche_dijkstra = False
    bouton_recreer_grille.place(x=75, y=780)
    bouton_replacer_entree_sortie.place(x=410, y=780)
    print("Recherche Main Droite terminée en "+str(temps_ecoule)+"s !")
    texte_nbr_secondes.place_forget()
    texte_nbr_secondes.config(text="Le chemin a été généré en " + str(temps_ecoule) + "s \nvia la méthode de recherche de la Main Droite !")
    texte_nbr_secondes.place(x=100, y=850)



def recherche_methode_DFS():
    "recherche_methode_DFS est la fonction qui permet de parcourir le labyrinthe via l'algorithme DFS"
    global recherche_DFS,recherche_main_droite,recherche_dijkstra
    #Mise à jour de l'interface:
    bouton_recreer_grille.place_forget()
    bouton_replacer_entree_sortie.place_forget()
    texte_nbr_secondes.place_forget()
    n = int(entree_nbr_cellule_basique.get())
    #Pour y voir plus clair lors du parcours,on reset la couleur des cellules mais pas leurs murs pour garder les murs supprimés du labyrinthe intacts:
    for i in range(n):
        for j in range(n):
            lab.grille[i][j].set_etat(0)
            lab.grille[i][j].set_couleur("light blue","light blue")
            lab.grille[2][2].set_couleur("light blue","light blue")
    #On lance le chrono pour savoir le temps mis pour trouver un chemin
    temps_depart = time()
    parcours = Pile()
    #Méthode DFS:
    parcours.empile(lab.entree)
    while not parcours.est_vide():
        cellule_actuelle = parcours.depile()
        cellule_actuelle.set_couleur("orange","orange")
        liste_voisine = lab.Recherche_Voisine_DFS(cellule_actuelle)
        if cellule_actuelle == lab.sortie:
            while not parcours.est_vide():
                fenetre.update()
                lab.sortie.set_couleur("green","green")
                cellule_actuelle = parcours.depile()
                cellule_actuelle.set_couleur("green","green")
                if cellule_actuelle == lab.entree:
                    #La cellule actuelle est égale à la cellule d'entrée : la recherche est finie donc fin du chrono
                    temps_fin = time()
                    # Différence entre le temps de départ et le temps de fin pour avoir le temps écoulé:
                    temps_ecoule = temps_fin - temps_depart
                    # Initialisation des variables boolénnes à False/True et mise à jour de l'interface:
                    print("Recherche DFS terminée en "+str(temps_ecoule)+"s !")
                    texte_nbr_secondes.place_forget()
                    texte_nbr_secondes.config(text="Le chemin a été généré en " + str(temps_ecoule) + "s \nvia la méthode de recherche DFS !")
                    texte_nbr_secondes.place(x=100, y=850)
                    bouton_recreer_grille.place(x=75, y=780)
                    bouton_replacer_entree_sortie.place(x=410, y=780)
                    recherche_DFS = True
                    recherche_main_droite = False
                    recherche_dijkstra = False
                    #Le return permet d'arrêter la fonction une fois que la recherche DFS est terminée:
                    return None
        if liste_voisine != []:
            prochaine_cellule = choice(liste_voisine)
            parcours.empile(cellule_actuelle)
            parcours.empile(prochaine_cellule)
            fenetre.update()



def creation_reseau(R):
    "creation_reseau est la fonction qui permet de créer un réseau à partir du labyrinthe, qui prend en paramètre un dico et retourne le dico sous la forme d'un réseau (R1 : R2 , pas)"
    n = int(entree_nbr_cellule_basique.get())
    #On parcourt toutes les lignes et colonnes du labyrinthe:
    for i in range(n):
        for j in range(n):
            cellule = lab.grille[i][j]
            #Pour chaque cellule,on regarde ses cellules voisines (qui n'ont pas de mur entre la cellule actuelle et la cellule voisine)
            voisines = lab.Recherche_Voisine_DFS(cellule)
            #distance_voisine est donc une des cellules voisines et lui est associé un pas:
            distance_voisine = [(v, 1) for v in voisines]
            #Pour la clé de réseau l'une de ses cellules voisines intégrée dans le dico:
            R[cellule] = distance_voisine
    return R

def minimum(dico):
    "minimum est la fonction qui retourne la cellule au nombre de pas minimum d'un sommet à un autre, elle prend en paramètre un dico"
    #Code vu et donné en classe:
    mini, s = inf, -1
    for clef in dico:
        if dico[clef] < mini:
            s = clef
            mini = dico[clef]
    return s

def dijkstra(G,s):
    "dijkstra est la fonction qui permet de trouver le chemin le plus court entre un sommet s et tous les autres sommets du réseau"
    "qui prend en paramètre G qui est un dico sous forme de réseau et s qui est un sommet du réseau"
    #Code vu et donné en classe:
    D , d = {}, {clef : inf for clef in G} # tab des distances minimales, initiales
    d[s] = 0 # s: sommets
    while len(d) > 0 : # c'est fini lorsque d est vide
        k = minimum(d)
        for j in range(len(G[k])): # on regarde les voisins de k
            v, c = G[k][j] # v est le voisin, c le cout
            if v not in D : d[v]=min(d[v],d[k]+c)
        D[k] = d[k] # on copie le sommet et la distance dans D
        del d[k]
    return D



def recherche_methode_dijkstra():
    "recherche_methode_dijkstra est la fonction qui permet de parcourir le labyrinthe via l'algorithme de Dijkstra"
    global recherche_DFS,recherche_main_droite,recherche_dijkstra,reseau
    texte_nbr_secondes.place_forget()
    #On initialise le réseau en tant que dico vide:
    reseau = {}
    #resultats_dijkstra est le dico qui stock les chemins les plus courts entre la sortie (lab.sortie) et toutes les autres cellules du labyrinthe:
    resultats_dijkstra = dijkstra(creation_reseau(reseau), lab.sortie)
    #On lance le chrono pour savoir le temps mis pour trouver un chemin
    temps_depart = time()
    #On parcourt le labyrinthe grâce au dico resultats_dijkstra qui contient des objets de type cellule et leur pas par rapport à la sortie:
    for cellule, distance in resultats_dijkstra.items():
        fenetre.update()
        #L'aller de la recherche Dijkstra est marqué par la couleur rouge:
        cellule.set_couleur("red","red")
    #On démarre à la cellule d'entrée:
    cellule_actuelle = lab.entree
    #chemin_plus_court est la liste qui va contenir les objets de type cellule qui forment le chemin le plus court jusqu'à la sortie (lab.sortie)
    chemin_plus_court = []
    chemin_plus_court.append(cellule_actuelle)
    while cellule_actuelle != lab.sortie:
        #voisin_min_distance est la variable qui va contenir la cellule voisine qui est à la distance minimale de la cellule actuelle
        voisin_min_distance = None
        #Initialisation à l'infini comme dans la recherche Dijkstra vu en classe:
        min_distance = inf
        for voisin in lab.Recherche_Voisine_DFS(cellule_actuelle):
            #La condition ci-dessous vérifie que la distance entre le voisin et la cellule actuelle est plus petite que min_distance:
            if voisin in resultats_dijkstra and resultats_dijkstra[voisin] < min_distance:
                #On met à jour les distances et leur voisin à distance minimale:
                voisin_min_distance = voisin
                min_distance = resultats_dijkstra[voisin]
        #Le chemin le plus court se forme dans la liste petit à petit:
        chemin_plus_court.append(voisin_min_distance)
        #On avance dans le labyrinthe avec cette égalité:
        cellule_actuelle = voisin_min_distance
    #Le retour de la recherche Dijkstra est marqué par la couleur violet,on affiche le chemin le plus court en violet:
    for cellule in chemin_plus_court:
        fenetre.update()
        cellule.set_couleur("#8A2BE2", "#8A2BE2")
    #On sort de la boucle : donc fin du chrono
    temps_fin = time()
    #Différence entre le temps de départ et le temps de fin pour avoir le temps écoulé:
    temps_ecoule = temps_fin - temps_depart
    #Initialisation des variables boolénnes à False/True et mise à jour de l'interface:
    recherche_dijkstra = True
    recherche_DFS = False
    recherche_main_droite = False
    print("Recherche Dijkstra terminée en "+str(temps_ecoule)+"s !")
    texte_nbr_secondes.place_forget()
    texte_nbr_secondes.config(text = "Le chemin a été généré en "+str(temps_ecoule)+"s \nvia la méthode de recherche Dijkstra !")
    texte_nbr_secondes.place(x=100,y=850)


########################################################################################################################

#Création de toutes les variables booléennes, initialement égales à False :
#Ces variables servent à faire en sorte que lorsque l'utilisateur replace ses entrées et sorties,la cellule qui était anciennement l'entrée/la sortie ait une couleur correspondante au type de recherche effectuée

labyrinthe_genere = False
sortie_placee = False
entree_placee = False
recherche_main_droite = False
recherche_DFS = False
recherche_dijkstra = False

########################################################################################################################

#Création / Importation des dictionnaires nécessaires pour le parcours du labyrinthe :

depl = {'n': coord(0, -1), 'e': coord(1,0), 's': coord(0,1), 'w': coord(-1,0)}
Ldepl = [(0, -1),(1,0),(0,1), (-1,0)]
news = {}
for k,v in depl.items(): news[str(v)] = k
m_oppose = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}

#bleu clair au bleu plus foncé
couleur_cellule = ["#C1E9FC","#95DAEE","#6ACDE5","#00B6D3","#0085BD"]

coul_mur = "white"  # Couleur des murs

sens_horaire = {'n': 'e', 'e': 's', 's': 'w', 'w': 'n'}
sens_anti_horaire = {'n': 'w','e': 'n','s': 'e','w':'s'}
mouvement_cardinaux = {'n' : [0,-1],'e' : [1,0],'s' : [0,1], 'w' : [-1,0]}
direction_cardinaux = ['n','e','s','w']


########################################################################################################################

#Création des boutons et textes pour l'interface:

texte_labyrinthe = Label(fenetre,text = "Génération de labyrinthe",font = ("Courier",31,"underline"),fg="white",bg ='#009DE4')

texte_grille = Label(fenetre,text = "Génération d'une \ngrille",font = ("Courier",22,"underline"),fg="white",bg ='#009DE4')

texte_generation_grille = Label(fenetre,text = "Générer une grille \nde nxn cellules",font = ("Courier",15,""),fg="white",bg ='#009DE4')

bouton_valider_nbr_cellule_grille = Button(fenetre,text = "Valider",font=("Courier",15,""),bg='#009DE4',fg="white",height=1,width=14,command = generation_grille)

entree_nbr_cellule_basique = Entry(fenetre,font=("",12,""),width=15)

texte_methode_generation_dfs= Label(fenetre,text = "Méthode DFS",font = ("Courier",25,"underline"),fg="white",bg ='#009DE4')

texte_creer_labyrinthe_dfs = Label(fenetre,text = "Créer un labyrinthe",font = ("Courier",15,""),fg="white",bg ='#009DE4')

bouton_creer_labyrinthe_dfs = Button(fenetre,text = "Créer",font=("Courier",15,""),bg='#009DE4',fg="white",height=1,width=14,command = generation_labyrinthe_methode_DFS)

texte_recherche_methode_main_droite= Label(fenetre,text = "Recherche Main Droite",font = ("Courier",18,"underline"),fg="white",bg ='#009DE4')

texte_recherche_main_droite = Label(fenetre,text = "Rechercher un chemin via la\n méthode de la main droite",font = ("Courier",13,""),fg="white",bg ='#009DE4')

bouton_recherche_methode_main_droite = Button(fenetre,text = "Rechercher",font=("Courier",15,""),bg='#009DE4',fg="white",height=1,width=14)

texte_replacer_entree_sortie = Label(fenetre,text = "Replacer l'entrée\net la sortie !",font = ("Courier",15,""),fg="white",bg ='#009DE4')

bouton_replacer_entree_sortie = Button(fenetre,text = "Replacer",font=("Courier",15,""),bg='#009DE4',fg="white",height=1,width=15,command = replacer_entree_sortie)

texte_recreer_grille = Label(fenetre,text = "Regénérer une grille \nde nxn cellules",font = ("Courier",15,""),fg="white",bg ='#009DE4')

bouton_recreer_grille = Button(fenetre,text = "Recréer",font=("Courier",15,""),bg='#009DE4',fg="white",height=1,width=18,command = recreer_grille)

texte_recherche_methode_DFS = Label(fenetre,text = "Recherche DFS",font = ("Courier",25,"underline"),fg="white",bg ='#009DE4')

texte_recherche_DFS = Label(fenetre,text = "Rechercher un chemin \nvia la méthode DFS",font = ("Courier",13,""),fg="white",bg ='#009DE4')

bouton_recherche_methode_DFS = Button(fenetre,text = "Rechercher",font=("Courier",15,""),bg='#009DE4',fg="white",height=1,width=14)

texte_recherche_methode_Dijkstra = Label(fenetre,text = "Recherche Dijkstra",font = ("Courier",21,"underline"),fg="white",bg ='#009DE4')

texte_recherche_Dijkstra = Label(fenetre,text = "Rechercher un chemin \nvia la méthode Dijkstra",font = ("Courier",13,""),fg="white",bg ='#009DE4')

bouton_recherche_methode_Dijkstra = Button(fenetre,text = "Rechercher",font=("Courier",15,""),bg='#009DE4',fg="white",height=1,width=14)

texte_nbr_secondes = Label(fenetre,font = ("Courier",13,""),fg="white",bg ='#009DE4')
########################################################################################################################

#Mise en place de la fenêtre pour créer les labyrinthes :

texte_labyrinthe.place(x=45,y=10)
texte_grille.place(x=695,y=30)
texte_generation_grille.place(x=715,y=120)
entree_nbr_cellule_basique.place(x=770,y=180)
bouton_valider_nbr_cellule_grille.place(x=750,y=210)
texte_methode_generation_dfs.place(x=725,y=270)
texte_creer_labyrinthe_dfs.place(x=720,y=320)
bouton_creer_labyrinthe_dfs.place(x=750,y=360)
texte_recherche_methode_main_droite.place(x=695,y=420)
texte_recherche_main_droite.place(x=710,y=470)
bouton_recherche_methode_main_droite.place(x=750,y=530)
texte_recherche_methode_DFS.place(x=710,y=595)
texte_recherche_DFS.place(x=730,y=645)
bouton_recherche_methode_DFS.place(x=750,y=705)
texte_recherche_methode_Dijkstra.place(x=700,y=765)
texte_recherche_Dijkstra.place(x=730,y=815)
bouton_recherche_methode_Dijkstra.place(x=750,y=875)

########################################################################################################################

fenetre.mainloop()