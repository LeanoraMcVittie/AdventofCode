from typing import List
import itertools as it


def determinant3x3(m: List[List[int]]) -> int:
    return (
        m[0][0]*m[1][1]*m[2][2]
        + m[0][1]*m[1][2]*m[2][0]
        + m[0][2]*m[1][0]*m[2][1]
        - m[0][2]*m[1][1]*m[2][0]
        - m[0][1]*m[1][0]*m[2][2]
        - m[0][0]*m[1][2]*m[2][1]
    )


if __name__ == "__main__":
    matricies = []
    count = 0
    for a, b, c in it.permutations(range(3)):
        for x, y, z in it.product([1, -1], repeat=3):
            matrix = [[0 for _ in range(3)] for _ in range(3)]
            matrix[0][a] = x
            matrix[1][b] = y
            matrix[2][c] = z
            det = determinant3x3(matrix)
            if determinant3x3(matrix) == 1:
                matricies.append(matrix)
    print(matricies)
