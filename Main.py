#Libraries
import pygame
import os
from pygame.locals import *
from random import randint
import time

os.environ['SDL_VIDEO_CENTERED']='1' #Centers the window on the screen
pygame.init()

#Variables
bombs=0 # Total Bombs
hits=0 #Counter the number of bombs marked with flags
t=10 #board headquarters size
endgame=False #End of the game
fullscreen=False #Defines if the game is in FS or not

#Generates a headquarters to store values ​​and bombs
field = [["" for j in range(t)] for i in range(t)]
#Matrix that determines if a position was opened or not by the user
af = [[0 for j in range(t)] for i in range(t)]
#Matrix that keeps if the position was marked with a flag
mband = [[0 for j in range(t)] for i in range(t)]


#create a clock to time the game
clock = pygame.time.Clock()

#Defines Window, Title, Cursor and Icon
wnd = pygame.display.set_mode( (640,610), 0, 32)
pygame.display.set_caption("Deviget Minesweeper - By Murilo Hunold")
pygame.mouse.set_cursor(*pygame.cursors.diamond)

#Create Surfaces
header = pygame.Surface((640, 80), 0, 32)
screen = pygame.Surface( (640, 480), 0, 32)
pts = pygame.Surface( (640, 50), 0, 32)

#Defines the length and height of each minefield house
width = int(screen.get_width() / t)
height = int(screen.get_height() / t)

#Create font for field numbers according to matrix size and default font
my_font = pygame.font.SysFont("", int(700/t))
menu_fnt = pygame.font.SysFont("Segoe UI", 16, True, False)
msg_fnt = pygame.font.SysFont("Verdana", 14, True, False)

#Images
#Normal square
q = pygame.transform.scale(pygame.image.load("images/quad0.png").convert_alpha(), (width, height))
#clicked square
q2 = pygame.transform.scale(pygame.image.load("images/quad1.png").convert_alpha(), (width, height))
#Flag
flag = pygame.transform.scale(pygame.image.load("images/band.png").convert_alpha(), (width, height))
#Bomb
bomba = pygame.transform.scale(pygame.image.load("images/bomb.png").convert_alpha(), (width, height))
#Logo do Jogo
#logo = pygame.image.load("logo.png").convert_alpha()


#Defines the window icon
pygame.display.set_icon(bomba)

#Function that starts the game
def Start():
    #Defines the use of global variables
    global field, af, mband, t, bombs, hits, endgame, played, clock
    #Initializes / resets global variables
    bombs=0; hits=0; endgame=False; played=False
    field= [["" for j in range(t)] for i in range(t)]
    af= [[0 for j in range(t)] for i in range(t)]
    mband= [[0 for j in range(t)] for i in range(t)]

    #Design the Menu
    pts.fill( (0,0,0) )
    pts.blit(menu_fnt.render("[F] Full Screen [R] Restart [Q] Quit", True, (255, 255, 255)), (250, 20))
    #Design the scenery
    for x in range(t):
        for y in range(t):
            screen.blit(q, (x * width, y * height))
        pygame.display.update()

#
#Function to distribute the bombs in the matrix
def Create(x1, y1):
    global bombs
    #Add bombs to the matrix by drawing a position
    for b in range(0, int((t*t)/5)):
        a1=randint(0,t-1)
        a2=randint(0,t-1)
        if((a1!=y1 or a2!=x1) and field[a1][a2]!= "*"):
            field[a1][a2]= "*"
            bombs+=1
        else:
            b-=1
    num=0
    #Count the number of bombs around each matrix position
    for y in range(t):
        for x in range(t):
            if (field[y][x] == ""):
                for a in range((y-1),(y+2)):
                    for b in range((x-1),(x+2)):
                        if ((a>=0 and b>=0) and a<t and b<t):
                            if (field[a][b]== "*"):
                                num+=1
                field[y][x]=str(num)
                num=0
    return True

#Function that adds different colors to the numbers
def Color(v):
    if(v =="1"):
        imgpeca = my_font.render(v, True, (176, 196, 222))
    elif(v == "2"):
        imgpeca = my_font.render(v, True, (50, 205, 50))
    elif (v == "3"):
        imgpeca = my_font.render(v, True, (178, 34, 34))
    else:
        imgpeca = my_font.render(v, True, (0, 0, 140))
    return imgpeca

#Recursive function to open blank fields
def Open(x, y):
    for l in range((y-1), (y+2)):
        for c in range((x - 1), (x + 2)):
            if ((l>=0 and c>=0) and (l<t and c<t)):
                if(mband[l][c]==0):
                    screen.blit(q2, (c * width, l * height))
                    if(field[l][c]!= "0"):
                        screen.blit(Color(field[l][c]), ((c * width + (width / 4)), l * height))
                    elif(field[l][c] == "0" and (af[l][c] == 0 and (l != y or c != x))):
                        Open(c, l)
                    af[l][c]=1

