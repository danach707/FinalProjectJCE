import Enums as e
import Search
from kivy.clock import Clock
from kivy.uix.popup import Popup
from functools import partial
import threading
import FIleExplorer as fe

class SearchHandler:

    def __init__(self):
        self.filename = ''

    def set_vars(self, inp_password, progressbar, pass_result, lbl_search_filename):
        self.password = inp_password.text
        self.progressbar = progressbar
        self.pass_result = pass_result
        self.lbl_search_filename = lbl_search_filename
        self.etr_pass = inp_password

    def start_search(self):

        self.pass_result.text = ''
        self.num_lines_in_file = self.get_number_of_lines_in_file(self.filename)
        self.search = Search.Search(self.password, self.filename, self.update_search_progressbar, self.num_lines_in_file)
        Clock.create_trigger(self.update_search_progressbar)

        self.progressbar.max = self.num_lines_in_file
        self.progressbar.value = 0

        search_thread = threading.Thread(target=self.search.search)
        search_thread.start()

    def print_results(self):

        print('self.search.res=', str(self.search.res))

        if self.search.res == e.Error_No_Dictionary or self.num_lines_in_file == -1:
            self.pass_result.text = "[color=#000000][b][size=20]Error, no dictionary found.\n" \
                            "You can create one with the application![/b]"
        elif self.search.res == e.Error_Empty_Password:
            self.pass_result.text = "[color=#000000][b][size=20]Password is empty..[/b]"
        elif self.search.res == e.Password_Not_Found:
            self.pass_result.text = '[color=#29a329][b][size=20]Password is not in the dictionary.[/b]'
        elif self.search.res == e.Password_Found and self.search.min_mistakes == 0:
            self.pass_result.text = '[color=#ff1a1a][b][size=20]Found a match!\n' \
                           'Your password can be hacked with this dictionary.\n' \
                           'We recommend you to change it to something less guessable.[/b]\n'
        elif self.search.res == e.Password_Found and self.search.min_mistakes != 0:
            print('here')
            self.pass_result.text = '[color=#ff9900][b][size=20]Found a partial match!\n' \
                           'Your password is closed by {0:.2f}% to a password in our dictionary.\n' \
                           'Number of different characters: {1}\n' \
                           'Password found in the dictionary: {2}[/b]\n'.format(self.search.calculate_mistakes_percentage(self.password),
                                                                            self.search.min_mistakes,
                                                                            self.search.similar_pass)
        self.etr_pass.text = ''

    def update_search_progressbar(self, val):
        if val != -1:
            self.progressbar.value += val
        else:
            self.progressbar.value = self.num_lines_in_file

        if self.progressbar.value >= self.num_lines_in_file:
            self.print_results()

    # ==================== load file =============================

    def load_file(self, lbl_search_filename, instance):

        content = fe.FileExplorer()
        popup_load_file = Popup(title="Load file",
                                content=content,
                                size_hint=(.9, .9),
                                on_dismiss=partial(self.update_lbl_filename, content, lbl_search_filename))
        popup_load_file.open()

    def update_lbl_filename(self, content, lbl_search_filename, instance):
        self.filename = content.update_lbl_filename
        lbl_search_filename.text = content.update_lbl_filename.split('\\')[-1]

    def get_number_of_lines_in_file(self, path):
        # with open(path, 'r') as f:
        #     count = 0
        #     for line in f:
        #         count += 1
        # return count
        with open(path, "r", encoding="utf-8", errors='ignore') as f:
            return sum(bl.count("\n") for bl in self.blocks(f))

    def blocks(self, files, size=65536):
        while True:
            b = files.read(size)
            if not b: break
            yield b