from basic_moves import basic_move_permutation
from permutation import Permutation


def dfs(p, visited, depth, path):
    if depth >= 11:
        return
    if p.order == 3:
        print(path)
        print(p)
    depth += 1
    if p not in visited:
        visited.add(p)
        for move, permutation in basic_move_permutation.items():
            dfs(p * permutation, visited, depth, path + [move])


visited = set()
e = Permutation()
dfs(e, visited, 0, [])
