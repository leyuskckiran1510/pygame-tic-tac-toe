import pygame
import itertools
import time
import random


pygame.init()
pygame.font.init()
pygame.display.set_caption("tik tak toe.BY LEYUSKC")
myfont = pygame.font.SysFont('Comic Sans MS', 30)
screen=pygame.display.set_mode([800,500])
game2=pygame.draw
game=pygame.mouse
pos_x=180
pos_y=140
pos_y=140
t_c=(0,0,0)
f_c=[255,255,255]
screen.fill(f_c)
global box_no
p_count=0
turn=random.randint(1,2)
box_no=0
run=True
place_x=0
place_y=0
plyr_x={}
plyr_x=set(plyr_x)
plyr_o={}
plyr_o=set(plyr_o)
lisv=""
checker=''
#def new_game():
pygame.mixer.init()
#pygame.mixer.Channel(2)
pygame.mixer.Channel(0).set_volume(40)
pygame.mixer.Channel(0).play(pygame.mixer.Sound('./lol1.wav'))
pygame.mixer.music.load('invalid.mp3')
#music1.play(loops=1,start=0)
def turn_publisher():
   pygame.display.update()
   if turn==1:
      game2.line(screen,f_c,[60,20],[700,20],100)
      textsurface = myfont.render("X's TURN....", False, t_c)
      screen.blit(textsurface,(60,20))
      pygame.display.flip()
   if turn==2:
      game2.line(screen,f_c,[60,20],[700,20],100)
      textsurface = myfont.render("O's TURN....", False,t_c)
      screen.blit(textsurface,(60,20))
      pygame.display.flip()
def chart():
   #game2.rect(screen,[i*2,i*3,i*4],[100+i,100+i,50+i,50+i],i)
   for i in range(1,3):
      game2.line(screen,[0,0,0],[pos_x,pos_y+(i*60)],[pos_x+(60*3),pos_y+(i*60)],3)
      pygame.display.update()
   for i in range(1,3):
      game2.line(screen,[0,0,0],[pos_x+(i*60),pos_y],[pos_x+(i*60),pos_y+(60*3)],3)
      pygame.display.update()
   #time.sleep(5)
   pygame.display.flip()
def plotter():
   global checker,p_count
   for val in checker:
      if int(val)==box_no:
         p_count-=1
         print("invalid location choose next location")
         pygame.mixer.music.set_volume(30)
         pygame.mixer.music.play(1)
         pygame.mixer.music.fadeout(1000)
         return 
   checker=checker+str(box_no)
   
   for i in range(1,10):
      if box_no==i and turn==1:
         game2.line(screen,[255,0,255],[place_x,place_y],[place_x+30,place_y+30],5)
         game2.line(screen,[255,0,255],[place_x+30,place_y],[place_x,place_y+30],5)
         pygame.display.flip()
      if box_no==i and turn==2:
         game2.circle(screen,[255,0,0],[(place_x+10),(place_y+15)],15,5)
         pygame.display.flip()  
   mtch_fixer()
def presschecker():
   global p_count,turn,run
   time.sleep(0.05)
   for ev in pygame.event.get():
      if ev.type ==pygame.MOUSEBUTTONDOWN:
         p_count+=1
         plotter()
      if p_count==9:
            run=False
            print("tie"*10)
         #print(p_count)
      if p_count%2==0:
         #print("player 2")
         turn=2
      
      if p_count%2!=0:
         # print("player 1")
         turn=1
