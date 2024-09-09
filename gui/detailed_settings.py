import customtkinter
import tkinter.messagebox
from typing import Dict
from datetime import datetime, timedelta
from lib.custom_time import CustomTime
from loguru import logger


class DetailedSettingsWindow(customtkinter.CTkToplevel):
    def __init__(
        self,
        master: customtkinter.CTk,
        num_lines: int,
        bus_data: Dict[int, int],
        start_time_default: str,
        end_time_default: str,
    ) -> None:
        super().__init__(master)
        self.title("Detailed Settings")
        self.attributes("-topmost", True)

        self.bus_data = bus_data
        self.entries = []

        self.state("zoomed")
        times = []
        current_time = CustomTime(-5)
        end_time = CustomTime(28)
        while current_time.total_minutes <= end_time.total_minutes:
            times.append(current_time.to_24_hour_format())
            current_time += timedelta(minutes=60)
        headers = ["Line", "Stops", "Start", "End", "Passengers per hour"]

        for col, header in enumerate(headers):
            label = customtkinter.CTkLabel(
                self, text=header, anchor="w", font=("Arial", 16, "bold")
            )
            label.grid(row=0, column=col, padx=20, pady=(10, 0))

        for i in range(1, num_lines + 1):
            label = customtkinter.CTkLabel(self, text=f"Line {i}", anchor="w")
            label.grid(row=i, column=0, padx=20, pady=(10, 0))

            entry_stops = customtkinter.CTkEntry(self)
            entry_stops.grid(row=i, column=1, padx=20, pady=(10, 0))

            entry_start_time = customtkinter.CTkOptionMenu(self, values=times)
            entry_start_time.grid(row=i, column=2, padx=20, pady=(10, 0))

            entry_end_time = customtkinter.CTkOptionMenu(self, values=times)
            entry_end_time.grid(row=i, column=3, padx=20, pady=(10, 0))

            entry_passengers = customtkinter.CTkEntry(self)
            entry_passengers.grid(row=i, column=4, padx=20, pady=(10, 0))

            #### default values ####
            entry_stops.insert(0, "2")
            entry_start_time.set(start_time_default)
            entry_end_time.set(end_time_default)
            entry_passengers.insert(0, "50")
            self.entries.append(entry_stops)

        save_button = customtkinter.CTkButton(
            self, text="Save", command=self.save_and_close_detailed
        )
        save_button.grid(row=num_lines + 1, column=0, columnspan=2, pady=(10, 0))

    def save_and_close_detailed(self) -> None:
        logger.info("Saving detailed settings")
        pass


#
# try:
# self.bus_data.update(
# {
# int(i): {
# "stops": int(entry_stops.get()),
# "start_time": entry_start_time.get(),
# "end_time": entry_end_time.get(),
# "passengers": int(entry_passengers.get()),
# }
# for i, (
# entry_stops,
# entry_start_time,
# entry_end_time,
# entry_passengers,
# ) in enumerate(self.entries)
# }
# )
# self.destroy()
# tkinter.messagebox.showinfo("Data Saved", "Bus data saved successfully.")
# except ValueError:
# tkinter.messagebox.showerror(
# "Invalid Input", "Please enter valid numbers for all bus lines."
# )
#
