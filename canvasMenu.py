import tkinter as tk

import game


LARGE_FONT = ("Verdana", 12)

class GameFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        menu_frame = tk.Frame(self)

        button0 = tk.Button(menu_frame, text="Main Menu",
                            command=lambda: controller.show_frame(game.top_menu[0]))
        button0.pack(side=tk.LEFT)


        button1 = tk.Button(menu_frame, text="System Data",
                            command=lambda: controller.show_frame(game.top_menu[1]))
        button1.pack(side=tk.LEFT)


        button2 = tk.Button(menu_frame, text="Faction Data",
                    command=lambda: controller.show_frame(game.top_menu[2]))
        button2.pack(side=tk.LEFT)

        menu_frame.pack(side=tk.TOP)

