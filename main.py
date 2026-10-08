import pyxel


# ============================================================
# CONFIGURAÇÃO DO COMBO DO BLUU
# ============================================================

# Tempo do primeiro golpe
GOLPE1_FRAME1 = 4
GOLPE1_FRAME2 = 7

# Tempo do segundo golpe
GOLPE2_FRAME1 = 0
GOLPE2_FRAME2 = 7

# Tempo do terceiro golpe
GOLPE3_FRAME1 = 0
GOLPE3_FRAME2 = 7

# Pequeno intervalo entre os golpes
DELAY_ENTRE_GOLPES = 2

# Tempo depois do terceiro golpe
DELAY_FIM_COMBO = 8

# Dano de cada golpe
DANO_GOLPE1 = 1
DANO_GOLPE2 = 1
DANO_GOLPE3 = 1

# ============================================================
# CONFIGURAÇÃO DO TIRO DA REDD
# ============================================================

VELOCIDADE_TIRO_REDD = 6
DISTANCIA_MAX_TIRO_REDD = 120
MAX_TIROS_REDD = 4
DANO_TIRO_REDD = 1
DELAY_TIRO_REDD = 2

# Deslocamento horizontal da colisão do tiro com o Luxur
# Tiro vindo da direita = tiro indo para a esquerda
OFFSET_X_COLISAO_TIRO_REDD_ESQUERDA = 0

# Tiro vindo da esquerda = tiro indo para a direita
OFFSET_X_COLISAO_TIRO_REDD_DIREITA = -12

# Deslocamento vertical exclusivo do queixo para tiros
OFFSET_Y_QUEIXO_TIRO_REDD = 5

# Deslocamentos verticais exclusivos do retângulo superior para tiros
OFFSET_Y_SUPERIOR_TIRO_REDD_CIMA = 10
OFFSET_Y_SUPERIOR_TIRO_REDD_BAIXO = 3


# ============================================================
# HITBOX DE COLISÃO DO LUXUR
# ============================================================

# Retângulo superior
HITBOX_COLISAO_LUXUR_LARGURA = 36
HITBOX_COLISAO_LUXUR_ALTURA = 30
HITBOX_COLISAO_LUXUR_OFFSET_X = -26
HITBOX_COLISAO_LUXUR_OFFSET_Y = -27

