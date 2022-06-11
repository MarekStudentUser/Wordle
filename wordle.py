import pygame
import time
import pygame.locals
import random

pygame.init()

#tworzenie okna gry o wymiarach 800x650, ustalenie koloru, nazwy okna
okno = pygame.display.set_mode((800,650),0,32)
tlo = (0,0,0)
pygame.display.set_caption('WORDLE')

#ustawienia kafelka klawiatury - rozmiar, kolor
kafelek_tlo = pygame.Surface([50,50])
kafelek_tlo.fill((100,100,100))

#ustawienia kafelka który będzie zakrywał usuwane litery
kafelek_tlo2 = pygame.Surface([50,50])
kafelek_tlo2.fill((0,0,0))

#ustawienia czcionki liter na kafelkach, lista alfabetu w kolejności qwerty, która pomoże stworzyć klawiaturę
litera = pygame.font.SysFont('arial',40,True,False)
alf = ['Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']

#w liście kafelki będą zapisane kolejne kafelki klawiatury
kafelki = []
kafelki_poz = []
haslo_poz1 = []
haslo_poz2 = []

#haslo ktore ma zgadnać gracz,idk zmiencie to jakos najwyzej
haslo='arrow'
#funkcja, która rysuje miejsce na wpisywanie hasła, zależne od 2 danych dłguość hasła = ile; liczba prób = proby
def rysuj_haslo(ile,proby):
    for i in range(proby):
        for j in range(ile):
            pygame.draw.rect(okno,(255,255,255),pygame.Rect((280+j*50,10+i*50),(50,50)),1)
            haslo_poz1.append((280+j*50+10,10+i*50))
            haslo_poz2.append((280 + j * 50, 10+i * 50))
            pygame.display.update()

#funkcja rysuje klawiaturę 'QWERTY', za pomocą której gracz będzie wpisywać hasło
def rysuj_klawiature():
    for i in range(10):
        kafelek_tlo = pygame.Surface([50, 50])
        kafelek_tlo.fill((100, 100, 100))
        kafelek = litera.render(alf[i], True, (255, 255, 255), None)
        kafelki.append(kafelek_tlo)
        kafelki[i].blit(kafelek,(10,4))
        okno.blit(kafelki[i], (140+5*i + (i * 50),465))
        kafelki_poz.append([140+5*i + (i * 50),465])
        del kafelek_tlo
    for i in range(9):
        kafelek_tlo = pygame.Surface([50, 50])
        kafelek_tlo.fill((100, 100, 100))
        kafelek = litera.render(alf[10+i], True, (255, 255, 255), None)
        kafelki.append(kafelek_tlo)
        kafelki[10+i].blit(kafelek, (10, 4))
        okno.blit(kafelki[10+i], (170 + 5 * i + (i * 50), 520))
        kafelki_poz.append([170 + 5 * i + (i * 50), 520])
        del kafelek_tlo
    for i in range(7):
        kafelek_tlo = pygame.Surface([50, 50])
        kafelek_tlo.fill((100, 100, 100))
        kafelek = litera.render(alf[19+i], True, (255, 255, 255), None)
        kafelki.append(kafelek_tlo)
        kafelki[19+i].blit(kafelek, (10, 4))
        okno.blit(kafelki[19+i], (200 + 5 * i + (i * 50), 575))
        kafelki_poz.append([200 + 5 * i + (i * 50), 575])
        del kafelek_tlo
    #kafelek do usuwania błędnie wprowadzonych liter
    kafelek_tlo = pygame.Surface([50, 50])
    kafelek_tlo.fill((100, 100, 100))
    kafelek = litera.render("<-", True, (255, 255, 255), None)
    kafelki.append(kafelek_tlo)
    kafelki[26].blit(kafelek, (5, 10))
    okno.blit(kafelki[26], (200 + 5 * 7 + (7 * 50), 575))
    kafelki_poz.append([200 + 5 * 7 + (7 * 50), 575])
    del kafelek_tlo
    #kafelek do sprawdzenia hasła
    kafelek_tlo = pygame.Surface([50, 50])
    kafelek_tlo.fill((100, 100, 100))
    kafelek = litera.render("+", True, (255, 255, 255), None)
    kafelki.append(kafelek_tlo)
    kafelki[27].blit(kafelek, (12, 5))
    okno.blit(kafelki[27], (200 + 5 * 8 + (8 * 50), 575))
    kafelki_poz.append([200 + 5 * 8 + (8 * 50), 575])
    del kafelek_tlo
   
        
