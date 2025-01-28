import tkinter as tk
from tkinter import filedialog
from src.classes.Network import Network
from .edit_stop import update_lines_listbox
import os


class Menu:
    def __init__(self, main_window):
        self.main_window = main_window
        self.create_menu()

    def create_menu(self):
        self.main_window.file_menu = tk.Menu(self.main_window.menu_bar, tearoff=0)
        self.main_window.menu_bar.add_cascade(label="Fichier", menu=self.main_window.file_menu)

        self.main_window.file_menu.add_command(label="Nouveau", command=self.new_file)
        self.main_window.file_menu.add_command(label="Ouvrir", command=self.open_file)
        self.main_window.file_menu.add_command(label="Enregistrer", command=self.save_file)
        self.main_window.file_menu.add_command(label="Enregistrer sous", command=self.save_as_file)

    def new_file(self):
        folder_path = filedialog.askdirectory()
        self.main_window.network = Network(folder_path)
        self.main_window.selected_line = None


    def open_file(self):
        data_folder_path = os.path.join(os.path.dirname(__file__), '../data/')
        subfolders = [f.name for f in os.scandir(data_folder_path) if f.is_dir()]
        folder_name = tk.StringVar()
        folder_name.set(subfolders[0] if subfolders else '')

        def select_folder():
            selected_folder = folder_name.get()
            folder_path = os.path.join(data_folder_path + selected_folder)
            self.main_window.network = Network(folder_path)
            self.main_window.selected_line = None
            
            update_lines_listbox(self.main_window)

        popup = tk.Toplevel(self.main_window.root)
        popup.title("Sélectionner un dossier")

        folder_menu = tk.OptionMenu(popup, folder_name, *subfolders)
        folder_menu.pack(side=tk.LEFT)

        def on_select():
            select_folder()
            popup.destroy()

        select_button = tk.Button(popup, text="Ouvrir", command=on_select)
        select_button.pack(side=tk.LEFT)

    def save_file(self, folder_path=None):
        for line in self.main_window.network.lines:
            out = ""
            for stop in line.getAllStopsOnLine():
                out += stop.name + " N "
            out = out[:-3]
        
            out += "\n\n"
            
            for key in ['regular_date_go', 'regular_date_back']:
                for stop_name, dates in line.data[key].items():
                    out += stop_name + " "
                    for date in dates:
                        out += date + " "
                    out = out[:-1]
                    out += "\n"
                out += "\n"
                
            for stop in line.getAllStopsOnLine():
                out += stop.name + " N "
            out = out[:-3]
            
            out += "\n\n"
            
            for key in ['we_holidays_date_go', 'we_holidays_date_back']:
                for stop_name, dates in line.data[key].items():
                    out += stop_name + " "
                    for date in dates:
                        out += date + " "
                    out = out[:-1]
                    out += "\n"
                out += "\n"

            out += line.color
            
            if not folder_path:
                folder_path = self.main_window.network.folder_path
            with open(os.path.join(folder_path, f"{line.name}.txt"), 'w') as file:
                file.write(out) 
                

    def save_as_file(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.save_file(folder_path)