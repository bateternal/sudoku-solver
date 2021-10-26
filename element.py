
class Element:
    
    def __init__(self, rindex, cindex):
        self.rindex = rindex
        self.cindex = cindex
        self.number = None
        self.color = None
        self.state = 0

    def update(self, color=None, number=None, string=None):
        if string:
            if string[-1] != "#":
                self.color = string[-1]
            if string[:-1] != "*":
                self.number = string[:-1]
        if color and color != "#":
            self.color = color
        if number and number != "*":
            self.number = number
        self.state = bool(number)*2 + bool(color)

    def get_neighbors(self, size):
        result = []
        if self.rindex > 0:
            result.append((self.rindex - 1, self.cindex))
        if self.rindex < size-1:
            result.append((self.rindex + 1, self.cindex))
        if self.cindex > 0:
            result.append((self.rindex, self.cindex - 1))
        if self.cindex < size-1:
            result.append((self.rindex, self.cindex + 1))
        return result

    def __str__(self):
        return "%s%s" % (self.number or "*",
                         self.color or "#")
