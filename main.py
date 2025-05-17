import numpy as np

from config import face2idx
from cube import Cube
from permutation import Permutation


li = np.array([i for i in range(6 * 3 * 3)]).reshape(6, 3, 3)
cube = Cube(li)

p = {}
for face in face2idx:
    old_facelets = cube.faces.reshape(-1).tolist()
    cube.rotate(face)
    new_facelets = cube.faces.reshape(-1).tolist()
    cube.rotate(face, False)
    p[face] = Permutation(old_facelets, new_facelets)

e = Permutation()
