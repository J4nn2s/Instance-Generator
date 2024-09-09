import customtkinter
from datetime import datetime, timedelta
import tkinter.messagebox
from lib.create_file import CreateFile
from gui.appearance import AppearanceOptions
from gui.detailed_settings import DetailedSettingsWindow
from lib.custom_time import CustomTime


class Sidebar(customtkinter.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.bus_data: dict[int, int] = {}
        self.create_widgets()

    def create_widgets(self) -> None:
        self.logo_label = customtkinter.CTkLabel(
            self,
            text="Instance Creator",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.number_bus_label = customtkinter.CTkLabel(
            self,
            text="Number of Bus Lines:",
            font=customtkinter.CTkFont(size=12, weight="normal"),
            anchor="w",
        )
        self.number_bus_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.number_bus_entry = customtkinter.CTkEntry(
            self,
            validate="key",
            validatecommand=(self.register(self.on_number_bus_entry_change), "%P"),
        )
        self.number_bus_entry.grid(row=2, column=0, padx=20, pady=(10, 0))
        self.takt_label = customtkinter.CTkLabel(
            self,
            text="Start time",
            font=customtkinter.CTkFont(size=12, weight="normal"),
            anchor="w",
        )
        self.takt_label.grid(row=3, column=0, padx=20, pady=(10, 0))

        self.end_label = customtkinter.CTkLabel(
            self,
            text="End time",
            font=customtkinter.CTkFont(size=12, weight="normal"),
            anchor="w",
        )
        self.end_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        times = []

        current_time = CustomTime(-5)
        end_time = CustomTime(28)
        while current_time.total_minutes <= end_time.total_minutes:
            times.append(current_time.to_24_hour_format())
            current_time += timedelta(minutes=60)

        self.start_time_dropdown = customtkinter.CTkOptionMenu(self, values=times)
        self.start_time_dropdown.grid(row=4, column=0, padx=20, pady=(10, 0))

        self.end_time_dropdown = customtkinter.CTkOptionMenu(self, values=times)
        self.end_time_dropdown.grid(row=6, column=0, padx=20, pady=(10, 20))

        ##### Passagierzahlen #####
        self.passenger_label = customtkinter.CTkLabel(
            self,
            text="Passengers per hour:",
            font=customtkinter.CTkFont(size=12, weight="normal"),
            anchor="w",
        )
        self.passenger_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.passenger_count_entry = customtkinter.CTkEntry(
            self,
            validate="key",
            validatecommand=(self.register(self.validate_number), "%P"),
        )
        self.passenger_count_entry.grid(row=8, column=0, padx=20, pady=(10, 20))

        self.detailed_settings_button = customtkinter.CTkButton(
            self, text="Detailed Settings", command=self.show_detailed_settings_window
        )
        self.detailed_settings_button.grid(row=9, column=0, padx=20, pady=(10, 0))

        ##### Appearance #####
        # Appearance options
        self.appearance_options = AppearanceOptions(self)
        ##### Set default Values #####
        self.number_bus_entry.insert(0, "2")
        self.passenger_count_entry.insert(0, "100")
        self.start_time_dropdown.set("08:00")
        self.end_time_dropdown.set("18:00")

    def validate_number(self, value) -> bool:
        try:
            if value == "" or int(value) >= 0 and int(value) <= 1000:
                return True
            else:
                return False
        except ValueError:
            return False

    def show_pop_up(self) -> None:
        try:
            num_lines = int(self.number_bus_entry.get())
            if num_lines <= 0:
                raise ValueError("Number of bus lines must be positive.")
        except ValueError as e:
            tkinter.messagebox.showerror("Invalid Input", str(e))
            return

        popup = customtkinter.CTkToplevel(self)
        popup.title("Stops per Line")
        popup.attributes("-topmost", True)

        width = 400
        height = 100 + num_lines * 30
        popup.geometry(f"{width}x{height}")

        entries = []
        for i in range(0, num_lines):
            label = customtkinter.CTkLabel(popup, text=f"Line {i} stops:", anchor="w")
            label.grid(row=i, column=0, padx=20, pady=(10, 0))

            entry = customtkinter.CTkEntry(popup)
            entry.grid(row=i, column=1, padx=20, pady=(10, 0))
            entry.insert(0, "2")
            entries.append(entry)

        def save_and_close() -> None:
            try:
                self.bus_data = {
                    int(i): int(entry.get()) for i, entry in enumerate(entries)
                }
                popup.destroy()
                tkinter.messagebox.showinfo(
                    "Data Saved", "Bus data saved successfully."
                )
            except ValueError:
                tkinter.messagebox.showerror(
                    "Invalid Input", "Please enter valid numbers for all bus lines."
                )

        save_button = customtkinter.CTkButton(
            popup, text="Save", command=save_and_close
        )
        save_button.grid(row=num_lines, column=0, columnspan=2, pady=(10, 0))

    def get_bus_data(self) -> dict[int, int]:
        return self.bus_data

    def on_number_bus_entry_change(self, P: str) -> bool:
        if self.validate_number(P):
            try:
                num_lines = int(P) if P else 0
                if num_lines > 0:
                    self.bus_data = {i: 2 for i in range(num_lines)}
                else:
                    self.bus_data = {}
            except ValueError:
                self.bus_data = {}
            return True
        return False

    def show_detailed_settings_window(self) -> None:
        try:
            num_lines = int(self.number_bus_entry.get())
            if num_lines <= 0:
                raise ValueError("Number of bus lines must be positive.")
        except ValueError as e:
            tkinter.messagebox.showerror("Invalid Input", str(e))
            return

        detailed_window = DetailedSettingsWindow(
            self,
            num_lines,
            self.bus_data,
            self.start_time_dropdown.get(),
            self.end_time_dropdown.get(),
        )
        detailed_window.mainloop()