# Retângulo inferior / queixo
HITBOX_COLISAO_LUXUR_QUEIXO_LARGURA = 16
HITBOX_COLISAO_LUXUR_QUEIXO_ALTURA = 16
HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_X = -15
HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_Y = -5


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

        # Variáveis usadas para controlar o ataque.
        self.atacando=False
        self.tempo_ataque=0
        self.frame_ataque=0
        self.hit_aplicado=False

        # Número do golpe atual.
        self.golpe=0

        # Delay entre golpes.
        self.delay_combo=0

        # Delay depois do combo.
        self.delay_fim_combo=0

        # Guarda se o jogador pediu o próximo golpe.
        self.proximo_golpe=False

        # Tiros da Redd.
        self.tiros = []
        self.delay_tiro = 0


    # Move o personagem horizontalmente e verifica colisões.
    def move_lat(self, x):
        self.x += x

        # ====================================================
        # HITBOX SUPERIOR DO LUXUR
        # ====================================================

        colisao_luxur = (
            self.x >
            self.luxur.x + HITBOX_COLISAO_LUXUR_OFFSET_X
            and
            self.x <
            self.luxur.x +
            HITBOX_COLISAO_LUXUR_OFFSET_X +
            HITBOX_COLISAO_LUXUR_LARGURA
            and
            self.y >
            self.luxur.y + HITBOX_COLISAO_LUXUR_OFFSET_Y
            and
            self.y <
            self.luxur.y +
            HITBOX_COLISAO_LUXUR_OFFSET_Y +
            HITBOX_COLISAO_LUXUR_ALTURA
        )


        # ====================================================
        # HITBOX DO QUEIXO DO LUXUR
        # ====================================================

        colisao_queixo = (
            self.x >
            self.luxur.x + HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_X
            and
            self.x <
            self.luxur.x +
            HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_X +
            HITBOX_COLISAO_LUXUR_QUEIXO_LARGURA
            and
            self.y >
            self.luxur.y + HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_Y
            and
            self.y <
            self.luxur.y +
            HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_Y +
            HITBOX_COLISAO_LUXUR_QUEIXO_ALTURA
        )


        # Se bater em qualquer uma das duas hitboxes,
        # desfaz o movimento.
        if colisao_luxur or colisao_queixo:
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


    # Move o personagem verticalmente e verifica colisões.
    def move_ups(self, y):
        self.y += y

        # ====================================================
        # HITBOX SUPERIOR DO LUXUR
        # ====================================================

        colisao_luxur = (
            self.x >
            self.luxur.x + HITBOX_COLISAO_LUXUR_OFFSET_X
            and
            self.x <
            self.luxur.x +
            HITBOX_COLISAO_LUXUR_OFFSET_X +
            HITBOX_COLISAO_LUXUR_LARGURA
            and
            self.y >
            self.luxur.y + HITBOX_COLISAO_LUXUR_OFFSET_Y
            and
            self.y <
            self.luxur.y +
            HITBOX_COLISAO_LUXUR_OFFSET_Y +
            HITBOX_COLISAO_LUXUR_ALTURA
        )


        # ====================================================
        # HITBOX DO QUEIXO DO LUXUR
        # ====================================================

        colisao_queixo = (
            self.x >
            self.luxur.x + HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_X
            and
            self.x <
            self.luxur.x +
            HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_X +
            HITBOX_COLISAO_LUXUR_QUEIXO_LARGURA
            and
            self.y >
            self.luxur.y + HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_Y
            and
            self.y <
            self.luxur.y +
            HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_Y +
            HITBOX_COLISAO_LUXUR_QUEIXO_ALTURA
        )


        # Se bater em qualquer uma das duas hitboxes,
        # desfaz o movimento.
        if colisao_luxur or colisao_queixo:
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
                self.direcao = 1
                andando = True

            if pyxel.btn(pyxel.KEY_LEFT):
                self.move_lat(-3)
                self.direcao = -1
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


    # ========================================================
    # ATAQUE NORMAL DA REDD
    # ========================================================

    def atira(self):
        if self.keys is not False:
            return

        # Conta o delay entre tiros.
        if self.delay_tiro > 0:
            self.delay_tiro -= 1

        # Tecla de ataque da Redd: T.
        if (pyxel.btnp(pyxel.KEY_P) or pyxel.btnp(pyxel.KEY_KP_ENTER)) and self.delay_tiro == 0:
            if len(self.tiros) < MAX_TIROS_REDD:
                self.tiros.append(
                    Tiro(
                        self.x + (11 if self.direcao == 1 else 4),
                        self.y + 8,
                        self.direcao,
                        self.luxur
                    )
                )
                self.delay_tiro = DELAY_TIRO_REDD

        # Atualiza os tiros e remove os que desapareceram.
        for tiro in self.tiros:
            tiro.update()

        self.tiros = [tiro for tiro in self.tiros if tiro.ativo]


    def mostra_tiros(self):
        if self.keys is False:
            for tiro in self.tiros:
                tiro.show()


    # ========================================================
    # ATAQUE / COMBO DO BLUU
    # ========================================================

    def ataque(self):

        # Delay depois do combo.
        if self.delay_fim_combo > 0:
            self.delay_fim_combo -= 1
            return


        # ====================================================
        # INPUT DO T
        # ====================================================

        if self.keys is True and (pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_R)):

            # T começa o primeiro golpe.
            if not self.atacando and self.golpe == 0:

                self.golpe = 1
                self.atacando = True
                self.tempo_ataque = 0
                self.frame_ataque = 0
                self.hit_aplicado = False

            # T pede o próximo golpe.
            elif self.atacando and self.golpe < 3:

                self.proximo_golpe = True


        # ====================================================
        # DELAY ENTRE OS GOLPES
        # ====================================================

        if self.delay_combo > 0:

            self.delay_combo -= 1

            if self.delay_combo == 0:

                if self.proximo_golpe:

                    self.proximo_golpe = False
                    self.golpe += 1

                    self.atacando = True
                    self.tempo_ataque = 0
                    self.frame_ataque = 0
                    self.hit_aplicado = False

                else:

                    self.golpe = 0

            return


        # Se não está atacando, para aqui.
        if not self.atacando:
            return


        # Conta os frames do golpe atual.
        self.tempo_ataque += 1


        # ====================================================
        # DEFINE O TEMPO DO GOLPE
        # ====================================================

        if self.golpe == 1:

            limite_frame1 = GOLPE1_FRAME1
            limite_frame2 = GOLPE1_FRAME1 + GOLPE1_FRAME2

        elif self.golpe == 2:

            limite_frame1 = GOLPE2_FRAME1
            limite_frame2 = GOLPE2_FRAME1 + GOLPE2_FRAME2

        else:

            limite_frame1 = GOLPE3_FRAME1
            limite_frame2 = GOLPE3_FRAME1 + GOLPE3_FRAME2


        # ====================================================
        # ANIMAÇÃO DO GOLPE
        # ====================================================

        if self.tempo_ataque <= limite_frame1:
            self.frame_ataque=0
        else:
            self.frame_ataque=1


        # ====================================================
        # HITBOX DO ATAQUE
        # ====================================================

        if self.frame_ataque == 1 and not self.hit_aplicado:

            if self.direcao == 1:
                espada_x = self.x + 16
            else:
                espada_x = self.x - 16


            if self.golpe == 1 or self.golpe == 3:
                espada_y = self.y + 6
            else:
                espada_y = self.y - 8


            # A hitbox da espada é metade do sprite: 8x16.
            # Sempre usamos a metade mais distante do Bluu.
            if self.direcao == 1:
                hitbox_espada_x = espada_x + 8
            else:
                hitbox_espada_x = espada_x - 8

            hitbox_espada_y = espada_y
            hitbox_espada_largura = 8
            hitbox_espada_altura = 16

            colisao_luxur = (
                hitbox_espada_x < self.luxur.x + HITBOX_COLISAO_LUXUR_OFFSET_X + HITBOX_COLISAO_LUXUR_LARGURA
                and
                hitbox_espada_x + hitbox_espada_largura > self.luxur.x + HITBOX_COLISAO_LUXUR_OFFSET_X
                and
                hitbox_espada_y < self.luxur.y + HITBOX_COLISAO_LUXUR_OFFSET_Y + HITBOX_COLISAO_LUXUR_ALTURA
                and
                hitbox_espada_y + hitbox_espada_altura > self.luxur.y + HITBOX_COLISAO_LUXUR_OFFSET_Y
            )

            colisao_queixo = (
                hitbox_espada_x < self.luxur.x + HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_X + HITBOX_COLISAO_LUXUR_QUEIXO_LARGURA
                and
                hitbox_espada_x + hitbox_espada_largura > self.luxur.x + HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_X
                and
                hitbox_espada_y < self.luxur.y + HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_Y + HITBOX_COLISAO_LUXUR_QUEIXO_ALTURA
                and
                hitbox_espada_y + hitbox_espada_altura > self.luxur.y + HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_Y
            )

            if colisao_luxur or colisao_queixo:

                if self.golpe == 1:
                    dano = DANO_GOLPE1

                elif self.golpe == 2:
                    dano = DANO_GOLPE2

                else:
                    dano = DANO_GOLPE3

                self.luxur.takehit(dano)
                self.hit_aplicado=True


        # ====================================================
        # FIM DO GOLPE
        # ====================================================

        if self.tempo_ataque > limite_frame2:

            self.atacando=False
            self.tempo_ataque=0
            self.frame_ataque=0
            self.hit_aplicado=False


            if self.golpe < 3:

                self.delay_combo = DELAY_ENTRE_GOLPES

            else:

                self.golpe=0
                self.proximo_golpe=False
                self.delay_fim_combo=DELAY_FIM_COMBO


    # ========================================================
    # DESENHO DO PERSONAGEM E DA ESPADA
    # ========================================================

    def show(self):

        if self.sprite_y is not None:

            # Inverte o sprite horizontalmente quando estiver virado para a esquerda.
            sprite_largura = 16 if self.direcao == 1 else -16

            pyxel.blt(
                self.x, self.y,
                0,
                self.frame * 16,
                self.sprite_y,
                sprite_largura, 16,
                0
            )


            if self.atacando:

                # =================================================
                # GOLPE 1 E GOLPE 3
                # =================================================

                if self.golpe == 1 or self.golpe == 3:

                    if self.frame_ataque == 0:

                        if self.direcao == 1:
                            espada_x = self.x + 16
                            espada_largura = 16
                        else:
                            espada_x = self.x - 16
                            espada_largura = -16

                        espada_y = self.y - 8

                        pyxel.blt(
                            espada_x,
                            espada_y,
                            0,
                            32,
                            0,
                            espada_largura,
                            16,
                            0
                        )

                    else:

                        if self.direcao == 1:
                            espada_x = self.x + 16
                            espada_largura = 16
                        else:
                            espada_x = self.x - 16
                            espada_largura = -16

                        espada_y = self.y + 6

                        pyxel.blt(
                            espada_x,
                            espada_y,
                            0,
                            48,
                            0,
                            espada_largura,
                            16,
                            0
                        )


                # =================================================
                # GOLPE 2
                # INVERTIDO NO EIXO Y
                # =================================================

                elif self.golpe == 2:

                    if self.frame_ataque == 0:

                        if self.direcao == 1:
                            espada_x = self.x + 16
                            espada_largura = 16
                        else:
                            espada_x = self.x - 16
                            espada_largura = -16

                        espada_y = self.y + 8

                        pyxel.blt(
                            espada_x,
                            espada_y,
                            0,
                            32,
                            0,
                            espada_largura,
                            -16,
                            0
                        )

                    else:

                        if self.direcao == 1:
                            espada_x = self.x + 16
                            espada_largura = 16
                        else:
                            espada_x = self.x - 16
                            espada_largura = -16

                        espada_y = self.y - 12

                        pyxel.blt(
                            espada_x,
                            espada_y,
                            0,
                            48,
                            0,
                            espada_largura,
                            -16,
                            0
                        )

        else:
            pyxel.rect(self.x, self.y, 10, 10, self.cor)


