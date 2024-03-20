import pyxel, random

class App:
    def __init__(self, WIDTH=144, HEIGHT=144):
        pyxel.init(WIDTH, HEIGHT, "RPG",  display_scale=4)
        pyxel.load("res.pyxres")
        
        #Affichage
        self.player_x=64
        self.player_y=64
        self.map_x = 0
        self.map_y = 0
        self.curseur=[0, 0]
        self.curseur_menu = 0
        self.curseur_sort = 0
        self.direction = "left"
        
        #Monstres
        self.necromancien = Monstre(80, 10, 20, 16, 48, 20)
        self.masque = Monstre(60, 20, 30, 16, 0, 20)
        self.rencontres = [self.necromancien, self.masque]
          
        
        #Interne
        self.tour = True
        self.PV_ennemi = 60
        self.solide=[(4,0), (4,1), (5,0), (5,1), (6,0), (6,1), (7,0), (7,1), (8,0), (8,1), (9,0), (9,1), (4,2), (5,2), (4,3), (5,3), (6,2), (6,3), (7,2), (7,3)]
        self.state="Titre" #peut etre Gameplay, Dialogue, Combat ou Titre
        self.animation_combat = {"tranche":0, "feu":0, "glace":0}
        self.menu_sort = False
        
        #sorts
        self.feu = Sort("feu", self.PV_ennemi, 30, 5, 48, 0)
        
        #Stats
        self.stats = {"PV_max":60, "MP_max":40, "Att":20, "Def":10, "Mag":20}
        self.PV = self.stats["PV_max"]
        self.MP = self.stats["MP_max"]
        self.sorts = [self.feu]
        
        pyxel.run(self.update, self.draw)
        
    
    #Interne
    
    def mouvement(self):
        """Permet le déplacement du personnage a l'aide des flèches directionelles, changeant la
        direction dans laquelle il regarde, et en fonction de sa position et si il n'y a aucun
        obstacle, déplace soit lui soit la carte, avant de lancer une potentiel rencontre de monstre"""
        if pyxel.btnp(pyxel.KEY_UP) and self.player_y > 0: 
                self.direction = "up"
                if pyxel.tilemaps[0].pget((self.player_x+ self.map_x)//8 , (self.player_y+ self.map_y) //8  -1) not in self.solide :
                    if self.player_y > 32:
                        self.player_y -= 16
                    else:
                        self.map_y -= 16
                    self.rencontre_aleatoire()
                    
        if pyxel.btnp(pyxel.KEY_DOWN) and self.player_y < 128 :
                self.direction = "down"
                if pyxel.tilemaps[0].pget((self.player_x+ self.map_x )//8, (self.player_y+ self.map_y+17)//8 ) not in self.solide :
                    if self.player_y < 96:
                        self.player_y += 16
                    else:
                        self.map_y += 16
                    self.rencontre_aleatoire()
                
        if pyxel.btnp(pyxel.KEY_LEFT) and self.player_x > 0 :
                self.direction = "left"
                if pyxel.tilemaps[0].pget((self.player_x+ self.map_x) //8 -1, (self.player_y+ self.map_y )//8) not in self.solide :
                    if self.player_x > 32:
                        self.player_x -=16
                    else:
                        self.map_x -= 16
                    self.rencontre_aleatoire()
                
        if pyxel.btnp(pyxel.KEY_RIGHT) and self.player_x < 128 :
                self.direction = "right"
                if pyxel.tilemaps[0].pget((self.player_x+17+ self.map_x) //8 , (self.player_y+ self.map_y)//8 ) not in self.solide:
                    if self.player_x < 96:
                        self.player_x += 16
                    else:
                        self.map_x += 16
                    self.rencontre_aleatoire()

    def dep_curseur_menu(self):
        """Permet le déplacement du curseur dans le menu de la carte"""
        if pyxel.btnp(pyxel.KEY_DOWN):
            if self.curseur_menu == 4:
                self.curseur_menu = 0
                pyxel.play(0, 0)
            else :
                self.curseur_menu += 1
                pyxel.play(0, 0)
        if pyxel.btnp(pyxel.KEY_UP):
            if self.curseur_menu == 0:
                self.curseur_menu = 4
                pyxel.play(0, 0)
            else :
                self.curseur_menu -= 1
                pyxel.play(0, 0)
    
    def dep_curseur_combat(self):
        """permet le déplacement du curseur en combat"""
        if pyxel.btnp(pyxel.KEY_UP) and  self.curseur[0] > 0:
            self.curseur[0]-=1
            pyxel.play(0, 0)
        if pyxel.btnp(pyxel.KEY_DOWN) and  self.curseur[0] < 1:
            self.curseur[0]+=1
            pyxel.play(0, 0)
        if pyxel.btnp(pyxel.KEY_LEFT) and  self.curseur[1] > 0:
            self.curseur[1]-=1
            pyxel.play(0, 0)
        if pyxel.btnp(pyxel.KEY_RIGHT) and  self.curseur[1] < 1:
            self.curseur[1]+=1
            pyxel.play(0, 0)

    def rencontre_aleatoire(self):
        """1 chance sur 15 de déclencher un combat, puis choisit un monstre au hasard dans la table
        de rencontres"""
        if random.randint(1,15) == 1:
            self.new_ms = self.rencontres[random.randint(0,len(self.rencontres)-1)]
            self.PV_ennemi = self.new_ms.msPV
            self.state = "Combat"
            
    def test_animation(self, dicanim):
        """Renvoie True si aucune animation de la catégorie donnée est en cours, et False sinon"""
        for anim in dicanim:
            if dicanim[anim] > 0:
                return False
        return True
            
     
     
     
    #Dessin   
            
    def dessin_menu(self):
        """Dessin du menu de l'overworld"""
        pyxel.rect(104, 0, 40, 54, 7)
        pyxel.rect(106, 2, 36, 50, 0)
        if self.curseur_menu == 0:
            pyxel.text(116, 5, "Statut", 3)
        if self.curseur_menu == 1:
            pyxel.text(116, 15, "Objets", 3)
        if self.curseur_menu == 2:
            pyxel.text(116, 25, "Sorts", 3)
        if self.curseur_menu == 3:
            pyxel.text(116, 35, "Equip.", 3)
        if self.curseur_menu == 4:
            pyxel.text(116, 45, "Sauv.", 3)
        
        pyxel.text(115, 4, "Statut", 7)
        pyxel.text(115, 14, "Objets", 7)
        pyxel.text(115, 24, "Sorts", 7)
        pyxel.text(115, 34, "Equip.", 7)
        pyxel.text(115, 44, "Sauv.", 7)
        
    def dessin_menu_sort(self, orx, ory):
        pyxel.rect(orx, ory, 40, 36, 7)
        pyxel.rect(orx+2, ory+2, 36, 32, 0)
        
    
    def dessin_monde(self):
        """Dessin de la carte de jeu"""
        pyxel.bltm(0,0, 0, self.map_x, self.map_y, 144, 144)
        self.dessin_joueur()
          #pyxel.blt(0, 144-31, 2, 0, 0, 32, 32)

    def dessin_joueur(self):
        """Dessine le joueur en fonction de sa position et sa direction"""
        if self.direction == "up":
            pyxel.blt(self.player_x, self.player_y, 0, 0, 16, 16, 16, 13)
        if self.direction == "down":
            pyxel.blt(self.player_x, self.player_y, 0, 0, 32, 16, 16, 13)
        if self.direction == "left":
            pyxel.blt(self.player_x, self.player_y, 0, 0, 0, 16, 16, 13)
        if self.direction == "right":
            pyxel.blt(self.player_x, self.player_y, 0, 0, 48, 16, 16, 13)
            
    
    def dessin_combat(self):
        """Dessine la fenêtre de combat"""
        pyxel.rectb(1,113, 142,30, 7)
        pyxel.rectb(2,114, 140,28, 7)
        pyxel.text(90, 119, "PV", 7)
        pyxel.text(90, 134, "MP", 7)

        if self.curseur == [0,0]:
            pyxel.blt(3, 118, 1, 0,0, 8,8, 0)
            pyxel.text(11, 120, "Attaque", 3)
        elif self.curseur == [1,0]:
            pyxel.blt(3, 133, 1, 0,0, 8,8, 0)
            pyxel.text(11, 135, "Sort", 3)
        elif self.curseur == [0,1]:
            pyxel.blt(43, 118, 1, 0,0, 8,8, 0)
            pyxel.text(51, 120, "Objets", 3)
        elif self.curseur == [1,1]:
            pyxel.blt(43, 133, 1, 0,0, 8,8, 0)
            pyxel.text(51, 135, "Fuite",3)
            
        pyxel.text(10, 119, "Attaque", 7)
        pyxel.text(10, 134, "Sort", 7)
        pyxel.text(50, 119, "Objets", 7)
        pyxel.text(50, 134, "Fuite",7)
        pyxel.rect(100, 119, 30, 3, 11)
        pyxel.rect(100, 134, 30, 3, 5)
        pyxel.text(133, 119, str(self.PV), 7)
        pyxel.text(133, 134, str(self.MP), 7)
        pyxel.blt(50, 50, 1, self.new_ms.orix, self.new_ms.oriy, 32, 40, 0)
        self.dessin_barre(100, 119, self.PV, self.stats["PV_max"], 8)
        self.dessin_barre(100, 134, self.MP, self.stats["MP_max"], 1)
        #pyxel.text(45, 50, str(self.PV_ennemi), 7)
        
        if self.menu_sort == True:
            self.dessin_menu_sort(103,75)
        
        
    def dessin_barre(self, orx, ory, stat, statmax, col):
        """Permet de dessiner une barre qui descend de 30 pixel de long"""
        if stat == statmax:
            pass
        elif (stat*100)/statmax >90:
            pyxel.rect(orx+27, ory, 3, 3, col)
        elif (stat*100)/statmax >80:
            pyxel.rect(orx+24, ory, 6, 3, col)
        elif (stat*100)/statmax >70:
            pyxel.rect(orx+21, ory, 9, 3, col)
        elif (stat*100)/statmax >60:
            pyxel.rect(orx+18, ory, 12, 3, col)
        elif (stat*100)/statmax >50:
            pyxel.rect(orx+15, ory, 15, 3, col)
        elif (stat*100)/statmax >40:
            pyxel.rect(orx+12, ory, 18, 3, col)
        elif (stat*100)/statmax >30:
            pyxel.rect(orx+9, ory, 21, 3, col)
        elif (stat*100)/statmax >20:
            pyxel.rect(orx+6, ory, 24, 3, col)
        elif (stat*100)/statmax >10:
            pyxel.rect(orx+3, ory, 27, 3, col)
        elif (stat*100)/statmax > 0:
            pyxel.rect(orx+1, ory, 29, 3, col)
        elif (stat*100)/statmax <= 0:
            pyxel.rect(orx, ory, 30, 3, col)
    

    
    #UPDATE&DRAW
    def update(self):
        if self.state == "Titre":
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.state = "Gameplay"
        
        
        if self.state == "Gameplay":
            self.mouvement()
            if pyxel.btnp(pyxel.KEY_TAB):
                self.state = "Menu"

            
        elif self.state == "Combat":
            if self.PV_ennemi <= 0 and self.test_animation(self.animation_combat):
                self.state = "Gameplay"
                
            if self.tour and self.test_animation(self.animation_combat):
                self.dep_curseur_combat()
                if pyxel.btnp(pyxel.KEY_SPACE):
                    if self.curseur == [0,0]:
                        pyxel.play(0,1)
                        self.PV_ennemi -=20
                    elif self.curseur == [1,0]:
                        self.menu_sort = True
                    
                    elif self.curseur == [0,1]:
                        pass
                        
                    elif self.curseur == [1,1]:
                        if random.random() < 0.67:
                            self.state = "Gameplay"
                            self.PV_ennemi = 0
                        else:
                            print("Failed to escp")
                        
                    
                
                
             
             
        elif self.state == "Menu":
            if pyxel.btnp(pyxel.KEY_TAB):
                self.state = "Gameplay"
            self.dep_curseur_menu()

            
    def draw(self):
        pyxel.cls(0)
        
        if self.state == "Titre" :
            pyxel.blt(25, 25, 2, 0, 32, 89, 95-32, 0)
            pyxel.text(53, 101, "COMMENCER", 3)
            pyxel.text(52, 100, "COMMENCER", 7)
            pyxel.blt(45, 98, 1, 0, 0, 8, 8, 0)
            
        if self.state == "Gameplay" :
            self.dessin_monde()

            
        
        if self.state == "Menu":
            self.dessin_monde()
            self.dessin_menu()
            

                
        if self.state == "Combat":
            self.dessin_combat()
            
            
            if pyxel.btnp(pyxel.KEY_SPACE) and self.curseur==[0, 0] and self.test_animation(self.animation_combat):
                self.animation_combat["tranche"]=32
            elif self.animation_combat["tranche"]>0:
                self.animation_combat["tranche"]-= 3
                
            if self.animation_combat["tranche"]>0:
                pyxel.blt(65,50, 1, 0, 8, 16, 32-self.animation_combat["tranche"], 0)
                

class Monstre:
    def __init__(self, p, a, d, x, y, xp):
        self.msPV = p
        self.msAtt = a
        self.msdef = d
        self.orix = x
        self.oriy = y
        self.exp = xp
        
class Sort:
    def __init__(self, nom, cible, degats, cout, orx, ory):
        self.nom = nom
        self.cible = cible
        self.degats = degats
        self.cout = cout
        self.orx = orx
        self.ory = ory
        
                
App()
                    
                    