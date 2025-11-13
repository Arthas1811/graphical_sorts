import random

def bogosort(array, visualizer):
    count = 0
    def is_sorted(arr):
        for i in range(len(arr) - 1):
            if arr[i] > arr[i + 1]:
                return False
        return True

    while not is_sorted(array):
        n = len(array)
        colors = ["yellow"] * n
        visualizer(array, colors)

        random.shuffle(array)
        colors = ["red" if i != sorted(array)[i] else "blue" for i in range(n)]
        visualizer(array, colors)
        count+= 1
    
    print(count)
    visualizer(array, ["green"] * len(array))
