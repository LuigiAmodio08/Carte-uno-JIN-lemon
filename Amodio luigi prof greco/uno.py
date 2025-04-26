import pygame
import random
import sys

pygame.init()

LARGHEZZA, ALTEZZA = 1000, 800
SFONDO = (34, 139, 34)
LARG_CARTA = 50
ALTEZZA_CARTA = 75
colore_scelto = None
font = pygame.font.Font(None, 36)

schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA), pygame.RESIZABLE)
pygame.display.set_caption("UNO - Gioco di Carte")

class Carta:
    def __init__(self, colore, valore, tipo):
        self.colore = colore
        self.valore = valore
        self.tipo = tipo

    def __str__(self):
        return f"{self.colore} {self.valore}" if self.colore else self.valore

class Mazzo:
    COLORI = ["Rosso", "Blu", "Verde", "Giallo"]
    VALORI = [str(i) for i in range(10)] + ["+2", "Stop", "C.G"]
    SPECIALI = ["+4", "C.C"]

    def __init__(self):
        self.carte = []
        self.crea_mazzo()
        random.shuffle(self.carte)

    def crea_mazzo(self):
        for colore in self.COLORI:
            for valore in self.VALORI:
                self.carte.append(Carta(colore, valore, "numero" if valore.isdigit() else "azione"))
                if valore != "0":
                    self.carte.append(Carta(colore, valore, "numero" if valore.isdigit() else "azione"))
        for _ in range(4):
            self.carte.append(Carta(None, "+4", "azione"))
            self.carte.append(Carta(None, "C.C", "azione"))

    def pesca_carta(self):
        return self.carte.pop() if self.carte else None

class Giocatore:
    def __init__(self, nome):
        self.nome = nome
        self.mano = []

    def pesca(self, mazzo, num):
        for _ in range(num):
            carta = mazzo.pesca_carta()
            if carta:
                self.mano.append(carta)

    def rimuovi_carta(self, carta):
        if carta in self.mano:
            self.mano.remove(carta)

def disegna_carta(schermo, carta, x, y):
    colori = {
        "Rosso": (255, 0, 0),
        "Blu": (0, 0, 255),
        "Verde": (0, 255, 0),
        "Giallo": (255, 255, 0),
        None: (128, 128, 128)
    }
    pygame.draw.rect(schermo, colori.get(carta.colore, (255, 255, 255)), (x, y, LARG_CARTA, ALTEZZA_CARTA))
    pygame.draw.rect(schermo, (0, 0, 0), (x, y, LARG_CARTA, ALTEZZA_CARTA), 2)
    testo = pygame.font.Font(None, 24).render(str(carta.valore), True, (0, 0, 0))
    schermo.blit(testo, (x + 5, y + 25))

def disegna_mazzo(schermo, x, y):
    pygame.draw.rect(schermo, (50, 50, 50), (x, y, LARG_CARTA, ALTEZZA_CARTA))
    pygame.draw.rect(schermo, (0, 0, 0), (x, y, LARG_CARTA, ALTEZZA_CARTA), 2)
    testo = pygame.font.Font(None, 20).render("MAZZO", True, (255, 255, 255))
    schermo.blit(testo, (x + 2, y + 25))

