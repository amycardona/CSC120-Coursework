'''
File: linkedlist_sort.py
Author: Amy Cardona
Class: CSC120, Fall 2025
Purpose: The program reads integers from a file, creates a linked
list of Node objects, sorts the list in descending order using
a node-based insertion sort (moving nodes, not swapping values),
and prints the sorted linked list using the provided __str__ method.
'''

class Node:
    def __init__(self, value):
        self._value = value
        self._next = None


class LinkedList:
    def __init__(self):
        self._head = None

    def add(self, value):
        """Add a new node with the given value at the end of the list."""
        new_node = Node(value)
        if self._head is None:
            self._head = new_node
        else:
            current = self._head
            while current._next:
                current = current._next
            current._next = new_node

    def __str__(self):
        """Return a string representation of the list."""
        result = "List[ "
        current = self._head
        while current:
            result += str(current._value) + "; "
            current = current._next
        result += "]"
        return result

    def sort(self):
        '''
        Sorts the linked list in descending order by moving nodes
        into a new sorted list using an insertion-style algorithm.
        Nodes are repositioned (not value-swapped), and the head
        is updated once sorting is complete.
        '''
        sorted_head = None
        current = self._head

        while current:
            next_node = current._next  # store next before insertion

            # Insert current node into sorted list
            if sorted_head is None or current._value > sorted_head._value:
                # Insert at the beginning
                current._next = sorted_head
                sorted_head = current
            else:
                # Find position to insert
                search = sorted_head
                while search._next and search._next._value >= current._value:
                    search = search._next
                current._next = search._next
                search._next = current

            current = next_node

        self._head = sorted_head


def main():
    # Read the filename
    filename = input().strip()

    # Read numbers from the file
    with open(filename, 'r') as f:
        numbers = f.readline().strip().split()

    # Create a LinkedList and add nodes
    lst = LinkedList()
    for num in numbers:
        lst.add(int(num))

    lst.sort()

    print(lst)


if __name__ == "__main__":
    main()
