import pyxel


# ============================================================
# CLASSE DOS PERSONAGENS
# Controla movimentação, ataque, sprites e direção.
# ============================================================

class Char:

    # Cria um personagem e define suas características iniciais.
    def __init__(self, x, y, colide, keys, cor, luxur, sprite_y=None):
        self.x=x
        self.y=y
        self.colide=colide
        self.keys=keys
        self.cor=cor
        self.luxur=luxur
        self.sprite_y=sprite_y
        self.frame=0

        # Guarda para qual lado o personagem está virado:
        # 1 = direita / -1 = esquerda.
        self.direcao=1

        # Variáveis usadas para controlar o ataque e sua animação.
        self.atacando=False
        self.tempo_ataque=0
        self.frame_ataque=0
        self.hit_aplicado=False
       
       
    # Move o personagem horizontalmente e verifica colisões/laterais da tela.
    def move_lat(self, x):
        self.x += x

        # Impede o personagem de atravessar o Luxur.
        if (self.x > self.luxur.x-22 and 
            self.x < self.luxur.x+14 and
            self.y < self.luxur.y+12 and
            self.y > self.luxur.y-22):
            self.x -= x

        # Bluu fica preso dentro da tela.
        if self.colide is True and (self.x >= 150 or self.x <= 0):
            self.x -= x
           
        # Redd atravessa uma borda e aparece na outra.
        elif self.colide is False:
            if self.x <= -16:
                self.x = 160
            elif self.x >= 160:
                self.x = -16


    # Move o personagem verticalmente e verifica colisões/laterais da tela.
    def move_ups(self, y):
        self.y += y

        # Impede o personagem de atravessar o Luxur.
        if (self.y > self.luxur.y-23 and
            self.y < self.luxur.y+14 and
            self.x < self.luxur.x+12 and
            self.x > self.luxur.x-20):
            self.y -= y

        # Bluu fica preso dentro da tela.
        if self.colide is True and (self.y >= 91 or self.y <= 0):
            self.y -= y
           
        # Redd atravessa uma borda e aparece na outra.
        elif self.colide is False:
            if self.y <= -16:
                self.y = 120
            elif self.y >= 120:
                self.y = -16


    # Lê as teclas de movimento e atualiza a animação de caminhada.
    def walk(self):
        andando = False

        # Controles do Bluu: WASD.
        if self.keys is True:
            if pyxel.btn(pyxel.KEY_D):
                self.move_lat(2)
                self.direcao=1
                andando = True

            if pyxel.btn(pyxel.KEY_A):
                self.move_lat(-2)
                self.direcao=-1
                andando = True

            if pyxel.btn(pyxel.KEY_S):
                self.move_ups(2)
                andando = True

            if pyxel.btn(pyxel.KEY_W):
                self.move_ups(-2)
                andando = True

        # Controles do Redd: setas direcionais.
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

        # Alterna entre os dois sprites de caminhada.
        if andando:
            self.frame = (pyxel.frame_count // 8) % 2
        else:
            self.frame = 0


    # Controla o ataque do Bluu, incluindo animação e hitbox.
    def ataque(self):

        # R inicia o ataque se o personagem não estiver atacando.
        if self.keys is True and pyxel.btnp(pyxel.KEY_R) and not self.atacando:
            self.atacando=True
            self.tempo_ataque=0
            self.hit_aplicado=False

        # Enquanto o ataque estiver acontecendo, conta seus frames.
        if self.atacando:
            self.tempo_ataque += 1

            # FRAME 1: espada erguida durante 3 frames.
            if self.tempo_ataque < 4:
                self.frame_ataque=0

            # FRAME 2: espada descendo durante 7 frames.
            elif self.tempo_ataque < 11:
                self.frame_ataque=1

            # Verifica se a espada atingiu o Luxur.
            if self.frame_ataque == 1 and not self.hit_aplicado:

                # Define a posição horizontal do hitbox conforme a direção.
                if self.direcao == 1:
                    # Espada para a direita.
                    espada_x = self.x + 16

                else:
                    # Espada para a esquerda.
                    espada_x = self.x - 16

                # Define a posição vertical do hitbox.
                espada_y = self.y + 6

                # Hitbox da espada: retângulo de 16x16.
                if (espada_x < self.luxur.x + 15 and
                    espada_x + 16 > self.luxur.x - 15 and
                    espada_y < self.luxur.y + 25 and
                    espada_y + 16 > self.luxur.y - 18):

                    # Causa 1 de dano e impede que o mesmo golpe cause dano novamente.
                    self.luxur.takehit(1)
                    self.hit_aplicado=True

            # Depois de 10 frames, encerra o ataque e reseta suas variáveis.
            if self.tempo_ataque >= 11:
                self.atacando=False
                self.tempo_ataque=0
                self.frame_ataque=0
                self.hit_aplicado=False


    # Desenha o personagem e a espada na tela.
    def show(self):

        # Se existe um sprite, desenha o personagem usando o arquivo .pyxres.
        if self.sprite_y is not None:
            pyxel.blt(
                self.x, self.y,
                0,
                self.frame * 16,
                self.sprite_y,
                16, 16,
                0
            )

            # Desenha a espada somente enquanto o personagem estiver atacando.
            if self.atacando:

                # Seleciona o primeiro frame da espada.
                if self.frame_ataque == 0:

                    # Espada normal, apontando para a direita.
                    if self.direcao == 1:
                        pyxel.blt(
                            self.x + 16,
                            self.y - 8,
                            0,
                            32,
                            0,
                            16, 16,
                            0
                        )

                    # Espada espelhada, apontando para a esquerda.
                    else:
                        pyxel.blt(
                            self.x - 16,
                            self.y - 8,
                            0,
                            32,
                            0,
                            -16, 16,
                            0
                        )

                # Seleciona o segundo frame da espada.
                else:

                    # Espada normal, apontando para a direita.
                    if self.direcao == 1:
                        pyxel.blt(
                            self.x + 16,
                            self.y + 6,
                            0,
                            48,
                            0,
                            16, 16,
                            0
                        )

                    # Espada espelhada, apontando para a esquerda.
                    else:
                        pyxel.blt(
                            self.x - 16,
                            self.y + 6,
                            0,
                            48,
                            0,
                            -16, 16,
                            0
                        )

        # Se não existe sprite, desenha um quadrado simples.
        else:
            pyxel.rect(self.x, self.y, 10, 10, self.cor)


# ============================================================
# CLASSE DO LUXUR
# Controla HP, aparência e recebimento de dano.
# ============================================================

class Vil:

    # Cria o Luxur e define seu HP máximo e atual.
    def __init__(self, x, y, hpmax, cor):
        self.x=x
        self.y=y
        self.hpmax=hpmax
        self.hp=hpmax
        self.cor=cor


    # Verifica se o Luxur ainda está vivo.
    def alive(self):
        return self.hp > 0


    # Desenha o corpo, chifres, olhos e rosto do Luxur.
    def show(self):

        # Corpo e partes inferiores.
        pyxel.circ(self.x, self.y, 15, 2)
        pyxel.circ(self.x-15, self.y+15, 10, 0)
        pyxel.circ(self.x+15, self.y+15, 10, 0)

        # Chifre esquerdo.
        pyxel.tri(self.x-10, self.y-10,
            self.x-15, self.y-18,
            self.x-5, self.y-12, 4)

        # Chifre direito.
        pyxel.tri(self.x+10, self.y-10,
            self.x+15, self.y-18,
            self.x+5, self.y-12, 4)

        # Parte preta dos olhos.
        pyxel.rect(self.x-7, self.y-3, 5, 5, 0)
        pyxel.rect(self.x+3, self.y-3, 5, 5, 0)

        # Parte colorida dos olhos.
        pyxel.circ(self.x-3, self.y-4, 3, 2)
        pyxel.circ(self.x+3, self.y-4, 3, 2)

        # Pequenos detalhes dos olhos.
        pyxel.circ(self.x-5, self.y-1, 1, 9)
        pyxel.circ(self.x+5, self.y-1, 1, 9)

        # Narina esquerda.
        pyxel.tri(self.x-1, self.y+3,
            self.x-1, self.y+7,
            self.x-3, self.y+7, 0)

        # Narina direita.
        pyxel.tri(self.x+1, self.y+3,
            self.x+1, self.y+7,
            self.x+3, self.y+7, 0)


    # Retira uma quantidade de HP do Luxur.
    def takehit(self, hit):
        self.hp -= hit


# ============================================================
# CLASSE PRINCIPAL DO JOGO
# Inicializa o Pyxel, personagens e loop principal.
# ============================================================

class App:

    # Cria a janela, carrega recursos e cria os personagens.
    def __init__(self):
        pyxel.init(160,120)

        # Carrega os sprites do arquivo .pyxres.
        pyxel.load("recursos.pyxres")

        # Cria o Luxur com 100 HP.
        self.luxur=Vil(80, 60, 100, 2)

        # Cria o Bluu na posição inicial.
        self.bluu=Char(
            50, 50, True, True, 5, self.luxur, 0
        )

        # Cria o Redd na posição inicial.
        self.redd=Char(
            10, 10, False, False, 8, self.luxur, 16
        )

        # Inicia o loop do jogo.
        pyxel.run(self.update, self.draw)


    # Atualiza a lógica do jogo a cada frame.
    def update(self):
        self.bluu.walk()
        self.redd.walk()

        # Atualiza o ataque do Bluu.
        self.bluu.ataque()


    # Desenha tudo na tela a cada frame.
    def draw(self):
        pyxel.cls(0)

        # Desenha primeiro o Luxur, depois Redd e depois Bluu.
        self.luxur.show()
        self.redd.show()
        self.bluu.show()

        # Fundo da barra de HP.
        pyxel.rect(10, 108, 140, 5, 13)

        # Parte vermelha da barra, proporcional ao HP restante.
        pyxel.rect(10, 108, self.luxur.hp * 1.4, 5, 8)


# Inicia o jogo.
App()
