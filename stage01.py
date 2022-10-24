import pygame
from pygame.locals import *
from sys import exit
import os
import constantes
from random import randrange

pygame.init()
pygame.mixer.init()

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'imagens')
diretorio_sons = os.path.join(diretorio_principal, 'audios')

# cria a tela
tela = pygame.display.set_mode((constantes.LARGURA, constantes.ALTURA))
# da o nome a tela
pygame.display.set_caption('Mario alternativo')

# carregando as imagens
sprite_movimento_mario = pygame.image.load(os.path.join(diretorio_imagens, 'sheet.png')).convert_alpha()
sprite_ambiente = pygame.image.load(os.path.join(diretorio_imagens, 'chao.png')).convert_alpha()
nuvem = pygame.image.load(os.path.join(diretorio_imagens, 'nuvens.png')).convert_alpha()
montanha = pygame.image.load(os.path.join(diretorio_imagens, 'montanha.png')).convert_alpha()
tubo = pygame.image.load(os.path.join(diretorio_imagens, 'tubo.png')).convert_alpha()
bala_1 = pygame.image.load(os.path.join(diretorio_imagens, 'bala_01.png')).convert_alpha()

som_colisao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'alert.wav'))
som_colisao.set_volume(1)
colidiu = False

som_pontuacao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'pontuacao.wav'))
som_pontuacao.set_volume(1)
som_jogando = pygame.mixer.Sound(os.path.join(diretorio_sons, 'Super Mario - Overworld Theme (GFM Trap Remix).mp3'))
som_jogando.set_volume(1)


# pontuacao
def exibir(mensagem, tamanho, cor):
    fonte = pygame.font.SysFont('comicsansms', tamanho, True, False)
    mensagem = f'{mensagem}'
    texto_formatado = fonte.render(mensagem, True, cor)
    return texto_formatado


def reiniciar_jogo():
    global pontos, velocidade_jogo, colidiu
    pontos = 0
    velocidade_jogo = 10
    colidiu = False
    objeto_tubo_pequeno.rect.x = constantes.LARGURA
    som_jogando.play()


# Encerra loop e passa para proxima fase
def retornar1():
    return 1


pontos = 0

velocidade_jogo = 10