#Function to explode the bombs
def Explode(x, y):
    screen.blit(bomba, ((int(x) * width), (int(y) * height)))
    wnd.blit(screen, (0,0))
    b=1
    m=0
    n=1
    global bombs, endgame, clock
    while(b<bombs):
        for l in range(y+n-1, y-n-1, -1):
            if((l>=0 and (x-n)>=0)and (l<t and (x-n)<t)):
                if(field[l][x - n]== "*"):
                    af[l][x-n]=1
                    time.sleep(0.05)
                    screen.blit(bomba, ((x-n) * width, l * height))
                    wnd.blit(screen, (0,0))
                    pygame.display.update()
                    b+=1
        for l in range(y-n, y-n-1, -1):
            for c in range(x-1-m, x+2+m):
                if ((l>=0 and c>=0) and (l<t and c<t)):
                    if(field[l][c]== "*"):
                        af[l][c]=1
                        time.sleep(0.05)
                        screen.blit(bomba, (c * width, l * height))
                        wnd.blit(screen, (0, 0))
                        pygame.display.update()
                        b += 1
        for l in range(y-n+1, y+n, 1):
            if ((l>=0 and (x+n)>=0) and (l<t and (x+n)<t)):
                if(field[l][x + n]== "*"):
                    af[l][x+n]=1
                    time.sleep(0.05)
                    screen.blit(bomba, ((x+n) * width, l * height))
                    wnd.blit(screen, (0, 0))
                    pygame.display.update()
                    b += 1
        for l in range(y+n, y+n+1, 1):
            for c in range(x + 1 + m,x-2-m, -1):
                if ((l>=0 and c>=0) and (l<t and c<t)):
                    if(field[l][c]== "*"):
                        af[l][c]=1
                        time.sleep(0.05)
                        screen.blit(bomba, (c * width, l * height))
                        wnd.blit(screen, (0, 0))
                        pygame.display.update()
                        b += 1
        m+=1
        n+=1
    endgame=True
    pts.blit(msg_fnt.render("Sorry, you lose! Time: " + str(clock.tick() / 1000) + " seg", True, (230, 230, 0)), (10, 0))

#Function to check the player move
def Play(x, y):
    af[y][x]=1
    screen.blit(q2, (x * width, y * height))
    if (field[y][x] != '*'):
        if(field[y][x]== "0"):
            Open(x, y)
        else:
            screen.blit(Color(field[y][x]), ((x * width + (width / 4)), y * height))
    else:
        Explode(x, y)

#Mark Flags
def Flags(x, y):
    global hits, bombs, endgame
    if(mband[y][x]==0 and af[y][x]==0):
        if(field[y][x]== "*"):
            hits+=1
        mband[y][x]=1
        screen.blit(flag, ((int(x) * width + (width / 8)), (int(y) * height + (height / 8))))
    elif(af[y][x]==0):
        if(field[y][x]== "*"):
            hits-=1
        screen.blit(q, ((int(x)) * width, (int(y)) * height))
        mband[y][x]=0
    if(hits==bombs and bombs>0):
        endgame=True
        pts.blit(msg_fnt.render("Congratulations, you WON! Time: " + str(clock.tick() / 1000) + " seg", True, (230, 230, 0)), (10, 0))
pygame.display.update()
played=False
Start()

while True:
    for e in pygame.event.get():
        if e.type == QUIT:
            exit()
        #click options
        if ((e.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed() == (1,0,0) and endgame == False)):
            (x,y) = e.pos
            if(int(y / height)<t):
                if(not played):
                    played=Create(int(x / width), int(y / height))
                    Play(int(x / width), int(y / height))
                    #Starts clock
                    clock.tick()
                elif(mband[int(y / height)][int(x / width)] == 0):
                    Play(int(x / width), int(y / height))
        if (((e.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()==(0,0,1)) and endgame == False)and played==True):
            if(int(y / height)<t):
                (x,y) = e.pos
                Flags(int(x / width), int(y / height))
        wnd.blit(header, (0, 480))
        wnd.blit(screen, (0, 0))
        wnd.blit(pts, (0, 560))
        #cabec.blit(logo, (0, 0))

        pygame.display.update()

        #keyboard options
        if(e.type == KEYDOWN and e.key==K_r):
            Start()
        if (e.type == KEYDOWN and e.key == K_q):
            exit()
        if (e.type == KEYDOWN and e.key == K_f):
            if not fullscreen:
                wnd = pygame.display.set_mode( (800, 765), pygame.FULLSCREEN, 32)
                fullscreen=True
            else:
                wnd = pygame.display.set_mode((640, 610), 0, 32)
                fullscreen=False
    pygame.display.update()
