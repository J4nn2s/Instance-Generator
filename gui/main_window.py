import customtkinter
from gui.sidebar import Sidebar
from gui.graph_playground import GraphPlayground
from lib.create_file import CreateFile
from validation.validate_instance import check_empty_driving_times
from loguru import logger
import tkinter as tk
from lib.button_functions import ButtonFunctions


class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        logger.info("MainWindow initialized")
        self.title("Instance Creator & Tester")
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("blue")

        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="ns")

        ##############################
        # Graph Playground
        ##############################
        self.cancas_frame = customtkinter.CTkFrame(
            self, width=300, height=300, corner_radius=0
        )
        self.cancas_frame.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")
        self.graph_playground_frame = tk.Frame(self.cancas_frame)
        self.graph_playground_frame.pack(fill="both", expand=True)

        self.graph_playground = GraphPlayground(
            master=self.graph_playground_frame, sidebar=self.sidebar
        )
        self.graph_playground.pack(fill="both", expand=True)

        self.button_functions = ButtonFunctions(self)

        ##############################
        # Create File Button
        ##############################
        self.create_instance_button = customtkinter.CTkButton(
            self,
            text="Generate instance",
            corner_radius=0,
            command=self.button_functions.create_file,
        )
        self.create_instance_button.grid(row=0, column=2, sticky="ne", padx=20, pady=20)


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
