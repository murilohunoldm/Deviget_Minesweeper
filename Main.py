#Libraries
import pygame, os
from pygame.locals import *
from pygame import font
from random import randint
import time

os.environ['SDL_VIDEO_CENTERED']='1' #Centraliza a janela na tela
pygame.init()

#Variables
bombs=0 # Total Bombas
acertos=0 #Contador do numero de bombas marcadas com bandeiras
t=10 #tamanho da matriz quadrada
fim=False #Define se o jogo terminou ou nao
fullscreen=False #Define se o jogo está em FS ou nao

#Gera uma matriz para guardar os valores e bombas
campo = [["" for j in range(t)] for i in range(t)]
#Matriz que determina se uma posicao foi aberta ou nao pelo usuario
af = [[0 for j in range(t)] for i in range(t)]
#Matriz que guarda se a posicao foi marcada com uma bandeira
mband = [[0 for j in range(t)] for i in range(t)]


#Cria um relogio para cronometrar o jogo
relogio = pygame.time.Clock()

#Define a Janela, titulo, cursor e icone
wnd = pygame.display.set_mode( (640,610), 0, 32)
pygame.display.set_caption("Deviget Minesweeper - By Murilo Hunold")
pygame.mouse.set_cursor(*pygame.cursors.diamond)

#Cria Surfaces
cabec = pygame.Surface( (640, 80), 0, 32)
screen = pygame.Surface( (640, 480), 0, 32)
pts = pygame.Surface( (640, 50), 0, 32)
