from __future__ import annotations

from typing import Any, Callable, Generator, List, Optional, Tuple, Union
from heapq import heappush, heappop
from dataclasses import dataclass


@dataclass
class Coord:
    x: int
    y: int


class Cell(Coord):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.value = None

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, type(self))
            and self.value == other.value
            and self.x == other.x
            and self.y == other.y
        )

    def __str__(self) -> str:
        if not self.value:
            return "."
        return str(self.value)

    def __bool__(self) -> bool:
        return self.value is not None

    def __hash__(self) -> int:
        return hash((self.value, self.x, self.y))

    def set_value(self, value: Any) -> Any:
        self.value = value

    def cost(self) -> int:
        return int(self.value)

    def is_neighbor(self, coords: Coord, include_diagonals: bool = True) -> bool:
        x_diff = abs(self.x - coords.x)
        y_diff = abs(self.y - coords.y)
        if x_diff > 1 or y_diff > 1:
            return False
        if x_diff == 0 and y_diff == 0:
            return False
        if x_diff == 0 or y_diff == 0:
            return True
        return include_diagonals


class Field:
    items: List[List[Cell]]

    def __init__(self, x_size: int, y_size: int, cell_class: Callable) -> None:
        self.items = [[cell_class(x, y) for y in range(y_size)] for x in range(x_size)]
        self.specialized_init()

    @classmethod
    def create_from_input(cls, input_lines: List[str], cell_class) -> Field:
        field = cls(len(input_lines), len(input_lines[0]), cell_class)
        field.apply(transform=lambda x: x.set_value(input_lines[x.x][x.y]))
        return field

    def __eq__(self, other: Field) -> bool:
        return (
            isinstance(other, type(self))
            and len(self.items) == len(other.items)
            and len(self.items[0]) == len(other.items[0])
            and all(self.gen_cells(transform=lambda c: c == other.get(c.x, c.y)))
        )

    def get(self, x: int, y: int, default: Any = None) -> Union[Optional[Cell], Any]:
        if x < 0 or y < 0:
            return default
        try:
            return self.items[x][y]
        except IndexError:
            return default

    def specialized_init(self):
        pass

    def gen_adjacent_cells(
        self,
        cell: Cell,
        include_diagonals: bool = True,
        transform: Callable[[Cell], Any] = lambda x: x,
        filterer: Callable[[Cell], bool] = lambda x: True,
    ) -> Generator[Cell, None, None]:
        for x in range(cell.x - 1, cell.x + 2):
            for y in range(cell.y - 1, cell.y + 2):
                neighbor = self.get(x, y)
                if (
                    neighbor is not None
                    and neighbor is not cell
                    and (
                        include_diagonals
                        or neighbor.x == cell.x
                        or neighbor.y == cell.y
                    )
                    and filterer(neighbor)
                ):
                    yield transform(neighbor)

    def apply_adjacent(
        self,
        cell: Cell,
        include_diagonals: bool = True,
        transform: Callable[[Cell], Any] = lambda x: x,
        filterer: Callable[[Cell], bool] = lambda x: True,
    ) -> int:
        return len(
            [
                cell
                for cell in self.gen_adjacent_cells(
                    cell, include_diagonals, transform, filterer
                )
            ]
        )

    def gen_cells(
        self,
        transform: Callable[[Cell], Any] = lambda x: x,
        filterer: Callable[[Cell], bool] = lambda x: True,
    ) -> Generator[Cell, None, None]:
        for x in range(len(self.items)):
            for y in range(len(self.items[0])):
                if filterer(self.items[x][y]):
                    yield transform(self.items[x][y])

    def apply(
        self,
        transform: Callable[[Cell], Any] = lambda x: x,
        filterer: Callable[[Cell], bool] = lambda x: True,
    ) -> None:
        return len([cell for cell in self.gen_cells(transform, filterer)])

    def clone(self, for_rotating: bool = False) -> Field:
        x_size = len(self.items) if for_rotating else len(self.items[0])
        y_size = len(self.items[0]) if for_rotating else len(self.items)
        new_field = type(self)(y_size, x_size, type(self.items[0][0]))
        return new_field

    def rotate(self) -> Field:
        # clockwise
        rotated_field = self.clone(for_rotating=True)
        rotated_field.apply(
            transform=lambda x: x.set_value(
                self.items[x.y][len(self.items) - (x.x + 1)].value
            )
        )
        return rotated_field

    def switch_top_bottom(self) -> Field:
        flipped_field = self.clone()
        flipped_field.apply(
            transform=lambda x: x.set_value(
                self.items[
                    int(len(self.items[0]) / 2)
                    - (x.x - int((len(self.items[0]) + 1) / 2))
                    - 1
                ][x.y].value
            )
        )
        return flipped_field

    def switch_left_right(self) -> Field:
        flipped_field = self.clone()
        flipped_field.apply(
            transform=lambda x: x.set_value(
                self.items[x.x][
                    int(len(self.items) / 2)
                    - (x.y - int((len(self.items) + 1) / 2))
                    - 1
                ].value
            )
        )
        return flipped_field

    def dijkstra(
        self,
        start: Cell,
        end: Cell,
        include_diagonals: bool = True,
        filterer: Callable[[Cell], bool] = lambda x: True,
    ) -> Tuple[Optional[int], Optional[List[Cell]]]:
        unvisited = {i: [] for i in self.gen_cells()}
        it = 0  # sorting hack for heapq
        unvisited[start] = [start]
        reachable = [(0, it, start)]
        while reachable:
            cost_to_current, _, current = heappop(reachable)
            if current not in unvisited:
                continue

            path_to_current = unvisited[current]
            if current is end:
                return cost_to_current, path_to_current

            neighbors = self.gen_adjacent_cells(
                current,
                include_diagonals=include_diagonals,
                filterer=filterer,
            )
            for neighbor in neighbors:
                if neighbor not in unvisited:
                    continue
                cost = cost_to_current + neighbor.cost()
                path = unvisited[neighbor]
                if path and sum(c.cost() for c in path) < cost:
                    continue
                path = path_to_current + [neighbor]
                unvisited[neighbor] = path
                it += 1
                heappush(reachable, (cost, it, neighbor))
            del unvisited[current]
        return None, None

    def print(self) -> None:
        for x in range(len(self.items)):
            for y in range(len(self.items[0])):
                print(str(self.items[x][y]), end="")
            print()
        print()
