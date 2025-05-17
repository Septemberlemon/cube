from typing import List

import numpy as np

from config import *


class Cube:
    def __init__(self, faces: List[np.ndarray] | np.ndarray):
        """
        初始化一个魔方
        :param faces: 一个长度为 6 的列表，每个元素为shape为[3, 3]的多维数组，分别代表上下前后左右的各三行三列
        顺序：上、下、前、后、左、右
        """
        self.faces = []
        self.faces.append(faces[0])
        self.faces.append(np.rot90(faces[3], 1))
        self.faces.append(np.rot90(faces[4], 2))
        self.faces.append(faces[1])
        self.faces.append(np.rot90(faces[2], 1))
        self.faces.append(faces[5])
        self.faces = np.array(self.faces)

    def rotate(self, face, clockwise=True):
        """
        转动指定面
        :param face: 要转动的面
        :param clockwise: 若为True，则顺时针转动，否则逆时针转动
        """
        idx = face2idx[face]
        self.faces[idx] = np.rot90(self.faces[idx], -1 if clockwise else 1)
        side_idxes = [idx + 1, idx + 2, idx + 4, idx + 5]
        side_idxes = [i % 6 for i in side_idxes]
        if idx & 1:
            if clockwise:
                temp = self.faces[side_idxes[0]][:, -1].copy()
                self.faces[side_idxes[0]][:, -1] = self.faces[side_idxes[3]][0]
                self.faces[side_idxes[3]][0] = self.faces[side_idxes[2]][:, -1]
                self.faces[side_idxes[2]][:, -1] = self.faces[side_idxes[1]][-1][::-1]
                self.faces[side_idxes[1]][-1][::-1] = temp
            else:
                temp = self.faces[side_idxes[0]][:, -1].copy()
                self.faces[side_idxes[0]][:, -1] = self.faces[side_idxes[1]][-1][::-1]
                self.faces[side_idxes[1]][-1] = self.faces[side_idxes[2]][:, -1][::-1]
                self.faces[side_idxes[2]][:, -1] = self.faces[side_idxes[3]][0]
                self.faces[side_idxes[3]][0] = temp
        else:
            if clockwise:
                temp = self.faces[side_idxes[0]][:, 0].copy()
                self.faces[side_idxes[0]][:, 0] = self.faces[side_idxes[1]][-1]
                self.faces[side_idxes[1]][-1] = self.faces[side_idxes[2]][:, 0]
                self.faces[side_idxes[2]][:, 0] = self.faces[side_idxes[3]][0][::-1]
                self.faces[side_idxes[3]][0][::-1] = temp
            else:
                temp = self.faces[side_idxes[0]][:, 0].copy()
                self.faces[side_idxes[0]][:, 0] = self.faces[side_idxes[3]][0][::-1]
                self.faces[side_idxes[3]][0] = self.faces[side_idxes[2]][:, 0][::-1]
                self.faces[side_idxes[2]][:, 0] = self.faces[side_idxes[1]][-1]
                self.faces[side_idxes[1]][-1] = temp

    def show(self):
        self._draw_face(self.faces[0])
        for row in range(3):
            line = [color_num for idx in range(4)
                    for color_num in np.rot90(self.faces[idx + 1 + idx // 2], 3 - idx if idx & 1 else -1)[row]]
            self._draw_row(line)
        self._draw_face(self.faces[3])
        print(4 * 3 * (5 + 1) * "=")

    @staticmethod
    def _draw_row(line, prefix_spaces=0, suffix_spaces=0):
        for _ in range(2):
            print(prefix_spaces * " ", end="")
            for color_num in line:
                r, g, b = color2rgb[num2color[color_num]]
                print(f"\033[48;2;{r};{g};{b}m" + " " * 6 + "\033[0m", end="")
            print(suffix_spaces * " ")

    def _draw_face(self, face):
        for line in face:
            self._draw_row(line, prefix_spaces=2 * 3 * (5 + 1), suffix_spaces=3 * (5 + 1))
