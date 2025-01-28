import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog


class Path:
    def __init__(self, main_window):
        self.main_window = main_window
        
        self.path_frame = tk.Frame(self.main_window.root)
        
        self.main_window.departure_label = tk.Label(self.path_frame, text="Départ:")
        self.main_window.departure_label.pack(pady=5, padx=5, side="left")
        
        self.main_window.departure_select = ttk.Combobox(self.path_frame)
        self.main_window.departure_select.pack(pady=5, padx=5, side="left")
        
        self.main_window.arrival_label = tk.Label(self.path_frame, text="Arrivée:")
        self.main_window.arrival_label.pack(pady=5, padx=5, side="left")
        
        self.main_window.arrival_select = ttk.Combobox(self.path_frame)
        self.main_window.arrival_select.pack(pady=5, padx=5, side="left")
        
        self.main_window.datetime_label = tk.Label(self.path_frame, text="Date heure de départ:")
        self.main_window.datetime_label.pack(pady=5, padx=5, side="left")
        
        self.main_window.datetime_entry = tk.Entry(self.path_frame)
        self.main_window.datetime_entry.pack(pady=5, padx=5, side="left")
        
        self.path_frame.pack(pady=10)
        
        self.algorithm_frame = tk.Frame(self.main_window.root)
        
        self.main_window.algorithm_label = tk.Label(self.algorithm_frame, text="Algorithme:")
        self.main_window.algorithm_label.pack(pady=5, padx=5, side="left")
        
        self.main_window.algorithm_select = ttk.Combobox(self.algorithm_frame)
        self.main_window.algorithm_select.pack(pady=5, padx=5, side="left")
        self.main_window.algorithm_select['values'] = ["Shortest", "Fastest", "Foremost"]
        
        self.main_window.calculate_route_button = tk.Button(self.algorithm_frame, text="Calculer le trajet", command=self.calculate_route)
        self.main_window.calculate_route_button.pack(pady=5, padx=5, side="left")
        
        self.algorithm_frame.pack(pady=10)
        
        
    def calculate_route(self):
        departure = self.main_window.departure_select.get(tk.ACTIVE)
        arrival = self.main_window.arrival_select.get(tk.ACTIVE)
        datetime_departure = self.main_window.datetime_entry.get()
        
        if not departure or not arrival or not datetime_departure:
            self.main_window.error_message.set("Veuillez remplir tous les champs")
            return
        
        # Add logic to calculate the route here
        self.main_window.error_message.set("Calcul du trajet en cours...")
        # Example: self.main_window.network.calculate_route(departure, arrival, datetime_departure)