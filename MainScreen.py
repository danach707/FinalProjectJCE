import DictionaryBuilder as db
import tkinter as tk
from tkinter.ttk import *
import Lists
import Search as search
import re
import Enums
import Themes


class MainScreen():

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Personal Password Dictionary")
        self.root.geometry("600x450")
        self.root.resizable(0, 0)
        #style
        self.style = Themes.Themes()
        self.style.set_app_light_theme()
        # frame search
        self.frame_search = Frame(self.root)
        self.frame_search.grid(row=2)
        # frame questionirre
        self.frame_questionirre = Frame(self.root)
        self.frame_questionirre.grid(row=2)
        # frame buttons
        self.frame_navbar = Frame(self.root)
        self.frame_navbar.grid(row=1)

        self.dictionary = db.DictionaryBuilder(Enums.WORD_MAX_LEN, Enums.WORD_MIN_LEN)
        self.search = search.Search()

    def createScreen(self):
        btn_goto_questionirre = tk.Button(self.frame_navbar, text='Make Dictionary', width=25,
                                         command=lambda: self.goto_questionirre())
        btn_goto_questionirre.grid(row=1, column=0)
        btn_goto_search = tk.Button(self.frame_navbar, text='Search', width=25,
                                         command=lambda: self.goto_search())
        btn_goto_search.grid(row=1, column=1)

        tk.Label(self.root, text="Personal Password Dictionary", fg="#6699ff", font="Tahoma").grid(row=0)
        # ================================dictionary============================

        # ============================questionirre==============================
        self.lbl_questionirre = tk.Label(self.frame_questionirre, text="Questionirre:").grid(row=0)
        # first name
        self.etr_fname = tk.Entry(self.frame_questionirre)
        self.etr_fname.grid(row=1, column=1)
        self.lbl_fname = tk.Label(self.frame_questionirre, text="First Name:", fg="#6699ff", font="Tahoma").grid(row=1, column=0)
        # last name
        self.etr_lname = tk.Entry(self.frame_questionirre)
        self.etr_lname.grid(row=2, column=1)
        self.lbl_lname = tk.Label(self.frame_questionirre, text="Last Name:", fg="#6699ff", font="Tahoma").grid(row=2, column=0)
        # date of birth
        self.etr_dob = tk.Entry(self.frame_questionirre)
        self.etr_dob.grid(row=3, column=1)
        self.lbl_dob = tk.Label(self.frame_questionirre, text="Date of Birth:", fg="#6699ff", font="Tahoma").grid(row=3, column=0)
        # work place
        self.etr_workplace = tk.Entry(self.frame_questionirre)
        self.etr_workplace.grid(row=4, column=1)
        self.lbl_workplace= tk.Label(self.frame_questionirre, text="Work Place:", fg="#6699ff", font="Tahoma").grid(row=4, column=0)
        # job
        self.etr_job = tk.Entry(self.frame_questionirre)
        self.etr_job.grid(row=5, column=1)
        self.lbl_job = tk.Label(self.frame_questionirre, text="Job:", fg="#6699ff", font="Tahoma").grid(row=5, column=0)
        # family
        self.etr_family = tk.Entry(self.frame_questionirre)
        self.etr_family.grid(row=6, column=1)
        self.lbl_family = tk.Label(self.frame_questionirre, text="Family Members:", fg="#6699ff", font="Tahoma").grid(row=6, column=0)
        # college\university
        self.etr_college = tk.Entry(self.frame_questionirre)
        self.etr_college.grid(row=7, column=1)
        self.lbl_college = tk.Label(self.frame_questionirre, text="College/University:", fg="#6699ff", font="Tahoma").grid(row=7, column=0)
        # school
        self.etr_school = tk.Entry(self.frame_questionirre)
        self.etr_school.grid(row=8, column=1)
        self.lbl_school = tk.Label(self.frame_questionirre, text="School Name:", fg="#6699ff", font="Tahoma").grid(row=8, column=0)
        # email
        self.etr_email = tk.Entry(self.frame_questionirre)
        self.etr_email.grid(row=9, column=1)
        self.lbl_email = tk.Label(self.frame_questionirre, text="Email:", fg="#6699ff", font="Tahoma").grid(row=9, column=0)

        # submit button
        btn_make_dict = tk.Button(self.frame_questionirre, text='Make me a dictionary!', width=25,
                                  command=lambda: self.submitQuestionirre())
        btn_make_dict.grid(row=11)
        # =============================search password==========================   ##different window~
        self.etr_pass = tk.Entry(self.frame_search)
        self.etr_pass.grid(row=2)
        btn_search = tk.Button(self.frame_search, text='Search', width=25, command=lambda: self.handleSearch())
        btn_search.grid(row=3)
        self.lbl_res = tk.Label(self.frame_search, text="", fg="#6699ff", font="Tahoma")
        self.lbl_res.grid(row=4)
        # ======================================================================


    def handleSearch(self):
        password = self.etr_pass.get()
        self.search.search(password, self.dictionary.fileName)
        print(self.search.match, self.search.min_mistakes)
        self.lbl_res.config(text="Password: %s\n"
                                 "Result: %s with %d mistakes" % (password, self.search.match, self.search.min_mistakes))
        self.etr_pass.delete(0, len(password))

    def submitQuestionirre(self):
        if self.etr_fname.get() != '':
            self.dictionary.wordList.append(self.etr_fname.get())
        if self.etr_lname.get() != '':
            self.dictionary.wordList.append(self.etr_lname.get())
        if self.etr_dob.get() != '':
            parse = [x.strip() for x in self.etr_dob.get().split('/')]
            self.dictionary.numbersList.extend(parse)
            self.dictionary.wordList.append(self.etr_dob.get())
        if self.etr_workplace.get() != '':
            workplaces = [x.strip() for x in self.etr_workplace.get().split(',')]
            self.dictionary.wordList.extend(workplaces)
        if self.etr_job.get() != '':
            jobs = [x.strip() for x in self.etr_job.get().split(',')]
            self.dictionary.wordList.extend(jobs)
        if self.etr_family.get() != '':
            members = [x.strip() for x in self.etr_family.get().split(',')]
            self.dictionary.wordList.extend(members)
        if self.etr_college.get() != '':
            colleges = [x.strip() for x in self.etr_college.get().split(',')]
            self.dictionary.wordList.extend(colleges)
        if self.etr_school.get() != '':
            schools = [x.strip() for x in self.etr_school.get().split(',')]
            self.dictionary.wordList.extend(schools)
        if self.etr_email.get() != '':
            self.parseEmail()

        # self.dictionary = db.DictionaryBuilder(self.dictionary.wordList, self.dictionary.numbersList, Enums.WORD_MAX_LEN, Enums.WORD_MIN_LEN)
        self.dictionary.buildDictionary()
        self.dictionary.cleanLists()

    def goto_questionirre(self):
        self.frame_search.grid_remove()
        self.frame_questionirre.grid()

    def goto_search(self):
        self.frame_questionirre.grid_remove()
        self.frame_search.grid()

    def parseEmail(self):
        prefix = self.etr_email.get().split("@")
        match = re.findall(r'([a-zA-Z]+)', prefix[0])
        if match:
            self.dictionary.wordList.extend(match)
        match = re.findall(r'([0-9]+)', prefix[0])
        if match:
            self.dictionary.numbersList.extend(match)


if __name__ == '__main__':
    screen = MainScreen()
    screen.createScreen()
    screen.root.mainloop()

