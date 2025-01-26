import tkinter as tk
from src.classes.Network import Network
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
        # Logic for creating a new file
        pass

    def open_file(self):
        data_folder_path = os.path.join(os.path.dirname(__file__), '../data/')
        subfolders = [f.name for f in os.scandir(data_folder_path) if f.is_dir()]
        folder_name = tk.StringVar()
        folder_name.set(subfolders[0] if subfolders else '')

        def select_folder():
            selected_folder = folder_name.get()
            folder_path = os.path.join(data_folder_path + selected_folder)
            self.main_window.network = Network(folder_path)
            
            lines_listbox = tk.Listbox(self.main_window.root)
            for line in self.main_window.network.lines:
                lines_listbox.insert(tk.END, line)
            lines_listbox.pack()

        popup = tk.Toplevel(self.main_window.root)
        popup.title("Sélectionner un dossier")

        folder_menu = tk.OptionMenu(popup, folder_name, *subfolders)
        folder_menu.pack(side=tk.LEFT)

        def on_select():
            select_folder()
            popup.destroy()

        select_button = tk.Button(popup, text="Ouvrir", command=on_select)
        select_button.pack(side=tk.LEFT)

    def save_file(self):
        # Logic for saving the current file
        pass

    def save_as_file(self):
        # Logic for saving the current file with a new name
        pass