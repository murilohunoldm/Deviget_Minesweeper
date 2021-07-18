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

#Define comprimento e altura de cada casa do campo minado
comp = int(screen.get_width()/t)
alt = int(screen.get_height()/t)

#Cria fonte para os numeros do campo de acordo com o tamanho da matriz e com fonte padrao
my_font = pygame.font.SysFont("",700/t)
menu_fnt = pygame.font.SysFont("Segoe UI", 16, True, False)
msg_fnt = pygame.font.SysFont("Verdana", 14, True, False)

#Images
#Casa padrao
q = pygame.transform.scale(pygame.image.load("quad0.png").convert_alpha(), (comp, alt))
#Casa clicada
q2 = pygame.transform.scale(pygame.image.load("quad1.png").convert_alpha(), (comp, alt))
#Bandeira
q2 = pygame.transform.scale(pygame.image.load("band.png").convert_alpha(), (comp, alt))
#Bomb
bomba = pygame.transform.scale(pygame.image.load("bomb.png").convert_alpha(), (comp, alt))
#Logo do Jogo
#logo = pygame.image.load("logo.png").convert_alpha()


#Define o icone da janela
pygame.display.set_icon(bomba)

#Funcao que inicia a partida
def inicio():
    #Define o uso de variaveis globais
    global campo, af, mband, t, bombs, acertos, fim, jogou, relogio
    #Inicializa/zera as variaveis globais
    bombs=0; acertos=0; fim=False; jogou=False
    campo= [["" for j in range(t)] for i in range(t)]
    af= [[0 for j in range(t)] for i in range(t)]
    mband= [[0 for j in range(t)] for i in range(t)]

    #Desenha o Menu
    pts.fill( (0,0,0) )
    pts.blit(menu_fnt.render("[M] Música [T] Tela cheia [R] Reiniciar [S] Sair", True, (255, 255, 255)), (250, 20) )
    #Desenho o cenário
    for x in range(t):
        for y in range(t):
            screen.blit(q, (x*comp, y*alt))
        pygame.display.update()


#Funcao para distribuir as bombas na matriz



