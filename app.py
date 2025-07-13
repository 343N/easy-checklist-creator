import yaml
import tkinter as tk
from list import ChecklistItem

from tkinter import ttk, simpledialog

DATA_FILE = "checklist_state.txt"


class ChecklistApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.items = []
        self.checklist_items = []
        self.title("Checklist App")
        self.geometry("400x500")
        self.protocol("WM_DELETE_WINDOW", self.onclose)
        self.item_container = None
        self.canvas = None

        self._build_ui()

    def _build_ui(self):

        # Create a canvas with scrollbar in case of many items
        container = tk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True)
        # self.countContainer = ttk.Frame(container)
        # self.countContainer.pack(fill=tk.X, padx=10, pady=10)
        # self.countLabel = ttk.Label(self.canvas, text="Complete: 0/0")
        self.canvas = tk.Canvas(container)
        canvas = self.canvas
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        self.item_container = scrollable_frame

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=False)
        scrollbar.pack(side="right", fill="y")
        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )        
    
        config_file = "config.yaml"
        try:
            with open(config_file, "r") as file:
                config = yaml.safe_load(file)
                self.checklist_items = config.get("checklist-items", [])
        except FileNotFoundError:
            print(f"Configuration file '{config_file}' not found. Using default items.")
            self.checklist_items = ["Item 1", "Item 2", "Item 3"]

        self.load_data(scrollable_frame)
        if not self.items:
            contents = [(False, items) for items in self.checklist_items]
            self.items.append(ChecklistItem("Example", contents, scrollable_frame, self.save_data))

        self.reverse_items()
        
        # Button to print selected items
        btn = ttk.Button(self, text="Add Item", command=self._show_selected)
        btn.pack(pady=10)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")


    def load_data(self, parent):
        # Load data from a file or other source if needed
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    title, contents = line.strip().split("|")
                    items = contents.split("\t")
                    contents = []
                    for item in items:
                        text, checked = item.split("²")
                        contents.append((checked == "True", text))
                    
                    self.items.append(ChecklistItem(title, contents, parent, self.save_data))

        
        except FileNotFoundError:
            print(f"Data file '{DATA_FILE}' not found. Starting with empty checklist.")
        


    def save_data(self):
        # Save the state of checkboxes to a file or process them as needed
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            for item in self.items:
                f.write(item.title + "|")

                for i, (var, chk) in enumerate(item.data):
                    f.write(f"{chk.cget('text')}²{var.get()}")
                    if i != len(item.data) - 1:
                        f.write("\t")
                f.write("\n")
        print("Data saved successfully.")

    def onclose(self):
        self.save_data()
        self.destroy()

    def reverse_items(self):
        """Reverse the order of items in the checklist."""
        self.items.reverse()
        for item in self.items:
            item.repack()
        self.items.reverse()

    def _show_selected(self):
        user_input = simpledialog.askstring("Add Item", "Enter item name:")
        if user_input is not None:
            contents = [(False, items) for items in self.checklist_items]
            self.reverse_items()
            self.items.append(ChecklistItem(user_input, contents,self.item_container))
            self.reverse_items()



if __name__ == "__main__":
    app = ChecklistApp()
    app.mainloop()
