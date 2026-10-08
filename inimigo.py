import pyxel


class Inimigo:
    def __init__(self, x, y, vida_maxima, cor):
        self.x = x
        self.y = y
        self.vida_maxima = vida_maxima
        self.vida = vida_maxima
        self.cor = cor

    def esta_vivo(self):
        return self.vida > 0

    def desenhar(self):
        # Corpo
        pyxel.circ(self.x, self.y, 15, 2)
        pyxel.circ(self.x - 15, self.y + 15, 10, 0)
        pyxel.circ(self.x + 15, self.y + 15, 10, 0)

        # Chifres
        pyxel.tri(
            self.x - 10, self.y - 10,
            self.x - 15, self.y - 18,
            self.x - 5, self.y - 12,
            4
        )

        pyxel.tri(
            self.x + 10, self.y - 10,
            self.x + 15, self.y - 18,
            self.x + 5, self.y - 12,
            4
        )

        # Olhos
        pyxel.rect(self.x - 7, self.y - 3, 5, 5, 0)
        pyxel.rect(self.x + 3, self.y - 3, 5, 5, 0)

        pyxel.circ(self.x - 3, self.y - 4, 3, 2)
        pyxel.circ(self.x + 3, self.y - 4, 3, 2)

        pyxel.circ(self.x - 5, self.y - 1, 1, 9)
        pyxel.circ(self.x + 5, self.y - 1, 1, 9)

        # Nariz
        pyxel.tri(
            self.x - 1, self.y + 3,
            self.x - 1, self.y + 7,
            self.x - 3, self.y + 7,
            0
        )

        pyxel.tri(
            self.x + 1, self.y + 3,
            self.x + 1, self.y + 7,
            self.x + 3, self.y + 7,
            0
        )

    def receber_dano(self, dano):
        self.vida -= dano