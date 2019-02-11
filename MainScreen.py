import tkinter as tk
from tkinter import *
import DictionaryBuilder as db
import Lists
import Search as search

class MainScreen():

    def __init__(self):
        self.root = tk.Tk()
        self.frame = Frame(self.root, width=300, height=150)
        self.frame.pack()
        self.dictionary = db.DictionaryBuilder(Lists.words, Lists.numbers, 1000, 6)
        self.search = search.Search()

    def createScreen(self):

        self.root.title("Personal Password Dictionary")
        tk.Label(self.root, text="Personal Password Dictionary", fg="#6699ff", font="Tahoma").pack()
        # ================================dictionary============================
        btn_make_dict = tk.Button(self.root, text='Make me a dictionary!', width=25, command=lambda: self.dictionary.buildDictionary())
        btn_make_dict.pack()
        # =============================search password==========================
        self.etr_pass = tk.Entry()
        self.etr_pass.pack()
        btn_search = tk.Button(self.root, text='Search', width=25, command=lambda: self.handleSearch())
        btn_search.pack()
        self.lbl_res = tk.Label(self.root, text="", fg="#6699ff", font="Tahoma")
        self.lbl_res.pack()
        # ======================================================================

        self.root.mainloop()

    def handleSearch(self):
        password = self.etr_pass.get()
        self.search.search(password, self.dictionary.fileName)
        print(self.search.match, self.search.min_mistakes)
        self.lbl_res.config(text="Password: %s\n"
                                 "Result: %s with %d mistakes" % (password, self.search.match, self.search.min_mistakes))
        self.etr_pass.delete(0, len(password))


if __name__ == '__main__':
    screen = MainScreen()
    screen.createScreen()


