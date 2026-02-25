""" 
File: word_search.py
Author: Amy Cardona
Course: CSC 120, Fall 2025
Program: The program reads two filenames (word list and letter grid) from input without 
prompts. It loads the word list into a list (one word per line) and the letter grid into
an NxN matrix of space-separated letters. It then searches the grid for valid, 
case-insensitive words from the list, collects matches, and prints them in a specified 
format.
"""

# Helper functions for reading input files-------------------------------
def get_word_list():
    """Read the word-list filename from input and return a list of words (lowercase)."""
    word_file = input().strip()
    words = []
    f = open(word_file, "r")
    line = f.readline()
    while line != "":
        word = line.strip()
        if word != "":
            words.append(word.lower())
        line = f.readline()
    f.close()
    return words


def read_letters_file():
    """Read the grid-of-letters filename from input and return a grid (list of lists)."""
    grid_file = input().strip()
    grid = []

    f = open(grid_file, "r")
    line = f.readline()
    while line != "":
        stripped = line.strip()
        if stripped != "":
            parts = stripped.split()
            row = []
            i = 0
            while i < len(parts):
                row.append(parts[i].lower())
                i = i + 1
            grid.append(row)
        line = f.readline()
    f.close()

    return grid

# Simple list utilities (like concat_list and column2list)

def concat_list(lst, start, end):
    """
    Concatenate elements lst[start:end] into a single string.
    end is exclusive (like slicing).
    """
    s = ""
    i = start
    while i < end and i < len(lst):
        s = s + lst[i]
        i = i + 1
    return s


def column2list(grid, col_index):
    """Return the col_index-th column of grid as a list of letters."""
    col = []
    row = 0
    while row < len(grid):
        col.append(grid[row][col_index])
        row = row + 1
    return col


def reverse_list(lst):
    """Return a new list containing the elements of lst in reverse order."""
    result = []
    i = len(lst) - 1
    while i >= 0:
        result.append(lst[i])
        i = i - 1
    return result

# Core word-search helpers-----------------------------------------------

def add_word_if_valid(candidate, word_list, found_words):
    """
    If candidate is at least 3 letters, appears in word_list, and is not
    already in found_words, append it to found_words.
    """
    if len(candidate) < 3:
        return

    candidate_lower = candidate.lower()

    # Check if candidate is in word_list
    in_word_list = False
    i = 0
    while i < len(word_list):
        if word_list[i] == candidate_lower:
            in_word_list = True
            break
        i = i + 1

    if not in_word_list:
        return

    # Check for duplicates in found_words
    already_found = False
    j = 0
    while j < len(found_words):
        if found_words[j] == candidate_lower:
            already_found = True
            break
        j = j + 1

    if not already_found:
        found_words.append(candidate_lower)


def search_line(line_letters, word_list, found_words):
    """
    Given a list of letters (one-dimensional), search all contiguous
    substrings of length >= 3 and record legal words.
    """
    n = len(line_letters)
    start = 0
    while start < n:
        length = 3
        while start + length <= n:
            candidate = concat_list(line_letters, start, start + length)
            add_word_if_valid(candidate, word_list, found_words)
            length = length + 1
        start = start + 1


def get_diagonal(grid, start_row, start_col):
    """
    Extract a diagonal going from upper-left to lower-right,
    starting at (start_row, start_col), as a list of letters.
    """
    diag = []
    r = start_row
    c = start_col
    n_rows = len(grid)
    if n_rows == 0:
        return diag
    n_cols = len(grid[0])

    while r < n_rows and c < n_cols:
        diag.append(grid[r][c])
        r = r + 1
        c = c + 1

    return diag


# Search in different directions---------------------------------

def find_horizontal_words(grid, word_list, found_words):
    """Find words horizontally (left-to-right and right-to-left)."""
    row_index = 0
    while row_index < len(grid):
        row = grid[row_index]
        # Left-to-right
        search_line(row, word_list, found_words)
        # Right-to-left (search on reversed row)
        rev_row = reverse_list(row)
        search_line(rev_row, word_list, found_words)
        row_index = row_index + 1


def find_vertical_words(grid, word_list, found_words):
    """Find words vertically (top-to-bottom and bottom-to-top)."""
    if len(grid) == 0:
        return

    n_rows = len(grid)
    n_cols = len(grid[0])

    col_index = 0
    while col_index < n_cols:
        col = column2list(grid, col_index)
        # Top-to-bottom
        search_line(col, word_list, found_words)
        # Bottom-to-top
        rev_col = reverse_list(col)
        search_line(rev_col, word_list, found_words)
        col_index = col_index + 1


def find_diagonal_words(grid, word_list, found_words):
    """
    Find words along diagonals from upper-left to lower-right.
    Only this diagonal direction is searched (no reverse diagonal search).
    """
    n_rows = len(grid)
    if n_rows == 0:
        return
    n_cols = len(grid[0])

    # Diagonals starting on the top row
    col = 0
    while col < n_cols:
        diag = get_diagonal(grid, 0, col)
        search_line(diag, word_list, found_words)
        col = col + 1

    # Diagonals starting on the leftmost column (excluding (0,0) already done)
    row = 1
    while row < n_rows:
        diag = get_diagonal(grid, row, 0)
        search_line(diag, word_list, found_words)
        row = row + 1


# Output---------------------------------------------------------

def print_words(found_words):
    """Print all found words in alphabetical order, one per line."""
    found_words.sort()
    i = 0
    while i < len(found_words):
        print(found_words[i])
        i = i + 1

# main----------------------------------------------------------

def main():
    word_list = get_word_list()
    letters_grid = read_letters_file()

    # If the grid file is empty, no output (spec requirement)
    if len(letters_grid) == 0:
        return

    all_words = []

    find_horizontal_words(letters_grid, word_list, all_words)
    find_vertical_words(letters_grid, word_list, all_words)
    find_diagonal_words(letters_grid, word_list, all_words)

    print_words(all_words)


main()