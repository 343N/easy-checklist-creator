import time
import tkinter as tk
from tkinter import ttk
from ctypes import windll


class ChecklistItem:

    def __init__(self, title: str, contents: list[tuple[bool, str]], parent: tk.Frame, onchecked=None):
        self.title = title
        self.container = tk.Frame(parent)
        self.heading = ttk.Label(self.container, text=title, font=(None, 14, "bold"))
        self.heading.pack(anchor="w", pady=(10, 2), padx=10)
        self.onchecked = onchecked

        itemCnt = len(contents)
        self.data = []
        self.numChecked = 0
        
        for checked, item in contents:
            var = tk.BooleanVar(value=1 if checked else 0)
            print(checked, item)
            var.set(checked)
            if (checked):
                self.numChecked += 1

            chk = ttk.Checkbutton(self.container, text=item, variable=var, command=self.checkedItemEvent)
            chk.pack(anchor="w", padx=20)
            self.data.append((var, chk))

            self.container.pack(fill=tk.X, padx=10, pady=5)
        
        if itemCnt == self.numChecked:
            self.doDone()
        else:
            self.doUndone()
    
    def checkedItemEvent(self):
        """Event handler for checkbox state change."""
        self.onchecked() if self.onchecked else None

        self.numChecked = sum(var.get() for var, _ in self.data)
        if self.numChecked == len(self.data):
            self.doDone()
        else:
            self.doUndone()
            

    def isDone(self):
        """Check if all items in this checklist are checked."""
        return self.numChecked == len(self.data)

    def doDone(self):
        # time.sleep(0.1)
        # self.set_opacity(0.9)
        # self.container.config(bg="lightgreen")
        # for var, chk in self.data:
        #     chk.config(foreground="green")
        # self.container.config(background="lightgreen")
        self.heading.config(foreground="green")

    def doUndone(self):
        # time.sleep(0.1)
        # self.set_opacity(1)
        # self.set_opacity(1)
        # self.container.config(background="white")
        # for var, chk in self.data:
        #     chk.config(foreground="black")
        # self.config(background="lightgreen")
        # self.container.config(bg="white")
        self.heading.config(foreground="black")

    

    def set_opacity(self, value: float):
        widget = self.container.winfo_id()
        value = int(255*value) # value from 0 to 1
        wnd_exstyle = windll.user32.GetWindowLongA(widget, -20)
        new_exstyle = wnd_exstyle | 0x00080000  
        windll.user32.SetWindowLongA(widget, -20, new_exstyle)  
        windll.user32.SetLayeredWindowAttributes(widget, 0, value, 2)

    def repack(self):
        """Repack the container to update the layout."""
        self.container.pack_forget()
        self.container.pack(fill=tk.X, padx=10, pady=5)

