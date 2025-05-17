import numpy as np

from config import face2idx
from cube import Cube
from permutation import Permutation


li = [np.array([idx for _ in range(9)]).reshape([3, 3]) for idx in range(6)]
cube = Cube(li)

cube.show()
for i in range(105):
    cube.rotate("up")
    cube.show()
    cube.rotate("front")
    cube.show()
