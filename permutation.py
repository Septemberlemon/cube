from typing import List, Tuple, Set
from math import lcm


# 置换的类
class Permutation:
    def __init__(self, cycles: List[Tuple] | Tuple | List | None = None, mapping_to: List | None = None):
        if mapping_to:
            assert isinstance(mapping_to, list) and isinstance(cycles, list)
            assert len(set(cycles)) == len(cycles) and len(set(mapping_to)) == len(mapping_to)
            assert set(cycles) == set(mapping_to)
            self.mapping = {k: v for k, v in zip(cycles, mapping_to) if k != v}
        else:
            if cycles is None:
                cycles = []
            if isinstance(cycles, tuple):
                cycles = [cycles]
            assert isinstance(cycles, list)
            self.mapping = {}
            for cycle in cycles:
                assert isinstance(cycle, tuple)
                if len(cycle) == 1:
                    continue
                for i, element in enumerate(cycle):
                    if element in self.mapping:
                        raise ValueError(f"元素{element}重复")
                    self.mapping[element] = cycle[(i + 1) % len(cycle)]

    @property
    def elements(self) -> Set:
        return set(self.mapping)

    @property
    def order(self) -> int:
        cycles = self._get_cycles()
        return lcm(*(len(cycle) for cycle in cycles))

    def _get_cycles(self, sort=False) -> List[Tuple]:
        cycles: List[Tuple] = []
        processed_elements = set()
        elements = self.elements if not sort else sorted(self.elements)
        for element in elements:
            if element not in processed_elements:
                cycle = [element]
                processed_elements.add(element)
                while (element := self(cycle[-1])) != cycle[0]:
                    cycle.append(element)
                    processed_elements.add(element)
                cycles.append(tuple(cycle))
        return cycles

    def __str__(self) -> str:
        cycles = self._get_cycles(sort=True)

        if not cycles:
            return "[]"
        cycle_strs = ["(" + ", ".join(map(str, cycle)) + ")" for cycle in cycles]

        return "[" + " ".join(cycle_strs) + "]"

    def __call__(self, x):
        return self.mapping.get(x, x)

    def __eq__(self, other: "Permutation") -> bool:
        assert isinstance(other, Permutation)
        return self.mapping == other.mapping

    def __hash__(self):
        return hash(tuple(self._get_cycles(sort=True)))

    @staticmethod
    def _create_permutation_from_mapping(mapping: dict) -> "Permutation":
        res = Permutation()
        res.mapping = mapping
        return res

    def __mul__(self, other: "Permutation") -> "Permutation":
        mapping = {}
        for k in self.mapping:
            if (v := self(other(k))) != k:
                mapping[k] = v
        for k in other.mapping:
            if k not in self.mapping:
                if (v := self(other(k))) != k:
                    mapping[k] = v
        return self._create_permutation_from_mapping(mapping)

    def inverse(self) -> "Permutation":
        mapping = {v: k for k, v in self.mapping.items()}
        return self._create_permutation_from_mapping(mapping)

    def __pow__(self, power: int) -> "Permutation":
        assert isinstance(power, int)
        # 恒等置换
        e = Permutation([])

        if power == 0:
            return e

        if power < 0:
            return (self.inverse()) ** (-power)

        # 现在 power > 0
        result = e
        base = self

        # 二分幂主循环
        while power > 0:
            if power & 1:
                result = result * base
            base = base * base
            power >>= 1

        return result


if __name__ == '__main__':
    e = Permutation()
    p1 = Permutation((1, 2, 3))
    p2 = Permutation([(1, 2), (3, 4, 5)])
    p3 = Permutation([1, 2, 3, 4, 5], [1, 3, 4, 5, 2])
    print(e)
    print(p1)
    print(p2)
    print(p3)
    print(p2.elements)
    print(p2.order)
    print(p1 == p2)
    print(p1 * p2)
    print(p2 ** 10)
    print(p2(4))
