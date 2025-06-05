import random
import numpy as np

from permutation import Permutation
from cube import Cube
from config import *


li = [np.array([idx for _ in range(9)]).reshape(3, 3) for idx in range(6)]
cube = Cube(li)
cube.show()
for _ in range(100):
    cube.rotate(random.choice(list(short_name)))
    # cube.show()

cube.show()
faces = 1 << cube.faces
print(faces)
permutation_li = [_ for _ in range(6 * 3 * 3)]
print(permutation_li)

for idx in range(6):
    side_idxes = [idx + 1, idx + 2, idx + 4, idx + 5]
    side_idxes = [i % 6 for i in side_idxes]
    if idx & 1:
        pass
        # temp = faces[side_idxes[0]][:, -1].copy()
        # faces[side_idxes[0]][:, -1] = faces[side_idxes[3]][0]
        # faces[side_idxes[3]][0] = faces[side_idxes[2]][:, -1]
        # faces[side_idxes[2]][:, -1] = faces[side_idxes[1]][-1][::-1]
        # faces[side_idxes[1]][-1][::-1] = temp
    else:
        face = faces[idx].copy()
        face[0] += faces[side_idxes[0]][:, 0]
        face[:, 0] += faces[side_idxes[1]][-1][::-1]
        face[-1] += faces[side_idxes[2]][:, 0][::-1]
        face[:, -1] += faces[side_idxes[3]][0][::-1]
        print(side_idxes)
        for i in faces[idx]:
            for j in i:
                print(f"{j:06b}", end=" ")
            print()
        for i in face:
            for j in i:
                print(f"{j:06b}", end=" ")
            print()
        assert 0
