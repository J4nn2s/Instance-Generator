import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import json
import os
from loguru import logger


class GraphPlayground(ctk.CTkFrame):
    def __init__(self, master, sidebar):
        super().__init__(master)
        self.sidebar = sidebar
        self.master = master
        self.pack(expand=True, fill=tk.BOTH)
        self.create_widgets()
        self.lines: list[list[str]] = []
        self.nodes: dict[str, tuple[str, str]] = {}

        #### special to separate library grafics from bus / line data
        self.lines_to_save: list[list[str]] = []
        self.nodes_to_save: dict[str, tuple[str, str]] = {}

    def create_widgets(self):
        self.canvas = ctk.CTkCanvas(self, width=800, height=600, bg="#34495E")
        self.canvas.pack(expand=True, fill=tk.BOTH)
        self.selected_item = None
        self.offset_x = 0
        self.offset_y = 0

        self.colors = ["#3498DB", "#E74C3C", "#2ECC71", "#F39C12"]
        self.color_index = 0
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.move_item)
        self.canvas.bind("<ButtonRelease-1>", self.release_item)

        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.clear_button = ctk.CTkButton(
            self.control_frame, text="Clear Playground", command=self.clear_playground
        )
        self.clear_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.use_button = ctk.CTkButton(
            self.control_frame, text="Use this Data", command=self.integrate_in_sidebar
        )
        self.use_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.save_button = ctk.CTkButton(
            self.control_frame, text="Save Coordinates", command=self.save_coordinates
        )
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.load_button = ctk.CTkButton(
            self.control_frame, text="Load Coordinates", command=self.load_coordinates
        )
        self.load_button.pack(side=tk.LEFT, padx=5, pady=5)

    def on_canvas_click(self, event):
        items = self.canvas.find_overlapping(
            event.x - 10, event.y - 10, event.x + 10, event.y + 10
        )
        if items:
            item = items[0]
            if item in self.nodes or item in [line[2] for line in self.lines]:
                self.selected_item = item
                bbox = self.canvas.bbox(item)
                self.offset_x = event.x - (bbox[0] + bbox[2]) // 2
                self.offset_y = event.y - (bbox[1] + bbox[3]) // 2
            else:
                self.create_line(event)
        else:
            self.create_line(event)

    def create_line(self, event):
        color = self.colors[self.color_index]
        x, y = event.x, event.y

        start_node_id = len(self.nodes_to_save) + 1
        end_node_id = len(self.nodes_to_save) + 2

        start_node = self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=color)
        end_node = self.canvas.create_oval(
            x + 400 - 10, y - 10, x + 400 + 10, y + 10, fill=color
        )
        line = self.canvas.create_line(x, y, x + 400, y, fill=color, width=5)

        self.lines.append((start_node, end_node, line))
        self.nodes[start_node] = (x, y)
        self.nodes[end_node] = (x + 400, y)

        #### TO SAVE AND LOAD #### STRICTLY separate from GUI library // customtkinter-objects
        self.lines_to_save.append(
            (start_node_id, end_node_id, len(self.lines_to_save) + 1)
        )
        self.nodes_to_save[start_node_id] = (x, y)
        self.nodes_to_save[end_node_id] = (x + 400, y)

        self.color_index = (self.color_index + 1) % len(self.colors)

    def move_item(self, event):
        if self.selected_item:
            if self.selected_item in self.nodes:
                x, y = event.x - self.offset_x, event.y - self.offset_y
                self.canvas.coords(self.selected_item, x - 10, y - 10, x + 10, y + 10)
                self.nodes[self.selected_item] = (x, y)
                for start_node, end_node, line in self.lines:
                    if self.selected_item == start_node:
                        end_pos = self.nodes[end_node]
                        self.canvas.coords(line, x, y, end_pos[0], end_pos[1])
                    elif self.selected_item == end_node:
                        start_pos = self.nodes[start_node]
                        self.canvas.coords(line, start_pos[0], start_pos[1], x, y)
            elif self.selected_item in [line[2] for line in self.lines]:
                line = [line for line in self.lines if line[2] == self.selected_item][0]
                start_node, end_node, _ = line
                start_x, start_y = self.nodes[start_node]
                end_x, end_y = self.nodes[end_node]
                dx = event.x - (start_x + end_x) // 2
                dy = event.y - (start_y + end_y) // 2
                self.canvas.move(start_node, dx, dy)
                self.canvas.move(end_node, dx, dy)
                self.canvas.move(self.selected_item, dx, dy)
                self.nodes[start_node] = (start_x + dx, start_y + dy)
                self.nodes[end_node] = (end_x + dx, end_y + dy)

    def release_item(self, event):
        self.selected_item = None

    def clear_playground(self):
        self.canvas.delete("all")
        self.lines = []
        self.nodes = {}
        self.nodes_to_save = {}
        self.lines_to_save = []

    def save_coordinates(self):
        file_path = os.path.join("Data", "Coordinates", "coordinates.json")
        data = {
            "nodes": {
                str(i + 1): pos
                for i, (node_id, pos) in enumerate(self.nodes_to_save.items())
            },
            "lines": [
                [str(start), str(end), str(line_id)]
                for start, end, line_id in self.lines_to_save
            ],
        }
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Lines Data Structure: {self.lines_to_save}")
        logger.info(f"Nodes Data Structure: {self.nodes_to_save}")

    def load_coordinates(self):
        self.clear_playground()

        file_path = filedialog.askopenfilename(
            initialdir="Data/Coordinates",
            title="Select file",
            filetypes=(("JSON files", "*.json"), ("all files", "*.*")),
        )
        if file_path:
            with open(file_path, "r") as f:
                data = json.load(f)

            node_map = {}
            for node_str, pos in data["nodes"].items():
                x, y = pos
                node = self.canvas.create_oval(
                    x - 10, y - 10, x + 10, y + 10, fill=self.colors[self.color_index]
                )
                node_id = int(node_str)
                self.nodes[node_id] = (x, y)
                node_map[node_str] = node
                self.color_index = (self.color_index + 1) % len(self.colors)

            for start_str, end_str, line_id in data["lines"]:
                start_node = node_map[start_str]
                end_node = node_map[end_str]
                start_pos = self.nodes[int(start_str)]
                end_pos = self.nodes[int(end_str)]
                line = self.canvas.create_line(
                    start_pos[0],
                    start_pos[1],
                    end_pos[0],
                    end_pos[1],
                    fill=self.colors[self.color_index],
                    width=5,
                )
                self.lines.append((start_node, end_node, line))
                self.lines_to_save.append((int(start_str), int(end_str), line_id))
                self.color_index = (self.color_index + 1) % len(self.colors)

    def integrate_in_sidebar(self) -> None:
        num_lines = len(self.lines_to_save)
        # Aktualisieren Sie das Label in der Sidebar mit der Anzahl der Linien
        self.sidebar.number_bus_entry.delete(0, tk.END)
        self.sidebar.number_bus_entry.insert(0, str(num_lines))

    def mainloop(self):
        super().mainloop()
