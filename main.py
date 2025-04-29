import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import random
from algo import FCFS, SSTF, SCAN, CSCAN, LOOK, CLOOK  # Import algorithms from algo.py

class AlgorithmPlotter:
    def __init__(self, root):
        self.root = root
        self.algorithms = {"FCFS": FCFS, "SSTF": SSTF, "SCAN": SCAN, "C-SCAN": CSCAN, "LOOK": LOOK, "C-LOOK": CLOOK}
        self.algorithm_names = list(self.algorithms.keys())
        self.current_algorithm = self.algorithm_names[0]

        # Create a larger matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.ax.set_xlabel("Cylinder Number", labelpad=15)
        self.ax.xaxis.set_label_position('top')
        self.ax.xaxis.tick_top()
        self.ax.invert_yaxis()
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])

        # Embed the matplotlib figure in the tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

        # Create input fields and organize them in a grid layout
        input_frame = tk.Frame(root)
        input_frame.pack(side=tk.TOP, pady=10, anchor="w")  # Left-align the frame

        # Algorithm selection
        tk.Label(input_frame, text="Algorithm:").grid(row=0, column=0, padx=5, sticky="w")
        self.algo_selection = ttk.Combobox(input_frame, values=self.algorithm_names, state="readonly", width=15)
        self.algo_selection.set(self.current_algorithm)
        self.algo_selection.grid(row=0, column=1, padx=5, sticky="w")
        self.algo_selection.bind("<<ComboboxSelected>>", self.select_algorithm)

        # Sequence input
        tk.Label(input_frame, text="Sequence:").grid(row=0, column=2, padx=5, sticky="w")
        self.sequence_entry = ttk.Combobox(input_frame, width=30, state="normal")
        self.sequence_entry.grid(row=0, column=3, columnspan=4, padx=5, pady=5, sticky="w")

        # Random sequence generation
        self.random_button = tk.Button(input_frame, text="Random", command=self.generate_random_sequence)
        self.random_button.grid(row=0, column=8, padx=5, pady=5, sticky="w")

        tk.Label(input_frame, text="Sequence size:").grid(row=0, column=6, padx=5, sticky="w")
        self.sequence_size_entry = tk.Entry(input_frame, width=10)
        self.sequence_size_entry.grid(row=0, column=7, padx=5, sticky="w")

        # Direction selection
        tk.Label(input_frame, text="Direction:").grid(row=1, column=0, padx=5, sticky="w")
        self.directions = ttk.Combobox(input_frame, values=['Left', 'Right'], state='readonly', width=10)
        self.directions.set('Left')
        self.directions.grid(row=1, column=1, padx=5, sticky="w")

        # Head input
        tk.Label(input_frame, text="Head:").grid(row=1, column=2, padx=5, sticky="w")
        self.head_entry = tk.Entry(input_frame, width=10)
        self.head_entry.grid(row=1, column=3, padx=5, sticky="w")

        # Disk size input
        tk.Label(input_frame, text="Disk size:").grid(row=1, column=4, padx=5, sticky="w")
        self.size_entry = tk.Entry(input_frame, width=10)
        self.size_entry.insert(0, "200")
        self.size_entry.grid(row=1, column=5, padx=5, sticky="w")

        # Add a button to compute and plot
        self.compute_button = tk.Button(root, text="Compute and Plot", command=self.compute_and_plot)
        self.compute_button.pack(side=tk.TOP, pady=10)

        # Add a label to display the distance below the graph
        self.distance_label = tk.Label(root, text="Distance: ", font=("Arial", 12), fg="green")
        self.distance_label.pack(side=tk.BOTTOM, pady=10)

        # Load sequences from file
        self.sequences = self.load_sequences("sequences.txt")
        self.sequence_entry['values'] = self.sequences  # Set initial dropdown values

    def load_sequences(self, file_path):
        try:
            with open(file_path, "r") as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            return []

    def select_algorithm(self, event):
        self.current_algorithm = self.algo_selection.get()

    def generate_random_sequence(self):
        try:
            size = int(self.sequence_size_entry.get())
            disk_size = int(self.size_entry.get())
            random_sequence = [random.randint(0, disk_size - 1) for _ in range(size)]
            
            # Set the first value as the head
            self.head_entry.delete(0, tk.END)
            self.head_entry.insert(0, random_sequence[0])
            
            # Set the rest of the values as the sequence
            self.sequence_entry.set(','.join(map(str, random_sequence[1:])))
        except ValueError:
            tk.messagebox.showerror("Input Error", "Please enter valid numeric values for sequence size and disk size.")

    def compute_and_plot(self):
        sequence = self.sequence_entry.get()
        head = self.head_entry.get()

        try:
            if sequence not in self.sequences:
                self.update_sequences('sequences.txt', self.sequence_entry.get())
            sequence = list(map(int, sequence.split(',')))
            head = int(head)
            direction = self.directions.get()
            disk_size = int(self.size_entry.get())

            algorithm = self.algorithms[self.current_algorithm]
            distance, memory = algorithm(sequence, head, direction, disk_size)

            # Update the distance label
            self.distance_label.config(text=f"Distance: {distance}")

            self.plot_algorithm(memory, self.current_algorithm)

        except ValueError:
            tk.messagebox.showerror("Input Error", "Please enter valid numeric values for sequence and head.")

    def update_sequences(self, file_path, new_sequence):
        try:
            with open(file_path, 'w') as file:
                self.sequences.append(new_sequence)
                file.write('\n'.join(self.sequences))
        except Exception as e:
            print(f"An error occurred while updating sequences: {e}")

    def plot_algorithm(self, memory, algorithm_name):
        self.ax.clear()
        steps = list(range(1, len(memory) + 1))

        self.ax.plot(memory, steps, marker='o', label=algorithm_name)
        self.ax.set_xticks(memory)
        self.ax.set_xticklabels(memory, rotation=45, fontsize=8)
        self.ax.set_yticks(steps)
        self.ax.set_yticklabels(steps, fontsize=8)


        self.ax.set_title(f"Disk Scheduling: {algorithm_name}")
        self.ax.set_xlabel("Cylinder Number", labelpad=15)
        self.ax.set_ylabel("Step")
        self.ax.xaxis.set_label_position('top')
        self.ax.xaxis.tick_top()
        self.ax.invert_yaxis()
        self.ax.legend()
        self.ax.grid(True)
        self.fig.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Disk Scheduling Visualization")
    plotter = AlgorithmPlotter(root)
    root.mainloop()