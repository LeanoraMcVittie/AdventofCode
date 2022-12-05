from __future__ import annotations
from typing import List, Optional
from utils.field.two_d import Cell, Coord, Field


WHITESPACE: bool = True


class PortalCell(Cell):
    portal: Optional[PortalCell]

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.portal = None

    def neighbor_coords(self, include_diagonals: bool = False) -> List[Coord]:
        neighbor_coords = super().neighbor_coords(include_diagonals)
        if self.portal:
            neighbor_coords.append(self.portal)
        return neighbor_coords

    def cost(self) -> int:
        return 1 if self.value == "." else 0

    def add_portal(self, portal: PortalCell) -> None:
        self.portal = portal
        portal.portal = self

    def concat(self, secondary: PortalCell) -> None:
        self.value += secondary.value
        secondary.value = " "


class Donut(Field):
    def fix_portal_names(self) -> None:
        self.apply(
            filterer=lambda c: (
                c.value.isupper()
                and self.apply_adjacent(
                    cell=c,
                    include_diagonals=False,
                    filterer=lambda n: n.value == ".",
                )
                == 1
            ),
            transform=lambda c: c.concat(
                self.first_adjacent(
                    cell=c,
                    include_diagonals=False,
                    filterer=lambda n: n.value.isupper(),
                )
            ),
        )

    def setup_portals(self) -> None:
        self.fix_portal_names()
        self.apply(
            filterer=lambda c: c.value.isupper() and not c.portal,
            transform=lambda c: self.first(
                filterer=lambda p: (
                    p.value == c.value or p.value == f"{c.value[1]}{c.value[0]}"
                )
                and p is not c,
                transform=lambda p: p.add_portal(c),
            ),
        )


def run(input_data: List[str], **kwargs) -> int:
    donut = Donut.create_from_input([l.strip("\n") for l in input_data], PortalCell)
    donut.setup_portals()
    steps, _ = donut.dijkstra(
        start=donut.first(filterer=lambda x: x.value == "AA"),
        end=donut.first(filterer=lambda x: x.value == "ZZ"),
        include_diagonals=False,
        filterer=lambda x: x.value == "." or x.value.isupper(),
    )
    return steps - 1
