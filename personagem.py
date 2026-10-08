import pyxel


class Personagem:
    def __init__(self, x, y, possui_colisao, usa_teclas_wasd, cor, inimigo):
        self.x = x
        self.y = y
        self.possui_colisao = possui_colisao
        self.usa_teclas_wasd = usa_teclas_wasd
        self.cor = cor
        self.inimigo = inimigo

    def mover_horizontalmente(self, deslocamento):
        self.x += deslocamento

        if (self.x > self.inimigo.x - 22 and
            self.x < self.inimigo.x + 14 and
            self.y < self.inimigo.y + 12 and
            self.y > self.inimigo.y - 22):
            self.x -= deslocamento

        if self.possui_colisao is True and (self.x >= 150 or self.x <= 0):
            self.x -= deslocamento

        elif self.possui_colisao is False:
            if self.x <= -10:
                self.x = 160
            elif self.x >= 160:
                self.x = 0
            else:
                pass

        else:
            pass

    def mover_verticalmente(self, deslocamento):
        self.y += deslocamento

        if (self.y > self.inimigo.y - 23 and
            self.y < self.inimigo.y + 14 and
            self.x < self.inimigo.x + 12 and
            self.x > self.inimigo.x - 20):
            self.y -= deslocamento

        if self.possui_colisao is True and (self.y >= 110 or self.y <= 0):
            self.y -= deslocamento

        elif self.possui_colisao is False:
            if self.y <= -10:
                self.y = 120
            elif self.y >= 120:
                self.y = 0
            else:
                pass

    def movimentar(self):
        if self.usa_teclas_wasd is True:

            if pyxel.btn(pyxel.KEY_D):
                self.mover_horizontalmente(2)

            if pyxel.btn(pyxel.KEY_A):
                self.mover_horizontalmente(-2)

            if pyxel.btn(pyxel.KEY_S):
                self.mover_verticalmente(2)

            if pyxel.btn(pyxel.KEY_W):
                self.mover_verticalmente(-2)

        if self.usa_teclas_wasd is False:

            if pyxel.btn(pyxel.KEY_RIGHT):
                self.mover_horizontalmente(3)

            if pyxel.btn(pyxel.KEY_LEFT):
                self.mover_horizontalmente(-3)

            if pyxel.btn(pyxel.KEY_DOWN):
                self.mover_verticalmente(3)

            if pyxel.btn(pyxel.KEY_UP):
                self.mover_verticalmente(-3)

    def desenhar(self):
        pyxel.rect(self.x, self.y, 10, 10, self.cor)