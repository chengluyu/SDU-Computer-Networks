import matplotlib.pyplot as plt
import sys

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        data = map(float, f.readlines())
        plt.hist(list(data), bins=200, log=True)
        plt.show()
    
