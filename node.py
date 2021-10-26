from element import Element
from copy import deepcopy


class Node:

    colors = None

    def __init__(self, size, parent=None):
        self.parent = parent
        self.size = size
        if parent:
            self.depth = parent.depth + 1
            self.table = deepcopy(parent.table)
            self.rows_set = deepcopy(parent.rows_set)
            self.columns_set = deepcopy(parent.columns_set)
        else:
            self.depth = 0
            self.table = [[Element(j, i) for i in range(self.size)]
                          for j in range(self.size)]
            self.rows_set = [set() for i in range(self.size)]
            self.columns_set = [set() for i in range(self.size)]
        self.cban_elements = []
        self.nban_elements = []

    def add_element(self, string, rindex, cindex):
        self.table[rindex][cindex].update(string=string)
        self.rows_set[rindex].add(string[:-1])
        self.columns_set[cindex].add(string[:-1])

    def update_element(self, rindex, cindex, color=None, number=None):
        if number:
            if self[rindex][cindex].number:
                self.rows_set.remove(self[rindex][cindex].number)
                self.columns_set.remove(self[rindex][cindex].number)
            self.rows_set[rindex].add(number)
            self.columns_set[cindex].add(number)
        self[rindex][cindex].update(color=color, number=number)

    def get_all_upper_colors(self, element):
        ns = element.get_neighbors(self.size)
        index = 0
        lindex = len(Node.colors)
        for n in ns:
            el = self[n[0]][n[1]]
            if el.color and el.number and element.number:
                if element.number > el.number:
                    index = max(index, Node.colors.index(el.color) + 1)
                else:
                    lindex = min(lindex, Node.colors.index(el.color))
        return Node.colors[index:lindex]

    def get_all_valid_numbers(self, element):
        rindex, cindex = element.rindex, element.cindex
        items = [str(i) for i in range(1, self.size + 1)]
        nitems = deepcopy(items)
        for item in items:
            if item in self.rows_set[rindex] or \
                    item in self.columns_set[cindex]:
                nitems.remove(item)
        return nitems

    def ban_color(self, element):
        self.cban_elements.append((element.rindex, element.cindex))
    
    def ban_number(self, element):
        self.nban_elements.append((element.rindex, element.cindex))

    def is_ban(self, element):
        return (element.rindex, element.cindex) in self.cban_elements and \
            (element.rindex, element.cindex) in self.nban_elements

    def degree_heuristic(self):
        m = self.size + 1
        target = None
        action = ""
        for i in range(self.size):
            for j in range(self.size):
                uclrs = self.get_all_upper_colors(self[i][j]) 
                vnums = self.get_all_valid_numbers(self[i][j])
                if self.is_ban(self[i][j]):
                    continue
                if not self[i][j].color and len(uclrs) < m and \
                        (i, j) not in self.cban_elements:
                    target = self[i][j]
                    action = "color"
                    m = len(uclrs)
                if not self[i][j].number and len(vnums) < m and \
                        (i, j) not in self.nban_elements:
                    target = self[i][j]
                    action = "number"
                    m = len(vnums)
        
        if m == 0:
            return None, ""
        return target, action

    def __iter__(self, index):
        return self.table[index]

    def __getitem__(self, index):
        return self.table[index]

    def __str__(self):
        result = ""
        for i in range(self.size):
            for j in range(self.size):
                result += "%s " % self[i][j]
            result += "\n"
        return result

    def is_complete(self):
        for i in range(self.size):
            for j in range(self.size):
                if not self[i][j].color or not self[i][j].number:
                    return False
        return True

    def mrv_heuristic(self):
        m = self.size + 1
        target = None
        action = ""
        for i in range(self.size):
            for j in range(self.size):
                if self.is_ban(self[i][j]):
                    continue
                uclrs = self.get_all_upper_colors(self[i][j]) 
                vnums = self.get_all_valid_numbers(self[i][j])
                if not self[i][j].color and len(uclrs) < m and \
                        (i, j) not in self.cban_elements:
                    target = self[i][j]
                    action = "color"
                    m = len(uclrs)
                if not self[i][j].number and len(vnums) < m and \
                        (i, j) not in self.nban_elements:
                    target = self[i][j]
                    action = "number"
                    m = len(vnums)
        
        if not m:
            return None, ""
        return target, action

    def backtrack(self):
        el, action = self.mrv_heuristic()
        while el:
            if action == "color":
                for c in self.get_all_upper_colors(el):
                    new_node = Node(self.size, parent=self)
                    new_node.update_element(el.rindex, el.cindex, color=c)
                    answer = new_node.backtrack()
                    if answer:
                        return answer
                self.ban_color(el)
            
            if action == "number":
                for num in self.get_all_valid_numbers(el):
                    new_node = Node(self.size, parent=self)
                    new_node.update_element(el.rindex, el.cindex, number=num)
                    answer = new_node.backtrack()
                    if answer:
                        return answer

                self.ban_number(el)

            el, action = self.mrv_heuristic()
        
        if self.is_complete():
            return self
        
        return None
