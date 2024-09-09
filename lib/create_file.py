# from instanceCreator import createAndTestInstances
from typing import List, Any
import os
import warnings
import random
from lib.edge import Edge


class CreateFile:
    def __init__(
        self,
        bus_data: dict[int, int],
        # taktBusEntry: int,
        passengerCountEntry: int,
        timeStart: str,
        timeEnd: str,
    ) -> None:

        self.bus_data = bus_data
        # self.taktBusEntry = taktBusEntry
        self.passengerCountEntry = passengerCountEntry
        # self.taktBusEntry = taktBusEntry
        self.timeStart = timeStart
        self.timeEnd = timeEnd
        self.convert_time_to_second()

    def create_text_file(self) -> None:
        folderName = "Instances"
        folderPath = os.path.join("Data", folderName)

        if not os.path.exists(folderPath):
            warnings.warn("Could not find directory to save files")
            a = input(
                "Do you want to create an example Folder for the instances?  (Y/W)"
            )
            if a == "Y" or a == "y":
                os.makedirs(folderPath)

        fileName = os.path.join(folderPath, "example.txt")
        with open(fileName, "w") as file:

            file.write("* Haltestellen\n*\n$STOP:ID;Code\n")
            self.create_stops(file)

            file.write("*\n")
            file.write(
                "* Fahrzeugtypen\n*\n"
                "$VEHICLETYPE:ID;Code;Name;VehCost;KmCost;HourCost;Capacity;MinUsage;TotalCapacity;"
                "ReliefCar;MaxBlockTime;Maxrun_time;RefuelingDuration;MaxBlockDistance;Operator;"
                "FuelCapacity;FuelConsumptionPerMeter;FuelConsumptionPerSecond;RefuelingPower;"
                "RefuelingFunctionID;PassengerCapacity\n"
            )

            file.write("0;NF;;100000;3;3;5;0;-1;0;0;0;-1;0;-1;-1;0;0;0;-1;104\n")
            file.write("*\n")

            file.write(
                "* Fahrzeugkapazitaeten\n*\n$VEHTYPECAPTOSTOPPOINT:ID;VehTypeID;StoppointID;Min;Max;TotalMax\n"
            )
            for i in range(len(self.bus_data.keys())):
                file.write(f"{i};{i};{20};0;5;-1\n")
            file.write("*\n")

            file.write(
                "* Routen\n*\n$PATTERN:ID;PatternNo;LineId;DirectionNo;TotalDistance\n"
            )
            self.create_routes(file)

            file.write("*\n")
            file.write(
                "* Fahrzeitarten und Bedienzeiten\n\*\n$PATTERN_OPERATING_HOURS:ID;TimeDemandTypeCode;TimeStart;TimeEnd\n"
            )
            self.create_driving_times(file)
            file.write("*\n")
            file.write(
                "* Routenverlauf und Fahrzeiten\n\*\n$PATTERN_DRIVING_TIMES:ID;PatternId;StopIndex;PatternOperatingHoursId;StopId;DrivingTime;PointId\n"
            )
            self.route_and_driving(file)
            #
            #
            #
            file.write("*\n")
            file.write("* Messpunkte\n*\n$TRACKING_GATE:ID;FromStopId;ToStopId\n")
            self.set_tracking_gate(file)

            file.write("*\n")
            file.write(
                "* Messpunkte - Bedienzeiten\n*\n$TRACKING_GATE_OPERATINGHOUR:ID;TrackingGateId;TimeStart;TimeEnd;PassengersPerHour;MinHeadway;MaxHeadway\n"
            )
            self.service_times(file)
            file.write("*\n")
            file.write(
                "* Transfers\n*\n$CONNECTION:ID;FeederPatternId;TakerPatternId;StopId;ConnectingTime\n"
            )

            #
            #
            #
            file.write("*\n")
            file.write(
                "* Verbindungsfahrten\n*\n$DEADrun_time:ID;FromStopID;ToStopID;FromTime;ToTime;Distance;run_time;Source\n"
            )
            self.set_dead_runtime(file)

    def create_stops(self, file) -> None:
        stops = sum(self.bus_data.values())
        for i in range(0, stops):
            file.write(f"{i};{i+1}Stop\n")

    ##### Distance will be neglected so far -> basis value of 1000
    def create_routes(self, file) -> None:
        for i in range(0, len(self.bus_data)):
            file.write(f"{i};{i+1};{i+1};1;1000\n")

    def create_driving_times(self, file) -> None:
        for i in range(0, len(self.bus_data)):
            file.write(f'{i};"Allday";{self.timeStart};{self.timeEnd}\n')

    def route_and_driving(self, file) -> None:
        #### vielleicht hier network loaden

        bus_data: dict[int, int] = self.bus_data
        stopsRange = sum(bus_data.values())
        ##### TO DO ######
        # hier stop_index == point_id , weil wir keine Überschneidungen haben, Knotennr unabhängig
        for i in range(0, stopsRange):
            pattern_id = self.get_pattern_id(i, bus_data)
            stop_index = self.get_stop_index(i, bus_data)  ## testing hier
            randomDrivinTime = random.randint(3, 9) * 100
            file.write(
                f"{i};{pattern_id};{stop_index};{pattern_id};{i+1};{randomDrivinTime};{i+1}\n"
            )

    @staticmethod
    def get_pattern_id(index: int, bus_data: dict[int, int]) -> int:
        current_sum = 0
        for key, value in bus_data.items():
            current_sum += value
            if index < current_sum:
                return key
        return -1

    @staticmethod
    def get_stop_index(index: int, bus_data: dict[int, int]) -> int:
        current_sum = 0
        for value in bus_data.values():
            next_sum = current_sum + value
            if index < next_sum:
                return index - current_sum
            current_sum = next_sum
        return -1

    def set_tracking_gate(self, file) -> None:
        for i in range(0, len(self.bus_data)):
            if i > 0:
                file.write(f"{i};{i+2};{i+3}\n")
            else:
                file.write(f"{i};{i+1};{i+2}\n")

    def service_times(self, file) -> None:
        for i in range(0, len(self.bus_data)):
            for j in range(3):
                if j == 0:
                    file.write(f"{j};{i};{self.timeStart};{self.timeEnd};1;NULL;600\n")
                elif j < len(self.bus_data):
                    file.write(
                        f"{j};{i};{self.timeStart};{self.timeEnd};{self.passengerCountEntry};300;780\n"
                    )
                else:
                    file.write(f"{j};{i};{self.timeStart};{self.timeEnd};1;NULL;NULL\n")

    def transform_bus_data(
        self, bus_data: dict[int, int]
    ) -> dict[int, list[int] | str]:
        next_number = 1
        new_bus_data: dict[int, list[int] | str] = {}
        for key, value in bus_data.items():
            new_list = list(range(next_number, next_number + value))
            new_bus_data[key] = new_list
            next_number += value

        return new_bus_data

    def create_edges_dict(
        self, bus_data: dict[int, list[int] | str]
    ) -> dict[int, list[Edge]]:
        edges_dict: dict[int, list[Edge]] = {}

        all_nodes = [node for nodes in bus_data.values() for node in nodes]

        for key1, list1 in bus_data.items():
            edges_dict[key1] = []

            for node1 in list1:

                for node2 in all_nodes:

                    if node1 != node2:
                        key2 = next(
                            key for key, nodes in bus_data.items() if node2 in nodes
                        )

                        distance = CreateFile.calculate_distance(key1, key2)

                        run_time = distance * 6

                        edges_dict[key1].append(
                            Edge(
                                edge=(node1, node2),
                                distance=distance,
                                run_time=run_time,
                            )
                        )

        return edges_dict

    def set_dead_runtime(self, file) -> None:
        new_bus_data: dict[int, list[int] | str] = self.transform_bus_data(
            bus_data=self.bus_data
        )
        new_bus_data[-1] = "D"

        print("Hier das Dict für die Bus Daten: ", new_bus_data)

        edges_dict: dict[int, list[Edge]] = self.create_edges_dict(new_bus_data)

        i: int = 0

        for key, edges_list in edges_dict.items():

            for edge in edges_list:
                print(edge)
                file.write(
                    f"{i};{edge.edge[0]};{edge.edge[1]};NULL;NULL;{edge.distance};{edge.run_time};S\n"
                )

            i = i + 1

    def convert_time_to_second(self) -> None:
        start_time_str = self.timeStart
        end_time_str = self.timeEnd

        start_hours, start_minutes = map(int, start_time_str.split(":"))
        end_hours, end_minutes = map(int, end_time_str.split(":"))

        self.timeStart = str(start_hours * 3600 + start_minutes * 60)
        self.timeEnd = str(end_hours * 3600 + end_minutes * 60)

    @staticmethod
    def calculate_distance(key1: int, key2: int) -> int:
        if key1 == key2:
            return 1000
        else:
            return 300 * abs(key1 - key2)
