from node import Node


class Game:
    
    def make(self, colors, size):
        self.head = Node(size)
        self.size = size
        Node.colors = colors[::-1]

    def add_row(self, row, rindex):
        items = row.split()
        for cindex, item in enumerate(items):
            self.head.add_element(item, rindex, cindex)

    def start(self):
        return self.head.backtrack()


sudoku = Game()
