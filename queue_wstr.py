class Queue:
    def __init__(self):
        # items holds the queue contents as a string
        self.items = ""


    def enqueue(self, item):
        # add item to the back
        self.items = self.items + item

    def dequeue(self):
        # remove and return the front character
        if self.items == "":
            return None
        front = self.items[0]
        self.items = self.items[1:]
        return front

    def is_empty(self):
        return self.items == ""

    def __str__(self):
        return self.items

        
#Do not modify anything below this line
def test01():
    q = Queue()
    for c in "abcd":
        q.enqueue(c)
    return str(q)

def test02():
    q = Queue()
    for c in "abcd":
        q.enqueue(c)
    q.dequeue()
    return q.dequeue()
def test03():
    q = Queue()
    for c in "abcd":
        q.enqueue(c)
    q.dequeue()
    q.dequeue()
    return q.is_empty()

def test04():
    q = Queue()
    for c in "hide":
        q.enqueue(c)
    q.dequeue()
    q.dequeue()
    q.enqueue("e")
    q.enqueue("p")
    return str(q)
