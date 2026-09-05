# Projeto Jogo: Melda

## Equipe
Amanda e Matheus

## Descrição do Jogo
"Melda" é um jogo de aventura no estilo boss fight coop local, fortemente inspirado no clássico Zelda. O objetivo dos jogadores é trabalharem juntos para derrotar um chefão em uma arena, utilizando movimentação estratégica e ataques coordenados. O jogo está sendo desenvolvido em Python utilizando a biblioteca Pyxel.

## Integração STEAM
Este projeto atende aos requisitos STEAM com foco principal no eixo de *Artes (Arts)*. A integração ocorre das seguintes formas:
* *Artes Visuais:* Todos os sprites (personagens, chefão, cenário e interface) estão sendo desenhados e animados manualmente pela equipe dentro das limitações de cores e resolução da engine.
* *Música e Design de Som:* A trilha sonora do jogo conta com composição musical original feita em formato chiptune (8-bits), além da criação de efeitos sonoros customizados para os golpes e interações do jogo.

## Requirements

- Python 3.7+
- Pyxel

## Setup

```bash
pip install pyxel
```

## Run

```bash
python main.py
```

## Controls

**Blue character (WASD):**
- W/A/S/D to move

**Red character (Arrow keys):**
- Arrow keys to move

## Game State

- **Luxur** (boss): Center arena, 100 HP
- **Bluu**: Collides with boss and boundaries
- **Redd**: Wraps around edges
