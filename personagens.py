import pyxel
from config import *
from projetil import Tiro


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
        self.hpmax = 100
        self._hp = self.hpmax
        self.ultimo_dano_recebido = -TEMPO_INVULNERABILIDADE_JOGADOR
        self.ultimo_contato_copia = -TEMPO_INVULNERABILIDADE_JOGADOR
        self.tempo_animacao_dano = 12
        self.knockback_restante = 0.0
        self.direcao_knockback = 0
        self._hp = 100
    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, valor):
        valor_anterior = getattr(self, "_hp", valor)
        self._hp = valor
        # Qualquer redução de HP inicia o knockback sem precisar alterar luxur.py.
        if valor < valor_anterior and hasattr(self, "direcao"):
            self.iniciar_knockback()

    def iniciar_knockback(self):
        # O personagem é lançado para o lado oposto ao que está olhando.
        self.direcao_knockback = -1 if self.direcao == 1 else 1
        self.knockback_restante = DISTANCIA_KNOCKBACK
        self.ultimo_dano_recebido = pyxel.frame_count

    # Move o personagem horizontalmente e verifica colisões.
    def move_lat(self, x):
        self.x += x
        # O sprite do personagem ocupa um retângulo de 16x16.
        # Encostar na borda das hitboxes do Luxur já bloqueia o movimento.
        jogador_esq, jogador_topo = self.x, self.y
        jogador_dir, jogador_base = self.x + 16, self.y + 16

        luxur_esq = self.luxur.x + HITBOX_COLISAO_LUXUR_OFFSET_X
        luxur_topo = self.luxur.y + HITBOX_COLISAO_LUXUR_OFFSET_Y
        luxur_dir = luxur_esq + HITBOX_COLISAO_LUXUR_LARGURA
        luxur_base = luxur_topo + HITBOX_COLISAO_LUXUR_ALTURA
        colisao_luxur = (
            jogador_esq <= luxur_dir and jogador_dir >= luxur_esq
            and jogador_topo <= luxur_base and jogador_base >= luxur_topo
        )

        queixo_esq = self.luxur.x + HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_X
        queixo_topo = self.luxur.y + HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_Y
        queixo_dir = queixo_esq + HITBOX_COLISAO_LUXUR_QUEIXO_LARGURA
        queixo_base = queixo_topo + HITBOX_COLISAO_LUXUR_QUEIXO_ALTURA
        colisao_queixo = (
            jogador_esq <= queixo_dir and jogador_dir >= queixo_esq
            and jogador_topo <= queixo_base and jogador_base >= queixo_topo
        )
        if colisao_luxur or colisao_queixo:
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
        # O sprite do personagem ocupa um retângulo de 16x16.
        # Encostar na borda das hitboxes do Luxur já bloqueia o movimento.
        jogador_esq, jogador_topo = self.x, self.y
        jogador_dir, jogador_base = self.x + 16, self.y + 16

        luxur_esq = self.luxur.x + HITBOX_COLISAO_LUXUR_OFFSET_X
        luxur_topo = self.luxur.y + HITBOX_COLISAO_LUXUR_OFFSET_Y
        luxur_dir = luxur_esq + HITBOX_COLISAO_LUXUR_LARGURA
        luxur_base = luxur_topo + HITBOX_COLISAO_LUXUR_ALTURA
        colisao_luxur = (
            jogador_esq <= luxur_dir and jogador_dir >= luxur_esq
            and jogador_topo <= luxur_base and jogador_base >= luxur_topo
        )

        queixo_esq = self.luxur.x + HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_X
        queixo_topo = self.luxur.y + HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_Y
        queixo_dir = queixo_esq + HITBOX_COLISAO_LUXUR_QUEIXO_LARGURA
        queixo_base = queixo_topo + HITBOX_COLISAO_LUXUR_QUEIXO_ALTURA
        colisao_queixo = (
            jogador_esq <= queixo_dir and jogador_dir >= queixo_esq
            and jogador_topo <= queixo_base and jogador_base >= queixo_topo
        )
        if colisao_luxur or colisao_queixo:
            self.y -= y

        if self.colide is True and (self.y >= 91 or self.y <= 0):
            self.y -= y
        elif self.colide is False:
            if self.y <= -16:
                self.y = 120
            elif self.y >= 120:
                self.y = -16
    # Lê as teclas de movimento e atualiza a animação de caminhada.
    def walk(self):
        andando = False
        # Durante o knockback, o movimento é automático e bloqueia os controles.
        if self.knockback_restante > 0:
            velocidade = max(0.1, VELOCIDADE_KNOCKBACK)
            deslocamento = min(velocidade, self.knockback_restante)
            self.x += self.direcao_knockback * deslocamento
            self.knockback_restante -= deslocamento
            self.x = max(0, min(160 - 16, self.x))
            self.frame = 0
            return
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
                hitbox_espada_x = espada_x + HITBOX_ESPADA_OFFSET_X_DIREITA
            else:
                hitbox_espada_x = espada_x + HITBOX_ESPADA_OFFSET_X_ESQUERDA
            hitbox_espada_y = espada_y + HITBOX_ESPADA_OFFSET_Y
            hitbox_espada_largura = HITBOX_ESPADA_LARGURA
            hitbox_espada_altura = HITBOX_ESPADA_ALTURA
            colisao_luxur = (
                hitbox_espada_x <= self.luxur.x + HITBOX_COLISAO_LUXUR_OFFSET_X + HITBOX_COLISAO_LUXUR_LARGURA
                and
                hitbox_espada_x + hitbox_espada_largura >= self.luxur.x + HITBOX_COLISAO_LUXUR_OFFSET_X
                and
                hitbox_espada_y <= self.luxur.y + HITBOX_COLISAO_LUXUR_OFFSET_Y + HITBOX_COLISAO_LUXUR_ALTURA
                and
                hitbox_espada_y + hitbox_espada_altura >= self.luxur.y + HITBOX_COLISAO_LUXUR_OFFSET_Y
            )
            colisao_queixo = (
                hitbox_espada_x <= self.luxur.x + HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_X + HITBOX_COLISAO_LUXUR_QUEIXO_LARGURA
                and
                hitbox_espada_x + hitbox_espada_largura >= self.luxur.x + HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_X
                and
                hitbox_espada_y <= self.luxur.y + HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_Y + HITBOX_COLISAO_LUXUR_QUEIXO_ALTURA
                and
                hitbox_espada_y + hitbox_espada_altura >= self.luxur.y + HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_Y
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
            # Durante o knockback e a breve animação de dano, usa o sprite de dano.
            sofrendo_dano = (
                self.knockback_restante > 0
                or pyxel.frame_count - self.ultimo_dano_recebido < self.tempo_animacao_dano
            )
            sprite_largura = 16 if self.direcao == 1 else -16
            if sofrendo_dano:
                sprite_x = 0 if self.sprite_y == 0 else 16
                sprite_y = 32
            else:
                sprite_x = self.frame * 16
                sprite_y = self.sprite_y
            pyxel.blt(
                self.x, self.y,
                0,
                sprite_x,
                sprite_y,
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

        # HITBOX VISUAL DO PERSONAGEM (vermelho vivo para destacar).
        # O contorno e apenas visual; nao altera a logica de colisao.
        tamanho = 16 if self.sprite_y is not None else 10
        #pyxel.rectb(self.x, self.y, tamanho, tamanho, 12)

        # HITBOX ATIVA DO GOLPE DO BLUU (amarelo).
        # Usa as mesmas dimensoes e posicoes da colisao em ataque().
        if self.keys is True and self.atacando and self.frame_ataque == 1 and not self.hit_aplicado:
            espada_x = self.x + 16 if self.direcao == 1 else self.x - 16
            if self.golpe == 1 or self.golpe == 3:
                espada_y = self.y + 6
            else:
                espada_y = self.y - 8

            if self.direcao == 1:
                hitbox_espada_x = espada_x + HITBOX_ESPADA_OFFSET_X_DIREITA
            else:
                hitbox_espada_x = espada_x + HITBOX_ESPADA_OFFSET_X_ESQUERDA
            hitbox_espada_y = espada_y + HITBOX_ESPADA_OFFSET_Y
            #pyxel.rectb(
            #    hitbox_espada_x, hitbox_espada_y,
            #    HITBOX_ESPADA_LARGURA, HITBOX_ESPADA_ALTURA, 10
            #)
# ============================================================
# CLASSE DO PROJÉTIL DA REDD
# Controla posição, direção, distância e colisão do tiro.
# ============================================================
