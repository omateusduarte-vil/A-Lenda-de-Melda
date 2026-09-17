import pyxel

class Char:
    def __init__(self, x, y, colide, keys, cor, luxur):
        self.x=x
        self.y=y
        self.colide=colide
        self.keys=keys
        self.cor=cor
        self.luxur=luxur
       
    def move_lat(self, x):
        self.x += x

        if (self.x > self.luxur.x-22 and 
            self.x < self.luxur.x+14 and
            self.y < self.luxur.y+12 and 
            self.y > self.luxur.y-22):
            self.x -= x

        if self.colide is True and (self.x >= 150 or self.x <= 0):
            self.x -= x
           
        elif self.colide is False:
            if self.x <= -10:
                self.x = 160
            elif self.x >= 160:
                self.x = 0
            else:
                pass
               
        else:
            pass

    def move_ups(self, y):
        self.y += y

        if (self.y > self.luxur.y-23 and 
            self.y < self.luxur.y+14 and
            self.x < self.luxur.x+12 and 
            self.x > self.luxur.x-20):
            self.y -= y

        if self.colide is True and (self.y >= 110 or self.y <= 0):
            self.y -= y
           
        elif self.colide is False:
            if self.y <= -10:
                self.y = 120
            elif self.y >= 120:
                self.y = 0
            else:
                pass

    def walk(self):
        if self.keys is True:

            if pyxel.btn(pyxel.KEY_D):
                self.move_lat(2)
            if pyxel.btn(pyxel.KEY_A):
                self.move_lat(-2)
            if pyxel.btn(pyxel.KEY_S):
                self.move_ups(2)
            if pyxel.btn(pyxel.KEY_W):
                self.move_ups(-2)

        if self.keys is False:

            if pyxel.btn(pyxel.KEY_RIGHT):
                self.move_lat(3)
            if pyxel.btn(pyxel.KEY_LEFT):
                self.move_lat(-3)
            if pyxel.btn(pyxel.KEY_DOWN):
                self.move_ups(3)
            if pyxel.btn(pyxel.KEY_UP):
                self.move_ups(-3)

    def show(self):
        pyxel.rect(self.x, self.y, 10, 10, self.cor)

class Vil:
    def __init__(self, x, y, hpmax, cor):
            self.x=x
            self.y=y
            self.hpmax=hpmax
            self.hp=hpmax
            self.cor=cor

    def alive(self):
        return self.hp > 0

    def show(self):
    # corpo
        pyxel.circ(self.x, self.y, 15, 2)
        pyxel.circ(self.x-15, self.y+15, 10, 0)
        pyxel.circ(self.x+15, self.y+15, 10, 0)

    # chifres
        pyxel.tri(self.x - 10, self.y - 10,
            self.x - 15, self.y - 18,
            self.x - 5, self.y - 12, 4)

        pyxel.tri(self.x + 10, self.y - 10,
            self.x + 15, self.y - 18,
            self.x + 5, self.y - 12, 4)

    # olhos
        
        pyxel.rect(self.x - 7, self.y - 3, 5, 5, 0)
        pyxel.rect(self.x + 3, self.y - 3, 5, 5, 0)

        pyxel.circ(self.x - 3, self.y - 4, 3, 2)
        pyxel.circ(self.x + 3, self.y - 4, 3, 2)

        pyxel.circ(self.x - 5, self.y - 1, 1, 9)
        pyxel.circ(self.x + 5, self.y - 1, 1, 9)

    # nariz

        pyxel.tri(self.x - 1, self.y + 3,
            self.x - 1, self.y + 7,
            self.x - 3, self.y + 7, 0)

        pyxel.tri(self.x + 1, self.y + 3,
            self.x + 1, self.y + 7,
            self.x + 3, self.y + 7, 0)
       

    def takehit(self, hit):
        self.hp -= hit

class App:
    def __init__(self):
        pyxel.init(160,120)

        self.luxur=Vil(80, 60, 100, 2)
        self.bluu=Char(50, 50, True, True, 5, self.luxur)
        self.redd=Char(10, 10, False, False, 8, self.luxur)
       
        pyxel.run(self.update, self.draw)
       
    def update(self):

        self.bluu.walk()
        self.redd.walk()   
       
    def draw(self):
        pyxel.cls(0)
        self.luxur.show()
        self.redd.show()
        self.bluu.show()
       
        pyxel.rect(10, 108, 140, 5, 13)  # fundo
        pyxel.rect(10, 108, self.luxur.hp * 1.4, 5, 8)  # HP

App()
