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
        self.direction = "left"
        
        #Monstres
        self.necromancien = Monstre(80, 10, 20, 16, 48)
        self.masque = Monstre(60, 20, 30, 16, 0)
        self.rencontres = [self.necromancien, self.masque]
        
        #Stats
        self.stats = {"PV_max":60, "MP_max":40, "Att":20, "Def":10, "Mag":20}
        self.PV = self.stats["PV_max"]
        self.MP = self.stats["MP_max"]
        
        #Interne
        self.tour = True
        self.PV_ennemi = 60
        self.solide=[(4,0), (4,1), (5,0), (5,1), (6,0), (6,1), (7,0), (7,1), (8,0), (8,1), (9,0), (9,1), (4,2), (5,2), (4,3), (5,3), (6,2), (6,3), (7,2), (7,3)]
        self.state="Gameplay" #peut etre Gameplay, Dialogue, Combat ou Title
        self.frame=0
        
        pyxel.run(self.update, self.draw)
        
    def mouvement(self):
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
                        
    def rencontre_aleatoire(self):
        if random.randint(1,15) == 1:
            self.new_ms = self.rencontres[random.randint(0,len(self.rencontres)-1)]
            self.PV_ennemi = self.new_ms.msPV
            self.state = "Combat"
            
    def dessin_PV(self):
        if self.PV == self.stats["PV_max"]:
            pass
        elif (self.PV*100)/self.stats["PV_max"] >90:
            pyxel.rect(127, 119, 3, 3, 8)
        elif (self.PV*100)/self.stats["PV_max"] >80:
            pyxel.rect(124, 119, 6, 3, 8)
        elif (self.PV*100)/self.stats["PV_max"] >70:
            pyxel.rect(121, 119, 9, 3, 8)
        elif (self.PV*100)/self.stats["PV_max"] >60:
            pyxel.rect(118, 119, 12, 3, 8)
        elif (self.PV*100)/self.stats["PV_max"] >50:
            pyxel.rect(115, 119, 15, 3, 8)
        elif (self.PV*100)/self.stats["PV_max"] >40:
            pyxel.rect(112, 119, 18, 3, 8)
        elif (self.PV*100)/self.stats["PV_max"] >30:
            pyxel.rect(109, 119, 21, 3, 8)
        elif (self.PV*100)/self.stats["PV_max"] >20:
            pyxel.rect(106, 119, 24, 3, 8)
        elif (self.PV*100)/self.stats["PV_max"] >10:
            pyxel.rect(103, 119, 27, 3, 8)
        elif (self.PV*100)/self.stats["PV_max"] > 0:
            pyxel.rect(101, 119, 29, 3, 8)
        elif (self.PV*100)/self.stats["PV_max"] <= 0:
            pyxel.rect(100, 119, 30, 3, 8)
       
    
            
            
            
            
            
    def dessin_combat(self):
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
        self.dessin_PV()
        pyxel.text(45, 50, str(self.PV_ennemi), 7)
        
        

            
    def dep_curseur_combat(self):
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
            
    
    def dep_curseur_menu(self):
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
                
        
            
    def dessin_menu(self):
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
    
    def dessin_monde(self):
        pyxel.bltm(0,0, 0, self.map_x, self.map_y, 144, 144)
        self.dessin_joueur()
        pyxel.blt(0, 144-31, 2, 0, 0, 32, 32)

    def dessin_joueur(self):
        if self.direction == "up":
            pyxel.blt(self.player_x, self.player_y, 0, 0, 16, 16, 16, 13)
        if self.direction == "down":
            pyxel.blt(self.player_x, self.player_y, 0, 0, 32, 16, 16, 13)
        if self.direction == "left":
            pyxel.blt(self.player_x, self.player_y, 0, 0, 0, 16, 16, 13)
        if self.direction == "right":
            pyxel.blt(self.player_x, self.player_y, 0, 0, 48, 16, 16, 13)
        
    
    
    
    #UPDATE&DRAW
    def update(self):
        if self.state == "Gameplay":
            self.mouvement()
            if pyxel.btnp(pyxel.KEY_TAB):
                self.state = "Menu"

            
        elif self.state == "Combat":
            if self.PV_ennemi <= 0 and not self.frame > 0:
                self.state = "Gameplay"
            if self.tour == True:
                self.dep_curseur_combat()
                if pyxel.btnp(pyxel.KEY_SPACE):
                    if self.curseur == [0,0]:
                        pyxel.play(0,1)
                        self.PV_ennemi-= 20
                if pyxel.btnp(pyxel.KEY_C):
                   self.state = "Gameplay"
             
             
        elif self.state == "Menu":
            if pyxel.btnp(pyxel.KEY_TAB):
                self.state = "Gameplay"
            self.dep_curseur_menu()

            
    def draw(self):
        pyxel.cls(0)
        
        if self.state == "Title" :
            pyxel.blt(25, 25, 2, 0, 32, 89, 95-32, 0)
        if self.state == "Gameplay" :
            self.dessin_monde()

            
        
        if self.state == "Menu":
            self.dessin_monde()
            self.dessin_menu()
            

                
        if self.state == "Combat":
            self.dessin_combat()
            
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.frame=32
            elif self.frame>0:
                self.frame-=2
                
            if self.frame>0:
                pyxel.blt(65,50, 1, 0, 8, 16, 32-self.frame, 0)
                

class Monstre:
    def __init__(self, p, a, d, x, y ):
        self.msPV = p
        self.msAtt = a
        self.msdef = d
        self.orix = x
        self.oriy = y
                
App()
                    
                    