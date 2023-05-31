import numpy as np
import matplotlib.pyplot as plt

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(np.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def ulam_spiral(size, start):
    dx, dy = 0, -1
    x, y = 0, 0
    primes = []
    coords = []
    for n in range(start, start + size**2):
        if is_prime(n):
            primes.append(n)
            coords.append((x, y))
        if (x == y) or (x < 0 and x == -y) or (x > 0 and x == 1-y):
            dx, dy = -dy, dx
        x, y = x+dx, y+dy
    return primes, coords

size = 201
start = 41
primes, coords = ulam_spiral(size, start)
coords = [(x + size//2, y + size//2) for x, y in coords]
img = np.zeros((size, size, 3))
for (x, y) in coords:
    img[x, y] = [1, 1, 1]  # white
img[size//2, size//2] = [1, 0, 0]  # red
plt.imshow(img)
plt.show()
