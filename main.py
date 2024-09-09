from gui.main_window import MainWindow

if __name__ == "__main__":
    app = MainWindow()
    app._state_before_windows_set_titlebar_color = "zoomed"

    app.mainloop()