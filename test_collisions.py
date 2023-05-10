import numpy as np

g1 = np.zeros((10, 10), dtype=np.uint8)
g2 = np.zeros((10, 10), dtype=np.uint8)
g3 = np.zeros((10, 10), dtype=np.uint8)

p = (5, 5)

g1[5][5] = 1
g2[5][5] = 1
g1[5][3] = 1
g2[5][6] = 1

g3[5][5] = 1
g3[5][2] = 1

print(g1)
print()
print(g2)
print()
# print(g1 + g2)
# print(g1 * g2)
# print()
print((g1 * g2).sum())
print((g1 * g2))
print()
c_mat = np.array([g1, g2, g3])
print(np.sum(c_mat, axis=0))
print((np.sum(c_mat, axis=0)//2).sum())
