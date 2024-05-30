import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk
import json
import os

SAVE_FILE = 'checklists_state.json'

class ChecklistApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Checklist Application")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.notebook_frame = tk.Frame(self.main_frame)
        self.notebook_frame.pack(side=tk.TOP, fill="x")

        self.notebook = ttk.Notebook(self.notebook_frame)
        self.notebook.pack(side=tk.LEFT, expand=1, fill="both")

        self.add_list_button = tk.Button(self.notebook_frame, text="+", bg="blue", fg="white", command=self.add_new_checklist, width=2, height=1)
        self.add_list_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.checklists = {}
        self.load_data()

        if not self.checklists:
            self.create_new_checklist("Liste 1")
        else:
            for list_name in self.checklists:
                self.add_checklist_tab(list_name)

        self.create_widgets()
        self.populate_checklists()

    def create_new_checklist(self, list_name):
        self.checklists[list_name] = {
            "row_names": ["Ligne 1"],
            "col_names": ["Colonne 1"],
            "data": [[False]]
        }
        self.add_checklist_tab(list_name)

    def create_widgets(self):
        default_font = ("Helvetica", 12)

        self.reset_button = tk.Button(self.main_frame, text="Reset", bg="#D9534F", fg="white", font=default_font, command=self.reset_checklist)
        self.reset_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.modify_list_button = tk.Button(self.main_frame, text="Modifier liste", font=default_font, command=self.modify_list_name)
        self.modify_list_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_list_button = tk.Button(self.main_frame, text="Supprimer liste", bg="#D9534F", fg="white", font=default_font, command=self.delete_current_checklist)
        self.delete_list_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.save_button = tk.Button(self.main_frame, text="Sauvegarder", font=default_font, command=self.save_data)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)

    def populate_checklists(self):
        for list_name in self.checklists:
            self.populate_checklist(list_name)

    def add_checklist_tab(self, list_name):
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text=list_name)
        self.notebook.select(frame)
        self.populate_checklist(list_name)

    def populate_checklist(self, list_name):
        frame = self.get_current_frame(list_name)
        for widget in frame.winfo_children():
            widget.destroy()

        checklist = self.checklists[list_name]
        default_font = ("Helvetica", 12)

        tk.Label(frame, text="", font=default_font).grid(row=0, column=1)
        for j, col_name in enumerate(checklist["col_names"]):
            edit_col_button = tk.Button(frame, text="✎", font=default_font, command=lambda c=j: self.edit_col_name(list_name, c))
            edit_col_button.grid(row=1, column=j+2, sticky="s")
            tk.Label(frame, text=col_name, font=default_font).grid(row=2, column=j+2)

        for i, row_name in enumerate(checklist["row_names"]):
            tk.Label(frame, text=row_name, font=default_font).grid(row=i+3, column=0, padx=(0, 10))
            edit_row_button = tk.Button(frame, text="✎", font=default_font, command=lambda r=i: self.edit_row_name(list_name, r))
            edit_row_button.grid(row=i+3, column=1, sticky="w")

        for i, row in enumerate(checklist["data"]):
            for j, value in enumerate(row):
                if isinstance(value, tk.BooleanVar):
                    value = value.get()
                var = tk.BooleanVar(value=value)
                cb = tk.Checkbutton(frame, variable=var, font=default_font)
                cb.grid(row=i+3, column=j+2)
                checklist["data"][i][j] = var

        for i in range(len(checklist["row_names"])):
            del_row_button = tk.Button(frame, text="X", bg="#D9534F", fg="white", font=default_font, command=lambda r=i: self.del_row(list_name, r))
            del_row_button.grid(row=i+3, column=len(checklist["col_names"])+3, sticky="w")

        for j in range(len(checklist["col_names"])):
            del_col_button = tk.Button(frame, text="X", bg="#D9534F", fg="white", font=default_font, command=lambda c=j: self.del_col(list_name, c))
            del_col_button.grid(row=len(checklist["row_names"])+3, column=j+2, sticky="n")

        add_row_button = tk.Button(frame, text="+", bg="blue", fg="white", font=default_font, command=lambda: self.add_row(list_name))
        add_row_button.grid(row=len(checklist["row_names"])+3, column=0, pady=10)

        add_col_button = tk.Button(frame, text="+", bg="blue", fg="white", font=default_font, command=lambda: self.add_col(list_name))
        add_col_button.grid(row=1, column=len(checklist["col_names"])+3, sticky="n")

    def get_current_frame(self, list_name):
        for idx in range(self.notebook.index("end")):
            if self.notebook.tab(idx, "text") == list_name:
                return self.notebook.nametowidget(self.notebook.tabs()[idx])
        return None

    def add_new_checklist(self):
        new_list_name = simpledialog.askstring("Nom de la nouvelle liste", "Entrez le nom de la nouvelle liste:", parent=self.root)
        if new_list_name:
            if new_list_name not in self.checklists:
                self.create_new_checklist(new_list_name)
            else:
                messagebox.showerror("Erreur", "Une liste avec ce nom existe déjà.")
        self.populate_checklists()

    def modify_list_name(self):
        current_tab = self.notebook.select()
        list_name = self.notebook.tab(current_tab, "text")
        new_list_name = simpledialog.askstring("Modifier le nom de la liste", "Entrez le nouveau nom de la liste:", initialvalue=list_name, parent=self.root)
        if new_list_name:
            if new_list_name not in self.checklists:
                self.checklists[new_list_name] = self.checklists.pop(list_name)
                self.notebook.tab(current_tab, text=new_list_name)
            else:
                messagebox.showerror("Erreur", "Une liste avec ce nom existe déjà.")

    def add_row(self, list_name):
        checklist = self.checklists[list_name]
        new_row_name = simpledialog.askstring("Nom de la nouvelle ligne", "Entrez le nom de la nouvelle ligne:", parent=self.root)
        if not new_row_name:
            new_row_name = f"Ligne {len(checklist['row_names']) + 1}"
        checklist['row_names'].append(new_row_name)
        new_row = [False for _ in range(len(checklist['col_names']))]
        checklist['data'].append(new_row)
        self.populate_checklist(list_name)

    def add_col(self, list_name):
        checklist = self.checklists[list_name]
        new_col_name = simpledialog.askstring("Nom de la nouvelle colonne", "Entrez le nom de la nouvelle colonne:", parent=self.root)
        if not new_col_name:
            new_col_name = f"Colonne {len(checklist['col_names']) + 1}"
        checklist['col_names'].append(new_col_name)
        for row in checklist['data']:
            row.append(False)
        self.populate_checklist(list_name)

    def edit_row_name(self, list_name, row_index):
        checklist = self.checklists[list_name]
        new_row_name = simpledialog.askstring("Modifier le nom de la ligne", "Entrez le nouveau nom de la ligne:", initialvalue=checklist['row_names'][row_index], parent=self.root)
        if new_row_name:
            checklist['row_names'][row_index] = new_row_name
        self.populate_checklist(list_name)

    def edit_col_name(self, list_name, col_index):
        checklist = self.checklists[list_name]
        new_col_name = simpledialog.askstring("Modifier le nom de la colonne", "Entrez le nouveau nom de la colonne:", initialvalue=checklist['col_names'][col_index], parent=self.root)
        if new_col_name:
            checklist['col_names'][col_index] = new_col_name
        self.populate_checklist(list_name)

    def del_row(self, list_name, row_index):
        checklist = self.checklists[list_name]
        del checklist['row_names'][row_index]
        del checklist['data'][row_index]
        self.populate_checklist(list_name)

    def del_col(self, list_name, col_index):
        checklist = self.checklists[list_name]
        del checklist['col_names'][col_index]
        for row in checklist['data']:
            del row[col_index]
        self.populate_checklist(list_name)

    def reset_checklist(self):
        current_tab = self.notebook.select()
        list_name = self.notebook.tab(current_tab, "text")
        self.checklists[list_name] = {
            "row_names": ["Ligne 1"],
            "col_names": ["Colonne 1"],
            "data": [[False]]
        }
        self.populate_checklist(list_name)

    def delete_current_checklist(self):
        current_tab = self.notebook.select()
        list_name = self.notebook.tab(current_tab, "text")
        self.delete_checklist(list_name, self.get_current_frame(list_name))

    def delete_checklist(self, list_name, frame):
        del self.checklists[list_name]
        self.notebook.forget(frame)
        if not self.checklists:
            self.create_new_checklist("Liste 1")

    def save_data(self):
        state = {
            "checklists": {
                list_name: {
                    "row_names": checklist["row_names"],
                    "col_names": checklist["col_names"],
                    "data": [[var.get() if isinstance(var, tk.BooleanVar) else var for var in row] for row in checklist["data"]]
                }
                for list_name, checklist in self.checklists.items()
            }
        }
        with open(SAVE_FILE, 'w') as f:
            json.dump(state, f)

    def load_data(self):
        if not os.path.exists(SAVE_FILE):
            self.create_save_file()
        with open(SAVE_FILE, 'r') as f:
            try:
                state = json.load(f)
                self.checklists = state.get("checklists", {})
                for checklist in self.checklists.values():
                    checklist["data"] = [[tk.BooleanVar(value=value) if isinstance(value, bool) else value for value in row] for row in checklist["data"]]
            except json.JSONDecodeError:
                self.checklists = {}

    def create_save_file(self):
        state = {
            "checklists": {
                "Liste 1": {
                    "row_names": ["Ligne 1"],
                    "col_names": ["Colonne 1"],
                    "data": [[False]]
                }
            }
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
