import customtkinter
import logging
from lib.create_file import CreateFile
from loguru import logger

class ButtonFunctions:
    def __init__(self, main_window) -> None:
        self.main_window = main_window


    def create_file(self) -> None:
        try:
            bus_lines = int(self.main_window.sidebar.number_bus_entry.get())
            bus_data = self.main_window.sidebar.get_bus_data()
            logger.info(f"Buslinien: {bus_lines}")
            logger.info(f"Anzahl der Passagiere: {self.main_window.sidebar.passenger_count_entry.get()}")
            logger.info(f"Startzeit: {self.main_window.sidebar.start_time_dropdown.get()}")
            logger.info(f"Endzeit: {self.main_window.sidebar.end_time_dropdown.get()}")
            
            if not bus_data or len(bus_data) != bus_lines:
                raise ValueError(
                    "Bitte geben Sie die Anzahl der Haltestellen für alle Buslinien an."
                )
            FileCreator: CreateFile = CreateFile(
                bus_data=bus_data,
                passengerCountEntry = int(self.main_window.sidebar.passenger_count_entry.get()),
                timeStart = self.main_window.sidebar.start_time_dropdown.get(),
                timeEnd=self.main_window.sidebar.end_time_dropdown.get(),
            )
            FileCreator.create_text_file()
            print("Instanz wird erstellt...")
        except ValueError:
            logger.warning("Es kann noch keine Instanz erstellt werden")
        except Exception as e:
            logger.warning(f"Fehler beim Erstellen der Instanz: {str(e)}")
        else:
            logger.success("Instanz erfolgreich erstellt")