def losuj_haslo(ile):
    wyborhasla = int(input("Jaką długość słów wybierasz? "))
    if wyborhasla == 4:
        print(random.choice(open('4litery.txt', 'r').readlines()).strip())
    elif wyborhasla == 5:
        print(random.choice(open('5liter.txt', 'r').readlines()).strip())
    elif wyborhasla == 6:
        print(random.choice(open('6liter.txt', 'r').readlines()).strip())
    else:
        print("Niestety nie mamy do wyboru słów o wybranej przez ciebie długości :(")
    #hasło ma być zwrócone (poprzez return) w formie stringa 

    
#na podstawie współrzędnych kliknięcia myszki funkcja szuka numeru, który jest indeksem w liście alf
def szukaj_znak(poz1,poz2):
    for i in range(28):
        if poz1>=(kafelki_poz[i][0]) and poz1<=(kafelki_poz[i][0]+50):
            for j in range(28):
                if poz2 >= (kafelki_poz[j][1]) and (poz2 <= kafelki_poz[j][1] + 50):
                    if j == i:
                        return i
#sprawdzenie                    
def sprawdz(wpisane,slowo):
    baza={z:slowo.count(z) for z in slowo}
    kolory=[(255, 0, 0) for _ in range(len(wpisane))]
    for (i,z) in enumerate(wpisane):
        if wpisane[i]==slowo[i]:
            kolory[i]=(0, 255, 0)
            baza[z]-=1
    for (i,z) in enumerate(wpisane):
        if kolory[i] != (0, 255 , 0) and wpisane[i] in slowo and baza[z]>0:
            kolory[i] = (255, 255, 0)
            baza[z]-=1
    return kolory 
#funkcja wpisuje znak w okienko wyboru hasła lub usuwa znak albo wywołuje funkcję sprawdzenia hasła           
def wpisz_znak(wpisane,poz,n):
    if n == 26:
        if wpisane:
            wpisane.pop()
            okno.blit(kafelek_tlo2,haslo_poz2[poz-1])
            pygame.draw.rect(okno, (255, 255, 255), pygame.Rect(haslo_poz2[poz-1], (50, 50)), 1)
            poz-=1
    elif n == 27:
        if len(wpisane)==5:
            kolory = sprawdz(wpisane,haslo.upper())
            for (i,z) in enumerate(wpisane):
                lit = litera.render(z, True, kolory[i], None)
                okno.blit(lit,haslo_poz1[poz-len(wpisane)+i])              
            wpisane = []
            return poz, wpisane
    else:
        if len(wpisane)<5:
            wpisane.append(alf[n])
            lit = litera.render(alf[n], True, (255, 255, 255), None)
            okno.blit(lit,haslo_poz1[poz])
            poz+=1
    return poz,wpisane

okno.fill(tlo)
dlugosc=5 #domyślna długość słowa
kratki=25 #domyślna liczba kratek do wpisania hasła
rysuj_haslo(dlugosc,int(kratki/dlugosc)) #parametry to długość hasła i liczba prób (liczba kratek/długosc hasła)
rysuj_klawiature()
pygame.display.update()
pozycja_wpisz=0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                poz1, poz2 = pygame.mouse.get_pos()
                znak = szukaj_znak(poz1,poz2)
                if znak:
                    pozycja_wpisz,wpisane=wpisz_znak(wpisane,pozycja_wpisz,znak)
                    pygame.display.update()
