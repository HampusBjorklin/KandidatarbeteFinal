import tkinter as tk


class BotInterface(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.entry_frame = tk.Frame()
        self.entry_frame.pack(fill=tk.X, expand=True)

        self.console_entry_frame = tk.Frame()
        self.console_entry_frame.pack(fill=tk.X, side=tk.BOTTOM, expand=True)

        self.entry_label = tk.Label(self.entry_frame, text="Name of file to load:")
        self.entry_filename = tk.Entry(self.entry_frame, text="trolley")
        self.entry_load = tk.Button(self.entry_frame, text="Load file", command=self.load_file)

        # lay the widgets out on the screen.
        self.entry_label.pack(side=tk.LEFT, expand=True)
        self.entry_filename.pack(side=tk.LEFT, expand=True)
        self.entry_load.pack(side=tk.LEFT, expand=True)

        self.load_config()

        self.textCons = tk.Text(width=20,
                                height=8,
                                bg="#17202A",
                                fg="#EAECEE",
                                font="Helvetica 14",
                                padx=5,
                                pady=5)

        self.textCons.pack(fill=tk.X)
        self.labelBottom = tk.Label(self.console_entry_frame,
                                    bg="#ABB2B9",
                                    height=80)

        self.labelBottom.place(relwidth=1,
                               rely=0.825)

        self.entryMsg = tk.Entry(self.console_entry_frame,
                                 bg="#2C3E50",
                                 fg="#EAECEE",
                                 font="Helvetica 13")

        # place the given widget
        # into the gui window
        self.entryMsg.pack(side=tk.LEFT)

        # create a Send Button
        self.buttonMsg = tk.Button(self.console_entry_frame,
                                   text="Send",
                                   font="Helvetica 10 bold",
                                   width=20,
                                   bg="#ABB2B9",
                                   command= self.enter_row)

        self.buttonMsg.pack(side=tk.LEFT)
        self.textCons.config(cursor="arrow")

        # create a scroll bar
        scrollbar = tk.Scrollbar(self.textCons)

        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=tk.DISABLED)

    def load_config(self):
        pass
        # TODO Implement loading and saving a config file

    def load_file(self):
        pass
        # TODO Load the selected file

    def write(self, text):
        self.textCons.config(state=tk.NORMAL)
        self.textCons.insert(tk.END,
                             text + "\n\n")

        self.textCons.config(state=tk.DISABLED)
        self.textCons.see(tk.END)

    def enter_row(self):
        message = self.entryMsg

# if this is run as a program (versus being imported),
# create a root window and an instance of our example,
# then start the event loop

if __name__ == "__main__":
    root = tk.Tk()
    BotInterface(root).pack(fill="both", expand=True)
    root.title("A smart chat bot")
    root.geometry("500x500")
    root.mainloop()
