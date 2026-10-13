import pyxel
import random
import math
from config import *

# Permite configurar o tempo de espera dos clones no config.py.
TEMPO_ESPERA_CLONE = globals().get("TEMPO_ESPERA_CLONE", 0)


class Vil:
    # Cria o Luxur e define seu HP máximo e atual.
    def __init__(self, x, y, hpmax, cor):
        self.x=x
        self.y=y
        self.hpmax=hpmax
        self.hp=hpmax
        self.cor=cor
        # Estado e temporizador do ciclo de ataques.
        self.estado_ataque = "inicial"
        self.temporizador_ataque = 0
        # Rotação inicial do Luxur enquanto estiver com HP cheio.
        self.angulo_giro_inicial = 0.0
        self.velocidade_giro_inicial = 12.0  # graus por quadro
        self.giro_multiplicacao_ativo = False
        self.direcao_investida = 1
        self.direcao_x_investida = 1.0
        self.direcao_y_investida = 0.0
        self.fase_investida = 1
        self.investidas_restantes = 0
        self.velocidade_investida = VELOCIDADE_BASE_INVESTIDA
        self.numero_ataque = None
        self.pilares = []
        self.fase_pilares = 1
        self.angulo_giro = 0
        self.ataque_atual = ""
        self.bolas_fogo = []
        self.fase_bolas = 1
        self.bolas_por_rajada = 12
        self.velocidade_bolas = 1.5
        self.rajadas_total = 1
        self.rajadas_disparadas = 0
        self.intervalo_rajadas = 20
        self.tempo_telegrafo_bolas = 45
        # -1 = olho esquerdo, 1 = olho direito, 0 = boca.
        self.origem_telegrafo_bolas = -1
        self.copias_luxur = []
        self.ondas_multiplicacao = []
        self.ordem_ondas_multiplicacao = []
        self.indice_onda_multiplicacao = 0
        self.fase_multiplicacao = 1
        self.velocidade_multiplicacao = 1.5
        self.delay_ondas_multiplicacao = 20
        self.fila_copias_finais = []
        self.temporizador_spawn_copia = 0
        self.dano_contato_aplicado = {}
        # CONTROLES TEMPORÁRIOS DAS HITBOXES (largura/altura em pixels).
        # offset_x/offset_y deslocam a hitbox em relação ao centro/origem.
        # Os valores iniciais reproduzem as dimensões usadas nas colisões originais.
        self.mostrar_hitboxes = True
        self.hitboxes = {
            "contato_luxur": {"largura": 40, "altura": 40, "offset_x": -20, "offset_y": -20},
            "bola_fogo": {"largura": 2 * (RAIO_BOLA_FOGO + 2), "altura": 2 * (RAIO_BOLA_FOGO + 2), "offset_x": 0, "offset_y": 0},
            "pilar": {"largura": None, "altura": Y_CHAO_PILARES, "offset_x": 0, "offset_y": 0},
            "clone": {"largura": 16, "altura": 16, "offset_x": -8, "offset_y": -8},
        }
        # Movimento aleatório do Luxur durante a multiplicação.
        self.direcao_movimento_aleatorio = random.choice([
            (-1, -1), (-1, 0), (-1, 1), (0, -1),
            (0, 1), (1, -1), (1, 0), (1, 1)
        ])
        self.tempo_movimento_aleatorio = random.randint(12, 28)
    # Verifica se o Luxur ainda está vivo.
    def alive(self):
        return self.hp > 0
    def teleportar(self):
        melhor_posicao = None
        maior_distancia = -1
        for _ in range(100):
            x = random.randint(30, 130)
            y = random.randint(30, 80)
            distancia_bluu = (x - self.app.bluu.x) ** 2 + (y - self.app.bluu.y) ** 2
            distancia_redd = (x - self.app.redd.x) ** 2 + (y - self.app.redd.y) ** 2
            distancia = min(distancia_bluu, distancia_redd)
            if distancia > maior_distancia:
                maior_distancia = distancia
                melhor_posicao = (x, y)
            if distancia >= DISTANCIA_MINIMA_TELEPORTE ** 2:
                self.x = x
                self.y = y
                return
        self.x, self.y = melhor_posicao
    def escolher_ataque(self):
        self.numero_ataque = random.randint(0, 9)
        return TABELA_ATAQUES_LUXUR[self.numero_ataque]
    # O teleporte é independente da lógica de cada golpe.
    def iniciar_ciclo_ataque(self):
        self.teleportar()
        ataque = self.escolher_ataque()
        self.ataque_atual = ataque
        if ataque == "investida":
            self.iniciar_investida()
        elif ataque == "pilares":
            self.iniciar_pilares()
        elif ataque == "bolas_fogo":
            self.iniciar_bolas_fogo()
        elif ataque == "multiplicacao":
            self.iniciar_multiplicacao()

    def iniciar_bolas_fogo(self):
        proporcao_hp = self.hp / self.hpmax
        if proporcao_hp > LIMITE_FASE_2_INVESTIDA:
            self.fase_bolas = 1
            self.bolas_por_rajada = QUANTIDADE_BOLAS_FASE_1
            self.velocidade_bolas = VELOCIDADE_BOLAS_FASE_1
            self.rajadas_total = QUANTIDADE_RAJADAS_FASE_1
            self.intervalo_rajadas = INTERVALO_RAJADAS_FASE_1
            self.tempo_telegrafo_bolas = TEMPO_TELEGRAFO_BOLAS_FASE_1
        elif proporcao_hp >= LIMITE_FASE_3_INVESTIDA:
            self.fase_bolas = 2
            self.bolas_por_rajada = QUANTIDADE_BOLAS_FASE_2
            self.velocidade_bolas = VELOCIDADE_BOLAS_FASE_2
            self.rajadas_total = QUANTIDADE_RAJADAS_FASE_2
            self.intervalo_rajadas = INTERVALO_RAJADAS_FASE_2
            self.tempo_telegrafo_bolas = TEMPO_TELEGRAFO_BOLAS_FASE_2
        else:
            self.fase_bolas = 3
            self.bolas_por_rajada = QUANTIDADE_BOLAS_FASE_3
            self.velocidade_bolas = VELOCIDADE_BOLAS_FASE_3
            self.rajadas_total = QUANTIDADE_RAJADAS_FASE_3
            self.intervalo_rajadas = INTERVALO_RAJADAS_FASE_3
            self.tempo_telegrafo_bolas = TEMPO_TELEGRAFO_BOLAS_FASE_3

        self.rajadas_disparadas = 0
        self.definir_origem_telegrafo_bolas()
        self.temporizador_ataque = self.tempo_telegrafo_bolas
        self.estado_ataque = "preparando_bolas"

    def definir_origem_telegrafo_bolas(self):
        # Indica visualmente de onde sairá a próxima rajada.
        if self.fase_bolas == 1:
            self.origem_telegrafo_bolas = random.choice([-1, 1])
        elif self.fase_bolas == 2:
            self.origem_telegrafo_bolas = -1 if self.rajadas_disparadas == 0 else 1
        else:
            if self.rajadas_disparadas == 0:
                self.origem_telegrafo_bolas = -1
            elif self.rajadas_disparadas == 1:
                self.origem_telegrafo_bolas = 1
            else:
                self.origem_telegrafo_bolas = 0

    def disparar_rajada_bolas(self):
        # Fase 1: um olho escolhido aleatoriamente.
        # Fase 2: os dois olhos, em rajadas separadas.
        # Fase 3: olho esquerdo, olho direito e centro da boca.
        if self.fase_bolas == 1:
            origens = [(-5, -1)] if self.origem_telegrafo_bolas == -1 else [(5, -1)]
        elif self.fase_bolas == 2:
            origens = [(-5, -1), (5, -1)]
            origem = origens[min(self.rajadas_disparadas, 1)]
            origens = [origem]
        else:
            origens = [(-5, -1), (5, -1), (0, 5)]
            origem = origens[min(self.rajadas_disparadas, 2)]
            origens = [origem]

        for origem_x, origem_y in origens:
            centro_x = self.x + origem_x
            centro_y = self.y + origem_y
            quantidade = max(1, self.bolas_por_rajada)
            for i in range(quantidade):
                angulo = (2 * math.pi * i / quantidade) - math.pi / 2
                self.bolas_fogo.append({
                    "x": float(centro_x),
                    "y": float(centro_y),
                    "dx": math.cos(angulo) * self.velocidade_bolas,
                    "dy": math.sin(angulo) * self.velocidade_bolas,
                    "ativa": True,
                })
        self.rajadas_disparadas += 1

    def iniciar_multiplicacao(self):
        """Prepara as ondas; só o objeto self continua sendo o Luxur verdadeiro."""
        proporcao_hp = self.hp / self.hpmax
        if proporcao_hp > LIMITE_FASE_2_INVESTIDA:
            self.fase_multiplicacao = 1
        elif proporcao_hp >= LIMITE_FASE_3_INVESTIDA:
            self.fase_multiplicacao = 2
        else:
            self.fase_multiplicacao = 3

        fase = self.fase_multiplicacao
        if fase == 1:
            qtd_v = QUANTIDADE_LUXURS_VERTICAIS_FASE_1
            qtd_h = 0
            self.delay_ondas_multiplicacao = DELAY_ENTRE_ONDAS_FASE_1
            vel_v = VELOCIDADE_ONDA_VERTICAL_FASE_1
            vel_h = VELOCIDADE_ONDA_HORIZONTAL_FASE_1
        elif fase == 2:
            qtd_v = QUANTIDADE_LUXURS_VERTICAIS_FASE_2
            qtd_h = QUANTIDADE_LUXURS_HORIZONTAIS_FASE_2
            self.delay_ondas_multiplicacao = DELAY_ENTRE_ONDAS_FASE_2
            vel_v = VELOCIDADE_ONDA_VERTICAL_FASE_2
            vel_h = VELOCIDADE_ONDA_HORIZONTAL_FASE_2
        else:
            qtd_v = QUANTIDADE_LUXURS_VERTICAIS_FASE_3
            qtd_h = QUANTIDADE_LUXURS_HORIZONTAIS_FASE_3
            self.delay_ondas_multiplicacao = DELAY_ENTRE_ONDAS_FASE_3
            vel_v = VELOCIDADE_ONDA_VERTICAL_FASE_3
            vel_h = VELOCIDADE_ONDA_HORIZONTAL_FASE_3

        self.copias_luxur = []
        self.ondas_multiplicacao = []
        self.fila_copias_finais = []
        self.indice_onda_multiplicacao = 0

        # Todos os Luxurs verticais aparecem juntos: os que vêm de cima
        # e os que vêm de baixo fazem parte da mesma onda.
        onda_vertical = (
            self.criar_onda_multiplicacao("vertical", "baixo", qtd_v, vel_v)
            + self.criar_onda_multiplicacao("vertical", "cima", qtd_v, vel_v)
        )
        self.ondas_multiplicacao.append(onda_vertical)

        # Nas fases 2/3, todos os Luxurs horizontais também aparecem juntos:
        # os que vêm da esquerda e os que vêm da direita formam uma única onda.
        if fase >= 2 and qtd_h > 0:
            onda_horizontal = (
                self.criar_onda_multiplicacao("horizontal", "direita", qtd_h, vel_h)
                + self.criar_onda_multiplicacao("horizontal", "esquerda", qtd_h, vel_h)
            )
            self.ondas_multiplicacao.append(onda_horizontal)

        self.ordem_ondas_multiplicacao = list(range(len(self.ondas_multiplicacao)))
        random.shuffle(self.ordem_ondas_multiplicacao)
        self.temporizador_ataque = 0
        # Uma volta completa usando o mesmo giro visual antes dos clones.
        self.angulo_giro_inicial = 0.0
        self.giro_multiplicacao_ativo = True
        self.estado_ataque = "telegrafo_multiplicacao"

    def criar_onda_multiplicacao(self, tipo, sentido, quantidade, velocidade):
        copias = []
        quantidade = max(0, int(quantidade))
        if quantidade == 0:
            return copias
        if tipo == "vertical":
            espacamento = 160 / (quantidade + 1)
            for i in range(quantidade):
                x = espacamento * (i + 1)
                y = -22 if sentido == "baixo" else 142
                dy = velocidade if sentido == "baixo" else -velocidade
                copias.append({
                    "x": float(x), "y": float(y), "dx": 0.0, "dy": dy,
                    "ativa": False, "tipo": tipo, "sentido": sentido,
                })
        else:
            espacamento = 100 / (quantidade + 1)
            for i in range(quantidade):
                y = 15 + espacamento * (i + 1)
                x = -22 if sentido == "direita" else 182
                dx = velocidade if sentido == "direita" else -velocidade
                copias.append({
                    "x": float(x), "y": float(y), "dx": dx, "dy": 0.0,
                    "ativa": False, "tipo": tipo, "sentido": sentido,
                })
        return copias

    def ativar_onda_multiplicacao(self):
        if self.indice_onda_multiplicacao >= len(self.ordem_ondas_multiplicacao):
            if self.fase_multiplicacao == 3:
                self.iniciar_onda_final_multiplicacao()
            else:
                self.estado_ataque = "recuperando_multiplicacao"
                self.temporizador_ataque = TEMPO_RECUPERACAO_MULTIPLICACAO
            return

        indice = self.ordem_ondas_multiplicacao[self.indice_onda_multiplicacao]
        onda = self.ondas_multiplicacao[indice]
        for copia in onda:
            copia["ativa"] = True
            copia["espera"] = TEMPO_ESPERA_CLONE
            self.copias_luxur.append(copia)
        self.indice_onda_multiplicacao += 1
        self.estado_ataque = "multiplicacao_onda_ativa"

    def iniciar_onda_final_multiplicacao(self):
        # Na fase 3, o limite é a soma das quatro ondas anteriores.
        quantidade = (
            2 * QUANTIDADE_LUXURS_VERTICAIS_FASE_3
            + 2 * QUANTIDADE_LUXURS_HORIZONTAIS_FASE_3
        )
        quantidade = min(
            quantidade, QUANTIDADE_MAX_COPIAS_ONDA_FINAL_FASE_3
        )
        lados = ["cima", "baixo", "esquerda", "direita"]
        self.fila_copias_finais = []
        for _ in range(max(0, quantidade)):
            lado = random.choice(lados)
            if lado == "cima":
                x, y = random.randint(5, 155), -20
            elif lado == "baixo":
                x, y = random.randint(5, 155), 140
            elif lado == "esquerda":
                x, y = -20, random.randint(5, 100)
            else:
                x, y = 180, random.randint(5, 100)
            alvo = random.choice([self.app.bluu, self.app.redd])
            dx, dy = alvo.x - x, alvo.y - y
            distancia = math.hypot(dx, dy) or 1
            self.fila_copias_finais.append({
                "x": float(x), "y": float(y),
                "dx": dx / distancia * VELOCIDADE_COPIAS_ONDA_FINAL_FASE_3,
                "dy": dy / distancia * VELOCIDADE_COPIAS_ONDA_FINAL_FASE_3,
                "ativa": False, "tipo": "final", "sentido": "alvo",
            })
        self.temporizador_spawn_copia = 0
        self.estado_ataque = "multiplicacao_final"

    def mover_aleatoriamente_durante_multiplicacao(self):
        # O Luxur verdadeiro passeia pela arena enquanto os clones atacam.
        self.tempo_movimento_aleatorio -= 1
        if self.tempo_movimento_aleatorio <= 0:
            self.direcao_movimento_aleatorio = random.choice([
                (-1, -1), (-1, 0), (-1, 1), (0, -1),
                (0, 1), (1, -1), (1, 0), (1, 1)
            ])
            self.tempo_movimento_aleatorio = random.randint(12, 28)

        dx, dy = self.direcao_movimento_aleatorio
        velocidade = 1.5
        novo_x = self.x + dx * velocidade
        novo_y = self.y + dy * velocidade
        # Mesmos limites de movimento do Bluu: x entre 0 e 150, y entre 0 e 91.
        if novo_x < 0 or novo_x > 150:
            dx *= -1
            novo_x = self.x + dx * velocidade
        if novo_y < 0 or novo_y > 91:
            dy *= -1
            novo_y = self.y + dy * velocidade
        self.direcao_movimento_aleatorio = (dx, dy)
        self.x = max(0, min(150, novo_x))
        self.y = max(0, min(91, novo_y))

    def atualizar_multiplicacao(self):
        self.mover_aleatoriamente_durante_multiplicacao()
        if self.estado_ataque == "multiplicacao_ondas":
            if self.temporizador_ataque > 0:
                self.temporizador_ataque -= 1
            else:
                self.ativar_onda_multiplicacao()
            return

        if self.estado_ataque == "multiplicacao_onda_ativa":
            # Só a onda atual se move. As cópias da mesma onda avançam juntas.
            onda_index = self.ordem_ondas_multiplicacao[self.indice_onda_multiplicacao - 1]
            onda = self.ondas_multiplicacao[onda_index]
            terminou = True
            for copia in onda:
                if copia["ativa"]:
                    if copia.get("espera", 0) > 0:
                        copia["espera"] -= 1
                        terminou = False
                        continue
                    copia["x"] += copia["dx"]
                    copia["y"] += copia["dy"]
                    if -28 <= copia["x"] <= 188 and -28 <= copia["y"] <= 148:
                        terminou = False
            if terminou:
                self.temporizador_ataque = self.delay_ondas_multiplicacao
                self.estado_ataque = "multiplicacao_ondas"
            return

        if self.estado_ataque == "multiplicacao_final":
            self.temporizador_spawn_copia -= 1
            if self.fila_copias_finais and self.temporizador_spawn_copia <= 0:
                copia = self.fila_copias_finais.pop(0)
                copia["ativa"] = True
                copia["espera"] = TEMPO_ESPERA_CLONE
                self.copias_luxur.append(copia)
                self.temporizador_spawn_copia = INTERVALO_COPIAS_ONDA_FINAL_FASE_3
            for copia in self.copias_luxur:
                if copia.get("tipo") == "final" and copia["ativa"]:
                    if copia.get("espera", 0) > 0:
                        copia["espera"] -= 1
                        continue
                    copia["x"] += copia["dx"]
                    copia["y"] += copia["dy"]
            if not self.fila_copias_finais and not any(
                c.get("tipo") == "final" and c["ativa"]
                and (c.get("espera", 0) > 0 or
                     (-28 <= c["x"] <= 188 and -28 <= c["y"] <= 148))
                for c in self.copias_luxur
            ):
                self.estado_ataque = "recuperando_multiplicacao"
                self.temporizador_ataque = TEMPO_RECUPERACAO_MULTIPLICACAO
            return

        if self.estado_ataque == "recuperando_multiplicacao":
            self.temporizador_ataque -= 1
            if self.temporizador_ataque <= 0:
                self.copias_luxur = []
                self.estado_ataque = "inicial"

    def jogador_pode_receber_dano(self, jogador):
        return (
            pyxel.frame_count - jogador.ultimo_dano_recebido
            >= TEMPO_INVULNERABILIDADE_JOGADOR
        )

    def causar_dano_jogador(self, jogador, dano):
        if self.jogador_pode_receber_dano(jogador):
            jogador.ultimo_dano_recebido = pyxel.frame_count
            jogador.ultimo_contato_copia = pyxel.frame_count
            jogador.hp = max(0, jogador.hp - dano)
            return True
        return False

    def atualizar_colisoes_copias(self):
        # Todas as colisões usam retângulos completos; tocar a borda conta.
        # Os clones causam dano de contato, mas não recebem dano dos jogadores.
        for jogador in (self.app.bluu, self.app.redd):
            jogador_esq = jogador.x
            jogador_topo = jogador.y
            jogador_dir = jogador_esq + 16
            jogador_base = jogador_topo + 16
            for copia in self.copias_luxur:
                if not copia["ativa"]:
                    continue
                hb = self.hitboxes["clone"]
                esquerda = copia["x"] + hb["offset_x"]
                topo = copia["y"] + hb["offset_y"]
                direita = esquerda + hb["largura"]
                base = topo + hb["altura"]
                if (jogador_esq <= direita and jogador_dir >= esquerda
                        and jogador_topo <= base and jogador_base >= topo):
                    self.causar_dano_jogador(jogador, DANO_CONTATO_COPIA)
                    break

    def atualizar_colisoes_jogadores(self):
        # O dano acontece quando os retângulos se sobrepõem ou apenas se encostam.
        for jogador in (self.app.bluu, self.app.redd):
            jogador_esq = jogador.x
            jogador_topo = jogador.y
            jogador_dir = jogador_esq + 16
            jogador_base = jogador_topo + 16

            # Contato com o Luxur: usa as mesmas duas hitboxes azuis
            # desenhadas e usadas para bloquear o movimento.
            hitboxes_contato = (
                (
                    self.x + HITBOX_COLISAO_LUXUR_OFFSET_X,
                    self.y + HITBOX_COLISAO_LUXUR_OFFSET_Y,
                    HITBOX_COLISAO_LUXUR_LARGURA,
                    HITBOX_COLISAO_LUXUR_ALTURA,
                ),
                (
                    self.x + HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_X,
                    self.y + HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_Y,
                    HITBOX_COLISAO_LUXUR_QUEIXO_LARGURA,
                    HITBOX_COLISAO_LUXUR_QUEIXO_ALTURA,
                ),
            )
            tocou_luxur = False
            for esquerda, topo, largura, altura in hitboxes_contato:
                direita = esquerda + largura
                base = topo + altura
                if (jogador_esq <= direita and jogador_dir >= esquerda
                        and jogador_topo <= base and jogador_base >= topo):
                    tocou_luxur = True
                    break
            if tocou_luxur:
                self.causar_dano_jogador(jogador, DANO_CONTATO_LUXUR)
                continue

            # Bola de fogo: colisão retângulo-retângulo, igual à hitbox desenhada.
            atingido_bola = False
            hb = self.hitboxes["bola_fogo"]
            for bola in self.bolas_fogo:
                if not bola["ativa"]:
                    continue
                esquerda = bola["x"] + hb["offset_x"] - hb["largura"] / 2
                topo = bola["y"] + hb["offset_y"] - hb["altura"] / 2
                direita = esquerda + hb["largura"]
                base = topo + hb["altura"]
                if (jogador_esq <= direita and jogador_dir >= esquerda
                        and jogador_topo <= base and jogador_base >= topo):
                    self.causar_dano_jogador(jogador, DANO_BOLA_FOGO)
                    atingido_bola = True
                    break
            if atingido_bola:
                continue

            # Só os pilares ativos causam dano; o telégrafo é apenas um aviso.
            for pilar in self.pilares:
                if pilar["estado"] != "ativo":
                    continue
                hb = self.hitboxes["pilar"]
                largura = pilar["largura"] if hb["largura"] is None else hb["largura"]
                esquerda = pilar["x"] + hb["offset_x"]
                topo = hb["offset_y"]
                direita = esquerda + largura
                base = topo + hb["altura"]
                if (jogador_esq <= direita and jogador_dir >= esquerda
                        and jogador_topo <= base and jogador_base >= topo):
                    self.causar_dano_jogador(jogador, DANO_PILAR)
                    break

    def iniciar_pilares(self):
        proporcao_hp = self.hp / self.hpmax
        if proporcao_hp > LIMITE_FASE_2_INVESTIDA:
            self.fase_pilares = 1
            largura = LARGURA_PILAR_FASE_1
            tempo = TEMPO_TELEGRAFO_PILAR_FASE_1
            quantidade = QUANTIDADE_PILARES_FASE_1
            ativo = TEMPO_ATIVO_PILAR_FASE_1
        elif proporcao_hp >= LIMITE_FASE_3_INVESTIDA:
            self.fase_pilares = 2
            largura = LARGURA_PILAR_FASE_2
            tempo = TEMPO_TELEGRAFO_PILAR_FASE_2
            quantidade = QUANTIDADE_PILARES_FASE_2
            ativo = TEMPO_ATIVO_PILAR_FASE_2
        else:
            self.fase_pilares = 3
            largura = LARGURA_PILAR_FASE_3
            tempo = TEMPO_TELEGRAFO_PILAR_FASE_3
            quantidade = QUANTIDADE_PILARES_FASE_3
            ativo = TEMPO_ATIVO_PILAR_FASE_3

        self.pilares = []
        # Evita que dois pilares apareçam praticamente no mesmo lugar.
        posicoes = []
        tentativas = 0
        while len(posicoes) < quantidade and tentativas < quantidade * 30:
            tentativas += 1
            x = random.randint(2, 158 - largura)
            if all(abs(x - anterior) >= largura + 8 for anterior in posicoes):
                posicoes.append(x)
        # Se a tela estiver cheia, completa com posições aleatórias válidas.
        while len(posicoes) < quantidade:
            posicoes.append(random.randint(2, 158 - largura))

        for x in posicoes:
            self.pilares.append({
                "x": x,
                "largura": largura,
                "telegrapho": tempo,
                "ativo": ativo,
                "estado": "aviso",
                "dano_aplicado": set(),
            })
        self.temporizador_ataque = tempo
        self.angulo_giro = 0
        self.estado_ataque = "preparando_pilares"

    def iniciar_investida(self):
        proporcao_hp = self.hp / self.hpmax

        if proporcao_hp > LIMITE_FASE_2_INVESTIDA:
            self.fase_investida = 1
        elif proporcao_hp >= LIMITE_FASE_3_INVESTIDA:
            self.fase_investida = 2
        else:
            self.fase_investida = 3

        self.investidas_restantes = 2 if self.fase_investida == 3 else 1
        self.alvo_primeira_investida = None

        # Na fase 1, a investida continua horizontal.
        # Nas fases 2 e 3, Luxur mira no jogador mais próximo.
        if self.fase_investida == 1:
            jogadores = [self.app.bluu, self.app.redd]
            alvo = min(jogadores, key=lambda jogador: abs(jogador.x - self.x))
            self.direcao_x_investida = 1.0 if alvo.x >= self.x else -1.0
            self.direcao_y_investida = 0.0
        else:
            jogadores = [self.app.bluu, self.app.redd]
            alvo = min(
                jogadores,
                key=lambda jogador: (jogador.x - self.x) ** 2 + (jogador.y - self.y) ** 2
            )
            self.alvo_primeira_investida = alvo
            dx = alvo.x - self.x
            dy = alvo.y - self.y
            distancia = math.hypot(dx, dy)

            if distancia == 0:
                self.direcao_x_investida = 1.0
                self.direcao_y_investida = 0.0
            else:
                self.direcao_x_investida = dx / distancia
                self.direcao_y_investida = dy / distancia

        self.direcao_investida = 1 if self.direcao_x_investida >= 0 else -1
        self.temporizador_ataque = TEMPO_TELEGRAPO_INVESTIDA
        self.estado_ataque = "preparando"

    def update(self):
        if self.hp <= 0:
            return

        # Luxur gira desde o início e só para depois de receber dano.
        # Durante o telégrafo da multiplicação, o giro é controlado abaixo
        # para completar exatamente uma volta antes de liberar os clones.
        estados_multiplicacao = (
            "telegrafo_multiplicacao", "multiplicacao_ondas",
            "multiplicacao_onda_ativa", "multiplicacao_final",
            "recuperando_multiplicacao"
        )
        if (
            self.hp >= self.hpmax
            and not self.giro_multiplicacao_ativo
            and self.estado_ataque not in estados_multiplicacao
        ):
            self.angulo_giro_inicial = (self.angulo_giro_inicial + self.velocidade_giro_inicial) % 360

        if self.estado_ataque == "inicial":
            self.iniciar_ciclo_ataque()
            return

        # Atualiza as bolas de fogo independentemente do estado do Luxur.
        for bola in self.bolas_fogo:
            bola["x"] += bola["dx"]
            bola["y"] += bola["dy"]
            if (bola["x"] < -5 or bola["x"] > 165 or
                    bola["y"] < -5 or bola["y"] > 125):
                bola["ativa"] = False
        self.bolas_fogo = [bola for bola in self.bolas_fogo if bola["ativa"]]

        if self.giro_multiplicacao_ativo:
            self.angulo_giro_inicial += self.velocidade_giro_inicial
            if self.angulo_giro_inicial >= 360:
                self.angulo_giro_inicial = 0.0
                self.giro_multiplicacao_ativo = False
                self.estado_ataque = "multiplicacao_ondas"
            return

        if self.estado_ataque in (
            "multiplicacao_ondas", "multiplicacao_onda_ativa",
            "multiplicacao_final", "recuperando_multiplicacao"
        ):
            self.atualizar_multiplicacao()
            self.atualizar_colisoes_copias()
            return

        if self.estado_ataque == "preparando_bolas":
            self.temporizador_ataque -= 1
            if self.temporizador_ataque <= 0:
                self.disparar_rajada_bolas()
                if self.rajadas_disparadas < self.rajadas_total:
                    self.estado_ataque = "intervalo_bolas"
                    self.temporizador_ataque = self.intervalo_rajadas
                else:
                    self.estado_ataque = "recuperando_bolas"
                    self.temporizador_ataque = TEMPO_RECUPERACAO_BOLAS
            return

        if self.estado_ataque == "intervalo_bolas":
            self.temporizador_ataque -= 1
            if self.temporizador_ataque <= 0:
                self.definir_origem_telegrafo_bolas()
                self.temporizador_ataque = self.tempo_telegrafo_bolas
                self.estado_ataque = "preparando_bolas"
            return

        if self.estado_ataque == "recuperando_bolas":
            self.temporizador_ataque -= 1
            if self.temporizador_ataque <= 0:
                self.estado_ataque = "inicial"
            return

        if self.estado_ataque == "preparando_pilares":
            self.angulo_giro = (self.angulo_giro + 18) % 360
            self.temporizador_ataque -= 1
            if self.temporizador_ataque <= 0:
                for pilar in self.pilares:
                    pilar["estado"] = "ativo"
                self.estado_ataque = "pilares_ativos"
                # Todos os pilares permanecem ativos pelo mesmo tempo.
                self.temporizador_ataque = max(pilar["ativo"] for pilar in self.pilares)
            return

        if self.estado_ataque == "pilares_ativos":
            self.angulo_giro = (self.angulo_giro + 18) % 360
            self.temporizador_ataque -= 1
            if self.temporizador_ataque <= 0:
                self.pilares = []
                self.estado_ataque = "recuperando"
                self.temporizador_ataque = TEMPO_RECUPERACAO_PILARES
            return

        if self.estado_ataque == "preparando":
            self.temporizador_ataque -= 1
            if self.temporizador_ataque <= 0:
                progresso = 1 - (self.hp / self.hpmax)
                self.velocidade_investida = (
                    VELOCIDADE_BASE_INVESTIDA
                    + (VELOCIDADE_MAX_INVESTIDA - VELOCIDADE_BASE_INVESTIDA) * progresso
                )
                self.estado_ataque = "investindo"
            return

        if self.estado_ataque == "investindo":
            proximo_x = self.x + self.velocidade_investida * self.direcao_x_investida
            proximo_y = self.y + self.velocidade_investida * self.direcao_y_investida

            # O Luxur colide com os mesmos limites usados pelo Bluu.
            bateu_parede = (
                proximo_x < 0 or proximo_x > 150
                or proximo_y < 0 or proximo_y > 91
            )
            if bateu_parede:
                self.x = max(0, min(150, proximo_x))
                self.y = max(0, min(91, proximo_y))
                if self.fase_investida == 3 and self.investidas_restantes > 1:
                    # A segunda investida mira no outro personagem.
                    self.investidas_restantes -= 1
                    jogadores = [self.app.bluu, self.app.redd]
                    alvo = next(
                        jogador for jogador in jogadores
                        if jogador is not self.alvo_primeira_investida
                    )
                    dx = alvo.x - self.x
                    dy = alvo.y - self.y
                    distancia = math.hypot(dx, dy)
                    if distancia == 0:
                        self.direcao_x_investida = 1.0
                        self.direcao_y_investida = 0.0
                    else:
                        self.direcao_x_investida = dx / distancia
                        self.direcao_y_investida = dy / distancia
                    self.direcao_investida = 1 if self.direcao_x_investida >= 0 else -1
                else:
                    self.investidas_restantes = 0
                    self.estado_ataque = "recuperando"
                    self.temporizador_ataque = TEMPO_RECUPERACAO_INVESTIDA
            else:
                self.x = proximo_x
                self.y = proximo_y
            return

        if self.estado_ataque == "recuperando":
            self.temporizador_ataque -= 1
            if self.temporizador_ataque <= 0:
                self.estado_ataque = "inicial"

    # Rotaciona pontos em torno do centro da cabeça sem alterar a geometria original.
    def ponto_giro_inicial(self, dx, dy):
        angulo = math.radians(self.angulo_giro_inicial)
        cos_a = math.cos(angulo)
        sin_a = math.sin(angulo)
        return (
            int(round(self.x + dx * cos_a - dy * sin_a)),
            int(round(self.y + dx * sin_a + dy * cos_a)),
        )

    def desenhar_cabeca_giro_inicial(self):
        # Os mesmos tamanhos, formas e offsets do desenho original.
        # Só as posições/orientações são transformadas pelo mesmo ângulo.
        x, y = self.ponto_giro_inicial(0, 0)
        pyxel.circ(x, y, 15, 2)

        x, y = self.ponto_giro_inicial(-15, 15)
        pyxel.circ(x, y, 10, 0)
        x, y = self.ponto_giro_inicial(15, 15)
        pyxel.circ(x, y, 10, 0)

        pontos = [(-10, -10), (-15, -18), (-5, -12)]
        p = [self.ponto_giro_inicial(px, py) for px, py in pontos]
        pyxel.tri(*p[0], *p[1], *p[2], 4)
        pontos = [(10, -10), (15, -18), (5, -12)]
        p = [self.ponto_giro_inicial(px, py) for px, py in pontos]
        pyxel.tri(*p[0], *p[1], *p[2], 4)

        # Retângulos originais viram quadriláteros rotacionados, sem mudar dimensões.
        for dx, dy, largura, altura, cor in (
            (-7, -3, 5, 5, 0),
            (3, -3, 5, 5, 0),
        ):
            pontos = [
                (dx, dy), (dx + largura, dy),
                (dx + largura, dy + altura), (dx, dy + altura),
            ]
            p = [self.ponto_giro_inicial(px, py) for px, py in pontos]
            pyxel.tri(*p[0], *p[1], *p[2], cor)
            pyxel.tri(*p[0], *p[2], *p[3], cor)

        x, y = self.ponto_giro_inicial(-3, -4)
        pyxel.circ(x, y, 3, 2)
        x, y = self.ponto_giro_inicial(3, -4)
        pyxel.circ(x, y, 3, 2)

        x, y = self.ponto_giro_inicial(-5, -1)
        pyxel.circ(x, y, 1, 9)
        x, y = self.ponto_giro_inicial(5, -1)
        pyxel.circ(x, y, 1, 9)

        pontos = [(-1, 3), (-1, 7), (-3, 7)]
        p = [self.ponto_giro_inicial(px, py) for px, py in pontos]
        pyxel.tri(*p[0], *p[1], *p[2], 0)
        pontos = [(1, 3), (1, 7), (3, 7)]
        p = [self.ponto_giro_inicial(px, py) for px, py in pontos]
        pyxel.tri(*p[0], *p[1], *p[2], 0)

    # Desenha temporariamente as hitboxes de dano para depuração.
    def desenhar_hitboxes(self):
        if not self.mostrar_hitboxes:
            return

        # Hitboxes que bloqueiam o movimento dos jogadores (mesmas medidas de config.py).
        pyxel.rectb(
            int(self.x + HITBOX_COLISAO_LUXUR_OFFSET_X),
            int(self.y + HITBOX_COLISAO_LUXUR_OFFSET_Y),
            int(HITBOX_COLISAO_LUXUR_LARGURA),
            int(HITBOX_COLISAO_LUXUR_ALTURA), 12
        )
        pyxel.rectb(
            int(self.x + HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_X),
            int(self.y + HITBOX_COLISAO_LUXUR_QUEIXO_OFFSET_Y),
            int(HITBOX_COLISAO_LUXUR_QUEIXO_LARGURA),
            int(HITBOX_COLISAO_LUXUR_QUEIXO_ALTURA), 6
        )

        # Hitboxes retangulares das bolas de fogo (amarelo).
        hb = self.hitboxes["bola_fogo"]
        for bola in self.bolas_fogo:
            if bola["ativa"]:
                pyxel.rectb(
                    int(bola["x"] + hb["offset_x"] - hb["largura"] / 2),
                    int(bola["y"] + hb["offset_y"] - hb["altura"] / 2),
                    int(hb["largura"]), int(hb["altura"]), 10
                )

        # Hitboxes dos pilares ativos (laranja).
        hb = self.hitboxes["pilar"]
        for pilar in self.pilares:
            if pilar["estado"] != "ativo":
                continue
            largura = pilar["largura"] if hb["largura"] is None else hb["largura"]
            pyxel.rectb(
                int(pilar["x"] + hb["offset_x"]), int(hb["offset_y"]),
                int(largura), int(hb["altura"]), 9
            )

        # Hitboxes das cópias/clones ativos (verde).
        hb = self.hitboxes["clone"]
        for copia in self.copias_luxur:
            if not copia["ativa"]:
                continue
            pyxel.rectb(
                int(copia["x"] + hb["offset_x"]), int(copia["y"] + hb["offset_y"]),
                int(hb["largura"]), int(hb["altura"]), 11
            )

    # Desenha o corpo, chifres, olhos e rosto do Luxur.
    def show(self):
        # Somente a investida faz o Luxur inteiro piscar.
        if self.estado_ataque == "preparando":
            frequencia = max(1, FREQUENCIA_PISCADA_TELEGRAPO)
            if (pyxel.frame_count // frequencia) % 2 == 1:
                return
        estados_multiplicacao = (
            "telegrafo_multiplicacao", "multiplicacao_ondas",
            "multiplicacao_onda_ativa", "multiplicacao_final",
            "recuperando_multiplicacao"
        )
        girando_no_inicio = self.giro_multiplicacao_ativo
        if girando_no_inicio:
            self.desenhar_cabeca_giro_inicial()
        else:
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
        # Durante o telégrafo das bolas, pisca apenas o olho de origem:
        # alterna entre a cor atual (9) e vermelho (8).
        cor_olho_esquerdo = 9
        cor_olho_direito = 9
        if self.estado_ataque == "preparando_bolas":
            frequencia = max(1, FREQUENCIA_PISCADA_TELEGRAPO)
            vermelho = (pyxel.frame_count // frequencia) % 2 == 1
            if vermelho:
                if self.origem_telegrafo_bolas == -1:
                    cor_olho_esquerdo = 8
                elif self.origem_telegrafo_bolas == 1:
                    cor_olho_direito = 8
                else:
                    # A terceira rajada da fase 3 sai da boca; os dois olhos
                    # ficam vermelhos para sinalizar o ataque central.
                    cor_olho_esquerdo = 8
                    cor_olho_direito = 8
        if not girando_no_inicio:
            pyxel.circ(self.x-5, self.y-1, 1, cor_olho_esquerdo)
            pyxel.circ(self.x+5, self.y-1, 1, cor_olho_direito)
            pyxel.tri(self.x-1, self.y+3,
                self.x-1, self.y+7,
                self.x-3, self.y+7, 0)
            pyxel.tri(self.x+1, self.y+3,
                self.x+1, self.y+7,
                self.x+3, self.y+7, 0)

        # Durante o ataque dos pilares, pequenas chamas orbitam a cabeça
        # para dar a impressão de que Luxur está girando.
        if self.estado_ataque in ("preparando_pilares", "pilares_ativos"):
            for deslocamento in (0, 180):
                angulo = math.radians(self.angulo_giro + deslocamento)
                fx = self.x + math.cos(angulo) * 21
                fy = self.y + math.sin(angulo) * 21
                pyxel.circ(fx, fy, 3, 8)
                pyxel.circ(fx, fy, 1, 10)

        # Minions da multiplicação: sprite 16x16 em (32, 16).
        # A cor 0 (preto) é tratada como transparente pelo colkey do blt.
        for copia in self.copias_luxur:
            if not copia["ativa"]:
                continue
            cx, cy = int(copia["x"]), int(copia["y"])
            pyxel.blt(
                cx - 8, cy - 8,
                0, 32, 16,
                16, 16,
                0
            )

        # Bolas de fogo em movimento: núcleo amarelo e borda vermelha.
        for bola in self.bolas_fogo:
            pyxel.circ(int(bola["x"]), int(bola["y"]), RAIO_BOLA_FOGO + 1, 8)
            pyxel.circ(int(bola["x"]), int(bola["y"]), RAIO_BOLA_FOGO, 9)
            pyxel.pset(int(bola["x"]), int(bola["y"]), 10)

        # Pilares: pequenos avisos piscando e depois colunas vermelhas.
        for pilar in self.pilares:
            x = int(pilar["x"])
            largura = pilar["largura"]
            if pilar["estado"] == "aviso":
                frequencia = max(1, FREQUENCIA_PISCADA_PILAR)
                if (pyxel.frame_count // frequencia) % 2 == 0:
                    pyxel.rect(x, Y_CHAO_PILARES - ALTURA_TELEGRAFO_PILAR,
                               largura, ALTURA_TELEGRAFO_PILAR, 8)
                    pyxel.rect(x + largura // 2, Y_CHAO_PILARES - ALTURA_TELEGRAFO_PILAR,
                               max(1, largura // 3), ALTURA_TELEGRAFO_PILAR, 7)
            else:
                pyxel.rect(x, 0, largura, Y_CHAO_PILARES, 8)
                if largura >= 4:
                    pyxel.rect(x + largura // 3, 0, max(1, largura // 3),
                               Y_CHAO_PILARES, 9)

        if self.estado_ataque == "preparando":
            if self.fase_investida == 1:
                if self.direcao_investida == 1:
                    pyxel.line(self.x + 12, self.y, 159, self.y, 10)
                else:
                    pyxel.line(0, self.y, self.x - 12, self.y, 10)
            else:
                fim_x = int(self.x + self.direcao_x_investida * 200)
                fim_y = int(self.y + self.direcao_y_investida * 200)
                pyxel.line(self.x, self.y, fim_x, fim_y, 10)

        self.desenhar_hitboxes()

    # Retira uma quantidade de HP do Luxur.
    def takehit(self, hit):
        self.hp -= hit
# ============================================================
# CLASSE PRINCIPAL DO JOGO
# Inicializa o Pyxel, personagens e loop principal.
# ============================================================
