import Colors
import tkinter.ttk as ttk
from tkinter.ttk import *


class Themes():

    def __init__(self):
        self.style = ttk.Style()

    def set_app_light_theme(self):

        self.style.theme_create("theme_light", parent="alt", settings={
            ".": {"configure": {"background": Colors.LIGHT_PURPLE,
                                "foreground": Colors.LIGHT_BLUE,
                                "relief": "flat",
                                "highlightcolor": Colors.LIGHT_BLUE}},

            "TLabel": {"configure": {"foreground": Colors.LIGHT_BLUE,
                                     "padding": 10,
                                     "font": ("Calibri", 12)}},

            "TNotebook": {"configure": {"padding": 5}},
            "TNotebook.Tab": {"configure": {"padding": [25, 5],
                                            "foreground": "white"},
                              "map": {"background": [("selected", Colors.LIGHT_BLUE)],
                                      "expand": [("selected", [1, 1, 1, 0])]}},

            "TCombobox": {"configure": {"selectbackground": Colors.LIGHT_BLUE,
                                        "fieldbackground": "white",
                                        "background": Colors.LIGHT_BLUE,
                                        "foreground": "black"}},

            "TButton": {"configure": {"font": ("Calibri", 13, 'bold'),
                                      "background": "black",
                                      "foreground": Colors.LIGHT_BLUE},
                        "map": {"background": [("active", Colors.LIGHT_BLUE)],
                                "foreground": [("active", 'black')]}},

            "TEntry": {"configure": {"foreground": "black"}},
            "Horizontal.TProgressbar": {"configure": {"background": Colors.LIGHT_BLUE}}
        })
        self.style.theme_use("theme_light")