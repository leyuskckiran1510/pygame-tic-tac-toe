from typing import Union


def itr_add(self: Union[list[int], tuple[int]], other: Union[list[int], tuple[int]]) -> Union[list[int], tuple[int]]:
    new: Union[list[int], tuple[int]] = []
    if len(self) < len(other):
        return self
    if len(other) == 1:
        new = [i + other[0] for i in self]
    else:
        new = [i + j for i, j in zip(self, other)]
    return new


def itr_sub(self: Union[list[int], tuple[int]], other: Union[list[int], tuple[int]]) -> Union[list[int], tuple[int]]:
    new: Union[list[int], tuple[int]] = []
    if len(self) < len(other):
        return self
    if len(other) == 1:
        new = [i + other[0] for i in self]

    else:
        new = [i + j for i, j in zip(self, other)]
    return new
