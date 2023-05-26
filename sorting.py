import tkinter as tk
from tkinter import messagebox
import random
import time
import threading

class SortingVisualizer:
    def __init__(self, master):
        self.master = master
        self.master.title("Sorting Visualizer")
        self.master.geometry("800x600")
        
        self.create_widgets()

        self.data = []

        self.sorting = False

    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=600, height=400, bg="white")
        self.canvas.pack(pady=10)
        
        self.options_frame = tk.Frame(self.master)
        self.options_frame.pack(pady=10)
        
        self.size_label = tk.Label(self.options_frame, text="Size:")
        self.size_label.pack(side="left")
        self.size_entry = tk.Entry(self.options_frame, width=10)
        self.size_entry.pack(side="left")
        
        self.speed_label = tk.Label(self.options_frame, text="Speed:")
        self.speed_label.pack(side="left")
        self.speed_entry = tk.Entry(self.options_frame, width=10)
        self.speed_entry.pack(side="left")

        self.graph_type = tk.StringVar()
        self.graph_type.set("Scatter")
        self.graph_type_menu = tk.OptionMenu(self.options_frame, self.graph_type, "Scatter", "Bar", "Stem")
        self.graph_type_menu.pack(side="left")

        self.algorithm = tk.StringVar()
        self.algorithm.set("Selection")
        self.algorithm_menu = tk.OptionMenu(self.options_frame, self.algorithm, "Selection", "Bubble", "Insertion", "Merge", "Quick")
        self.algorithm_menu.pack(side="left")

        self.create_button = tk.Button(self.options_frame, text="Create", command=self.create)
        self.create_button.pack(side="left")
        self.start_button = tk.Button(self.options_frame, text="Start", command=self.start)
        self.start_button.pack(side="left")
        self.stop_button = tk.Button(self.options_frame, text="Stop", command=self.stop)
        self.stop_button.pack(side="left")
        self.reset_button = tk.Button(self.options_frame, text="Reset", command=self.reset)
        self.reset_button.pack(side="left")

    def draw_on_canvas(self, data, type, colors=None, time_interval=0):
        self.canvas.delete("all")
        canvas_width = int(self.canvas['width'])
        canvas_height = int(self.canvas['height'])
        bar_width = canvas_width / (len(data) + 1)
        max_val = max(data)
        
        normalized_data = [i / max_val for i in data]

        if colors is None:
            colors = ["blue" for _ in range(len(data))]

        if type == "Scatter":
            for i, value in enumerate(normalized_data):
                x = i * bar_width + bar_width // 2
                y = canvas_height - value * canvas_height
                self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill=colors[i], outline="")
        elif type == "Bar":
            for i, value in enumerate(normalized_data):
                x1 = i * bar_width
                y1 = canvas_height - value * canvas_height
                x2 = (i + 1) * bar_width
                y2 = canvas_height
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=colors[i], outline="")
        elif type == "Stem":
            for i, value in enumerate(normalized_data):
                x = i * bar_width + bar_width // 2
                y1 = canvas_height
                y2 = canvas_height - value * canvas_height
                self.canvas.create_line(x, y1, x, y2, fill=colors[i])

        self.master.update()
        time.sleep(time_interval)

    def create(self):
        size = self.size_entry.get()
        if not size.isdigit() or int(size) < 1 or int(size) > 11:
            messagebox.showwarning("Invalid Size", "Please enter a valid size between 1 and 10.")
            return
        self.data = random.sample(range(1, 11), int(size))
        self.draw_on_canvas(self.data, self.graph_type.get())

    def start(self):
        if self.sorting: 
            return 
        if not self.data:
            messagebox.showwarning("No Data", "Please create data before starting the sorting.")
            return
        algorithm = self.algorithm.get()
        speed = self.speed_entry.get()
        if not speed.isdigit() or int(speed) < 1 or int(speed) > 11:
            messagebox.showwarning("Invalid Speed", "Please enter a valid speed between 1 and 10.")
            return         
        
        self.sorting = True

        self.sort_thread = threading.Thread(target=self.sort, args=(algorithm,))
        self.sort_thread.start()

    def stop(self):
       self.sorting = False
       self.draw_on_canvas(self.data, self.graph_type.get(), ["blue" for _ in self.data])

    def reset(self):
        self.stop()
        self.data = []
        self.canvas.delete("all")

    def sort(self, algorithm):
        if algorithm == "Selection":
            self.selection_sort()
        elif algorithm == "Bubble":
            self.bubble_sort()
        elif algorithm == "Insertion":
            self.insertion_sort()
        elif algorithm == "Merge":
            self.merge_sort(self.data)
        elif algorithm == "Quick":
            self.quick_sort(self.data, 0, len(self.data) - 1)

    def selection_sort(self):
        n = len(self.data)
        colors = ["red" for _ in range(n)]
        
        for i in range(n):
            if not self.sorting:
                return            
            min_idx = i
            for j in range(i+1, n):
                if self.data[j] < self.data[min_idx]:
                    min_idx = j
            self.data[i], self.data[min_idx] = self.data[min_idx], self.data[i]
            self.draw_on_canvas(self.data, self.graph_type.get(), colors, int(self.speed_entry.get()))

    def bubble_sort(self):
        n = len(self.data)
        colors = ["red" for _ in range(n)]
        
        for i in range(n-1):
            for j in range(n-i-1):
                if not self.sorting:
                    return
                
                if self.data[j] > self.data[j+1]:
                    self.data[j], self.data[j+1] = self.data[j+1], self.data[j]
                self.draw_on_canvas(self.data, self.graph_type.get(), colors, int(self.speed_entry.get()))

    def insertion_sort(self):
        n = len(self.data)
        colors = ["red" for _ in range(n)]
        
        for i in range(1, n):
            if not self.sorting:
                return
            key = self.data[i]
            j = i - 1
            while j >= 0 and self.data[j] > key:
                self.data[j + 1] = self.data[j]
                j -= 1
            self.data[j + 1] = key
            self.draw_on_canvas(self.data, self.graph_type.get(), colors, int(self.speed_entry.get()))

    def merge_sort(self, data):
        if not self.sorting:
            return

        if len(data) > 1:
            mid = len(data) // 2
            left_half = data[:mid]
            right_half = data[mid:]

            self.merge_sort(left_half)
            self.merge_sort(right_half)

            i = j = k = 0

            while i < len(left_half) and j < len(right_half):
                if left_half[i] < right_half[j]:
                    data[k] = left_half[i]
                    i += 1
                else:
                    data[k] = right_half[j]
                    j += 1
                k += 1

            while i < len(left_half):
                data[k] = left_half[i]
                i += 1
                k += 1

            while j < len(right_half):
                data[k] = right_half[j]
                j += 1
                k += 1

            self.draw_on_canvas(self.data, self.graph_type.get(), time_interval=int(self.speed_entry.get()))

    def partition(self, data, low, high):
        i = low - 1
        pivot = data[high]
        
        for j in range(low, high):
            if data[j] < pivot:
                i += 1
                data[i], data[j] = data[j], data[i]
        
        data[i + 1], data[high] = data[high], data[i + 1]
        
        return i + 1

    def quick_sort(self, data, low, high):
        if not self.sorting:
            return
        if low < high:
            pi = self.partition(data, low, high)
            self.quick_sort(data, low, pi - 1)
            self.quick_sort(data, pi + 1, high)

        self.draw_on_canvas(self.data, self.graph_type.get(), time_interval=int(self.speed_entry.get()))

root = tk.Tk()
sorting_visualizer = SortingVisualizer(root)
root.mainloop()