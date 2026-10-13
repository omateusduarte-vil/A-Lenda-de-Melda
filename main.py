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
        self.criar_partida()
        # O jogo começa na tela PRESS START.
        self.estado_final = "press_start"
        # Inicia o loop do jogo.
        pyxel.run(self.update, self.draw)
    # Cria ou reinicia os personagens para uma nova partida.
    def criar_partida(self):
        self.luxur = Vil(80, 60, luxurhpmax, 2)
        self.bluu = Char(50, 50, True, True, 5, self.luxur, 0)
        self.redd = Char(10, 10, False, False, 8, self.luxur, 16)
        self.luxur.app = self

    # Atualiza a lógica do jogo a cada frame.
    def update(self):
        if self.estado_final == "press_start":
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
                self.estado_final = None
            return

        if self.estado_final == "game_over":
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
                self.criar_partida()
                self.estado_final = "press_start"
            return

        if self.estado_final is not None:
            return

        if self.bluu.hp > 0:
            self.bluu.walk()
            self.bluu.ataque()
        if self.redd.hp > 0:
            self.redd.walk()
            self.redd.atira()
        if self.luxur.hp > 0:
            self.luxur.update()
            self.luxur.atualizar_colisoes_jogadores()

        # Verifica o resultado da luta após atualizar os personagens.
        if self.luxur.hp <= 0:
            self.estado_final = "you_win"
        elif self.bluu.hp <= 0 and self.redd.hp <= 0:
            self.estado_final = "game_over"
    # Desenha tudo na tela a cada frame.
    def draw(self):
        pyxel.cls(0)

        if self.estado_final == "press_start":
            pyxel.text(56, 56, "PRESS START", 7)
            return
        if self.estado_final == "game_over":
            pyxel.text(62, 56, "GAME OVER", 8)
            pyxel.text(43, 68, "ENTER OR SPACE", 7)
            return
        if self.estado_final == "you_win":
            pyxel.text(66, 56, "YOU WIN", 12)
            return

        # Desenha primeiro o Luxur, depois Redd e depois Bluu.
        if self.luxur.hp > 0:
            self.luxur.show()
        if self.redd.hp > 0:
            self.redd.show()
            self.redd.mostra_tiros()
        if self.bluu.hp > 0:
            self.bluu.show()

        # Barras simples de HP dos jogadores, usadas pelo dano de contato.
        pyxel.rect(3, 3, 45, 4, 13)
        if self.bluu.hp > 0:
            pyxel.rect(3, 3, 45 * (self.bluu.hp / self.bluu.hpmax), 4, 8)
        pyxel.rect(112, 3, 45, 4, 13)
        if self.redd.hp > 0:
            pyxel.rect(112, 3, 45 * (self.redd.hp / self.redd.hpmax), 4, 8)
        # Fundo da barra de HP do Luxur.
        pyxel.rect(10, 108, 140, 5, 13)
        # Parte vermelha, proporcional ao HP máximo.
        largura_hp = max(0, self.luxur.hp / self.luxur.hpmax) * 140
        pyxel.rect(10, 108, largura_hp, 5, 8)
# Inicia o jogo.
App()
