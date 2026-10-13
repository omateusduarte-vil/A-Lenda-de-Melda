import pyxel
from config import luxurhpmax
from personagens import Char
from luxur import Vil


class App:
    # Cria a janela, carrega recursos e cria os personagens.
    def __init__(self):
        pyxel.init(160,120)
        # Carrega os sprites do arquivo .pyxres.
        pyxel.load("recursos.pyxres")
        # Cria o Luxur com 100 HP.
        self.luxur=Vil(80, 60, luxurhpmax, 2)
        # Cria o Bluu na posição inicial.
        self.bluu=Char(
            50, 50, True, True, 5, self.luxur, 0
        )
        # Cria o Redd na posição inicial.
        self.redd=Char(
            10, 10, False, False, 8, self.luxur, 16
        )
        self.luxur.app = self
        # Inicia o loop do jogo.
        pyxel.run(self.update, self.draw)
    # Atualiza a lógica do jogo a cada frame.
    def update(self):
        self.bluu.walk()
        self.redd.walk()
        self.redd.atira()
        self.luxur.update()
        self.luxur.atualizar_colisoes_jogadores()
        # Atualiza o ataque do Bluu.
        self.bluu.ataque()
    # Desenha tudo na tela a cada frame.
    def draw(self):
        pyxel.cls(0)
        # Desenha primeiro o Luxur, depois Redd e depois Bluu.
        self.luxur.show()
        self.redd.show()
        self.redd.mostra_tiros()
        self.bluu.show()
        # Barras simples de HP dos jogadores, usadas pelo dano de contato.
        pyxel.rect(3, 3, 45, 4, 13)
        pyxel.rect(3, 3, 45 * (self.bluu.hp / self.bluu.hpmax), 4, 8)
        pyxel.rect(112, 3, 45, 4, 13)
        pyxel.rect(112, 3, 45 * (self.redd.hp / self.redd.hpmax), 4, 8)
        # Fundo da barra de HP do Luxur.
        pyxel.rect(10, 108, 140, 5, 13)
        # Parte vermelha, proporcional ao HP máximo.
        largura_hp = (self.luxur.hp / self.luxur.hpmax) * 140
        pyxel.rect(10, 108, largura_hp, 5, 8)
# Inicia o jogo.
App()
