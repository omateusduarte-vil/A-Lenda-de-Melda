import pyxel
from config import *


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
