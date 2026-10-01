import pyxel

class Char:
    def __init__(self, x, y, colide, keys, cor, luxur, sprite_y=None):
        self.x=x
        self.y=y
        self.colide=colide
        self.keys=keys
        self.cor=cor
        self.luxur=luxur
        self.sprite_y=sprite_y
        self.frame=0
       
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
            if self.x <= -16:
                self.x = 160
            elif self.x >= 160:
                self.x = -16

    def move_ups(self, y):
        self.y += y

        if (self.y > self.luxur.y-23 and
            self.y < self.luxur.y+14 and
            self.x < self.luxur.x+12 and
            self.x > self.luxur.x-20):
            self.y -= y

        if self.colide is True and (self.y >= 91 or self.y <= 0):
            self.y -= y
           
        elif self.colide is False:
            if self.y <= -16:
                self.y = 120
            elif self.y >= 120:
                self.y = -16

    def walk(self):
        andando = False

        if self.keys is True:
            if pyxel.btn(pyxel.KEY_D):
                self.move_lat(2)
                andando = True
            if pyxel.btn(pyxel.KEY_A):
                self.move_lat(-2)
                andando = True
            if pyxel.btn(pyxel.KEY_S):
                self.move_ups(2)
                andando = True
            if pyxel.btn(pyxel.KEY_W):
                self.move_ups(-2)
                andando = True

        if self.keys is False:
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.move_lat(3)
                andando = True
            if pyxel.btn(pyxel.KEY_LEFT):
                self.move_lat(-3)
                andando = True
            if pyxel.btn(pyxel.KEY_DOWN):
                self.move_ups(3)
                andando = True
            if pyxel.btn(pyxel.KEY_UP):
                self.move_ups(-3)
                andando = True

        if andando:
            self.frame = (pyxel.frame_count // 8) % 2
        else:
            self.frame = 0

    def show(self):
        if self.sprite_y is not None:
            pyxel.blt(
                self.x, self.y,
                0,
                self.frame * 16,
                self.sprite_y,
                16, 16,
                0
            )
        else:
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
        pyxel.circ(self.x, self.y, 15, 2)
        pyxel.circ(self.x-15, self.y+15, 10, 0)
        pyxel.circ(self.x+15, self.y+15, 10, 0)

        pyxel.tri(self.x-10, self.y-10,
            self.x-15, self.y-18,
            self.x-5, self.y-12, 4)

        pyxel.tri(self.x+10, self.y-10,
            self.x+15, self.y-18,
            self.x+5, self.y-12, 4)

        pyxel.rect(self.x-7, self.y-3, 5, 5, 0)
        pyxel.rect(self.x+3, self.y-3, 5, 5, 0)

        pyxel.circ(self.x-3, self.y-4, 3, 2)
        pyxel.circ(self.x+3, self.y-4, 3, 2)

        pyxel.circ(self.x-5, self.y-1, 1, 9)
        pyxel.circ(self.x+5, self.y-1, 1, 9)

        pyxel.tri(self.x-1, self.y+3,
            self.x-1, self.y+7,
            self.x-3, self.y+7, 0)

        pyxel.tri(self.x+1, self.y+3,
            self.x+1, self.y+7,
            self.x+3, self.y+7, 0)

    def takehit(self, hit):
        self.hp -= hit


class App:
    def __init__(self):
        pyxel.init(160,120)

        pyxel.load("recursos.pyxres")

        self.luxur=Vil(80, 60, 100, 2)

        self.bluu=Char(
            50, 50, True, True, 5, self.luxur, 0
        )

        self.redd=Char(
            10, 10, False, False, 8, self.luxur, 16
        )

        pyxel.run(self.update, self.draw)
       
    def update(self):
        self.bluu.walk()
        self.redd.walk()
       
    def draw(self):
        pyxel.cls(0)

        self.luxur.show()
        self.redd.show()
        self.bluu.show()
       
        pyxel.rect(10, 108, 140, 5, 13)
        pyxel.rect(10, 108, self.luxur.hp * 1.4, 5, 8)


App()
