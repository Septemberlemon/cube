import numpy as np
import itertools


class Piece:
    """基类：存储贴纸字典"""

    def __init__(self, stickers):
        # stickers: dict face->color
        self.stickers = stickers

    def rotate_stickers(self, axis, clockwise=True):
        """仅更新贴纸方向，不跟踪位置"""
        if axis == 'x':
            mapping = {'U': 'B', 'B': 'D', 'D': 'F', 'F': 'U', 'L': 'L', 'R': 'R'}
        elif axis == 'y':
            mapping = {'F': 'R', 'R': 'B', 'B': 'L', 'L': 'F', 'U': 'U', 'D': 'D'}
        else:  # 'z'
            mapping = {'U': 'L', 'L': 'D', 'D': 'R', 'R': 'U', 'F': 'F', 'B': 'B'}
        # 顺/逆时针 对贴纸方向映射本质相同，旋转方向体现在 grid 位置变动
        new_stickers = {mapping.get(face, face): color for face, color in self.stickers.items()}
        self.stickers = new_stickers


class CenterPiece(Piece): pass


class EdgePiece(Piece): pass


class CornerPiece(Piece): pass


class RubiksCube:
    def __init__(self):
        """使用 numpy 3D 网格存储 Piece 对象"""
        N = 3
        self.N = N
        coords = [-1, 0, 1]
        # 创建空网格
        self.grid = np.empty((N, N, N), dtype=object)
        # 填充 Piece 并放入 grid
        for pos in itertools.product(coords, repeat=3):
            if pos.count(0) == 3:
                continue
            stickers = {}
            x, y, z = pos
            if y == 1: stickers['U'] = 'W'
            if y == -1: stickers['D'] = 'Y'
            if z == 1: stickers['F'] = 'G'
            if z == -1: stickers['B'] = 'B'
            if x == -1: stickers['L'] = 'O'
            if x == 1: stickers['R'] = 'R'
            if len(stickers) == 1:
                p = CenterPiece(stickers)
            elif len(stickers) == 2:
                p = EdgePiece(stickers)
            else:
                p = CornerPiece(stickers)
            idx = (x + 1, y + 1, z + 1)
            self.grid[idx] = p

    def move(self, face, prime=False):
        """旋转某面外层: face∈{'U','D','F','B','L','R'}"""
        axis_map = {'U': 'y', 'D': 'y', 'F': 'z', 'B': 'z', 'L': 'x', 'R': 'x'}
        layer_map = {'U': 1, 'D': -1, 'F': 1, 'B': -1, 'L': -1, 'R': 1}
        axis = axis_map[face]
        layer = layer_map[face]
        idx_dim = {'x': 0, 'y': 1, 'z': 2}[axis]
        layer_idx = layer + 1  # -1->0, 1->2
        # 切片选取
        slc = [slice(None)] * 3
        slc[idx_dim] = layer_idx
        slice_grid = self.grid[tuple(slc)].copy()
        # 旋转网格对象位置
        k = -1 if not prime else 1
        axes = tuple(i for i in range(3) if i != idx_dim)
        rotated = np.rot90(slice_grid, k=k, axes=axes)
        # 写回并更新贴纸
        it = np.ndindex(*rotated.shape)
        for idx in it:
            # rotated 索引对应 slice_grid 的新位置
            # 计算全局坐标
            global_idx = list(idx)
            global_idx.insert(idx_dim, layer_idx)
            # 拆回 tuple
            full_idx = tuple(global_idx)
            piece = rotated[idx]
            # 更新贴纸
            piece.rotate_stickers(axis)
            # 放回 grid
            self.grid[full_idx] = piece

    def display(self):
        """打印六面展开: U-L-F-R-B-D 顺序"""
        N = self.N
        faces = {f: [[' '] * N for _ in range(N)] for f in ['U', 'L', 'F', 'R', 'B', 'D']}
        for idx, p in np.ndenumerate(self.grid):
            if p is None: continue
            x, y, z = [i - 1 for i in idx]
            for face, color in p.stickers.items():
                if face == 'U':
                    r, c = -z, x
                elif face == 'D':
                    r, c = z, x
                elif face == 'F':
                    r, c = -y, x
                elif face == 'B':
                    r, c = -y, -x
                elif face == 'L':
                    r, c = -y, -z
                else:  # 'R'
                    r, c = -y, z
                faces[face][r + 1][c + 1] = color
        for f in ['U', 'L', 'F', 'R', 'B', 'D']:
            print(f)
            for row in faces[f]: print(' '.join(row))
            print()


# 测试示例
if __name__ == '__main__':
    cube = RubiksCube()
    cube.display()
    cube.move('U')
    cube.move('R', prime=True)
    print("After U, R'")
    cube.display()
