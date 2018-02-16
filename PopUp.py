# This file can be used to create a pop up window with a certain style
import tkinter as tk
from tkinter import ttk

class PopUp:
    """
    This class can be used to create a pop up window in a certain style
    """
    def __init__(self):
        self.large_font = ("Verdana", 12)
        self.normal_font = ("Courier", 10)
        self.small_font = ("Helvetica", 8)

    def pop_up_normal(self, title, msg):
        """
        This will show a normal style popup window.
        :param msg: The message you want to show in the popup window
        :param title: The title of the popup window
        """
        popup = tk.Tk()
        popup.wm_title(title)
        label = ttk.Label(popup, text=msg, font=self.normal_font)
        label.pack(side="top", fill="x", pady=10)
        button = ttk.Button(popup, text="Close", command=popup.destroy)
        button.pack()
        popup.mainloop()
