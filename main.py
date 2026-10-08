import pyxel

from personagem import Personagem
from inimigo import Inimigo


class Jogo:
    def __init__(self):
        pyxel.init(160, 120)

        self.inimigo = Inimigo(80, 60, 100, 2)

        self.personagem_azul = Personagem(
            50, 50, True, True, 5, self.inimigo
        )

        self.personagem_vermelho = Personagem(
            10, 10, False, False, 8, self.inimigo
        )

        pyxel.run(self.atualizar, self.desenhar)

    def atualizar(self):
        self.personagem_azul.movimentar()
        self.personagem_vermelho.movimentar()

    def desenhar(self):
        pyxel.cls(0)

        self.inimigo.desenhar()
        self.personagem_vermelho.desenhar()
        self.personagem_azul.desenhar()

        pyxel.rect(10, 108, 140, 5, 13)
        pyxel.rect(10, 108, self.inimigo.vida * 1.4, 5, 8)


Jogo()