# criação da classe
class Mario(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons, 'pulo.wav'))
        self.som_pulo.set_volume(1)

        # lista para imagens
        self.imagens_mario = []

        for num in range(2):
            movimento_mario = sprite_movimento_mario.subsurface((num * 243, 0), (243, 324))
            movimento_mario = pygame.transform.scale(movimento_mario, (243 / 4, 324 / 4))
            self.imagens_mario.append(movimento_mario)

        self.index_lista = 0
        self.image = self.imagens_mario[self.index_lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_y_inicial = 230
        # posiciona o mario na tela
        self.rect.center = (100, 230)
        self.pulo = False

    def pular(self):
        self.pulo = True
        self.som_pulo.play()

    # faz o mario se movimentar
    def update(self):
        if self.pulo:
            if self.rect.y <= 120:
                self.pulo = False
            self.rect.y -= 12
        else:
            if self.rect.y < self.pos_y_inicial:
                self.rect.y += 12
            else:
                self.rect.y = self.pos_y_inicial

        if self.index_lista > 1:
            self.index_lista = 0
        self.index_lista += 0.20
        self.image = self.imagens_mario[int(self.index_lista)]


class Nuvens(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = nuvem.subsurface((0, 0), (230, 150))
        self.image = pygame.transform.scale(self.image, (230 / 4, 150 / 4))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50, 200, 10)
        self.rect.x = constantes.LARGURA - randrange(20, 620, 5)

    # faz a nuvem se movimentar
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = constantes.LARGURA
            self.rect.y = randrange(10, 100, 10)
        # faz a nuvem se movimentar a cada frame = 10 pixels
        self.rect.x -= velocidade_jogo


class Nuvens_grandes(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = nuvem.subsurface((0, 0), (230, 150))
        self.image = pygame.transform.scale(self.image, (230 / 2, 150 / 2))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(5, 100, 10)
        self.rect.x = constantes.LARGURA - randrange(20, 620, 5)

    # faz a nuvem se movimentar
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = constantes.LARGURA
            self.rect.y = randrange(10, 100, 10)
        # faz a nuvem se movimentar a cada frame = 10 pixels
        self.rect.x -= velocidade_jogo


class Ambiente(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_ambiente.subsurface((0, 0), (64, 50))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * 64
        self.rect.y = constantes.ALTURA - 50

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = constantes.LARGURA
        self.rect.x -= 10


class Montanhas(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = montanha.subsurface((0, 0), (440, 212))
        self.rect = self.image.get_rect()
        self.rect.center = (constantes.LARGURA, 230)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = constantes.LARGURA
        self.rect.x -= velocidade_jogo


class Montanhas_pequenas(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = montanha.subsurface((0, 0), (440, 212))
        self.image = pygame.transform.scale(self.image, (440 / 2, 212 / 2))
        self.rect = self.image.get_rect()
        self.rect.center = (constantes.LARGURA, 270)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = constantes.LARGURA
        self.rect.x -= velocidade_jogo


class Montanhas_pequenas_menores(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = montanha.subsurface((0, 0), (440, 212))
        self.image = pygame.transform.scale(self.image, (440 / 4, 212 / 4))
        self.rect = self.image.get_rect()
        self.rect.y = 270
        self.rect.x = constantes.LARGURA - randrange(20, 620, 5)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = constantes.LARGURA
        self.rect.x -= velocidade_jogo


class Tubo_pequeno(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = tubo.subsurface((0, 0), (227, 289))
        self.image = pygame.transform.scale(self.image, (227 / 4, 289 / 4))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.y = randrange(238, 278, 46)
        self.rect.x = constantes.LARGURA - 250

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = constantes.LARGURA
        self.rect.x -= velocidade_jogo


# criando o grupo e objeto para inserir na tela
todas_as_sprites = pygame.sprite.Group()

# objeto montanha
objeto_montanha = Montanhas()
todas_as_sprites.add(objeto_montanha)

# objeto montanha_pequena
objeto_montanha_pequena = Montanhas_pequenas()
todas_as_sprites.add(objeto_montanha_pequena)

# objeto montanha_pequena_menores
for i in range(randrange(2, 10, 1)):
    objeto_montanha_pequena_menor = Montanhas_pequenas_menores()
    todas_as_sprites.add(objeto_montanha_pequena_menor)

# objeto tubo_pequeno
for i in range(1):
    objeto_tubo_pequeno = Tubo_pequeno()
    todas_as_sprites.add(objeto_tubo_pequeno)

for i in range(30):
    # objeto ambiente
    objeto_ambiente = Ambiente(i)
    todas_as_sprites.add(objeto_ambiente)

# objeto nuvens faz as nuvens aparcerem e sorteia a quantidade que aparece
for i in range(randrange(1, 6, 1)):
    objeto_nuvem_grande = Nuvens_grandes()
    todas_as_sprites.add(objeto_nuvem_grande)

# objeto nuvens faz as nuvens aparcerem e sorteia a quantidade que aparece
for i in range(randrange(2, 10, 1)):
    objeto_nuvem = Nuvens()
    todas_as_sprites.add(objeto_nuvem)

# objeto mario
objeto_mario = Mario()
todas_as_sprites.add(objeto_mario)

# grupo de obstaculos
grupo_obstaculos = pygame.sprite.Group()

grupo_obstaculos.add(objeto_tubo_pequeno)

# função que permite chamar frame por segundos - mudança de tela
relogio = pygame.time.Clock()
som_jogando.play()
# laço principal
while True:

    # Controla a mudança de tela
    relogio.tick(constantes.FPS)

    # pintando a tela de azul
    tela.fill(constantes.AZUL_1)

    # definição dos eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if objeto_mario.rect.y != objeto_mario.pos_y_inicial:
                    pass
                else:
                    objeto_mario.pular()
            if event.key == K_r and colidiu == True:
                reiniciar_jogo()

    colisoes = pygame.sprite.spritecollide(objeto_mario, grupo_obstaculos, False, pygame.sprite.collide_mask)

    # inserindo na tela as sprites
    todas_as_sprites.draw(tela)

    if colisoes and colidiu == False:
        som_colisao.play()
        colidiu = True

    if colidiu:
        som_jogando.stop()
        if pontos % 100 == 0:
            pontos += 1
        game_over = exibir('VOCE PERDEU!', 40, (constantes.LARANJA))
        tela.blit(game_over, (constantes.LARGURA / 3.5, constantes.ALTURA / 3.5))
        mostrar_pontos = exibir(f'Pontuação:', 40, (constantes.PRETO))
        tela.blit(mostrar_pontos, (constantes.LARGURA / 2.1, constantes.ALTURA / 15.5))

        restart = exibir(f'Pressione "r" para reiniciar:', 20, (constantes.VERMELHO))
        tela.blit(restart, (constantes.LARGURA / 8, constantes.ALTURA / 2.4))

    else:
        pontos += 1
        # atualizando a tela
        todas_as_sprites.update()
        texto_pontos = exibir(pontos, 30, (constantes.PRETO))

    if pontos % 100 == 0 and pontos <= 800:
        som_pontuacao.play()

        if velocidade_jogo >= 18:
            velocidade_jogo += 0
        else:
            velocidade_jogo += 1

    if pontos >= 800 and colidiu == False:
        vel_max = exibir('Top speed!', 20, (constantes.VERMELHO))
        tela.blit(vel_max, (constantes.LARGURA / 1.25, constantes.ALTURA / 5.5))

    tela.blit(texto_pontos, (520, 30))

    if pontos >= 1200:
        vencedor = exibir('Nivel 01 concluido.', 30, constantes.PRETO)
        tela.blit(vencedor, (constantes.LARGURA / 2, constantes.ALTURA / 2))

    if pontos == 1200:
        retornar1()
        break

    pygame.display.flip()
