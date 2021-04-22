import tkinter as tk


class BotInterface(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.entry_label = tk.Label(text="Name of file to load:")
        self.entry_filename = tk.Entry(text="trolley")
        self.entry_load = tk.Button(text="Load file", command=self.load_file)

        # lay the widgets out on the screen.
        self.entry_label.place(relx=0, rely=0.025)
        self.entry_filename.place(relx=0.4, rely=0.025)
        self.entry_load.place(relx=0.8, rely=0.025)

        self.load_config()

        self.textCons = tk.Text(width=20,
                                height=8,
                                bg="#17202A",
                                fg="#EAECEE",
                                font="Helvetica 14",
                                padx=5,
                                pady=5)

        self.textCons.place(relwidth=1, relheight=0.73, rely=0.1)
        self.labelBottom = tk.Label(
                                    bg="#ABB2B9",
                                    height=10)

        self.labelBottom.place(relwidth=1,
                               rely=0.825)

        self.entryMsg = tk.Entry(
                                 bg="#2C3E50",
                                 fg="#EAECEE",
                                 font="Helvetica 13")

        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth=0.8, relx=0.025, rely=0.9)

        # create a Send Button
        self.buttonMsg = tk.Button(
                                   text="Send",
                                   font="Helvetica 10 bold",
                                   width=20,
                                   bg="#ABB2B9",
                                   command=self.enter_row)

        self.buttonMsg.place(relwidth=0.1,  relx=0.865, rely=0.9)
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
