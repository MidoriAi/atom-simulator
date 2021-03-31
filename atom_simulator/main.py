import pygame as pg, sys
from pygame.locals import *
from button import Button
import random

pg.init()

W = 600
H = 600
s = pg.display.set_mode((W, H))
pg.display.set_caption("Atomos")
clock = pg.time.Clock()

RED = (255, 0, 0)
GRAY = (150, 150, 150)
GREEN = (50, 250, 100)
WHITE = (255, 255, 255)

FONT = pg.font.SysFont("Arial", 30)
SMALL_FONT = pg.font.SysFont("Arial", 15)

E_RIGHT = [[pos, 280] for pos in range(400, 600, 20)] # the y pos of right/left is fixed!
E_LEFT = [[pos, 280] for pos in range(200, 0, -20)]
E_UP = [[280, pos] for pos in range(200, 0, -20)] # the x pos of up/down is fixed!
E_DOWN = [[280, pos] for pos in range(400, 600, 20)]
E_RIGHT2 = [[pos, 320] for pos in range(400, 600, 20)] # the y pos of right/left is fixed!
E_LEFT2 = [[pos, 320] for pos in range(200, 0, -20)]
E_UP2 = [[320, pos] for pos in range(200, 0, -20)] # the x pos of up/down is fixed!
E_DOWN2 = [[320, pos] for pos in range(400, 600, 20)]
E_SHELL = 0
E_POS = [E_RIGHT, E_LEFT, E_DOWN, E_UP, E_RIGHT2, E_LEFT2, E_DOWN2, E_UP2]
E_DIR = 0

RADIUS = 100
element_symbols = []

def make_txt(txt, font, color): return font.render(txt, True, color)

class Particle:
    def __init__(self, pos, particle_type):
        self.x = pos[0]
        self.y = pos[1]
        self.type = particle_type
        # 0:electron, 1:proton, 2:neutron
        if particle_type == 0:
            self.color = GREEN
        elif particle_type == 1:
            self.color = RED
        elif particle_type == 2:
            self.color = GRAY

    def draw(self): pg.draw.circle(s, self.color, (self.x, self.y), 5)


class Shell:
    def __init__(self, radius):
        self.radius = radius

    def draw_shell(self):
        pg.draw.circle(s, WHITE, (W / 2, H / 2), self.radius, 1)

first_electrons = []
electron_list = []
proton_list = []
neutron_list = []
shell_list = []

# CHEMICAL SYMBOLS
symbols = {}
with open('ex.txt') as file:
    output = []
    file = file.readlines()
    for lines in file:
        output.append(lines.split('\n '))

    for i, elem in enumerate(output):
        symbols[i] = (elem[0].replace('\n', '').split(' - '))
while True:
    s.fill((50, 50, 50))
    shell = Shell(RADIUS)
    shell_list.append(shell)

    # BUTTONS
    e = Button(H - 500, W - 100, make_txt("E", FONT, WHITE), 1)
    p = Button(H - 300, W - 100, make_txt("P", FONT, WHITE), 1)
    n = Button(H - 100, W - 100, make_txt("N", FONT, WHITE), 1)

    # SYMBOL AT TOP LEFT
    Button(40, 40, make_txt(f"{symbols[len(proton_list)][0]} - {symbols[len(proton_list)][1]}", FONT, WHITE), 1).draw(s)

    # QUANTITY OF EACH PARTICLE TYPES
    Button(105, 550, make_txt(f"{len(electron_list) + len(first_electrons)}", SMALL_FONT, WHITE), 1).draw(s)
    Button(305, 550, make_txt(f"{len(proton_list)}", SMALL_FONT, WHITE), 1).draw(s)
    Button(505, 550, make_txt(f"{len(neutron_list)}", SMALL_FONT, WHITE), 1).draw(s)

    # CLASSIFY IF ITS AN "ION" OR "ATOM"
    atom_type = ""
    if len(proton_list) == len(electron_list) + len(first_electrons): atom_type = "Atom"
    elif len(proton_list) > len(electron_list) + len(first_electrons): atom_type = "+Ion"
    elif len(proton_list) < len(electron_list) + len(first_electrons):atom_type = "-Ion"
    Button(40, 90, make_txt(f"{atom_type}", SMALL_FONT, WHITE), 1).draw(s)

    all_electrons = first_electrons + electron_list

    if e.draw(s) == 1:
        if E_SHELL == 0:
            E_DIR += 1
            if E_DIR > 2:
                E_DIR = 0
                E_SHELL += 1
                RADIUS += 20
                new_shell = Shell(RADIUS)
                shell_list.append(new_shell)
            new_e = Particle(E_POS[E_DIR][E_SHELL], 0)
            first_electrons.append(new_e)
        else:
            E_DIR += 1
            if E_DIR >= 8: E_DIR = 0
            if len(electron_list) % 8 == 0 and len(electron_list) != 0:
                E_SHELL += 1
                RADIUS += 20
                new_shell = Shell(RADIUS)
                shell_list.append(new_shell)

            new_e = Particle(E_POS[E_DIR][E_SHELL], 0)
            electron_list.append(new_e)
            # print(f'E: {len(electron_list) + len(first_electrons)}, E_DIR: {E_DIR}, E_SHELL: {E_SHELL}')

    if p.draw(s) == 1 and len(proton_list) <= 117:
        new_p = Particle([random.randint(280, W//2+20), random.randint(280, H//2+20)], 1)
        proton_list.append(new_p)

    if n.draw(s) == 1:
        new_n = Particle([random.randint(280, W//2+20), random.randint(280, H//2+20)], 2)
        neutron_list.append(new_n)

    if e.draw(s) == 2 and len(electron_list) > 0:
        electron_list.pop()
        if len(electron_list) % 8 == 0:
            E_DIR -= 1
            E_SHELL -= 1
            RADIUS -= 20
            shell_list.pop()

    elif e.draw(s) == 2 and len(first_electrons) > 0: first_electrons.pop()
    if p.draw(s) == 2 and len(proton_list) > 0: proton_list.pop()
    if n.draw(s) == 2 and len(neutron_list) > 0: neutron_list.pop()

    for shell in shell_list: shell.draw_shell()
    for electron in all_electrons: electron.draw()
    for proton in proton_list: proton.draw()
    for neutron in neutron_list: neutron.draw()

    for e in pg.event.get():
        if e.type == QUIT:
            pg.quit()
            sys.exit()

    clock.tick(8)
    pg.display.update()

# === Step 4 ===
# remove a particle when is btn right clicked
# figure out how to remove a shell when all electrons have been wiped out a shell

# === Step 3 ====
# only 2 Es in inner shell
# add the Element Symbol at the top left corner
# display the # of particles of each
# classify whether its an Atom or Ion, display text below the chemical symbol

# === Step 2 ===
# lets 1st try to spawn the Es to the edges of the smallest rectangle of a shell
# -- or div the shell and find the x & y to locate where the E will sit
# -- (THIS!) or just type out the exact location of the E then adding a certain x or y to adjust the pos
# make the Es spawn within the shells and if the Es % 8 add another shell...

# === Step 1 ===
# init class Particle and class Shell
# create a list for each the # of electrons, protons, neutrons and shells
# add btns so each time its clicked it creates a new particle then adds it to one of the lists
# add a clock
