from dataclasses import dataclass
from typing import Dict, Generator, Iterator, List, Optional
from collections import namedtuple

NON_ROOM_INDICES = [0, 1, 3, 5, 7, 9, 10]
ROOM_DEPTH = 4
AmphipodData = namedtuple("AmphipodData", ['room_index', 'value', 'letter'])


AMPHIPODS_DATA = {
    "A": AmphipodData(2, 1, "A"),
    "B": AmphipodData(4, 10, "B"),
    "C": AmphipodData(6, 100, "C"),
    "D": AmphipodData(8, 1000, "D"),
}


@dataclass(frozen=True)
class SimplifiedGameState:
    h0: str
    h1: str
    h2: str
    h3: str
    h4: str
    h5: str
    h6: str
    h7: str
    h8: str
    h9: str
    h10: str

    def _to_list(self) -> List[str]:
        return [
            self.h0,
            self.h1,
            self.h2,
            self.h3,
            self.h4,
            self.h5,
            self.h6,
            self.h7,
            self.h8,
            self.h9,
            self.h10,
        ]

    def get_from_index(self, index: int) -> str:
        return self._to_list()[index]

    def print(self) -> None:
        print("", end="|")
        for i in range(11):
            if i in NON_ROOM_INDICES and self.get_from_index(i):
                print(self.get_from_index(i), end="|")
            else:
                print(" ", end="|")
        print()
        for i in range(ROOM_DEPTH):
            print("   ", end="")
            for amphipod_data in AMPHIPODS_DATA.values():
                print(" ", end="|")
                print(
                    self.get_from_index(amphipod_data.room_index)[i : i + 1] or " ",
                    end="|",
                )
            print()


class GameState(SimplifiedGameState):
    def create_simplified_state(self) -> SimplifiedGameState:
        # https://docs.python.org/3/reference/expressions.html#boolean-operations
        # > The expression `x and y` first evaluates x; if x is false, its value is
        # > returned; otherwise, y is evaluated and the resulting value is returned.
        return SimplifiedGameState(
            h0=self.h0 and self.h0[0],
            h1=self.h1 and self.h1[0],
            h2=(
                self.h2
                and str.join("", [self.h2[i] for i in range(0, len(self.h2), 2)])
            ),
            h3=self.h3 and self.h3[0],
            h4=(
                self.h4
                and str.join("", [self.h4[i] for i in range(0, len(self.h4), 2)])
            ),
            h5=self.h5 and self.h5[0],
            h6=(
                self.h6
                and str.join("", [self.h6[i] for i in range(0, len(self.h6), 2)])
            ),
            h7=self.h7 and self.h7[0],
            h8=(
                self.h8
                and str.join("", [self.h8[i] for i in range(0, len(self.h8), 2)])
            ),
            h9=self.h9 and self.h9[0],
            h10=self.h10 and self.h10[0],
        )

    def gen_hallway(self, indices: Iterator[int]) -> Generator[str, None, None]:
        for i in indices:
            if i in NON_ROOM_INDICES:
                yield self.get_from_index(i)

    def is_room_open(self, amphipod_data: AmphipodData) -> bool:
        room = self.get_from_index(amphipod_data.room_index)
        return all(room[i] == amphipod_data.letter for i in range(0, len(room), 2))

    def is_room_complete(self, amphipod_data: AmphipodData) -> bool:
        room = self.get_from_index(amphipod_data.room_index)
        return len(room) == 2 * ROOM_DEPTH and self.is_room_open(amphipod_data)

    def is_complete(self) -> bool:
        return all(not h for h in self.gen_hallway(NON_ROOM_INDICES)) and all(
            self.is_room_complete(amphipod_data)
            for amphipod_data in AMPHIPODS_DATA.values()
        )

    def can_move(self, si: int, ei: int) -> bool:
        return (
            si < ei and all(not h for h in self.gen_hallway(range(si + 1, ei + 1)))
        ) or (ei < si and all(not h for h in self.gen_hallway(range(ei, si))))

    def create_moved_state(self, si: int, ei: int) -> "GameState":
        assert si != ei
        updated_game = self._to_list()
        updated_game[ei] = updated_game[si][:2] + updated_game[ei]
        updated_game[si] = updated_game[si][2:]
        return GameState(*updated_game)

    def print(self) -> None:
        print("", end="|")
        for i in range(11):
            if i in NON_ROOM_INDICES and self.get_from_index(i):
                print(self.get_from_index(i), end="|")
            else:
                print("  ", end="|")
        print()
        for i in range(ROOM_DEPTH):
            print("    ", end="")
            for amphipod_data in AMPHIPODS_DATA.values():
                print("  ", end="|")
                print(
                    self.get_from_index(amphipod_data.room_index)[
                        (i * 2) : (i * 2) + 2
                    ]
                    or "  ",
                    end="|",
                )
            print()


