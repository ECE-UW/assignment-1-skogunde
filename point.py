class Point(object):
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __str__(self):
        if self.x == round(self.x) and self.y == round(self.y):
            return "(" + str(int(self.x)) + "," + str(int(self.y)) + ")"
        elif self.x == round(self.x) and self.y != round(self.y):
            return "(" + str(int(self.x)) + "," + str("{1:0.2f}".format(self.x, self.y)) + ")"
        elif self.x != round(self.x) and self.y == round(self.y):
            return "(" + str("{0:0.2f}".format(self.x, self.y)) + "," + str(int(self.y)) + ")"
        elif self.x != round(self.x) and self.y != round(self.y):
            return "(" + str("{0:0.2f}, {1:0.2f}".format(self.x, self.y)) + ")"
        else:
            return "Error: Input not valid"

    # this is operator overloading (overloading == operator)
    # it returns true if point1 == point2, otherwise false
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x and self.y != other.y

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        elif self.y == other.y:
            return self.x < other.x

        return self.x < other.x

