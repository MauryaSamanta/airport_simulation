class Node:

    def __init__(self, name, type, x, y):
        self.name = name
        self.type = type
        self.x = x
        self.y = y
        self.outgoing_edges = []