#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
fig = plt.figure(figsize=(6, 4))
texts = np.array([
    ['e', 'f', 'g', 'h', 'i'],
    ['j', 'k', 'l', 'm', 'n'],
    ['Title', 'Color', 'Price', 'Count', "That's all"],
])
row, column = texts.shape
print(row, column)
plt.tight_layout()
plt.axis('off')
plt.xlim(0, column)
plt.ylim(-1, row - 1)
plt.plot([0, 0], [-1, row - 1], c='red', lw=4)
plt.plot([column, column], [-1, row - 1], c='red', lw=4)
for i in range(column):
    for j in range(row):
        middle_x = i + 0.5
        middle_y = j - 0.5
        plt.text(middle_x, middle_y, texts[j, i])
        plt.plot([i, i + 2], [j, j], c='black')
        plt.plot([i, i], [-1, j], c='black')
plt.plot([0, column], [-1, - 1], c='red', lw=4)
plt.show()
# plt.savefig('result.jpg', bbox_inches='tight', pad_inches=0.2)
