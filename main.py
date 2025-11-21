import pygame 
import time
import os
import random
import pickle
import pandas as pd
pygame.init() 



win = pygame.display.set_mode((800, 800)) 
pygame.display.set_caption("MI Beadandó") 

kar_x = 0
kar_y = 0

gon_x = 8
gon_y = 8

elet = 4#maximum 4
gon_elet = 5

width = 20
height = 20

mozgas = 50
run = True

start_ido = time.time()


with open('gonosz_ai_model.pkl', 'rb') as file:
    ai_model = pickle.load(file)


def karakter_rajz(pos, kari):
	win.blit(kari, pos)
    


def karakterek_betoltese(path):
	tabla = pygame.image.load(path).convert_alpha()
	tabla_width, tabla_height = tabla.get_size()
	kar_szelesseg = 42
	kar_magassag = 42
	karakterek_ = []
	for y in range(0, tabla_height, kar_magassag):
		for x in range(0, tabla_width, kar_szelesseg):
			
			rect = pygame.Rect(x, y, kar_szelesseg, kar_magassag)
			image = tabla.subsurface(rect).copy() 
			karakterek_.append(pygame.transform.scale(image, (100,100)))
	return karakterek_


def etelek_betoltese(path):
	etelek_neve = os.listdir(path)

	eredmeny =[]
	for nev in etelek_neve:
		kep = pygame.image.load(f"{path}/{nev}")
		eredmeny.append(pygame.transform.scale(kep, (50,50)))
	return eredmeny

def palya_elemk_betoltese(path):
	elem_nevek = os.listdir(path)
	
	eredmeny ={}
	for nev in elem_nevek:
		kep = pygame.image.load(f"{path}/{nev}")
		
		eredmeny[str(nev).split('.')[0]] = pygame.transform.scale(kep, (50,50))
        
	return eredmeny

def palya_terv_betoltese(path):
	palya = []
	
	with open(path, 'r') as file:
		for line in file:
			
			if(len(line)>=2 and line[0]+line[1] !="//"):
				vonal = []
				for char in line:
					vonal.append(char)
				palya.append(vonal)
	
	

	return palya

def palya_rajz(palya_terv, palyaElemek, kar_x,kar_y):
	if(len(palya_terv) > 0):
		
		

		elem_x =0
		elem_y = 0

		for y in range(kar_y, len(palya_terv)):
			elem_x = 0
			for x in range(kar_x ,len(palya_terv[y])):
				
				pos = (elem_x*mozgas,elem_y*mozgas)

				match palya_terv[y][x]:
					case '#':#Tégla
						win.blit(palyaElemek["Brick_wall"], pos)
							
					case '@':
						win.blit(palyaElemek["Brick_Wall_Cracked"], pos)
					case 'H':
						win.blit(palyaElemek["Wooden_Floor_Horizontal"], pos)
					case '*':
						win.blit(palyaElemek["Rocky_Road"], pos)
					case '.':
						win.blit(palyaElemek["Dirt_Road"], pos)
					case 'W':
						win.blit(palyaElemek["Water"], pos)
					case 'G':
						win.blit(palyaElemek["Grass"], pos)
					case '1':
						win.blit(palyaElemek["Grass"], pos)
						win.blit(palyaElemek["apple"], pos)
					case '2':
						win.blit(palyaElemek["Grass"], pos)
						win.blit(palyaElemek["cypress"], pos)
					case '3':
						win.blit(palyaElemek["Grass"], pos)
						win.blit(palyaElemek["dead tree"], pos)
					case '4':
						win.blit(palyaElemek["Grass"], pos)
						win.blit(palyaElemek["mangrove"], pos)
					case '5':
						win.blit(palyaElemek["Grass"], pos)
						win.blit(palyaElemek["maple"], pos)
					case '6':
						win.blit(palyaElemek["Grass"], pos)
						win.blit(palyaElemek["pine"], pos)
					case '7':
						win.blit(palyaElemek["Grass"], pos)
						win.blit(palyaElemek["sakura"], pos)
					case '8':
						win.blit(palyaElemek["Grass"], pos)
						win.blit(palyaElemek["willow"], pos)
				elem_x +=1
			elem_y +=1
					
def akadaj_teszt(palya_terv, kar_x, kar_y, akadaj):
	
	x = kar_x+8
	y = kar_y+8

	if(y < len(palya_terv)):
		if(x < len(palya_terv[y])):
			if(palya_terv[y][x] == akadaj):
				
				return False
	return True
			
def elet_rajz(kep):
	for i in range(0,4):
		if(i<elet):
			win.blit(kep[0], (i*32,0))
		else:
			win.blit(kep[1], (i*32,0))

def gon_elet_rajz(kep):
	for i in range(0,5):
		if(i<gon_elet):
			win.blit(kep[2], ( 800-(i*32),0))
		else:
			win.blit(kep[1], (800-(i*32),0))