def scegli_colore(schermo):
    global colore_scelto
    colori = ["Rosso", "Blu", "Verde", "Giallo"]
    posizioni = [(300, ALTEZZA // 2 - 75), (450, ALTEZZA // 2 - 75), (600, ALTEZZA // 2 - 75), (750, ALTEZZA // 2 - 75)]

    while True:
        for i, colore in enumerate(colori):
            x, y = posizioni[i]
            colore_rgb = {"Rosso": (255, 0, 0), "Blu": (0, 0, 255), "Verde": (0, 255, 0), "Giallo": (255, 255, 0)}
            pygame.draw.rect(schermo, colore_rgb[colore], (x, y, LARG_CARTA, ALTEZZA_CARTA))
            pygame.draw.rect(schermo, (0, 0, 0), (x, y, LARG_CARTA, ALTEZZA_CARTA), 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                for i, (x, y) in enumerate(posizioni):
                    if x < mouse[0] < x + LARG_CARTA and y < mouse[1] < y + ALTEZZA_CARTA:
                        colore_scelto = colori[i]
                        return

def disegna_uno(schermo, giocatore):
    if len(giocatore.mano) == 1:
        testo = pygame.font.Font(None, 48).render("UNO!", True, (255, 255, 0))
        schermo.blit(testo, (LARGHEZZA // 2 - 50, ALTEZZA // 2 - 200))

def turno(giocatore, mazzo, carta_in_tavola, mouse_pos, posizioni):
    for i, carta in enumerate(giocatore.mano):
        x, y = posizioni[i]
        if x <= mouse_pos[0] <= x + LARG_CARTA and y <= mouse_pos[1] <= y + ALTEZZA_CARTA:
            if carta.colore == carta_in_tavola.colore or carta.valore == carta_in_tavola.valore or carta.colore is None:
                giocatore.rimuovi_carta(carta)
                return carta, carta.valore
    pescata = mazzo.pesca_carta()
    if pescata:
        giocatore.mano.append(pescata)
    return carta_in_tavola, None

def schermata_iniziale():
    play_button = pygame.Rect(LARGHEZZA // 2 - 75, 400, 150, 60)

    while True:
        schermo.fill(SFONDO)
        titolo = pygame.font.Font(None, 96).render("CARTE UNO", True, (255, 255, 255))
        sottotitolo = pygame.font.Font(None, 36).render("by JIN lemon", True, (255, 255, 255))
        schermo.blit(titolo, (LARGHEZZA // 2 - titolo.get_width() // 2, 100))
        schermo.blit(sottotitolo, (LARGHEZZA // 2 - sottotitolo.get_width() // 2, 200))

        colore_btn = (0, 128, 0) if play_button.collidepoint(pygame.mouse.get_pos()) else (34, 139, 34)
        pygame.draw.rect(schermo, colore_btn, play_button)
        pygame.draw.rect(schermo, (255, 255, 255), play_button, 2)
        play_txt = font.render("GIOCA", True, (255, 255, 255))
        schermo.blit(play_txt, (play_button.x + 30, play_button.y + 15))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and play_button.collidepoint(event.pos):
                return

def schermata_login():
    texts = ["Nome Giocatore 1", "Nome Giocatore 2", "Nome Giocatore 3"]
    inputs = ["", "", ""]
    active = [False, False, False]
    input_rects = [pygame.Rect(LARGHEZZA//2 - 100, 300 + i*60, 200, 40) for i in range(3)]
    play_button = pygame.Rect(LARGHEZZA//2 - 75, 550, 150, 50)

    while True:
        schermo.fill(SFONDO)
        for i in range(3):
            colore = (255, 255, 255) if active[i] else (200, 200, 200)
            pygame.draw.rect(schermo, colore, input_rects[i], 2)
            if inputs[i] == "":
                placeholder = font.render(texts[i], True, (180, 180, 180))
                schermo.blit(placeholder, (input_rects[i].x + 5, input_rects[i].y + 5))
            else:
                testo_surface = font.render(inputs[i], True, (255, 255, 255))
                schermo.blit(testo_surface, (input_rects[i].x + 5, input_rects[i].y + 5))

        pygame.draw.rect(schermo, (0, 128, 0), play_button)
        play_text = font.render("GIOCA", True, (255, 255, 255))
        schermo.blit(play_text, (play_button.x + 30, play_button.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(input_rects):
                    active[i] = rect.collidepoint(event.pos)
                if play_button.collidepoint(event.pos) and all(inputs):
                    return inputs
            if event.type == pygame.KEYDOWN:
                for i in range(3):
                    if active[i]:
                        if event.key == pygame.K_BACKSPACE:
                            inputs[i] = inputs[i][:-1]
                        else:
                            inputs[i] += event.unicode

# TUTTO IL RESTO DEL TUO CODICE RIMANE IDENTICO FINO A:
# def avvia_gioco(nomi):
# Aggiungiamo la nuova versione di questa funzione modificata:

def avvia_gioco(nomi):
    mazzo = Mazzo()
    giocatori = [Giocatore(nome) for nome in nomi]
    for g in giocatori:
        g.pesca(mazzo, 7)

    while True:
        carta_in_tavola = mazzo.pesca_carta()
        if carta_in_tavola and carta_in_tavola.valore.isdigit():
            break

    turno_corrente = 0
    direzione = 1 
    running = True

    while running:
        schermo.fill(SFONDO)
        disegna_carta(schermo, carta_in_tavola, LARGHEZZA // 2 - 60, ALTEZZA // 2 - 50)
        disegna_mazzo(schermo, LARGHEZZA // 2 + 70, ALTEZZA // 2 - 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                g = giocatori[turno_corrente]
                mouse = pygame.mouse.get_pos()
                if turno_corrente == 0:
                    pos = [(200 + i * (LARG_CARTA + 5), ALTEZZA - 150) for i in range(len(g.mano))]
                elif turno_corrente == 1:
                    pos = [(200 + i * (LARG_CARTA + 5), 50) for i in range(len(g.mano))]
                else:
                    pos = [(50, 150 + i * (ALTEZZA_CARTA + 5)) for i in range(len(g.mano))]

                carta_in_tavola, azione = turno(g, mazzo, carta_in_tavola, mouse, pos)

                # Mostra "UNO!" se ha solo una carta
                if len(g.mano) == 1:
                    schermo.fill(SFONDO)
                    uno_txt = pygame.font.Font(None, 72).render("UNO!", True, (255, 255, 0))
                    schermo.blit(uno_txt, (LARGHEZZA // 2 - uno_txt.get_width() // 2, ALTEZZA // 2 - 100))
                    pygame.display.flip()
                    pygame.time.delay(2000)

                # Controlla se il giocatore ha vinto
                if len(g.mano) == 0:
                    schermo.fill(SFONDO)
                    vincita_txt = pygame.font.Font(None, 64).render(f"{g.nome} HA VINTO!", True, (255, 255, 255))
                    schermo.blit(vincita_txt, (LARGHEZZA // 2 - vincita_txt.get_width() // 2, ALTEZZA // 2))
                    pygame.display.flip()
                    pygame.time.delay(3000)
                    running = False
                    break

                # Gestione effetti carte speciali
                if azione in ["+4", "C.C"]:
                    scegli_colore(schermo)
                    carta_in_tavola.colore = colore_scelto
                if azione == "+4":
                    giocatori[(turno_corrente + direzione) % 3].pesca(mazzo, 4)
                elif azione == "+2":
                    giocatori[(turno_corrente + direzione) % 3].pesca(mazzo, 2)
                elif azione == "Stop":
                    turno_corrente = (turno_corrente + direzione) % 3
                elif azione == "C.G":
                    direzione *= -1  

                turno_corrente = (turno_corrente + direzione) % 3

        # Disegna carte e nomi giocatori
        for i, g in enumerate(giocatori):
            nome_txt = pygame.font.Font(None, 28).render(g.nome, True, (255, 255, 255))
            if i == 0:
                for j, carta in enumerate(g.mano):
                    disegna_carta(schermo, carta, 200 + j * (LARG_CARTA + 5), ALTEZZA - 150)
                schermo.blit(nome_txt, (LARGHEZZA // 2 - 60, ALTEZZA - 60))
            elif i == 1:
                for j, carta in enumerate(g.mano):
                    disegna_carta(schermo, carta, 200 + j * (LARG_CARTA + 5), 50)
                schermo.blit(nome_txt, (LARGHEZZA // 2 - 60, 20))
            else:
                for j, carta in enumerate(g.mano):
                    disegna_carta(schermo, carta, 50, 150 + j * (ALTEZZA_CARTA + 5))
                
                nome_txt_verticale = pygame.transform.rotate(nome_txt, 90)  # Ruota il testo di 90 gradi
                schermo.blit(nome_txt_verticale, (20, ALTEZZA // 2))  # Posiziona il nome ruotato
        pygame.display.flip()


def main():
    schermata_iniziale()
    nomi = schermata_login()
    avvia_gioco(nomi)

if __name__ == "__main__":
    main()    