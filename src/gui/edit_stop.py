import tkinter as tk


def add_stop(main_window, selected_line):
    if not selected_line:
        main_window.error_message.set("Aucune ligne sélectionnée")
        return

    popup = tk.Toplevel(main_window.root)
    popup.title("Ajouter un arrêt")
    
    label = tk.Label(popup, text="Nom de l'arrêt :")
    label.pack(pady=10)

    stop_name_entry = tk.Entry(popup)
    stop_name_entry.pack(pady=10)

    def save_stop_name():
        stop_name = stop_name_entry.get()
        if stop_name:
            selected_line.addStop(stop_name)
            main_window.stops_listbox.insert(tk.END, stop_name)
            popup.destroy()
            main_window.error_message.set("")
        else:
            main_window.error_message.set("Le nom de l'arrêt ne peut pas être vide")

    save_button = tk.Button(popup, text="Ajouter", command=save_stop_name)
    save_button.pack(pady=10)
    

def remove_stop(main_window, selected_line):
    if not selected_line:
        main_window.error_message.set("Aucune ligne sélectionnée")
        return
    
    selected_stop_index = main_window.stops_listbox.curselection()
    if not selected_stop_index:
        main_window.error_message.set("Aucun arrêt sélectionnée")
        return
    selected_stop = selected_line.getAllStopsOnLine()[selected_stop_index[0]]

    selected_line.removeStop(selected_stop)
    main_window.update_lines_listbox()
    main_window.update_stops_listbox()
    main_window.error_message.set("")


def move_up_stop(main_window, selected_line):
    pass


def move_down_stop(main_window, selected_line):
    pass

