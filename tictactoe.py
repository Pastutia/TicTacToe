# Kółko i krzyżyk
# Python 3.9.5

import pygame
import sys
import random
from pygame.locals import *

pygame.init()

OKNOGRY = pygame.display.set_mode((150, 150), 0, 32)

pygame.display.set_caption('Kółko i krzyżyk')

POLE_GRY = [0, 0, 0,
            0, 0, 0,
            0, 0, 0]

RUCH = (random.choice([1, 2]))
WYGRANY = 0
WYGRANA = False

def rysuj_plansze():
    for i in range(0, 3):
        for j in range(0, 3):
            pygame.draw.rect(OKNOGRY, (255, 255, 255), Rect((j * 50, i * 50), (50, 50)), 1)

def rysuj_pole_gry():
    for i in range(0, 3):
        for j in range(0, 3):
            pole = i * 3 + j
            x = j * 50 + 25
            y = i * 50 + 25

            if POLE_GRY[pole] == 1:
                pygame.draw.circle(OKNOGRY, (0, 0, 255), (x, y), 10)
            elif POLE_GRY[pole] == 2:
                pygame.draw.circle(OKNOGRY, (255, 0, 0), (x, y), 10)

def postaw_znak(pole, RUCH):
    if POLE_GRY[pole] == 0:
        if RUCH == 1:
            POLE_GRY[pole] = 1
            return 2
        elif RUCH == 2:
            POLE_GRY[pole] = 2
            return 1

    return RUCH

def sprawdz_pola(uklad, wygrany=None):
    wartosc = None
    POLA_INDEKSY = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
        ]

    for lista in POLA_INDEKSY:
        kol = []
        for ind in lista:
            kol.append(POLE_GRY[ind])
        if (kol in uklad):
            wartosc = wygrany if wygrany else lista[kol.index(0)]

    return wartosc

# ruchy komputera

def ai_ruch(RUCH):
    pole = None

    uklady_wygrywam = [[2, 2, 0], [2, 0, 2], [0, 2, 2]]
    uklady_blokuje = [[1, 1, 0], [1, 0, 1], [0, 1, 1]]

    pole = sprawdz_pola(uklady_wygrywam)
    if pole is not None:
        return postaw_znak(pole, RUCH)
    pole = sprawdz_pola(uklady_blokuje)
    if pole is not None:
        return postaw_znak(pole, RUCH)

    while pole is None:
        pos = random.randrange(0, 9)
        if POLE_GRY[pos] == 0:
            pole = pos

    return postaw_znak(pole, RUCH)

def kto_wygral():
    uklad_gracz = [[1, 1, 1]]
    uklad_komp = [[2, 2, 2]]

    WYGRANY = sprawdz_pola(uklad_gracz, 1)
    if not WYGRANY:
        WYGRANY = sprawdz_pola(uklad_komp, 2)
    if 0 not in POLE_GRY and WYGRANY not in[1, 2]:
        WYGRANY = 3

    return WYGRANY

def drukuj_wynik(WYGRANY):
    fontObj = pygame.font.Font('freesansbold.ttf', 16)
    global text
    if WYGRANY == 1:
        text = u'Wygrał gracz!'
    elif WYGRANY == 2:
        text = u'Wygrał komputer!'
    elif WYGRANY == 3:
        text = 'Remis!'
    text_obr = fontObj.render(text, True, (20, 255, 20))
    text_prost = text_obr.get_rect()
    text_prost.center = (75, 75)
    OKNOGRY.blit(text_obr, text_prost)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if WYGRANA is False:
            if RUCH == 1:
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouseX, mouseY = event.pos
                        pole = (int(mouseY / 50) * 3) + int(mouseX / 50)
                        RUCH = postaw_znak(pole, RUCH)
            elif RUCH == 2:
                RUCH = ai_ruch(RUCH)

            WYGRANY = kto_wygral()
            if WYGRANY is not None:
                WYGRANA = True

    OKNOGRY.fill((0, 0, 0))
    rysuj_plansze()
    rysuj_pole_gry()
    if WYGRANA:
        drukuj_wynik(WYGRANY)
    pygame.display.update()