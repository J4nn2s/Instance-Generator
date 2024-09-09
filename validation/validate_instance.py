import os
import sys
from loguru import logger
from typing import List, Tuple, TextIO
from lib.create_file import Edge


def check_empty_driving_times(file: TextIO) -> None:
    pass
    # start_processing = False
    # edges: List[Edge] = []
    # i: int = 0
    # for line in file:
    #     if (
    #         line.strip()
    #         == "$DEADrun_time:ID;FromStopID;ToStopID;FromTime;ToTime;Distance;run_time;Source"
    #     ):
    #         start_processing = True
    #         continue

    #     if start_processing:
    #         i += 1
    #         parts = line.strip().split(";")
    #         if len(parts) == 8:
    #             edge = (parts[1], parts[2])
    #             distance = int(parts[5])
    #             run_time = int(parts[6])

    #             edge_obj = Edge(edge=edge, distance=distance, run_time=run_time)
    #             edges.append(edge_obj)
    #         else:
    #             break
    # checking_edges = check_edges(edges)
    # print(checking_edges)
    # if checking_edges:
    #     logger.success("Die Instanz hat gültige Leerfahrten")
    # if not checking_edges:
    #     logger.warning("Es gibt Fehler in den Leerfahrten")
    #     b: List[Edge] = search_specific_mistakes_empty_rides(edges)
    #     logger.warning(
    #         "Folgende Leerfahrten enthalten inkonsistente Fahrzeiten oder Distanzen: \n"
    #     )
    #     for i in b:
    #         logger.info(f"{i}")


# def search_specific_mistakes_empty_rides(edges: List[Edge]) -> List[Edge]:
#     edge_dict: dict[tuple[int | str, int | str], Edge] = {}
#     inconsistent_edges: List[Edge] = []
#     for edge in edges:
#         key: tuple[int | str, int | str] = edge.edge
#         key_reversed: tuple[int | str, int | str] = (edge.edge[1], edge.edge[0])
#         if key_reversed in edge_dict:
#             existing_edge: Edge = edge_dict[key_reversed]
#             if (
#                 existing_edge.run_time != edge.run_time
#                 or existing_edge.distance != edge.distance
#             ):
#                 inconsistent_edges.append(edge)
#         else:
#             edge_dict[key] = edge
#     return inconsistent_edges


# def check_edges(edges: List[Edge]) -> bool:
#     edge_dict: dict[tuple[int | str, int | str], Edge] = {}

#     for edge in edges:
#         key: tuple[int | str, int | str] = edge.edge
#         key_reversed: tuple[int | str, int | str] = (edge.edge[1], edge.edge[0])
#         if key_reversed in edge_dict:
#             existing_edge: Edge = edge_dict[key_reversed]
#             if (
#                 existing_edge.run_time != edge.run_time
#                 or existing_edge.distance != edge.distance
#             ):
#                 return False
#         else:
#             edge_dict[key] = edge
#     return True


# if __name__ == "__main__":
#     textFilePath = os.path.abspath(
#         os.path.join(os.path.dirname(__file__), "..", "textFiles")
#     )
#     fileName = os.path.join(textFilePath, "example.txt")
#     with open(fileName, "r") as file:
#         check_empty_driving_times(file)
