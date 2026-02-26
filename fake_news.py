'''
File: fake_news.py
Author: Amy Cardona
Class: CSC120, Fall 2025
Purpose: The program reads fake news article data from a CSV file,
extracts and cleans the titles, and counts word occurrences using
a linked list (no dictionaries or Python lists for counting).
It then sorts the linked list in descending order by count using
a node-based insertion sort (moving nodes, not swapping values),
and prints all words whose counts are greater than or equal to
the nth word’s count, where n is a user-supplied integer.
'''

import csv
import string


class Node:
    """Represents a single word and how many times it’s appeared."""

    def __init__(self, word):
        """Start a node with its word, count=1, and no next node yet."""
        self._word = word
        self._count = 1
        self._next = None

    def word(self):
        """Return the word stored in this node."""
        return self._word

    def count(self):
        """Return how many times this word has shown up so far."""
        return self._count

    def next(self):
        """Return the next node in the list."""
        return self._next

    def set_next(self, target):
        """Link this node to another one (target)."""
        self._next = target

    def incr(self):
        """Increase the count by one — we saw this word again."""
        self._count += 1

    def __str__(self):
        """Return a readable version of the node."""
        return f"{self._word}: {self._count}"


class LinkedList:
    """A simple linked list that tracks all words and their counts."""

    def __init__(self):
        """Start off with an empty list (no head yet)."""
        self._head = None

    def is_empty(self):
        """Check if the list has anything in it."""
        return self._head is None

    def head(self):
        """Return the current head node (or None if empty)."""
        return self._head

    def update_count(self, word):
        """
        Go through the list:
        - If the word is already there, bump up its count.
        - If not, make a new node for it and stick it at the front.
        """
        curr = self._head
        while curr is not None:
            if curr.word() == word:
                curr.incr()
                return
            curr = curr.next()

        # Didn’t find it — make a new node and add it to the head
        new_node = Node(word)
        new_node.set_next(self._head)
        self._head = new_node

    def rm_from_hd(self):
        """Pop off the first node and return it."""
        if self._head is None:
            raise RuntimeError("Tried to remove from an empty list.")
        node = self._head
        self._head = node.next()
        node.set_next(None)
        return node

    def insert_after(self, node1, node2):
        """Drop node2 right after node1."""
        node2.set_next(node1.next())
        node1.set_next(node2)

    def sort(self):
        """
        Sort the list in descending order of count.
        This uses node-based insertion sort (we move the nodes themselves,
        not just their values). Same algorithm as used in class.
        """
        if self._head is None or self._head.next() is None:
            return

        sorted_head = None
        # Keep moving nodes from the unsorted list to the sorted list
        while self._head is not None:
            curr = self.rm_from_hd()
            # If sorted list is empty or current node is larger, put it up front
            if sorted_head is None or curr.count() > sorted_head.count():
                curr.set_next(sorted_head)
                sorted_head = curr
            else:
                # Otherwise, find where it belongs in the sorted list
                search = sorted_head
                while search.next() is not None and search.next().count() >= curr.count():
                    search = search.next()
                curr.set_next(search.next())
                search.set_next(curr)
        self._head = sorted_head

    def get_nth_highest_count(self, n):
        """Find the count value of the node sitting at position n (0 = first)."""
        curr = self._head
        index = 0
        while curr is not None and index < n:
            curr = curr.next()
            index += 1
        if curr is None:
            return 0
        return curr.count()

    def print_upto_count(self, n):
        """Print all words that appear n times or more."""
        curr = self._head
        while curr is not None:
            if curr.count() >= n:
                print("{} : {:d}".format(curr.word(), curr.count()))
            curr = curr.next()

    def __str__(self):
        """Make it easy to print out the whole list for debugging."""
        curr = self._head
        result = []
        while curr is not None:
            result.append(str(curr))
            curr = curr.next()
        return "\n".join(result)


def main():
    """Main function: read file, clean titles, count words, and print results."""
    filename = input().strip()

    ll = LinkedList()

    # You can set the delimiter via the `delimiter` parameter
    # (csv handles commas by default, but this makes it flexible)
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            # Ignore lines that are too short or are comment lines
            if len(row) < 5:
                continue
            if row[0].startswith("#") or row[0].startswith("!"):
                continue

            title = row[4]

            # Replace punctuation with spaces — makes splitting clean
            clean_title = ""
            for ch in title:
                if ch in string.punctuation:
                    clean_title += " "
                else:
                    clean_title += ch

            # Split on spaces to get the words
            words = clean_title.split()

            # Lowercase everything and skip tiny words
            for w in words:
                w = w.lower()
                if len(w) > 2:
                    ll.update_count(w)

    # Done reading — now sort the list
    ll.sort()

    # Get the user’s n value
    n = int(input().strip())
    if n < 0:
        n = 3  # fallback value

    # Find the count at that nth position
    k = ll.get_nth_highest_count(n)

    # Print everything with that count or higher
    ll.print_upto_count(k)


if __name__ == "__main__":
    main()
