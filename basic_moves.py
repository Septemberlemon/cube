import numpy as np

from config import face2idx
from cube import Cube
from permutation import Permutation


li = np.array([i for i in range(6 * 3 * 3)]).reshape(6, 3, 3)
cube = Cube(li)

basic_move_permutation = {}
for face in face2idx:
    old_facelets = cube.faces.reshape(-1).tolist()
    cube.rotate(face)
    new_facelets = cube.faces.reshape(-1).tolist()
    cube.rotate(face, False)
    basic_move_permutation[face[0].upper()] = Permutation(old_facelets, new_facelets, )
    basic_move_permutation[face[0].upper() + "'"] = Permutation(new_facelets, cube.faces.reshape(-1).tolist())

if __name__ == '__main__':
    for move, permutation in basic_move_permutation.items():
        print(move, permutation)
