import tkinter as tk
from tkinter import ttk, messagebox
from pathFind import Graph


class CampusPathFinderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Campus Path Finder")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        self.g = Graph(7)
        self.setup_graph()

        self.node_names = {
            1: "Parking Garage",
            2: "Engineering",
            3: "University Centre (UC)",
            4: "Library",
            5: "Education",
            6: "Field House",
            7: "Bruno Centre"
        }

        self.name_to_node = {name: key for key, name in self.node_names.items()}

        self.create_widgets()

    def setup_graph(self):
        self.g.add_edge(1, 2, 4.49, 5)     # Parking - Engineering
        self.g.add_edge(1, 3, 4.08, 5)     # Parking - UC
        self.g.add_edge(3, 2, 3.05, 5)     # UC - Engineering
        self.g.add_edge(3, 2, 3.1, 10)     # UC - Engineering alternative
        self.g.add_edge(1, 5, 5.33, 25)    # Parking - Education
        self.g.add_edge(1, 6, 8.55, 25)    # Parking - Field House
        self.g.add_edge(5, 6, 4.26, 15)    # Education - Field House
        self.g.add_edge(5, 4, 5.26, 20)    # Education - Library
        self.g.add_edge(6, 4, 3.4, 15)     # Field House - Library
        self.g.add_edge(4, 7, 1.2, 20)     # Library - Bruno
        self.g.add_edge(4, 3, 2.49, 15)    # Library - UC

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="Campus Path Finder",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=15)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Starting Location:", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.start_combo = ttk.Combobox(
            frame,
            values=list(self.node_names.values()),
            state="readonly",
            width=30
        )
        self.start_combo.grid(row=0, column=1, padx=10, pady=10)
        self.start_combo.current(0)

        tk.Label(frame, text="Destination:", font=("Arial", 11)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.end_combo = ttk.Combobox(
            frame,
            values=list(self.node_names.values()),
            state="readonly",
            width=30
        )
        self.end_combo.grid(row=1, column=1, padx=10, pady=10)
        self.end_combo.current(1)

        tk.Label(frame, text="Optimize For:", font=("Arial", 11)).grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.choice_var = tk.IntVar(value=1)

        radio_frame = tk.Frame(frame)
        radio_frame.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        tk.Radiobutton(
            radio_frame,
            text="Shortest Time",
            variable=self.choice_var,
            value=1
        ).pack(anchor="w")

        tk.Radiobutton(
            radio_frame,
            text="Most Accessible Path",
            variable=self.choice_var,
            value=2
        ).pack(anchor="w")

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=15)

        find_button = ttk.Button(
        button_frame,
        text="Find Path",
        command=self.find_path
        )
        
        find_button.grid(row=0, column=0, padx=10)

        clear_button = ttk.Button(
        button_frame,
        text="Clear",
        command=self.clear_output
        )
        clear_button.grid(row=0, column=1, padx=10)

        self.output_text = tk.Text(self.root, height=15, width=65, font=("Courier New", 10))
        self.output_text.pack(padx=15, pady=10)
        self.output_text.config(state="disabled")

    def find_path(self):
        start_name = self.start_combo.get()
        end_name = self.end_combo.get()

        if start_name == end_name:
            messagebox.showwarning("Invalid Input", "Starting location and destination cannot be the same.")
            return

        start = self.name_to_node[start_name]
        end = self.name_to_node[end_name]

        use_access = self.choice_var.get() == 2

        distances, previous = self.g.dijkstra(start, use_access)
        path = self.g.get_path(previous, end)

        self.output_text.config(state="normal")  
        self.output_text.delete("1.0", tk.END)

        if not path:
            self.output_text.insert(tk.END, "No path found.\n")
        else:
            self.output_text.insert(tk.END, "Path Found:\n\n")
            for node in path:
                self.output_text.insert(tk.END, f"{node} - {self.node_names[node]}\n")

            unit = "accessibility score" if use_access else "minutes"
            self.output_text.insert(tk.END, f"\nTotal cost: {distances[end]} {unit}")

        self.output_text.config(state="disabled") 

    def clear_output(self):
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = CampusPathFinderGUI(root)
    root.mainloop()