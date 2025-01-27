import tkinter as tk


def add_stop(self, selected_line):
    if not selected_line:
        self.error_message.set("Aucune ligne sélectionnée")
        return
    
    print(selected_line)

    popup = tk.Toplevel(self.root)
    popup.title("Ajouter un arrêt")
    
    label = tk.Label(popup, text="Nom de l'arrêt :")
    label.pack(pady=10)

    stop_name_entry = tk.Entry(popup)
    stop_name_entry.pack(pady=10)

    def save_stop_name():
        stop_name = stop_name_entry.get()
        if stop_name:
            selected_line.addStop(stop_name)
            self.update_stops_listbox()
            popup.destroy()
            self.error_message.set("")
        else:
            self.error_message.set("Le nom de l'arrêt ne peut pas être vide")

    save_button = tk.Button(popup, text="Ajouter", command=save_stop_name)
    save_button.pack(pady=10)
    


def remove_stop(self, selected_line):
    if not selected_line:
        self.error_message.set("Aucune ligne sélectionnée")
        return
    
    selected_stop_index = self.stops_listbox.curselection()
    if not selected_stop_index:
        self.error_message.set("Aucun arrêt sélectionnée")
        return
    selected_stop = selected_line.getAllStopsOnLine()[selected_stop_index[0]]
    
    print(selected_stop)


def move_up_stop(self, selected_line):
    pass


def move_down_stop(self, selected_line):
    pass

