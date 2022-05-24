import os

import IOHandler as io
from tkinter import filedialog, Tk
from Schedule import Schedule
import pygame
import sys

pygame.init()
pygame.display.set_caption("Graafiku koostamine")
screen = pygame.display.set_mode((1350, 650))

opening_image = pygame.image.load("images/opening.png")
opening_hover_image = pygame.image.load("images/opening_hover.png")
saving_image = pygame.image.load("images/saving.png")
saving_hover_image = pygame.image.load("images/saving_hover.png")

button_box = pygame.Rect(125, 480, 275, 55)

screen.blit(opening_image, (0, 0))

pygame.display.update()


def run(screen):
    Tk().withdraw()
    askopenfilename = filedialog.askopenfilename()
    sheets = io.read_from_excel(askopenfilename)
    bests = []
    for data in sheets:
        best = Schedule(data["month"], data["year"], data["template"], data["employees"])
        best.fill_schedule()

        screen.blit(pygame.image.load("images/loading.png"), (0, 0))
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(250, 417, 850, 70), 5)
        pygame.draw.rect(screen, (246, 246, 246), pygame.Rect(250, 417, 850, 70))
        pygame.display.update()

        schedule = Schedule(data["month"], data["year"], data["template"], data["employees"])
        schedule.fill_schedule()
        best = schedule
        for i in range(100):
            pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(250, 417, int(i * 835 / 100), 70))
            pygame.display.update()
            schedule = Schedule(data["month"], data["year"], data["template"], data["employees"])
            schedule.fill_schedule()
            if schedule.score > best.score:
                best = schedule
        bests.append(best)
    return bests, askopenfilename


def save(bests, filename):
    io.write_to_excel(bests, filename)


opening = True
while True:
    if button_box.collidepoint(pygame.mouse.get_pos()):
        if opening:
            screen.blit(opening_hover_image, (0, 0))
        else:
            screen.blit(saving_hover_image, (0, 0))
    else:
        if opening:
            screen.blit(opening_image, (0, 0))
        else:
            screen.blit(saving_image, (0, 0))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_box.collidepoint(event.pos):
                if opening:
                    bests, filename = run(screen)
                    screen.blit(saving_image, (0, 0))
                    pygame.display.update()
                    opening = not opening
                else:
                    Tk().withdraw()
                    filename = filedialog.asksaveasfilename(
                        initialdir="C:/Users/Reijo/PycharmProjects/graafik/outputs/",
                        filetypes=[('Excel Spreadsheet', '.xlsx')],
                        defaultextension=".xlsx",
                        title="Salvesta graafik",
                        initialfile=filename.split("/")[-1].split(".")[0] + "-graafik"
                    )
                    save(bests, filename)
                    os.startfile(filename)
                    sys.exit()
