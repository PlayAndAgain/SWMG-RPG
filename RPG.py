import pyxel, random

class App:
    def __init__(self, WIDTH=144, HEIGHT=144):
        pyxel.init(WIDTH, HEIGHT, "RPG",  display_scale=4)
        pyxel.load("res.pyxres")
        self.player_x=64
        self.player_y=64
        self.curseur=[0, 0]
        self.solide=[(4,0), (4,1), (5,0), (5,1), (6,0), (6,1), (7,0), (7,1), (8,0), (8,1), (9,0), (9,1)]
        self.state="Gameplay" #peut etre Gameplay, Dialogue, Combat ou menu
        pyxel.run(self.update, self.draw)
        

        
    def mouvement(self):
        if pyxel.btnp(pyxel.KEY_UP) and self.player_y > 0 and pyxel.tilemaps[0].pget(self.player_x //8, self.player_y //8 -1) not in self.solide: 
            self.player_y -= 16
        if pyxel.btnp(pyxel.KEY_DOWN) and self.player_y < 128 and pyxel.tilemaps[0].pget(self.player_x //8, self.player_y //8 -20) not in self.solide:
            self.player_y += 16
        if pyxel.btnp(pyxel.KEY_LEFT) and self.player_x > 0 and pyxel.tilemaps[0].pget(self.player_x //8 -1, self.player_y //8) not in self.solide:
            self.player_x -= 16
        if pyxel.btnp(pyxel.KEY_RIGHT) and self.player_x < 128 and pyxel.tilemaps[0].pget(self.player_x //8 +20, self.player_y //8 ) not in self.solide:
            self.player_x += 16
            
            
    def fenetre_combat(self):
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
        

            
    def dep_curseur(self):
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
        
    
    def update(self):
        print(pyxel.tilemaps[0].pget(self.player_x //8, self.player_y //8 -20))
        if self.state == "Gameplay":
            self.mouvement()
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.state = "Combat"
            
        elif self.state == "Combat":
            self.dep_curseur()
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.state = "Gameplay"
            
        
        
    
    def draw(self):
        pyxel.cls(0)
        if self.state == "Gameplay" :
            pyxel.bltm(0,0, 0, 0,0, 144, 144)
            pyxel.blt(self.player_x, self.player_y, 0, 0, 0, 16, 16, 13)
            
        if self.state == "Combat":
            self.fenetre_combat()
            pyxel.rect(100, 119, 30, 3, 11)
            pyxel.rect(100, 134, 30, 3, 5)
            pyxel.blt(56, 50, 1, 16, 0, 64, 48, 0)
            

App()

