import threading
import tkinter as tk
import main
import os.path
import gensim
import pandas as pd
import queue
import time

from text_cleaning import argument_list
from Skräp.create_model_test import create_model
from counterargument_db import create_dataframe
from bert_encoding import bert_encoding
from bot_response import counter_argument
import bot_response
import counterargument_db
from text_cleaning import informative_words_list


class BotInterface(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        # Create widgets
        self.entry_label = tk.Label(text="Name of file to load:")
        self.entry_filename = tk.Entry(text="trolley")  # TODO change to drop-down list
        self.entry_load = tk.Button(text="Load file", command=self.start)

        self.textCons = tk.Text(width=20,
                                height=8,
                                bg="#17202A",
                                fg="#EAECEE",
                                font="Helvetica 14",
                                padx=5,
                                pady=5)
        self.labelBottom = tk.Label(bg="#ABB2B9", height=10)
        self.entryMsg = tk.Entry(bg="#2C3E50", fg="#EAECEE", font="Helvetica 13")
        self.buttonMsg = tk.Button(text="Send",
                                   font="Helvetica 10 bold",
                                   width=20,
                                   bg="#ABB2B9",
                                   command=self.send_to_bot)
        self.scrollbar = tk.Scrollbar(command=self.textCons.yview)

        # lay the widgets out on the screen.
        self.entry_label.place(relx=0, rely=0.025)
        self.entry_filename.place(relx=0.4, rely=0.025)
        self.entry_load.place(relx=0.8, rely=0.025)

        self.textCons.place(relwidth=0.95, relheight=0.73, rely=0.1)
        self.labelBottom.place(relwidth=1, rely=0.825)
        self.entryMsg.place(relwidth=0.8, relx=0.025, rely=0.9)
        self.buttonMsg.place(relwidth=0.1, relx=0.865, rely=0.9)
        # self.scrollbar.place(relheight=1, relx=0.974)
        self.scrollbar.place(relheight=0.73, relx=0.955, rely=0.1)

        self.scrollbar.config(command=self.textCons.yview)
        self.textCons.config(cursor="arrow")
        self.textCons.config(state=tk.DISABLED)

        self.exit_words = ['bye', 'fuckoff', 'quit', 'exit', 'cya', 'goodbye']
        self.load_config()

        if os.path.isfile('embeddings_df.pkl'):
            self.dataframe = pd.read_pickle('embeddings_df.pkl')
        else:
            if os.path.isfile('Pickles/Trolley.pkl'):
                self.dataframe = pd.read_pickle('Pickles/trolley.pkl')
            else:
                counterargument_db.create_dataframe()
                self.dataframe = pd.read_pickle('Pickles/trolley.pkl')

            bert_encoding(self.dataframe)
            embeddings = pd.read_pickle('embeddings_df.pkl')

        if os.path.isfile('embeddings_df2.pkl'):
            self.dataframe2 = pd.read_pickle('embeddings_df2.pkl')
        else:
            self.dataframe2 = pd.read_pickle('sentiment_dataframe.pkl')
            claims = self.dataframe2['claim']
            word_tokens = []
            for c in claims:
                tokens = informative_words_list(c)
                word_tokens.append(tokens)
            self.dataframe2['word_tokens'] = word_tokens
            pd.to_pickle(self.dataframe2, 'embeddings_df2.pkl')

        # Redirect print:
        bot_response.print = self.write

        # Bind Return to send messages
        # self.bind('<Return>', self.send_to_bot_event)

        # Start bot conversation...
        self.write('BOT: As a bot I am a terrible debater and always agree')

    def load_config(self):
        pass
        # TODO Implement loading and saving a config file

    def load_file(self):
        pass
        # TODO Load the selected file

    def write(self, text, separator=" "):
        self.textCons.config(state=tk.NORMAL)
        if separator == " ":
            self.textCons.insert(tk.END, text + "\n\n")
        else:
            self.textCons.insert(tk.END, text + "\n\n")

        self.textCons.config(state=tk.DISABLED)
        self.textCons.see(tk.END)

    def send_to_bot(self):
        message = self.entryMsg.get()
        # bot_response.print = self.move_print
        if message != "":
            self.write(message)
            self.entryMsg.delete(0, tk.END)

        if message in self.exit_words:
            self.write('BOT: Good talk')
            # TODO Implement shutting down
        else:
            self.queue = queue.Queue()
            ThreadedTask(self.queue, message, self.dataframe2).start()
            self.master.after(100, self.process_queue)

    def send_to_bot_event(self, event):
        self.send_to_bot()

    def move_print(self, text):
        self.write(text)

    def move_input(self, text=""):
        yield self.send_to_bot()

    def start(self):
        pass

    def process_queue(self):
        try:
            msg = self.queue.get(0)
            self.write(f'BOT: {msg}')
        except queue.Empty:
            self.master.after(100, self.process_queue)


class ThreadedTask(threading.Thread):
    def __init__(self, queue, message, dataframe2):
        threading.Thread.__init__(self)
        self.queue = queue
        self.message = message
        self.dataframe2 = dataframe2

    def run(self) -> None:
        response = bot_response.counter_argument(self.message, self.dataframe2)
        self.queue.put(response)


# if this is run as a program (versus being imported),
# create a root window and an instance of our example,
# then start the event loop

if __name__ == "__main__":
    root = tk.Tk()
    BotInterface(root).pack(fill="both", expand=True)
    root.title("A smart chat bot")
    root.geometry("750x800")
    root.mainloop()
