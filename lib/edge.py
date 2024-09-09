from dataclasses import dataclass


@dataclass(frozen=True)
class Edge:
    edge: tuple[int | str, int | str]
    distance: int
    run_time: int
