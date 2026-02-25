""" 
File: word_grid.py
Author: Amy Cardona
Course: CSC 120, Fall 2025
Purpose: Generate and print a grid of random lowercase letters.
"""
import random


def init():
    """Read grid size and seed, initialize RNG, and return grid size."""
    grid_size = int(input())
    seed_value = input()
    random.seed(seed_value)
    return grid_size


def make_grid(grid_size):
    """Create and return a grid_size x grid_size grid of random letters."""
    grid = []

    # build each row
    row_index = 0
    while row_index < grid_size:
        row = []

        col_index = 0
        while col_index < grid_size:
            # random integer 0–25
            num = random.randint(0, 25)
            # convert to letter using ASCII: 'a' is 97
            letter = chr(ord('a') + num)
            row.append(letter)
            col_index = col_index + 1

        grid.append(row)
        row_index = row_index + 1

    return grid


def print_grid(grid):
    """Print the grid, one row per line, letters separated by commas."""
    row_index = 0
    while row_index < len(grid):
        row = grid[row_index]

        col_index = 0
        while col_index < len(row):
            letter = row[col_index]

            # print comma after each letter except the last
            if col_index < len(row) - 1:
                print(letter, end=",")
            else:
                print(letter, end="")

            col_index = col_index + 1

        print()  # newline at end of row
        row_index = row_index + 1


def main():
    grid_size = init()
    grid = make_grid(grid_size)
    print_grid(grid)


if __name__ == "__main__":
    main()
