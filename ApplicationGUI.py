from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.graphics import Rectangle
from kivy.uix.slider import Slider
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.progressbar import ProgressBar
from functools import partial
import DictionaryBuilder as db
import Search
import LinkedInScraper as ls
import FacebookScraper as fs
import Enums as e
from kivy.config import Config
from kivy.clock import Clock

import Questionnaire_Handler as qh
import Dictionary_Handler as dh
import List_Box_Handler as lbh
import FIleExplorer as fe

images_dir = './Images'

class MyDictionary(App):

    savefile = ObjectProperty(None)

    def build(self):

        Config.set('kivy', 'window_icon', '{0}/favicon.png'.format(images_dir))

        dictionary = db.DictionaryBuilder()
        self.qhandler = qh.Questionnaire_Handler()
        self.dictionaryhandler = dh.DictionaryHandler()

        # ============== root layout ==============
        root = BoxLayout(orientation='vertical', size=(800, 800))
        with root.canvas.before:
            self.root_rect = Rectangle(
                source='{0}/background-dict.jpg'.format(images_dir),
                allow_strech=True,
                keep_ratio=True,
                size=root.size,
                size_hint=(1, 1),
                pos=root.pos
            )
        root.bind(pos=self.update_root_rect, size=self.update_root_rect)

        # ============== nav bar ==============

        lay_nav = BoxLayout(orientation='horizontal', size_hint=(1, .1))

        btn_nav_search = Button(text='[b]Search Dictionary[/b]',
                                size_hint=(1, 1),
                                markup=True,
                                font_size=20,
                                background_normal='{0}/button_nav.png'.format(images_dir))

        btn_nav_create_dict = Button(text='[b]Create Dictionary[/b]',
                                     size_hint=(1, 1),
                                     markup=True,
                                     font_size=20,
                                     background_normal='{0}/button_nav.png'.format(images_dir))

        lay_nav.add_widget(btn_nav_search)
        lay_nav.add_widget(btn_nav_create_dict)

        # ============== container ==============

        lay_container = BoxLayout(orientation='vertical', size_hint=(1, .9), padding=[20, 20])

        # ============== search the password in the dictionary ==============
        lay_search = BoxLayout(orientation='vertical', padding=[10, 10], spacing=10)
        lay_search_load = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, .15))
        lay_search_btn_filename = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, .1))

        lbl_search_header = Label(text='[b][size=15][color=4d4d4d]Enter your password and we will check if it is in the dictionary builded for you.[/size]'
                                       '\nDont worry! We do not store your passwords or using them in any way.[/b]',
                                  size_hint=(1, .2),
                                  markup=True,
                                  )

        inp_pass = TextInput(text='',
                             size_hint=(.6, 1),
                             hint_text='Your password here',
                             font_size=15,
                             password=True,
                             padding_y=15
                             )

        btn_load_file = Button(text='[b][color=4d4d4d]Load file[/b]',
                            size_hint=(.2, 1),
                            markup=True,
                            background_normal='{0}/fbli_search_button.png'.format(images_dir),
                            background_down='{0}/fbli_search_button_back.png'.format(images_dir)
                            )
        btn_search = Button(text='[b][color=4d4d4d]Search[/b]',
                            size_hint=(1, 1),
                            markup=True,
                            background_normal='{0}/fbli_search_button.png'.format(images_dir),
                            background_down='{0}/fbli_search_button_back.png'.format(images_dir)
                            )

        self.lbl_search_filename = Label(text='',
                                size_hint=(1, 1),
                                color=(77, 77, 77),
                                markup=True
                                )

        lbl_pass_result = Label(text='',
                                size_hint=(1, .8),
                                markup=True
                                )
        with lbl_pass_result.canvas:
            self.pass_result_rect = Rectangle(
                                    size=lbl_pass_result.size,
                                    pos=lbl_pass_result.pos,
                                    allow_strech=True,
                                    keep_ratio=True,
                                    source='{0}/search_answer.png'.format(images_dir)
                                    )
        lbl_pass_result.bind(pos=self.update_pass_result_rect,
                             size=self.update_pass_result_rect)

        self.pb_search = ProgressBar(max=100, size_hint=(1, .1))

        btn_search.bind(on_press=partial(self.handle_search, lbl_pass_result, inp_pass))
        btn_load_file.bind(on_press=self.load_file)

        lay_search_load.add_widget(inp_pass)
        lay_search_load.add_widget(btn_load_file)

        lay_search_btn_filename.add_widget(btn_search)
        lay_search_btn_filename.add_widget(self.lbl_search_filename)

        lay_search.add_widget(lbl_search_header)
        lay_search.add_widget(lay_search_load)
        lay_search.add_widget(lay_search_btn_filename)
        lay_search.add_widget(self.pb_search)
        lay_search.add_widget(lbl_pass_result)

        # ============== create a dictionary ==============

        # dict layout:
        lay_dict = BoxLayout(orientation='horizontal', spacing=10)

        # buttons and list layouts:
        lay_dict_btns = BoxLayout(orientation='vertical', padding=[30, 30], spacing=10)
        lay_dict_list = BoxLayout(orientation='vertical', padding=[10, 10], spacing=10)
        with lay_dict_list.canvas:
            self.wordlist_rect = Rectangle(
                                    size=lay_dict_list.size,
                                    pos=lay_dict_list.pos,
                                    allow_strech=True,
                                    keep_ratio=True,
                                    source='{0}/wordlist.png'.format(images_dir)
                                )

        lay_dict_list.bind(pos=self.update_wordlist_rect, size=self.update_wordlist_rect)

        # list:
        lay_dict_list.add_widget(Label(text='[b][color=4d4d4d]Current list:[/b]',
                                       size_hint=(1, .1),
                                       markup=True,
                                       font_size=18
                                       ))
        lbl_list_box = Label(text='No Words in the list',
                             size_hint=(1, 1)
                             )
        btn_clean_list = Button(text='Clean List',
                                size_hint=(1, .1),
                                on_press=partial(self.clean_list, dictionary, lbl_list_box)
                                )

        lay_dict_list.add_widget(lbl_list_box)
        lay_dict_list.add_widget(btn_clean_list)

        # buttons:
        btn_calc_dict = Button(text='[b][color=4d4d4d]Make me a dictionary![/b]',
                               size_hint=(1, .2),
                               markup=True,
                               font_size=20,
                               background_normal='{0}/make_me_dictionary.png'.format(images_dir),
                               background_down='{0}/make_me_dictionary_back.png'.format(images_dir)
                               )
        btn_calc_dict.bind(on_press=partial(self.dictionaryhandler.popup_dictionary, dictionary))

        btn_open_quest = Button(text='[b][color=4d4d4d]Questionnaire[/b]',
                                size_hint=(1, .1),
                                markup=True,
                                font_size=15,
                                background_normal='{0}/questionnaire_button.png'.format(images_dir),
                                background_down='{0}/questionnaire_button_back.png'.format(images_dir))
        btn_open_quest.bind(on_press=partial(self.qhandler.questionnaire, dictionary, lbl_list_box))

        btn_linkedin_search = Button(text='[b][color=4d4d4d]LinkedIn Search[/b]',
                                     size_hint=(1, .1),
                                     markup=True,
                                     font_size=15,
                                     background_normal='{0}/li_search_button.png'.format(images_dir),
                                     background_down='{0}/li_search_button_back.png'.format(images_dir))

        btn_linkedin_search.bind(on_press=partial(self.web_scrap,
                                                  dictionary,
                                                  lbl_list_box,
                                                  "LinkedIn profile URL:\n"
                                                  "Example: https://www.linkedin.com/in/<PROFILE NAME>/",
                                                  e.LinkedIn_Search))

        btn_facebook_search = Button(text='[b][color=4d4d4d]Facebook Search[/b]',
                                     size_hint=(1, .1),
                                     markup=True,
                                     font_size=15,
                                     background_normal='{0}/fb_search_button.png'.format(images_dir),
                                     background_down='{0}/fb_search_button_back.png'.format(images_dir))
        btn_facebook_search.bind(on_press=partial(self.web_scrap,
                                                  dictionary,
                                                  lbl_list_box,
                                                  "Facebook profile URL:\n"
                                                  "Example: https://www.facebook.com/<PROFILE NAME>/",
                                                  e.Facebook_Search))

        lay_dict_btns.add_widget(btn_facebook_search)
        lay_dict_btns.add_widget(btn_linkedin_search)
        lay_dict_btns.add_widget(btn_open_quest)
        lay_dict_btns.add_widget(btn_calc_dict)

        # adding all to the dict layout:
        lay_dict.add_widget(lay_dict_btns)
        lay_dict.add_widget(lay_dict_list)

        # =============================================
        # bind nav bar function
        btn_nav_search.bind(on_press=partial(self.navigate, lay_container, lay_search, lay_dict))
        btn_nav_create_dict.bind(on_press=partial(self.navigate, lay_container, lay_dict, lay_search))

        # add widgets to the root layout
        lay_container.add_widget(lay_dict)
        root.add_widget(lay_nav)
        root.add_widget(lay_container)
        return root

    # ==================== load file =============================

    def load_file(self, instance):

        content = fe.FileExplorer()
        popup_load_file = Popup(title="Load file",
                                content=content,
                                size_hint=(0.9, 0.9),
                                on_dismiss=partial(self.update_lbl_filename, content))
        popup_load_file.open()

    def update_lbl_filename(self, content, instance):
        self.lbl_search_filename.text = content.update_lbl_filename.split('\\')[-1]

    # ======================= update rects =======================

    def update_root_rect(self, instance, value):
        self.root_rect.pos = instance.pos
        self.root_rect.size = instance.size

    def update_wordlist_rect(self, instance, value):
        self.wordlist_rect.pos = instance.pos
        self.wordlist_rect.size = instance.size

    def update_pass_result_rect(self, instance, value):
        self.pass_result_rect.pos = instance.pos
        self.pass_result_rect.size = instance.size

    # =============================================================

    def clean_list(self, dictionary, lbl_list_box, instance):
        dictionary.lists.cleanLists()
        lbh.printto_lbllist(None, lbl_list_box)

    def handle_search(self, lbl_res, etr_pass, instance):

        password = etr_pass.text
        s = Search.Search(password, self.lbl_search_filename.text, self.update_search_progressbar)
        update_bar = Clock.create_trigger(self.update_search_progressbar)
        self.num_lines_in_file = self.get_number_of_lines_in_file(self.lbl_search_filename.text)

        res = s.search()

        if res == e.Error_No_Dictionary or self.num_lines_in_file == -1:
            lbl_res.text = "[color=#000000][b][size=20]Error, no dictionary found.\n" \
                            "You can create one with the application![/b]"
        elif res == e.Error_Empty_Password:
            lbl_res.text = "[color=#000000][b][size=20]Password is empty..[/b]"
        elif res == e.Password_Not_Found:
            lbl_res.text = '[color=#29a329][b][size=20]Password is not in the dictionary.[/b]'
        elif res == e.Password_Found and s.min_mistakes == 0:
            lbl_res.text = '[color=#ff1a1a][b][size=20]Found a match!\n' \
                           'Your password can be hacked with this dictionary.\n' \
                           'We recommend you to change it to something less guessable.[/b]\n'
        elif res == e.Password_Found and s.min_mistakes != 0:
            lbl_res.text = '[color=#ff9900][b][size=20]Found a partial match!\n' \
                           'Your password is closed by {0}% to a password in our dictionary.\n' \
                           'Number of different characters: {1}\n' \
                           'Password found in the dictionary: {2}[/b]\n'.format(s.calculate_mistakes_percentage(password),
                                                                            s.min_mistakes,
                                                                            s.similar_pass)
        etr_pass.text = ''

    def update_search_progressbar(self, val):
        if val is None:
            self.pb_search.value += (1/self.num_lines_in_file)
        else:
            self.pb_search.value = val

    def get_number_of_lines_in_file(self, path):
        res = 0
        if path == '':
            return -1
        with open(path, 'r') as file:
            for line in file:
                res += 1
        return res

    def handle_questionnaire(self, dictionary, lbl_list_box, instance):
        self.qhandler.questionnaire(dictionary, lbl_list_box, instance)

    # nav function
    def navigate(self, layout, lay_to, *lay_from):

        for c in list(layout.children):
            if c == lay_to:
                return

        if lay_from is not None:
            for lay in lay_from:
                layout.remove_widget(lay)
        if lay_to is not None:
            layout.add_widget(lay_to)

    def scrap_and_add(self, dictionary, lbl_list, website, popup, instance):

        with open('creds.txt') as f:
            email = f.readline()
            password = f.readline()

        if website == e.LinkedIn_Search:
            self.scraper = ls.LinkedinScraper(email, password)
        elif website == e.Facebook_Search:
            self.scraper = fs.FacebookScraper()

        self.scraper.scrap(self.etr_url.text)
        dictionary.extend_dictionary(self.scraper.lists.words, e.Mode_Words)
        dictionary.extend_dictionary(self.scraper.lists.numbers, e.Mode_Numbers)
        lbh.printto_lbllist(dictionary.lists.words + dictionary.lists.numbers, lbl_list)
        popup.dismiss()

    def web_scrap(self, dictionary, lbl_list, text_to_show, website, instance):

        lay_web_scrap = BoxLayout(orientation='vertical', spacing=10)
        title = "LinkedIn Search" if website == e.LinkedIn_Search else "Facebook Search"
        popup = Popup(title=title, content=lay_web_scrap, size=(500, 250), size_hint=(None, None))

        lay_web_scrap.add_widget(Label(text=text_to_show, size_hint=(1, .6)))
        self.etr_url = TextInput(text='', size_hint=(1, .2), multiline=False)
        self.etr_url.bind(on_text_validate=partial(self.scrap_and_add, dictionary, lbl_list, website, popup))

        btn_scrap_start = Button(text="Start", size_hint=(1, .2),
                                 on_press=partial(self.scrap_and_add, dictionary, lbl_list, website, popup))

        lay_web_scrap.add_widget(self.etr_url)
        lay_web_scrap.add_widget(btn_scrap_start)
        popup.open()


if __name__ == '__main__':
    MyDictionary().run()