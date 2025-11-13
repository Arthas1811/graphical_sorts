import matplotlib.pyplot as plt
import time

class Visualizer:
    def __init__(self, array, delay=0.1):
        self.array = array
        self.delay = delay
        self.fig, self.ax = plt.subplots()
        self.bars = self.ax.bar(range(len(array)), array, color="blue")
        plt.ion()
        plt.show()

    def update(self, array):
        for bar, height in zip(self.bars, array):
            bar.set_height(height)
        self.fig.canvas.draw()
        plt.pause(self.delay)
