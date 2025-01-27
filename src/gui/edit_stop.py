import tkinter as tk
from tkinter import colorchooser


def update_lines_listbox(main_window):
    if not main_window.network:
        main_window.error_message.set("Aucun réseau chargé")
        return

    main_window.lines_listbox.delete(0, tk.END)
    for line in main_window.network.lines:
        main_window.lines_listbox.insert(tk.END, line.name)
    
    main_window.error_message.set("")
    main_window.stops_listbox.delete(0, tk.END)


def update_stops_listbox(main_window, event=None):
    selected_line_index = main_window.lines_listbox.curselection()
    if selected_line_index:
        selected_line_index = selected_line_index[0]
    elif main_window.selected_line:
        selected_line_index = main_window.network.lines.index(main_window.selected_line)
    else:
        return
        
    main_window.selected_line = main_window.network.lines[selected_line_index]
    main_window.stops_listbox.delete(0, tk.END)
    for stop in main_window.selected_line.getAllStopsOnLine():
        main_window.stops_listbox.insert(tk.END, stop.name)
    
    main_window.color_frame.config(bg=main_window.selected_line.color)
    main_window.stops_listbox.selection_clear(0, tk.END)


def change_line_color(main_window, event=None):
    selected_line_index = main_window.lines_listbox.curselection()
    if not selected_line_index:
        main_window.error_message.set("Aucune ligne sélectionnée")
        return

    selected_line = main_window.network.lines[selected_line_index[0]]
    new_color = colorchooser.askcolor()[1]
    if new_color:
        selected_line.color = new_color
        main_window.color_frame.config(bg=new_color)
        main_window.error_message.set("")


def verif_selected(main_window, selected_line) -> object:
    if not selected_line:
        main_window.error_message.set("Aucune ligne sélectionnée")
        return
    
    selected_stop_index = main_window.stops_listbox.curselection()
    if not selected_stop_index:
        main_window.error_message.set("Aucun arrêt sélectionnée")
        return
    selected_stop = selected_line.getAllStopsOnLine()[selected_stop_index[0]]
    
    return selected_stop


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
            selected_line.addStop(stop_name, date={})
            update_stops_listbox(main_window)
            popup.destroy()
            main_window.error_message.set("")
        else:
            main_window.error_message.set("Le nom de l'arrêt ne peut pas être vide")

    save_button = tk.Button(popup, text="Ajouter", command=save_stop_name)
    save_button.pack(pady=10)
    

def remove_stop(main_window, selected_line):
    selected_stop = verif_selected()
    if not selected_stop:
        return

    selected_line.removeStop(selected_stop)
    if selected_line.start == None:
        update_lines_listbox(main_window)
    update_stops_listbox(main_window)
    main_window.error_message.set("")


def move_up_stop(main_window, selected_line):
    selected_stop = verif_selected()
    if not selected_stop:
        return

    selected_line.moveUpStop(selected_stop)
    update_stops_listbox(main_window)
    main_window.error_message.set("")
    

def move_down_stop(main_window, selected_line):
    selected_stop = verif_selected()
    if not selected_stop:
        return

    selected_line.moveDownStop(selected_stop)
    update_stops_listbox(main_window)
    main_window.error_message.set("")


def edit_date_stop(main_window, selected_line):
    selected_stop = verif_selected()
    if not selected_stop:
        return
    
    popup = tk.Toplevel(main_window.root)
    popup.title("Modifier les horaires de l'arrêt")

    for i, (key, value) in enumerate(selected_stop.date[selected_line].items()):
        label = tk.Label(popup, text=key)
        label.grid(row=0, column=i+1, padx=10, pady=10)

        entry = tk.Entry(popup)
        entry.insert(0, value)
        entry.grid(row=1, column=i+1, padx=10, pady=10)
        entry.key = key

    def save_dates():
        for widget in popup.winfo_children():
            if isinstance(widget, tk.Entry):
                selected_stop.date[selected_line][widget.key] = widget.get()
        update_stops_listbox(main_window)
        popup.destroy()
        main_window.error_message.set("")

    save_button = tk.Button(popup, text="Enregistrer", command=save_dates)
    save_button.grid(row=2, columnspan=len(selected_stop.date[selected_line]), pady=10)