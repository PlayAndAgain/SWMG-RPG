import pyxel, random

class App:
    def __init__(self, WIDTH=144, HEIGHT=144):
        pyxel.init(WIDTH, HEIGHT, "RPG",  display_scale=4)
        pyxel.load("res.pyxres")
        self.player_x=64
        self.player_y=64
        self.direction = "left"
        self.PV = 60
        self.MP = 40
        self.PV_ennemi = 60
        self.animation = 0
        self.curseur=[0, 0]
        self.curseur_menu = 0
        self.solide=[(4,0), (4,1), (5,0), (5,1), (6,0), (6,1), (7,0), (7,1), (8,0), (8,1), (9,0), (9,1)]
        self.state="Gameplay" #peut etre Gameplay, Dialogue, Combat
        pyxel.run(self.update, self.draw)
        

        
    def mouvement(self):
        if pyxel.btnp(pyxel.KEY_UP) and self.player_y > 0: 
            self.direction = "up"
            if pyxel.tilemaps[0].pget(self.player_x //8, self.player_y //8 -1) not in self.solide :
                self.player_y -= 16
                
        if pyxel.btnp(pyxel.KEY_DOWN) and self.player_y < 128 :
            self.direction = "down"
            if pyxel.tilemaps[0].pget(self.player_x //8, (self.player_y+17)//8 ) not in self.solide :
                self.player_y += 16
            
        if pyxel.btnp(pyxel.KEY_LEFT) and self.player_x > 0 :
            self.direction = "left"
            if pyxel.tilemaps[0].pget(self.player_x //8 -1, self.player_y //8) not in self.solide :
                self.player_x -= 16
            
        if pyxel.btnp(pyxel.KEY_RIGHT) and self.player_x < 128 :
            self.direction = "right"
            if pyxel.tilemaps[0].pget((self.player_x+17) //8 , self.player_y //8 ) not in self.solide:
                self.player_x += 16
            
            
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
        pyxel.blt(56, 50, 1, 16, 0, 64, 48, 0)
        pyxel.text(50, 50, str(self.PV_ennemi), 7)
        
        

            
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
        pyxel.bltm(0,0, 0, 0,0, 144, 144)
        self.dessin_joueur()

    def dessin_joueur(self):
        if self.direction == "up":
            pyxel.blt(self.player_x, self.player_y, 0, 0, 16, 16, 16, 13)
        if self.direction == "down":
            pyxel.blt(self.player_x, self.player_y, 0, 0, 32, 16, 16, 13)
        if self.direction == "left":
            pyxel.blt(self.player_x, self.player_y, 0, 0, 0, 16, 16, 13)
        if self.direction == "right":
            pyxel.blt(self.player_x, self.player_y, 0, 0, 48, 16, 16, 13)
        
    
    def update(self):
        if self.state == "Gameplay":
            self.mouvement()
            if pyxel.btnp(pyxel.KEY_C):
                self.tour = True
                self.state = "Combat"
            if pyxel.btnp(pyxel.KEY_TAB):
                self.state = "Menu"

            
        elif self.state == "Combat":
            if self.tour == True:
                self.dep_curseur_combat()
                if pyxel.btnp(pyxel.KEY_SPACE):
                    if self.curseur == [0,0]:
                        pyxel.play(0,1)
                        self.PV_ennemi -= 20
                if pyxel.btnp(pyxel.KEY_C):
                   self.state = "Gameplay"
                   
            
        
        elif self.state == "Menu":
            if pyxel.btnp(pyxel.KEY_TAB):
                self.state = "Gameplay"
            self.dep_curseur_menu()

            
        
        
    
    def draw(self):
        pyxel.cls(0)
        if self.state == "Gameplay" :
            self.dessin_monde()

            
        
        if self.state == "Menu":
            self.dessin_monde()
            self.dessin_menu()
            

                
            
        if self.state == "Combat":
            self.dessin_combat()
            
            if pyxel.btnp(pyxel.KEY_SPACE):
                if self.curseur == [0,0]:
                    self.animation = 30
                    self.frame = pyxel.frame_count
                    while self.animation != 0:
                        pyxel.blt(65,50, 1, 0, 8, 16, pyxel.frame_count //0.4 %32, 0)
                        if self.frame != pyxel.frame_count:
                            self.frame = pyxel.frame_count
                        self.animation -= 1
            
            
            

App()

