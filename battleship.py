
'''
File: battleship.py
Author: Amy Cardona
Course: CSC 120 
Purpose: This program loads Player 1’s ship placements
onto a 10×10 grid, checks the placement file
for all required errors, and then processes
Player 2’s guesses one by one to report
misses, hits, and sunk ships. It ends when 
either all ships are sunk or there are no more 
guesses to process.
'''

import sys


class GridPos:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ship = None
        self.guessed = False

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"


class Ship:
    def __init__(self, kind, size):
        self.kind = kind
        self.size = size
        self.positions = []
        self.remaining = size

    def __str__(self):
        return self.kind


class Board:
    def __init__(self):
        self.grid = []
        y = 0
        while y < 10:
            row = []
            x = 0
            while x < 10:
                row.append(GridPos(x, y))
                x += 1
            self.grid.append(row)
            y += 1

        self.ships = {}

    def place_ship(self, kind, x1, y1, x2, y2, line):

        if x1 < 0 or x1 > 9 or x2 < 0 or x2 > 9 or y1 < 0 or y1 > 9 or y2 < 0 or y2 > 9:
            print("ERROR: ship out-of-bounds: " + line)
            sys.exit(0)

        if not (x1 == x2 or y1 == y2):
            print("ERROR: ship not horizontal or vertical: " + line)
            sys.exit(0)

        correct_size = 0
        if kind == "A":
            correct_size = 5
        elif kind == "B":
            correct_size = 4
        elif kind == "S":
            correct_size = 3
        elif kind == "D":
            correct_size = 3
        elif kind == "P":
            correct_size = 2

        coords = []

        if x1 == x2:
            low = y1
            high = y2
            if y2 < y1:
                low = y2
                high = y1
            y = low
            while y <= high:
                coords.append((x1, y))
                y += 1
        else:
            low = x1
            high = x2
            if x2 < x1:
                low = x2
                high = x1
            x = low
            while x <= high:
                coords.append((x, y1))
                x += 1

        if len(coords) != correct_size:
            print("ERROR: incorrect ship size: " + line)
            sys.exit(0)

        i = 0
        while i < len(coords):
            cx = coords[i][0]
            cy = coords[i][1]
            if self.grid[cy][cx].ship is not None:
                print("ERROR: overlapping ship: " + line)
                sys.exit(0)
            i += 1

        ship = Ship(kind, correct_size)
        i = 0
        while i < len(coords):
            cx = coords[i][0]
            cy = coords[i][1]
            pos = self.grid[cy][cx]
            pos.ship = ship
            ship.positions.append(pos)
            i += 1

        self.ships[kind] = ship

    def process_guess(self, x, y):

        if x < 0 or x > 9 or y < 0 or y > 9:
            print("illegal guess")
            return

        pos = self.grid[y][x]

        if pos.ship is None:
            if pos.guessed:
                print("miss (again)")
            else:
                print("miss")
                pos.guessed = True
            return

        ship = pos.ship

        if pos.guessed:
            all_hit_before = True
            j = 0
            while j < len(ship.positions):
                if not ship.positions[j].guessed:
                    all_hit_before = False
                j += 1
            print("hit (again)")
            return

        pos.guessed = True
        ship.remaining -= 1

        if ship.remaining == 0:
            print(ship.kind + " sunk")

            all_sunk = True
            for k in self.ships:
                if self.ships[k].remaining > 0:
                    all_sunk = False
            if all_sunk:
                print("all ships sunk: game over")
                sys.exit(0)
            return

        print("hit")


def main():

    placement_file = input()
    board = Board()

    try_file = open(placement_file, "r")
    lines = []
    line = try_file.readline()
    while line != "":
        lines.append(line.strip())
        line = try_file.readline()
    try_file.close()

    ship_counts = {"A": 0, "B": 0, "S": 0, "D": 0, "P": 0}

    i = 0
    while i < len(lines):
        parts = lines[i].split()
        if len(parts) == 5:
            kind = parts[0]
            if kind in ship_counts:
                ship_counts[kind] += 1
        i += 1

    for k in ship_counts:
        if ship_counts[k] != 1:
            print("ERROR: fleet composition incorrect")
            sys.exit(0)

    i = 0
    while i < len(lines):
        parts = lines[i].split()
        kind = parts[0]
        x1 = int(parts[1])
        y1 = int(parts[2])
        x2 = int(parts[3])
        y2 = int(parts[4])
        board.place_ship(kind, x1, y1, x2, y2, lines[i])
        i += 1

    guess_file = input()
    gf = open(guess_file, "r")
    glines = []
    g = gf.readline()
    while g != "":
        glines.append(g.strip())
        g = gf.readline()
    gf.close()

    i = 0
    while i < len(glines):
        parts = glines[i].split()
        if len(parts) == 2:
            x = int(parts[0])
            y = int(parts[1])
            board.process_guess(x, y)
        i += 1


main()
