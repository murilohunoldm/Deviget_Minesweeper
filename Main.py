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
my_font = pygame.font.SysFont("", int(700/t))
menu_fnt = pygame.font.SysFont("Segoe UI", 16, True, False)
msg_fnt = pygame.font.SysFont("Verdana", 14, True, False)

#Images
#Casa padrao
q = pygame.transform.scale(pygame.image.load("quad0.png").convert_alpha(), (comp, alt))
#Casa clicada
q2 = pygame.transform.scale(pygame.image.load("quad1.png").convert_alpha(), (comp, alt))
#Bandeira
band = pygame.transform.scale(pygame.image.load("band.png").convert_alpha(), (comp, alt))
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
    pts.blit(menu_fnt.render("[M] Música [T] Tela cheia [R] Reiniciar [S] Sair", True, (255, 255, 255)), (250, 20))
    #Desenho o cenário
    for x in range(t):
        for y in range(t):
            screen.blit(q, (x*comp, y*alt))
        pygame.display.update()


#Funcao para distribuir as bombas na matriz
def Criar(x1, y1):
    global bombs
    #Adiciona bombas na matriz sorteando uma posicao
    for b in range(0, int((t*t)/5)):
        a1=randint(0,t-1)
        a2=randint(0,t-1)
        if((a1!=y1 or a2!=x1) and campo[a1][a2]!="*"):
            campo[a1][a2]="*"
            bombs+=1
        else:
            b-=1
    num=0
    #Conta o numero de bombas em volta de cada posicao de matriz
    for y in range(t):
        for x in range(t):
            if (campo[y][x] == ""):
                for a in range((y-1),(y+2)):
                    for b in range((x-1),(x+2)):
                        if ((a>=0 and b>=0) and a<t and b<t):
                            if (campo[a][b]=="*"):
                                num+=1
                campo[y][x]=str(num)
                num=0
    return True

#Funcao que adiciona diferentes cores para os numeros
def Colorir(v):
    if(v =="1"):
        imgpeca = my_font.render(v, True, (176, 196, 222))
    elif(v == "2"):
        imgpeca = my_font.render(v, True, (50, 205, 50))
    elif (v == "3"):
        imgpeca = my_font.render(v, True, (178, 34, 34))
    else:
        imgpeca = my_font.render(v, True, (0, 0, 140))
    return imgpeca

#Funcao recursiva para abrir os campos em branco
def abrir(x, y):
    for l in range((y-1), (y+2)):
        for c in range((x - 1), (x + 2)):
            if ((l>=0 and c>=0) and (l<t and c<t)):
                if(mband[l][c]==0):
                    screen.blit(q2, (c*comp, l*alt))
                    if(campo[l][c]!="0"):
                        screen.blit(Colorir(campo[l][c]), ((c*comp+(comp/4)), l*alt))
                    elif(campo[l][c]=="0" and (af[l][c]==0 and (l!=y or c!=x))):
                        abrir(c,l)
                    af[l][c]=1

