
'''
File: fake_news_ms.py
Author: Amy Cardona
Course: CSC 120 
Purpose: Behaviorally identical to Assignment 6, except:
    1. Uses Python lists instead of LinkedList
    2. Sorting is done by recursive merge sort (msort)
    3. Ties in count are broken alphabetically (ascending)
'''

import sys

class Word:
    def __init__(self, word):
        self._word = word
        self._count = 1

    def word(self):
        return self._word

    def count(self):
        return self._count

    def incr(self):
        self._count += 1


def find_word(words, target):
    for i, w in enumerate(words):
        if w.word() == target:
            return i
    return -1


def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i].count() > right[j].count():
            result.append(left[i])
            i += 1
        elif left[i].count() < right[j].count():
            result.append(right[j])
            j += 1
        else:
            if left[i].word() <= right[j].word():
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def msort(L):
    if len(L) <= 1:
        return L
    mid = len(L) // 2
    left = msort(L[:mid])
    right = msort(L[mid:])
    return merge(left, right)


def read_words(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read().lower()
    except FileNotFoundError:
        print("File not found.")
        return []

    clean = ""
    for ch in text:
        if ch.isalpha() or ch == "'":
            clean += ch
        else:
            clean += " "

    tokens = clean.split()

    words = []
    for token in tokens:
        if not token.isalpha() and not ("'" in token and token.replace("'", "").isalpha()):
            continue
        idx = find_word(words, token)
        if idx == -1:
            words.append(Word(token))
        else:
            words[idx].incr()
    return words


def print_top(filename, words, n):
    print(f"File: {filename}")
    print(f"N: {n}")
    top_n = words[:n] if len(words) > n else words
    for w in top_n:
        print(f"{w.word()} : {w.count()}")


def main():
    sys.setrecursionlimit(4000)
    filename = input("File: ").strip()
    n = int(input("N: "))
    words = read_words(filename)
    if not words:
        return
    sorted_words = msort(words)
    print_top(filename, sorted_words, n)


if __name__ == "__main__":
    main()
