import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from algo import FCFS, SSTF, SCAN, CSCAN, LOOK, CLOOK  # Import algorithms from algo.py

class AlgorithmPlotter:
    def __init__(self, root):
        self.root = root
        self.algorithms = {"FCFS": FCFS, "SSTF": SSTF, "SCAN": SCAN, "C-SCAN": CSCAN, "LOOK": LOOK, "C-LOOK": CLOOK}  # Add more algorithms here as needed
        self.algorithm_names = list(self.algorithms.keys())
        self.current_algorithm = self.algorithm_names[0]

        # Create a larger matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(10, 6))  # Increase figure size
        self.ax.set_xlabel("Cylinder Number", labelpad=15)
        self.ax.set_ylabel("Step")
        self.ax.xaxis.set_label_position('top')  # Move x-axis label to the top
        self.ax.xaxis.tick_top()  # Move x-axis ticks to the top
        self.ax.invert_yaxis()  # Invert the y-axis to match the step order

        # Embed the matplotlib figure in the tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Create a dropdown menu
        self.dropdown = ttk.Combobox(root, values=self.algorithm_names, state="readonly")
        self.dropdown.set(self.current_algorithm)  # Set default value
        self.dropdown.pack(side=tk.TOP, pady=10)
        self.dropdown.bind("<<ComboboxSelected>>", self.select_algorithm)

        # Create input fields for sequence and head
        input_frame = tk.Frame(root)
        input_frame.pack(side=tk.TOP, pady=10)

        tk.Label(input_frame, text="Sequence (comma-separated):").grid(row=0, column=0, padx=5)
        self.sequence_entry = tk.Entry(input_frame, width=30)
        self.sequence_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Head:").grid(row=1, column=0, padx=5)
        self.head_entry = tk.Entry(input_frame, width=10)
        self.head_entry.grid(row=1, column=1, padx=5)

        # Add a button to compute and plot
        self.compute_button = tk.Button(root, text="Compute and Plot", command=self.compute_and_plot)
        self.compute_button.pack(side=tk.TOP, pady=10)

    def select_algorithm(self, event):
        self.current_algorithm = self.dropdown.get()  # Update the selected algorithm

    def compute_and_plot(self):
        # Get input values
        sequence = self.sequence_entry.get()
        head = self.head_entry.get()

        try:
            # Parse inputs
            sequence = list(map(int, sequence.split(',')))
            head = int(head)

            # Get the selected algorithm
            algorithm = self.algorithms[self.current_algorithm]

            # Compute the result
            distance, memory = algorithm(sequence, head)

            # Plot the result
            self.plot_algorithm(memory, self.current_algorithm)

        except ValueError:
            tk.messagebox.showerror("Input Error", "Please enter valid numeric values for sequence and head.")

    def plot_algorithm(self, memory, algorithm_name):
        self.ax.clear()
        steps = list(range(1, len(memory) + 1))  # Step numbers

        # Plot the points
        self.ax.plot(memory, steps, marker='o', label=algorithm_name)

        # Set x-ticks to match the cylinder values
        self.ax.set_xticks(memory)
        self.ax.set_xticklabels(memory, rotation=45, fontsize=8)  # Rotate for better visibility

        # Set graph properties
        self.ax.set_title(f"Disk Scheduling: {algorithm_name}")
        self.ax.set_xlabel("Cylinder Number", labelpad=15)
        self.ax.set_ylabel("Step")
        self.ax.xaxis.set_label_position('top')  # Move x-axis label to the top
        self.ax.xaxis.tick_top()  # Move x-axis ticks to the top
        self.ax.invert_yaxis()  # Invert the y-axis to match the step order
        self.ax.legend()
        self.ax.grid(True)
        self.fig.tight_layout()  # Adjust layout to avoid overlaps
        self.canvas.draw()

if __name__ == "__main__":
    # Create the tkinter root window
    root = tk.Tk()
    root.title("Disk Scheduling Visualization")

    # Create the AlgorithmPlotter
    plotter = AlgorithmPlotter(root)

    # Run the tkinter main loop
    root.mainloop()