#Funcao para explodir as bombas em espiral
def Explodir(x,y):
    screen.blit(bomba, ((int(x)*comp), (int(y)*alt)))
    #b_som.play()
    wnd.blit(screen, (0,0))
    b=1
    m=0
    n=1
    global bombs, fim, relogio
    while(b<bombs):
        for l in range(y+n-1, y-n-1, -1):
            if((l>=0 and (x-n)>=0)and (l<t and (x-n)<t)):
                if(campo[l][x-n]=="*"):
                    af[l][x-n]=1
                    time.sleep(0.05)
                    screen.blit(bomba, ((x-n)*comp, l*alt))
                    #b_som.play()
                    wnd.blit(screen, (0,0))
                    pygame.display.update()
                    b+=1
        for l in range(y-n, y-n-1, -1):
            for c in range(x-1-m, x+2+m):
                if ((l>=0 and c>=0) and (l<t and c<t)):
                    if(campo[l][c]=="*"):
                        af[l][c]=1
                        time.sleep(0.05)
                        screen.blit(bomba, (c*comp, l*alt))
                        # b_som.play()
                        wnd.blit(screen, (0, 0))
                        pygame.display.update()
                        b += 1
        for l in range(y-n+1, y+n, 1):
            if ((l>=0 and (x+n)>=0) and (l<t and (x+n)<t)):
                if(campo[l][x+n]=="*"):
                    af[l][x+n]=1
                    time.sleep(0.05)
                    screen.blit(bomba, ((x+n)*comp, l*alt))
                    # b_som.play()
                    wnd.blit(screen, (0, 0))
                    pygame.display.update()
                    b += 1
        m+=1
        n+=1
    fim=True
    #pts.blit(msg_fnt.render("Que pena, você perdeu! Tempo: "+str(relogio.tick()/1000)+ " seg", True, (230, 230, 0), (10, 10, 10)))
    pts.blit(msg_fnt.render("Que pena, você perdeu! Tempo: "+str(relogio.tick()/1000)+ " seg", True, (230, 230, 0)),  (0, 0))

#Funcao para verificar a jogada
def Jogar(x, y):
    af[y][x]=1
    screen.blit(q2, (x*comp, y*alt))
    if (campo[y][x] !='*'):
        if(campo[y][x]=="0"):
            abrir(x,y)
        else:
            screen.blit(Colorir(campo[y][x]), ((x*comp+(comp/4)), y*alt))
    else:
        Explodir(x,y)

#Marcar Bandeiras
def Bandeirar(x,y):
    global acertos, bombs, fim
    if(mband[y][x]==0 and af[y][x]==0):
        if(campo[y][x]=="*"):
            acertos+=1
        mband[y][x]=1
        screen.blit(band, ((int(x)*comp+(comp/8)), (int(y)*alt+(alt/8))))
    elif(af[y][x]==0):
        if(campo[y][x]=="*"):
            acertos-=1
        screen.blit(q, ( (int(x))*comp, (int(y))*alt))
        mband[y][x]=0
    if(acertos==bombs and bombs>0):
        fim=True
        pts.blit(msg_fnt.render("Parabéns você ganhou! Tempo: "+str(relogio.tick()/1000)+ " seg", True, (230, 230, 0)),  (0, 0))
pygame.display.update()
jogou=False
inicio()

while True:
    for e in pygame.event.get():
        if e.type == QUIT:
            exit()
        #Opcoes de clique
        if ((e.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()==(1,0,0) and fim ==False)):
            (x,y) = e.pos
            if(int(y/alt)<t):
                if(not jogou):
                    jogou=Criar(int(x/comp), int(y/alt))
                    Jogar(int(x/comp), int(y/alt))
                    #marca inicio da contagem
                    relogio.tick()
                elif(mband[int(y/alt)][int(x/comp)]==0):
                    Jogar(int(x / comp), int(y / alt))
        if (((e.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()==(0,0,1)) and fim == False)and jogou==True):
            if(int(y/alt)<t):
                (x,y) = e.pos
                Bandeirar(int(x/comp), int(y/alt))
        wnd.blit(cabec, (0, 480))
        wnd.blit(screen, (0, 0))
        wnd.blit(pts, (0, 560))
        #cabec.blit(logo, (0, 0))

        pygame.display.update()

        #Opcoes do teclado
        if(e.type == KEYDOWN and e.key==K_r):
            inicio()
        if (e.type == KEYDOWN and e.key == K_s):
            exit()
        if (e.type == KEYDOWN and e.key == K_t):
            if not fullscreen:
                wnd = pygame.display.set_mode( (800, 765), pygame.FULLSCREEN, 32)
                fullscreen=True
            else:
                wnd = pygame.display.set_mode((640, 610), 0, 32)
                fullscreen=False
        if (e.type == KEYDOWN and e.key == K_m):
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            else:
                pygame.mixer.music.play()
    pygame.display.update()