# created solely for debugging purposes - logic works just fine if all
# that is returned from play() is an aggregate score, but that is
# much harder to debug
class Move:
    def __init__(
        self,
        cost: int,
        state: GameState,
        next_move: Optional["Move"] = None,
    ) -> None:
        self.next_move = next_move
        self.game_state = state
        self.cost = cost
        self.total_score = cost + (self.next_move.total_score if self.next_move else 0)

    def print_game(self, running_total: int) -> None:
        self.game_state.create_simplified_state().print()
        if not self.next_move:
            return
        running_total += self.cost
        input()
        print(f"Cost: {self.cost}")
        print(f"Score: {running_total}")
        self.next_move.print_game(running_total)


game_results: Dict[SimplifiedGameState, Move] = {}
def play_cached_game(game: GameState) -> Optional[Move]:
    simplified_game = game.create_simplified_state()
    if simplified_game in game_results:
        return game_results[simplified_game]
    last_move = play(game)
    game_results[simplified_game] = last_move
    return last_move


def play(
    game: GameState,
) -> Optional[Move]:
    if game.is_complete():
        return Move(0, game)

    # if an amphipod can go home, it should - from hallway
    for i in NON_ROOM_INDICES:
        amphipod: str = game.get_from_index(i)
        if not amphipod: continue
        amphipod_data = AMPHIPODS_DATA[amphipod[0]]
        if game.is_room_open(amphipod_data) and game.can_move(
            i, amphipod_data.room_index
        ):
            cost = amphipod_data.value * abs(i - amphipod_data.room_index)
            cost += amphipod_data.value * (
                ROOM_DEPTH
                - int(len(game.get_from_index(amphipod_data.room_index)) / 2)
            )
            new_game_state = game.create_moved_state(i, amphipod_data.room_index)
            next_move = play_cached_game(new_game_state)
            if next_move is not None:
                return Move(cost, game, next_move)
            return None

    # if an amphipod can go home it should - from start room
    for start_amphipod_data in AMPHIPODS_DATA.values():
        if game.is_room_open(start_amphipod_data): continue
        start_room: str = game.get_from_index(start_amphipod_data.room_index)
        home_amphipod_data = AMPHIPODS_DATA[start_room[0]]
        if (
            start_amphipod_data.room_index != home_amphipod_data.room_index
            and game.is_room_open(home_amphipod_data)
            and game.can_move(
                start_amphipod_data.room_index, home_amphipod_data.room_index
            )
        ):
            cost = home_amphipod_data.value * abs(
                start_amphipod_data.room_index - home_amphipod_data.room_index
            )
            cost += home_amphipod_data.value * (
                ROOM_DEPTH
                - int(len(game.get_from_index(home_amphipod_data.room_index)) / 2)
            )
            cost += home_amphipod_data.value * (
                1
                + ROOM_DEPTH
                - int(len(game.get_from_index(start_amphipod_data.room_index)) / 2)
            )
            new_game_state = game.create_moved_state(
                start_amphipod_data.room_index, home_amphipod_data.room_index
            )
            next_move = play_cached_game(new_game_state)
            if next_move is not None:
                return Move(cost, game, next_move)
            return None

    winning_moves = []
    # move amphipods in the hallway around
    # for i in NON_ROOM_INDICES:
    # 	amphipod: str = game.get_from_index(i)
    # 	if not amphipod: continue
    # 	for j in NON_ROOM_INDICES:
    # 		if abs(i-j) < 2: continue
    # 		if game.can_move(i, j):
    # 			cost = AMPHIPODS_DATA[amphipod[0]].value * abs(i-j)
    # 			new_game_state = game.create_moved_state(i, j)
    # 			next_move = play_cached_game(new_game_state)
    # 			if next_move is not None:
    # 				winning_moves.append(Move(cost, game, next_move))

    # move amphipods out of rooms and into the hallway
    for amphipod_data in AMPHIPODS_DATA.values():
        if game.is_room_open(amphipod_data): continue
        amphipod: str = game.get_from_index(amphipod_data.room_index)[:2]
        for i in NON_ROOM_INDICES:
            if game.can_move(amphipod_data.room_index, i):
                value = AMPHIPODS_DATA[amphipod[0]].value
                cost = value * abs(amphipod_data.room_index - i)
                cost += value * (
                    1
                    + ROOM_DEPTH
                    - int(len(game.get_from_index(amphipod_data.room_index)) / 2)
                )
                new_game_state = game.create_moved_state(amphipod_data.room_index, i)
                next_move = play_cached_game(new_game_state)
                if next_move is not None:
                    winning_moves.append(Move(cost, game, next_move))

    if winning_moves:
        winning_moves.sort(key=lambda x: x.total_score)
        return winning_moves[0]
    return None


def run(input_data: List[str], **kwargs) -> int:
    # my input
    aroom = "C1D1D2B1"
    broom = "D3C2B2A1"
    croom = "A2B3A3D4"
    droom = "B4A4C3C4"

    # test input
    # aroom = "B1D1D2A1"
    # broom = "C1C2B2D3"
    # croom = "B3B4A2C3"
    # droom = "D4A3C4A4"

    # part1 input
    # aroom = "C1B1"
    # broom = "D1A1"
    # croom = "A2D2"
    # droom = "B2C2"

    start_game = GameState(
        "",
        "",
        aroom,
        "",
        broom,
        "",
        croom,
        "",
        droom,
        "",
        "",
    )
    move = play_cached_game(start_game)
    # move.print_game(0)
    return move.total_score
