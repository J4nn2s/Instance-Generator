# appearance.py
import customtkinter

class AppearanceOptions:
    def __init__(self, master):
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.appearance_mode_optionmenu = customtkinter.CTkOptionMenu(
            self.master,
            values=["Light", "Dark"],
            command=self.change_appearance_mode,
        )
        self.appearance_mode_optionmenu.grid(row=11, column=0, padx=20, pady=(10, 10))
        self.appearance_mode_optionmenu.set("Dark")
        self.scaling_optionmenu = customtkinter.CTkOptionMenu(
            self.master,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling_event,
        )
        self.scaling_optionmenu.grid(row=12, column=0, padx=20, pady=(10, 20))
        self.scaling_optionmenu.set("100%")
        self.appearance_mode_optionmenu.set("Dark")

    def change_appearance_mode(self, mode):
        customtkinter.set_appearance_mode(mode)

    def change_scaling_event(self, scaling):
        customtkinter.set_widget_scaling(int(scaling.strip('%')) / 100)