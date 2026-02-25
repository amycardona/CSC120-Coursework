""" 
File: street.py
Author: Amy Cardona
Course: CSC 120, Fall 2025
Purpose: This program reads a street description and recursively 
renders an ASCII street made of buildings, parks, and empty lots. 
Each element is represented by a class with an at_height() method 
that returns its appearance at a given height, and all iteration 
is handled through recursion instead of loops.
"""

def repeat(ch, n):
    """Return ch repeated n times using recursion."""
    if n <= 0:
        return ""
    return ch + repeat(ch, n - 1)


def concat_elements(elements, h):
    """Return the concatenation of all elements' text at height h (height counted from bottom: 1 = bottom)."""
    if elements == []:
        return ""
    return elements[0].at_height(h) + concat_elements(elements[1:], h)


def total_width(elements):
    """Return total width of all elements."""
    if elements == []:
        return 0
    return elements[0].width + total_width(elements[1:])


def tallest(elements):
    """Return the tallest height among all elements."""
    if elements == []:
        return 0
    first = elements[0]
    rest_max = tallest(elements[1:])
    return max(first.height, rest_max)


# Classes -------------------------------------------------

class Building:
    def __init__(self, width, height, brick):
        self.width = int(width)
        self.height = int(height)
        self.brick = brick

    def at_height(self, h):
        """
        h is measured from the bottom: h == 1 is the bottom row.
        The building occupies rows 1..height (from bottom).
        """
        if h <= self.height:
            return repeat(self.brick, self.width)
        else:
            return repeat(" ", self.width)


class Park:
    def __init__(self, width, foliage):
        self.width = int(width)
        self.foliage = foliage
        self.height = 5

    def _center(self, content):
        pad = (self.width - len(content)) // 2
        return repeat(" ", pad) + content + repeat(" ", self.width - len(content) - pad)

    def _tree_line(self, n):
        """
        n is measured from the bottom:
        - n == 1 -> bottommost row is trunk (|) (but tree shape described in spec has two trunk rows),
        - To match the instructor examples we use:
          bottom rows: 1 -> trunk, 2 -> trunk, 3 -> widest foliage (5),
          4 -> medium foliage (3), 5 -> small foliage (1)
        But since examples show foliage growing downward (small -> medium -> large) with trunks below,
        we'll map bottom-based n to draw the tree appropriately:
        bottom 1: '|'
        bottom 2: '|'
        bottom 3: foliage*5
        bottom 4: foliage*3
        bottom 5: foliage*1
        """
        if n == 1 or n == 2:
            return self._center("|")
        elif n == 3:
            return self._center(self.foliage * 5)
        elif n == 4:
            return self._center(self.foliage * 3)
        elif n == 5:
            return self._center(self.foliage)
        else:
            return repeat(" ", self.width)

    def at_height(self, h):
        if h <= self.height:
            return self._tree_line(h)
        else:
            return repeat(" ", self.width)


class EmptyLot:
    def __init__(self, width, trash):
        self.width = int(width)
        self.trash = trash
        self.height = 1

    def _expanded_trash(self, text, n):
        """Recursively repeat text until reaching n characters."""
        if len(text) >= n:
            return text[:n]
        return self._expanded_trash(text + self.trash, n)

    def _trash_to_display(self, s, i):
        """Recursively replace underscores with spaces."""
        if i >= len(s):
            return ""
        c = " " if s[i] == "_" else s[i]
        return c + self._trash_to_display(s, i + 1)

    def at_height(self, h):
        if h == 1:
            t = self._expanded_trash(self.trash, self.width)
            return self._trash_to_display(t, 0)
        else:
            return repeat(" ", self.width)


# Parsing ------------------------------------------------

def parse_element(spec):
    # Split only on the first colon so trash strings containing ':' are preserved
    kind, rest = spec.split(":", 1)
    parts = rest.split(",")
    if kind == "b":
        return Building(parts[0], parts[1], parts[2])
    elif kind == "p":
        return Park(parts[0], parts[1])
    elif kind == "e":
        return EmptyLot(parts[0], parts[1])
    else:
        return None


def parse_all(tokens, i=0):
    if i >= len(tokens):
        return []
    return [parse_element(tokens[i])] + parse_all(tokens, i + 1)


# Rendering the street
# -------------------------------------------------

def draw_lines(elements, total_rows, current_row_top):
    """
    Recursively draw rows from top to bottom.
    total_rows: number of rows to print (this is max_height + 1 per spec)
    current_row_top: current row index counting from top (1..total_rows)
    must convert the top-based row index to bottom-based height for at_height().
    bottom-based h = total_rows - current_row_top + 1
    """
    if current_row_top > total_rows:
        return
    h_from_bottom = total_rows - current_row_top + 1
    line = concat_elements(elements, h_from_bottom)
    print("|" + line + "|")
    draw_lines(elements, total_rows, current_row_top + 1)


def draw_street(elements):
    max_h = tallest(elements)
    total_w = total_width(elements)
    total_rows = max_h + 1  # one extra top padding row per spec
    print("+" + repeat("-", total_w) + "+")
    draw_lines(elements, total_rows, 1)
    print("+" + repeat("-", total_w) + "+")


# Main------------------------------------------------

def main():
    line = input("Street: ")
    tokens = line.split()
    elements = parse_all(tokens)
    draw_street(elements)


if __name__ == "__main__":
    main()