def gonosz_ai():
	global gon_x, gon_y

    
	mouse_x_screen, mouse_y_screen = pygame.mouse.get_pos()
    
    # Átszámítás játék-koordinátákra
    # A képernyő közepe (400, 400) a játékos helye.
    # A gonosz képernyőpozíciója: ((gon_x - kar_x) * mozgas) + 400


	mouse_x_game = gon_x + (mouse_x_screen - 400) / mozgas
	mouse_y_game = gon_y + (mouse_y_screen - 400) / mozgas
	#mouse_x_game = (mouse_x_screen-((gon_x+8)-kar_x)*mozgas)
	#mouse_y_game = (mouse_y_screen-((gon_y+8)-kar_y)*mozgas )

	#print(mouse_x_game, mouse_y_game)

   
	játékos_dx = kar_x - gon_x
	játékos_dy = kar_y - gon_y
	egér_dx = mouse_x_game - gon_x
	egér_dy = mouse_y_game - gon_y
    
	bemenet = [[játékos_dx, játékos_dy]]
	teszt = pd.DataFrame(bemenet, columns=['jatekos_dx', 'jatekos_dy'])

   
	josolt_lepes = ai_model.predict(teszt)[0]

    
	sebesseg = 0.5 # A gonosz sebessége
	if josolt_lepes == 0: # Fel
		gon_y -= sebesseg
	elif josolt_lepes == 1: # Le
		gon_y += sebesseg
	elif josolt_lepes == 2: # Balra
		gon_x -= sebesseg
	elif josolt_lepes == 3: # Jobbra
		gon_x += sebesseg

def killhim():
	global gon_elet
	mx, my = pygame.mouse.get_pos()
	dx = ((gon_x - kar_x) * 50) + 400
	dy = ((gon_y - kar_y) * 50) + 400
	if (mx < dx + 25 and mx > dx - 25) and (my < dy + 25 and my > dy - 25):
		gon_elet -= 1
		print("bumm hes deads")
	else:
		print("krasne ráno")
	
def etel_generalas(palya, le_etelek, etel_kepek):
	x = random.randrange(0, len(palya[0]))
	y = random.randrange(0, len(palya))

	le_etelek.append(((x,y), etel_kepek[random.randrange(0, len(etel_kepek))]))

def etelek_rajz(le_etelek, kar_x, kar_y):
	for i in range(0, len(le_etelek)):
		x = ((le_etelek[i][0][0]+8)-kar_x)*mozgas
		y = ((le_etelek[i][0][1]+8)-kar_y)*mozgas
		win.blit(le_etelek[i][1], (x,y))

#Ez a térképen egyhejben rajzolja meg hogy fenn maradjon a mozgás illuziója
def gonosz_mozgatas(kar_x, kar_y, gonosz_x, gonosz_y):

	#50px
	x = ((gonosz_x+8)-kar_x)*mozgas
	y = ((gonosz_y+8)-kar_y)*mozgas
	
	return (x-50,y-50)


def kaja_teszt(kar_x,kar_y, le_etelk):
	rmv = None
	global elet
	for i in range(0, len(le_etelk)):
		act = le_etelk[i]
		if(kar_x == act[0][0] and kar_y == act[0][1]):
			elet +=1
			
			rmv = act
			break
	if(rmv != None):
		le_etelk.remove(rmv)
			


#kepek meg pálya betöltése
karakterk = karakterek_betoltese("kepek/karakterek.png")
palya_elemk = palya_elemk_betoltese("kepek/palya")
palya = palya_terv_betoltese("palya2.txt")
elet_kep = [pygame.image.load("kepek/sziv.png").convert_alpha(),pygame.image.load("kepek/ures_sziv.png").convert_alpha(),pygame.image.load("kepek/gon_sziv.png").convert_alpha()]

etelek = etelek_betoltese("kepek/etelek")

lerakott_etelek =[]

gonosz_time = time.time()

hp_time = time.time()

etel_ido = time.time()

while run: 
	pygame.time.delay(10) 
	
	for event in pygame.event.get(): 
		if event.type == pygame.QUIT: 
			run = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			if pygame.mouse.get_pressed()[0]:
				killhim()

	keys = pygame.key.get_pressed() 
	
	if((time.time()-start_ido) >0.1):
		
		if keys[pygame.K_a] and akadaj_teszt(palya, max(kar_x-1, 0), kar_y, '#'):
			kar_x -= 1
			kar_x = max(kar_x, 0)

		if keys[pygame.K_d]and akadaj_teszt(palya, max(kar_x+1, 0), kar_y, '#'):
			kar_x += 1 
            
		if keys[pygame.K_w]and akadaj_teszt(palya, kar_x, max(kar_y-1, 0),'#'): 
			kar_y -= 1 
			kar_y = max(0, kar_y)
            
		if keys[pygame.K_s]and akadaj_teszt(palya, kar_x, max(kar_y+1, 0),'#'):
			kar_y += 1
		start_ido = time.time()
	
		
	if((time.time()-gonosz_time)>0.05):
		gonosz_ai()
		gonosz_time = time.time()
		
		#print("dx: ",dx,"  dy: ",dy, "    mx:",mx, " my: ",my)
		#print("dx: ",kar_x,"  dy: ",kar_y)
    
	if((time.time()-hp_time)>0.5):
		hp_time = time.time()
		if(kar_x < gon_x + 1 and kar_x > gon_x - 1) and (kar_y < gon_y + 1 and kar_y > gon_y - 1):
			elet = max(0, elet-1)

	if((time.time()-etel_ido)>2):
		etel_generalas(palya, lerakott_etelek, etelek)
		etel_ido = time.time()
	
	win.fill((255, 255, 255)) 
	
	
	palya_rajz(palya, palya_elemk,kar_x,kar_y)
	karakter_rajz((400 -50,400-50), karakterk[0])

	#gonosz
	if gon_elet > 1:
		karakter_rajz(gonosz_mozgatas(kar_x, kar_y, gon_x, gon_y), karakterk[19])


	#etelek
	etelek_rajz(lerakott_etelek, kar_x, kar_y)

	kaja_teszt(kar_x, kar_y, lerakott_etelek)
	elet_rajz(elet_kep)
	gon_elet_rajz(elet_kep)
	
	pygame.display.update() 




pygame.quit()