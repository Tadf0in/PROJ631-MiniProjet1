import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry


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

        self.main_window.datetime_label = tk.Label(self.path_frame, text="Date et heure de départ:")
        self.main_window.datetime_label.pack(pady=5, padx=5, side="left")

        self.main_window.date_entry = DateEntry(self.path_frame, date_pattern='y-mm-dd')
        self.main_window.date_entry.pack(pady=5, padx=5, side="left")
        
        self.main_window.hour_entry = ttk.Combobox(self.path_frame, width=3)
        self.main_window.hour_entry.pack(pady=5, padx=5, side="left")
        self.main_window.hour_entry['values'] = [f"{i:02d}" for i in range(24)]
        self.main_window.hour_entry.set("00")
        
        self.main_window.minute_entry = ttk.Combobox(self.path_frame, width=3)
        self.main_window.minute_entry.pack(pady=5, padx=5, side="left")
        self.main_window.minute_entry['values'] = [f"{i:02d}" for i in range(60)]
        self.main_window.minute_entry.set("00")
        
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
        departure = self.main_window.departure_select.get()
        arrival = self.main_window.arrival_select.get()
        date = self.main_window.date_entry.get_date().strftime('%Y-%m-%d')
        hour = self.main_window.hour_entry.get()
        minute = self.main_window.minute_entry.get()

        datetime_departure = f"{date} {hour}:{minute}"
        
        if not departure or not arrival or not datetime_departure:
            self.main_window.error_message.set("Veuillez remplir tous les champs")
            return
        
        self.main_window.error_message.set("Calcul du trajet en cours...")
        path = self.main_window.network.dijkstra(departure, arrival, date, hour, minute)
        
        if path:
            path_str = ""
            for stop in path:
                path_str += stop.name + " -> "
            path_str = path_str[:-4]
        else:
            path_str = "Aucun chemin"
        self.main_window.error_message.set(path_str)
        