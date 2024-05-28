import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os

SAVE_FILE = 'checklist_state.json'

class ChecklistApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Checklist Application")

        self.row_names = []
        self.col_names = []
        self.data = self.load_data()

        self.calculate_window_size()

        if not self.data or not self.row_names or not self.col_names:
            self.get_initial_names()

        self.create_widgets()
        self.populate_checklist()

    def calculate_window_size(self):
        width = max(600, 150 + len(self.col_names) * 100)
        height = max(300, 150 + len(self.row_names) * 50)
        self.root.geometry(f"{width}x{height}")

    def get_initial_names(self):
        self.first_row_name = simpledialog.askstring("Nom de la première ligne", "Entrez le nom de la première ligne:", parent=self.root)
        self.first_col_name = simpledialog.askstring("Nom de la première colonne", "Entrez le nom de la première colonne:", parent=self.root)
        
        if not self.first_row_name:
            self.first_row_name = "Ligne 1"
        if not self.first_col_name:
            self.first_col_name = "Colonne 1"
        
        self.row_names = [self.first_row_name]
        self.col_names = [self.first_col_name]
        self.data = [[False]]

    def create_widgets(self):
        default_font = ("Helvetica", 12)

        self.table_frame = tk.Frame(self.root)
        self.table_frame.grid(row=0, column=0, padx=10, pady=10)

        self.reset_button = tk.Button(self.root, text="Reset", bg="#D9534F", fg="white", font=default_font, command=self.reset_checklist)
        self.reset_button.grid(row=1, column=0, sticky="ew")

        self.save_button = tk.Button(self.root, text="Sauvegarder", font=default_font, command=self.save_data)
        self.save_button.grid(row=2, column=0, sticky="ew")

    def populate_checklist(self):
        default_font = ("Helvetica", 12)

        for widget in self.table_frame.winfo_children():
            widget.destroy()

        tk.Label(self.table_frame, text="", font=default_font).grid(row=0, column=0)
        for j, col_name in enumerate(self.col_names):
            edit_col_button = tk.Button(self.table_frame, text="✎", font=default_font, command=lambda c=j: self.edit_col_name(c))
            edit_col_button.grid(row=0, column=j+2, sticky="s")
            tk.Label(self.table_frame, text=col_name, font=default_font).grid(row=1, column=j+2)

        for i, row_name in enumerate(self.row_names):
            tk.Label(self.table_frame, text=row_name, font=default_font).grid(row=i+2, column=0, padx=(0, 10))
            edit_row_button = tk.Button(self.table_frame, text="✎", font=default_font, command=lambda r=i: self.edit_row_name(r))
            edit_row_button.grid(row=i+2, column=1, sticky="w")

        for i, row in enumerate(self.data):
            for j, value in enumerate(row):
                if isinstance(value, tk.BooleanVar):
                    value = value.get()
                var = tk.BooleanVar(value=value)
                cb = tk.Checkbutton(self.table_frame, variable=var, font=default_font)
                cb.grid(row=i+2, column=j+2)
                self.data[i][j] = var

        for i in range(len(self.row_names)):
            del_row_button = tk.Button(self.table_frame, text="X", bg="#D9534F", fg="white", font=default_font, command=lambda r=i: self.del_row(r))
            del_row_button.grid(row=i+2, column=len(self.col_names)+3, sticky="w")

        for j in range(len(self.col_names)):
            del_col_button = tk.Button(self.table_frame, text="X", bg="#D9534F", fg="white", font=default_font, command=lambda c=j: self.del_col(c))
            del_col_button.grid(row=len(self.row_names)+2, column=j+2, sticky="n")

        add_row_button = tk.Button(self.table_frame, text="+", bg="blue", fg="white", font=default_font, command=self.add_row)
        add_row_button.grid(row=len(self.row_names)+2, column=0, pady=10)

        add_col_button = tk.Button(self.table_frame, text="+", bg="blue", fg="white", font=default_font, command=self.add_col)
        add_col_button.grid(row=0, column=len(self.col_names)+3, sticky="n")

    def add_row(self):
        new_row_name = simpledialog.askstring("Nom de la nouvelle ligne", "Entrez le nom de la nouvelle ligne:", parent=self.root)
        if not new_row_name:
            new_row_name = f"Ligne {len(self.row_names) + 1}"
        self.row_names.append(new_row_name)

        new_row = [False for _ in range(len(self.col_names))]
        self.data.append(new_row)
        self.calculate_window_size()
        self.populate_checklist()

    def add_col(self):
        new_col_name = simpledialog.askstring("Nom de la nouvelle colonne", "Entrez le nom de la nouvelle colonne:", parent=self.root)
        if not new_col_name:
            new_col_name = f"Colonne {len(self.col_names) + 1}"
        self.col_names.append(new_col_name)

        for row in self.data:
            row.append(False)
        self.calculate_window_size()
        self.populate_checklist()

    def edit_row_name(self, row_index):
        new_row_name = simpledialog.askstring("Modifier le nom de la ligne", "Entrez le nouveau nom de la ligne:", initialvalue=self.row_names[row_index], parent=self.root)
        if new_row_name:
            self.row_names[row_index] = new_row_name
        self.populate_checklist()

    def edit_col_name(self, col_index):
        new_col_name = simpledialog.askstring("Modifier le nom de la colonne", "Entrez le nouveau nom de la colonne:", initialvalue=self.col_names[col_index], parent=self.root)
        if new_col_name:
            self.col_names[col_index] = new_col_name
        self.populate_checklist()

    def del_row(self, row_index):
        del self.row_names[row_index]
        del self.data[row_index]
        self.calculate_window_size()
        self.populate_checklist()

    def del_col(self, col_index):
        del self.col_names[col_index]
        for row in self.data:
            del row[col_index]
        self.calculate_window_size()
        self.populate_checklist()

    def reset_checklist(self):
        self.get_initial_names()
        self.calculate_window_size()
        self.populate_checklist()

    def save_data(self):
        state = {
            "data": [[var.get() if isinstance(var, tk.BooleanVar) else var for var in row] for row in self.data],
            "row_names": self.row_names,
            "col_names": self.col_names
        }
        with open(SAVE_FILE, 'w') as f:
            json.dump(state, f)

    def load_data(self):
        if not os.path.exists(SAVE_FILE):
            self.create_save_file()
        with open(SAVE_FILE, 'r') as f:
            try:
                state = json.load(f)
                self.row_names = state.get("row_names", [])
                self.col_names = state.get("col_names", [])
                return [[value for value in row] for row in state.get("data", [[False]])]
            except json.JSONDecodeError:
                return [[False]]

    def create_save_file(self):
        state = {
            "data": [[False]],
            "row_names": ["Ligne 1"],
            "col_names": ["Colonne 1"]
        }
        with open(SAVE_FILE, 'w') as f:
            json.dump(state, f)

    def on_closing(self):
        self.save_data()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChecklistApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
