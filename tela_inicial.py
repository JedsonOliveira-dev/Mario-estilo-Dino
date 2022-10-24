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


imagem_tela_tela = pygame.image.load(os.path.join(diretorio_imagens, 'tela_tela.png')).convert_alpha()
imagem_tela = pygame.image.load(os.path.join(diretorio_imagens, 'Logo.png')).convert_alpha()
image = pygame.transform.scale(imagem_tela, (696/2.5, 326/2.5))

som_tela_inicial = pygame.mixer.Sound(os.path.join(diretorio_sons, 'tela_inicial.mp3'))
som_tela_inicial.set_volume(1)




som_tela = False
som = True


relogio = pygame.time.Clock()

def inicio():
    # laço principal
    global som_tela, som
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
                     exit()

        if som == True and som_tela == False:
            som_tela_inicial.play()
            som_tela = True
        else:
            pass


        tela.blit(imagem_tela_tela, (0, 0))
        tela.blit(image, (350, 70))

        pygame.display.flip()


inicio()



