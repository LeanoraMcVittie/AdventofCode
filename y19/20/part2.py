from __future__ import annotations
from typing import Dict, List, Optional
from utils.field.two_d import Cell, Coord, Field
from heapq import heappush, heappop
from functools import partial
from itertools import combinations

WHITESPACE: bool = True


class PortalCell(Cell):
    portal: Optional[PortalCell]
    inside: bool = False

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

    def add_portal(self, portal: PortalCell, indicator: str) -> None:
        self.portal = portal
        portal.portal = self

        assert indicator == "o" or indicator == "i"
        inside = indicator == "i"
        self.inside = inside
        portal.inside = not inside

    def concat(self, secondary: PortalCell) -> None:
        self.value += secondary.value
        secondary.value = " "

    def set_inside(self, indicator: str) -> None:
        if indicator == "o":
            self.inside = False
        elif indicator == "i":
            self.inside = True
        raise Exception(f"{indicator} is not 'i' or 'o'")


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
                transform=lambda p: p.add_portal(
                    c,
                    self.first_adjacent(
                        cell=p,
                        filterer=lambda a: a.value.islower(),
                        transform=lambda a: a.value,
                    ),
                ),
            ),
        )

    def gen_portal_distances(self) -> Dict[PortalCell, Dict[PortalCell, int]]:
        distances = {}
        portal_cells = [c for c in self.gen_cells(filterer=lambda a: a.value.isupper())]
        for start, end in combinations(portal_cells, 2):
            cost, _ = self.dijkstra(
                start=start,
                end=end,
                include_diagonals=False,
                filterer=lambda x: x.value == "." or x == end,
            )
            if not cost:
                continue
            distances.setdefault(start, {})[end] = cost
            distances.setdefault(end, {})[start] = cost
        return distances

    def recursive_dijkstra(self, start: PortalCell, end: PortalCell) -> int:
        def can_move_to(layer: int, neighbor: PortalCell) -> bool:
            v = neighbor.value
            if v in ["#", " ", "i", "o"]:
                return False
            if layer == 0:
                return True
            if v == "AA" or v == "ZZ":
                return False
            return True

        def have_used_portal(
            path: List[PortalCell], current: PortalCell, next: PortalCell
        ) -> bool:
            if len(path) < 2:
                return False
            for i in range(len(path) - 1):
                if path[i] == current and path[i + 1] == next:
                    return True
            return False

        unvisited = {}
        it = 0  # sorting hack for heapq
        unvisited[(start, 0)] = [start]
        reachable = [(0, it, (start, 0))]
        visited = {}
        while reachable:
            cost_to_current, _, current = heappop(reachable)
            if current in visited:
                continue

            path_to_current = unvisited[current]
            current_cell = current[0]
            current_layer = current[1]
            if current_cell is end:
                return cost_to_current, path_to_current

            neighbors = self.gen_adjacent_cells(
                current_cell,
                include_diagonals=False,
                filterer=partial(can_move_to, current_layer),
            )
            for neighbor_cell in neighbors:
                if not current_cell.portal or not neighbor_cell.portal:
                    neighbor_layer = current_layer
                elif current_cell.inside and not neighbor_cell.inside:
                    neighbor_layer = current_layer + 1
                else:
                    neighbor_layer = current_layer - 1
                if neighbor_layer < 0:
                    continue

                neighbor = (neighbor_cell, neighbor_layer)
                if neighbor_layer in visited[neighbor_cell]:
                    continue
                cost = cost_to_current + neighbor_cell.cost
                path = unvisited.get(neighbor, [])
                if path and (
                    sum(c.cost for c in path) < cost
                    or have_used_portal(path, current_cell, neighbor_cell)
                ):
                    continue
                path = path_to_current + [neighbor_cell]
                unvisited[neighbor] = path
                it += 1
                heappush(reachable, (cost, it, (neighbor_cell, neighbor_layer)))
            visited.setdefault(current_cell, []).append(current_layer)
        return None, None


def run(input_data: List[str], **kwargs) -> int:
    donut = Donut.create_from_input([l.strip("\n") for l in input_data], PortalCell)
    donut.setup_portals()
    portal_distances = donut.gen_portal_distances()

    start_cell = donut.first(filterer=lambda x: x.value == "AA")
    end_cell = donut.first(filterer=lambda x: x.value == "ZZ")

    visited = []
    known_costs = {(start_cell, 0): 0}
    it = 0
    reachable = [(0, it, (start_cell, 0))]
    while reachable:
        cost_to_current, _, current = heappop(reachable)
        if current in visited:
            continue
        
        current_cell = current[0]
        current_layer = current[1]
        if current_cell is end_cell:
            return cost_to_current - 1
        
        for neighbor_cell, n_cost in portal_distances[
            current_cell.portal if current_cell.portal else current_cell
        ].items():
            if neighbor_cell is end_cell and current_layer != 0:
                continue
            if (
                neighbor_cell is not end_cell
                and not neighbor_cell.inside
                and current_layer == 0
            ):
                continue

            n_layer = current_layer + (1 if neighbor_cell.inside else -1)
            assert n_layer >= 0 or neighbor_cell is end_cell
            
            if (neighbor_cell, n_layer) in visited:
                continue
            cost = cost_to_current + n_cost
            prev_known_cost = known_costs.get((neighbor_cell, n_layer))
            if prev_known_cost and prev_known_cost < cost:
                continue
            known_costs[(neighbor_cell, n_layer)] = cost
            it += 1
            heappush(reachable, (cost, it, (neighbor_cell, n_layer)))
        visited.append(current)