def mtch_fixer():
   global lisv,plyr_o,plyr_x,run
   lisv=""
   plyr_o=set(plyr_o)
   plyr_x=set(plyr_x)
   if turn==1:
    plyr_x.add(box_no)
   if turn==2:
    plyr_o.add(box_no)
    plyr_o=list(plyr_o)
   plyr_x=list(plyr_x)
   try:
      li=list(itertools.combinations(set(plyr_x), 3))
      
      for i in range(len(plyr_x)):
         lisv=li[i]
         #print(lisv)
         poll=list(lisv)
         poll.sort()
         lisv=tuple(poll)
         print("x's",lisv)
         if lisv==(1,2,3) or lisv==(4,5,6) or lisv==(7,8,9)or lisv==(1,4,7)or lisv==(2,5,8)or lisv==(3,6,9)or lisv==(1,5,9)or lisv==(3,5,7):
            #pygame.display.flip()
            for jl in range(10,50):
               game2.line(screen,f_c,[60,400],[700,400],100)
               text = pygame.font.SysFont('Comic Sans MS',jl).render("WINNER IS X", False,[jl*5,jl*4,jl*3])
               screen.blit(text,(60,400))
               pygame.display.flip()
               #print("..winnner......xxxxxxx")
               pygame.mixer.Channel(5).set_volume(70)
               pygame.mixer.Channel(5).play(pygame.mixer.Sound('./win.wav'))
            time.sleep(4)
            run=False
            return
         else:
            pygame.mixer.Channel(1).set_volume(70)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('./hacker.wav'))
            pygame.mixer.Channel(1).fadeout(500)


      lisv2=""
   except IndexError:
      '''game2.line(screen,f_c,[60,400],[700,400],100)
      text =pygame.font.SysFont('Comic Sans MS',30).render("CHECKING.......", False,[0,0,255])
      screen.blit(text,(60,400))
      #print("checking..")'''
      pygame.mixer.Channel(1).set_volume(70)
      pygame.mixer.Channel(1).play(pygame.mixer.Sound('./hacker.wav'))
      pygame.mixer.Channel(1).fadeout(500)


   try:
      lisv=()
      li2=list(itertools.combinations(set(plyr_o), 3))
      for i in range(len(plyr_o)):
         lisv=li2[i]
         poll=list(lisv)
         poll.sort()
         lisv=tuple(poll)
         print("o's",lisv)
         if lisv==(1,2,3) or lisv==(4,5,6) or lisv==(7,8,9)or lisv==(1,4,7)or lisv==(2,5,8)or lisv==(3,6,9)or lisv==(1,5,9)or lisv==(3,5,7):
            #print("..winnner......ooooooo")
            for j2 in range(10,50):
               game2.line(screen,f_c,[60,400],[700,400],100)
               text =pygame.font.SysFont('Comic Sans MS',j2).render("WINNER IS O", False,[j2*3,j2*5,j2*4])
               screen.blit(text,(60,400))
               pygame.display.flip()
               pygame.mixer.Channel(5).set_volume(70)
               pygame.mixer.Channel(5).play(pygame.mixer.Sound('./win.wav'))
            time.sleep(4)
            run=False
            return
         else:
            pygame.mixer.Channel(1).set_volume(70)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('./hacker.wav'))
            pygame.mixer.Channel(1).fadeout(500)

   except IndexError:
      '''game2.line(screen,f_c,[60,400],[700,400],100)
      text =pygame.font.SysFont('Comic Sans MS',30).render("CHECKING......", False,[0,255,0])
      screen.blit(text,(60,400))
      pygame.display.flip()'''
      #print("checking...")
      pygame.mixer.Channel(1).set_volume(70)
      pygame.mixer.Channel(1).play(pygame.mixer.Sound('./hacker.wav'))
      pygame.mixer.Channel(1).fadeout(500)
lolll=False
countu=0
while lolll==True:
   #global run
   countu+=1 
   #screen.fill([255,255,255])
   run=True
   alll=pygame.mouse.get_pos()
   if alll[0]>=60 and alll[0]<=500 and alll[1]>=200 and alll[1]<=250:
       for ev in pygame.event.get():
         if ev.type ==pygame.MOUSEBUTTONDOWN:  
           lolll=False
   print(alll,countu)
   alll=0
   pygame.display.flip()
   textsurface = myfont.render("NEW GAME", False,[255,0,12])
   screen.blit(textsurface,(60,200))
   textsurface2 = myfont.render("EXIT", False,[255,0,12])
   screen.blit(textsurface2,(60,300))
   if countu==1000:
      lolll=False
   #time.sleep(2)

screen.fill([255,255,255])  
while run==True:
      #screen.fill([255,255,255])
      pygame.display.update()
      a=game.get_pos()
      chart()
      turn_publisher()
      for event in pygame.event.get():
         if event.type==pygame.QUIT:
            run=False
            print("quit")
         else:   
            run=True
      box_no=0
      for lol in range(1,4):      
         for lol1 in range(1,4): 
            if a[0]>=180+(60*(lol-1)) and a[0]<=240+(60*(lol-1)) and a[1]>=140+(60*(lol1-1)) and a[1]<=200+(60*(lol1-1)):
               box_no=((lol1*3)-3)+(lol)
               place_x=180+(60*(lol-1))+20
               place_y=140+(60*(lol1-1))+15
               #print(turn)
               presschecker()

         

