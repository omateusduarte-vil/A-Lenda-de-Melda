import pyxel
import random
import math

luxurhpmax = 100
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
DANO_GOLPE1 = 40
DANO_GOLPE2 = 40
DANO_GOLPE3 = 40
# ============================================================
# CONFIGURAÇÃO DO TIRO DA REDD
# ============================================================
VELOCIDADE_TIRO_REDD = 6
DISTANCIA_MAX_TIRO_REDD = 120
MAX_TIROS_REDD = 3
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
# CONFIGURAÇÃO DOS ATAQUES DO LUXUR
DISTANCIA_MINIMA_TELEPORTE = 100
TEMPO_TELEGRAPO_INVESTIDA = 24
# A cada quantos frames alterna entre visível e invisível.
FREQUENCIA_PISCADA_TELEGRAPO = 4
VELOCIDADE_BASE_INVESTIDA = 4
VELOCIDADE_MAX_INVESTIDA = 5
TEMPO_RECUPERACAO_INVESTIDA = 4
LIMITE_FASE_2_INVESTIDA = 0.70
LIMITE_FASE_3_INVESTIDA = 0.40

# ============================================================
# CONFIGURAÇÃO DOS PILARES DE FOGO — valores em frames
# Largura em pixels; o telégrafo pisca antes de cada pilar subir.
# ============================================================
LARGURA_PILAR_FASE_1 = 8
TEMPO_TELEGRAFO_PILAR_FASE_1 = 30
QUANTIDADE_PILARES_FASE_1 = 3
TEMPO_ATIVO_PILAR_FASE_1 = 35

LARGURA_PILAR_FASE_2 = 10
TEMPO_TELEGRAFO_PILAR_FASE_2 = 30
QUANTIDADE_PILARES_FASE_2 = 4
TEMPO_ATIVO_PILAR_FASE_2 = 40

LARGURA_PILAR_FASE_3 = 12
TEMPO_TELEGRAFO_PILAR_FASE_3 = 20
QUANTIDADE_PILARES_FASE_3 = 5
TEMPO_ATIVO_PILAR_FASE_3 = 45

FREQUENCIA_PISCADA_PILAR = 4
TEMPO_RECUPERACAO_PILARES = 20
DANO_PILAR = 10
ALTURA_TELEGRAFO_PILAR = 5
Y_CHAO_PILARES = 101

# ============================================================
# CONFIGURAÇÃO DAS BOLAS DE FOGO — valores em frames
# Todos os controles são independentes por fase.
# ============================================================
QUANTIDADE_BOLAS_FASE_1 = 12
VELOCIDADE_BOLAS_FASE_1 = 1.5
QUANTIDADE_RAJADAS_FASE_1 = 1
INTERVALO_RAJADAS_FASE_1 = 20
TEMPO_TELEGRAFO_BOLAS_FASE_1 = 45

QUANTIDADE_BOLAS_FASE_2 = 12
VELOCIDADE_BOLAS_FASE_2 = 1.8
QUANTIDADE_RAJADAS_FASE_2 = 2
INTERVALO_RAJADAS_FASE_2 = 18
TEMPO_TELEGRAFO_BOLAS_FASE_2 = 38

QUANTIDADE_BOLAS_FASE_3 = 12
VELOCIDADE_BOLAS_FASE_3 = 2.2
QUANTIDADE_RAJADAS_FASE_3 = 3
INTERVALO_RAJADAS_FASE_3 = 14
TEMPO_TELEGRAFO_BOLAS_FASE_3 = 30

RAIO_BOLA_FOGO = 2
TEMPO_RECUPERACAO_BOLAS = 30
# ============================================================
# CONFIGURAÇÃO DA MULTIPLICAÇÃO — valores em frames
# Cada fase tem seu próprio intervalo entre ondas.
# ============================================================
QUANTIDADE_LUXURS_VERTICAIS_FASE_1 = 2
QUANTIDADE_LUXURS_VERTICAIS_FASE_2 = 2
QUANTIDADE_LUXURS_VERTICAIS_FASE_3 = 2

QUANTIDADE_LUXURS_HORIZONTAIS_FASE_1 = 0
QUANTIDADE_LUXURS_HORIZONTAIS_FASE_2 = 2
QUANTIDADE_LUXURS_HORIZONTAIS_FASE_3 = 2

# Tempo que cada clone espera depois de aparecer antes de começar a se mover (frames).
TEMPO_ESPERA_CLONE = 30

DELAY_ENTRE_ONDAS_FASE_1 = 4
DELAY_ENTRE_ONDAS_FASE_2 = 4
DELAY_ENTRE_ONDAS_FASE_3 = 4

VELOCIDADE_ONDA_VERTICAL_FASE_1 = 3
VELOCIDADE_ONDA_VERTICAL_FASE_2 = 4
VELOCIDADE_ONDA_VERTICAL_FASE_3 = 5

VELOCIDADE_ONDA_HORIZONTAL_FASE_1 = 3
VELOCIDADE_ONDA_HORIZONTAL_FASE_2 = 4
VELOCIDADE_ONDA_HORIZONTAL_FASE_3 = 5

QUANTIDADE_MAX_COPIAS_ONDA_FINAL_FASE_3 = (
    2 * QUANTIDADE_LUXURS_VERTICAIS_FASE_3
    + 2 * QUANTIDADE_LUXURS_HORIZONTAIS_FASE_3
)
INTERVALO_COPIAS_ONDA_FINAL_FASE_3 = 3
VELOCIDADE_COPIAS_ONDA_FINAL_FASE_3 = 2.5
FREQUENCIA_PISCADA_COPIAS = 1
TEMPO_RECUPERACAO_MULTIPLICACAO = 30
DANO_CONTATO_COPIA = 10
DANO_CONTATO_LUXUR = 10
DANO_BOLA_FOGO = 10
TEMPO_INVULNERABILIDADE_JOGADOR = 30

# Distribuição temporária dos ataques: 2 investidas, 2 pilares e 6 rajadas de bolas de fogo.
TABELA_ATAQUES_LUXUR = {
    0: "investida",
    1: "investida",
    2: "pilares",
    3: "pilares",
    4: "bolas_fogo",
    5: "bolas_fogo",
    6: "bolas de fogo",
    7: "multiplicacao",
    8: "multiplicacao",
    9: "investida",
}
# HITBOX DE COLISÃO DO LUXUR
# ============================================================
# Retângulo superior
HITBOX_COLISAO_LUXUR_LARGURA = 32
HITBOX_COLISAO_LUXUR_ALTURA = 26
HITBOX_COLISAO_LUXUR_OFFSET_X = -15
HITBOX_COLISAO_LUXUR_OFFSET_Y = -17
# Retângulo inferior / queixo
HITBOX_COLISAO_LUXUR_QUEIXO_LARGURA = 16
HITBOX_COLISAO_LUXUR_QUEIXO_ALTURA = 16
HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_X = -7
HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_Y = 0
# ============================================================

# Configuração do efeito de knockback.
DISTANCIA_KNOCKBACK = 24
VELOCIDADE_KNOCKBACK = 3

# HITBOX DA ESPADA DO BLUU — dimensões e deslocamentos em pixels.
# Altere estes valores para ajustar a colisão e o contorno amarelo juntos.
HITBOX_ESPADA_LARGURA = 16
HITBOX_ESPADA_ALTURA = 16
HITBOX_ESPADA_OFFSET_X_DIREITA = 8
HITBOX_ESPADA_OFFSET_X_ESQUERDA = -8
HITBOX_ESPADA_OFFSET_Y = 0
