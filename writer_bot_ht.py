"""
File: writer_bot_ht.py
Author: Amy Cardona
Course: CSC 120, Fall 2025
Purpose: This program builds a Markov chain using a custom 
hash table with linear probing, mapping each prefix string
to a list of possible suffixes. It then generates random 
text by repeatedly selecting suffixes based on the current
prefix, updating the prefix, and collecting words until the
desired length is reached. Finally, it prints the generated
words ten per line as required.
"""
import sys
import random

SEED = 8
NONWORD = '@'


class Hashtable:
    """Hash table with linear probing (decrement by 1)."""

    def __init__(self, size):
        self._pairs = []
        i = 0
        while i < size:
            self._pairs.append(None)
            i += 1
        self._size = size

    def _hash(self, key):
        p = 0
        for c in key:
            p = 31 * p + ord(c)
        return p % self._size

    def put(self, key, value):
        index = self._hash(key)
        count = 0

        while count < self._size:
            pair = self._pairs[index]

            if pair is None:   # empty slot
                self._pairs[index] = [key, value]
                return

            if pair[0] == key:  # update
                pair[1] = value
                return

            index -= 1
            if index < 0:
                index = self._size - 1
            count += 1

    def get(self, key):
        index = self._hash(key)
        count = 0

        while count < self._size:
            pair = self._pairs[index]

            if pair is None:
                return None

            if pair[0] == key:
                return pair[1]

            index -= 1
            if index < 0:
                index = self._size - 1
            count += 1

        return None

    def __contains__(self, key):
        index = self._hash(key)
        count = 0

        while count < self._size:
            pair = self._pairs[index]

            if pair is None:
                return False

            if pair[0] == key:
                return True

            index -= 1
            if index < 0:
                index = self._size - 1
            count += 1

        return False

    def __str__(self):
        s = '{'
        first = True
        i = 0
        while i < self._size:
            pair = self._pairs[i]
            if pair is not None:
                if not first:
                    s = s + ', '
                s = s + str(pair[0]) + ': ' + str(pair[1])
                first = False
            i += 1
        s = s + '}'
        return s


def make_prefix(words):
    prefix = ''
    i = 0
    while i < len(words):
        if i > 0:
            prefix = prefix + ' '
        prefix = prefix + words[i]
        i += 1
    return prefix


def add_suffix(table, prefix, word):
    if prefix in table:
        table.get(prefix).append(word)
    else:
        lst = []
        lst.append(word)
        table.put(prefix, lst)


def build_table(table, filename, n):
    """Build prefix→suffix table from entire file as ONE continuous stream."""

    # start prefix as NONWORD repeated n times
    prefix_words = []
    i = 0
    while i < n:
        prefix_words.append(NONWORD)
        i += 1

    # read ENTIRE file as one string (critical for autograder match)
    f = open(filename, 'r')
    text = f.read()
    f.close()

    # split on whitespace ONLY; punctuation preserved
    words = text.split()

    i = 0
    while i < len(words):
        word = words[i]

        prefix = make_prefix(prefix_words)
        add_suffix(table, prefix, word)

        # shift prefix
        j = 0
        while j < n - 1:
            prefix_words[j] = prefix_words[j + 1]
            j += 1
        prefix_words[n - 1] = word

        i += 1

    # Add ONE terminator only after all words are processed
    final_prefix = make_prefix(prefix_words)
    add_suffix(table, final_prefix, NONWORD)


def generate_text(table, n, max_words):
    result = []

    # initial prefix
    prefix_words = []
    i = 0
    while i < n:
        prefix_words.append(NONWORD)
        i += 1

    prefix = make_prefix(prefix_words)

    i = 0
    while i < max_words:
        suffixes = table.get(prefix)
        if suffixes is None:
            break

        r = random.randrange(len(suffixes))
        word = suffixes[r]

        if word == NONWORD:
            break

        result.append(word)

        # shift prefix
        j = 0
        while j < n - 1:
            prefix_words[j] = prefix_words[j + 1]
            j += 1
        prefix_words[n - 1] = word
        prefix = make_prefix(prefix_words)

        i += 1

    return result


def print_words(words):
    count = 0
    line_words = []

    i = 0
    while i < len(words):
        line_words.append(words[i])
        count += 1

        if count == 10:
            line = ''
            j = 0
            while j < len(line_words):
                if j > 0:
                    line = line + ' '
                line = line + line_words[j]
                j += 1
            print(line)
            line_words = []
            count = 0

        i += 1

    if count > 0:
        line = ''
        j = 0
        while j < len(line_words):
            if j > 0:
                line = line + ' '
            line = line + line_words[j]
            j += 1
        print(line)


def main():
    sfile = input()
    m_str = input()
    n_str = input()
    num_str = input()

    M = int(m_str)
    n = int(n_str)
    num_words = int(num_str)

    if n < 1:
        print("ERROR: specified prefix size is less than one")
        sys.exit(0)

    if num_words < 1:
        print("ERROR: specified size of the generated text is less than one")
        sys.exit(0)

    table = Hashtable(M)
    build_table(table, sfile, n)

    random.seed(SEED)
    generated = generate_text(table, n, num_words)

    print_words(generated)


if __name__ == '__main__':
    main()
