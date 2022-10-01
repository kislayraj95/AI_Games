import matplotlib.pyplot as plt
class Ant:
    def __init__(self, name, x=0, y=0, color='magenta'):
        self.name = name
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        plt.plot(self.x, self.y, color=self.color, marker="o")

    def move(self, fwd, width):
        if self.x + fwd <= width:
            self.x += fwd
        else:
            self.x = width

    def at_edge(self, width):
        if self.x == width:
            return True
        return False

    def __str__(self):
        return f"Name: {self.name}, x: {self.x}, y: {self.y}, color: {self.color}"