# ============================================================
# CLASSE DO PROJÉTIL DA REDD
# Controla posição, direção, distância e colisão do tiro.
# ============================================================

class Tiro:
    def __init__(self, x, y, direcao, luxur):
        self.x = x
        self.y = y
        self.direcao = direcao
        self.luxur = luxur
        self.distancia = 0
        self.ativo = True

    def update(self):
        if not self.ativo:
            return

        movimento = VELOCIDADE_TIRO_REDD * self.direcao
        self.x += movimento
        self.distancia += abs(movimento)

        # Some ao atingir as paredes laterais.
        if self.x <= 0 or self.x >= 160:
            self.ativo = False
            return

        # Some depois de percorrer a distância configurada.
        if self.distancia >= DISTANCIA_MAX_TIRO_REDD:
            self.ativo = False
            return

        # A hitbox do tiro é exatamente 1 pixel:
        # o pixel central da esferinha.
        # O offset X depende da direção em que o tiro está viajando.
        if self.direcao == 1:
            ponto_colisao_x = self.x + OFFSET_X_COLISAO_TIRO_REDD_DIREITA
        else:
            ponto_colisao_x = self.x + OFFSET_X_COLISAO_TIRO_REDD_ESQUERDA

        # Hitbox superior exclusiva dos tiros.
        superior_y_cima = (
            self.luxur.y
            + HITBOX_COLISAO_LUXUR_OFFSET_Y
            + OFFSET_Y_SUPERIOR_TIRO_REDD_CIMA
        )

        superior_y_baixo = (
            self.luxur.y
            + HITBOX_COLISAO_LUXUR_OFFSET_Y
            + HITBOX_COLISAO_LUXUR_ALTURA
            + OFFSET_Y_SUPERIOR_TIRO_REDD_BAIXO
        )

        colisao_superior = (
            ponto_colisao_x >= self.luxur.x + HITBOX_COLISAO_LUXUR_OFFSET_X
            and
            ponto_colisao_x < self.luxur.x + HITBOX_COLISAO_LUXUR_OFFSET_X + HITBOX_COLISAO_LUXUR_LARGURA
            and
            self.y >= superior_y_cima
            and
            self.y < superior_y_baixo
        )

        # Hitbox do queixo: somente para tiros, desce o valor configurado.
        queixo_y = (
            self.luxur.y
            + HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_Y
            + OFFSET_Y_QUEIXO_TIRO_REDD
        )

        colisao_queixo = (
            ponto_colisao_x >= self.luxur.x + HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_X
            and
            ponto_colisao_x < self.luxur.x + HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_X + HITBOX_COLISAO_LUXUR_QUEIXO_LARGURA
            and
            self.y >= queixo_y
            and
            self.y < queixo_y + HITBOX_COLISAO_LUXUR_QUEIXO_ALTURA
        )

        if colisao_superior or colisao_queixo:
            self.luxur.takehit(DANO_TIRO_REDD)
            self.ativo = False

    def show(self):
        if self.ativo:
            pyxel.circ(self.x, self.y, 1, 7)


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
        self.luxur=Vil(80, 60, 500, 2)

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
        self.redd.atira()

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

        # Fundo da barra de HP.
        pyxel.rect(10, 108, 140, 5, 13)

        # Parte vermelha, proporcional ao HP máximo.
        largura_hp = (self.luxur.hp / self.luxur.hpmax) * 140
        pyxel.rect(10, 108, largura_hp, 5, 8)


# Inicia o jogo.
App()
