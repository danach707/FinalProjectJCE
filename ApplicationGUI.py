import os
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from functools import partial
import DictionaryBuilder as db
import Search
import re
import Enums as e


# class SaveDialog(FloatLayout):
#     save = ObjectProperty(None)
#     text_input = ObjectProperty(None)
#     cancel = ObjectProperty(None)


class MyDictionary(App):

    savefile = ObjectProperty(None)

    def build(self):

        dictionary = db.DictionaryBuilder()

        # ============== root layout ==============
        root = BoxLayout(orientation='vertical')

        # ============== nav bar ==============
        lay_nav = BoxLayout(orientation='horizontal', size_hint=(1, .1))

        btn_nav_search = Button(text='Search Password', size_hint=(1, 1))
        btn_nav_create_dict = Button(text='Create Dictionary', size_hint=(1, 1))
        lay_nav.add_widget(btn_nav_search)
        lay_nav.add_widget(btn_nav_create_dict)

        # ============== container ==============

        lay_container = BoxLayout(orientation='vertical', size_hint=(1, .9))

        # ============== search the password in the dictionary ==============
        lay_search = BoxLayout(orientation='vertical', padding=[100, 100], spacing=10)

        inp_pass = TextInput(text='', size_hint=(.4, .1))
        btn_search = Button(text='Search', size_hint=(.3, .1))
        lbl_pass_result = Label(text='result', size_hint=(1, .8))
        btn_search.bind(on_press=partial(self.handleSearch, lbl_pass_result, inp_pass, dictionary))

        # btn_nav_search.bind(partial(self.goto_search, lay_search, lay_dict))

        lay_search.add_widget(inp_pass)
        lay_search.add_widget(btn_search)
        lay_search.add_widget(lbl_pass_result)

        # ============== create a dictionary ==============

        lay_dict = BoxLayout(orientation='vertical', padding=[100, 100], spacing=10)
        btn_calc_dict = Button(text='Make me a dictionary!', size_hint=(.5, .1))
        lbl_calc = Label(text='', size_hint=(1, .5))
        btn_calc_dict.bind(on_press=partial(self.calc_dictionary, dictionary))
        btn_open_quest = Button(text='Questionnaire', size_hint=(.5, .1))
        btn_open_quest.bind(on_press=partial(self.questionnaire, dictionary))

        lay_dict.add_widget(btn_open_quest)
        lay_dict.add_widget(btn_calc_dict)
        lay_dict.add_widget(lbl_calc)

        # =============================================
        # bind nav bar function
        btn_nav_search.bind(on_press=partial(self.navigate, lay_container, lay_search, lay_dict))
        btn_nav_create_dict.bind(on_press=partial(self.navigate, lay_container, lay_dict, lay_search))

        # add widgets to the root layout
        root.add_widget(lay_nav)
        root.add_widget(lay_container)
        return root

    def handleSearch(self, lbl_res, etr_pass, dict, instance):
        s = Search.Search()
        res = s.search(etr_pass.text, dict.fileName)
        if res == e.Error_No_Dictionary:
            lbl_res.text = "Error, no dictionary found.\n" \
                            "You can create one with the application!"
        elif res == e.Error_Empty_Password:
            lbl_res.text = "Password is empty.."
        elif s.min_mistakes == 0:
            lbl_res.text = 'Found a match!\n' \
                           'Your password can be hacked with this dictionary.\n' \
                           'We recommend you to change it to something less guessable.\n'
        else:
            # change # to %
            lbl_res.text = 'Found a partial match!\n' \
                           'Your password is closed by {0} to a password in our dictionary.\n' \
                           'Number of different characters: {1}\n' \
                           'Password found in the dictionary: {2}\n'.format(res, s.min_mistakes, s.similar_pass)
        etr_pass.text = ''

    def calc_dictionary(self, dictionary, instance):
        dictionary.buildDictionary()
        dictionary.lists.cleanLists()
        print('Finished!')

    # nav function
    def navigate(self, layout, lay_to, *lay_from):
        if lay_from is not None:
            for lay in lay_from:
                layout.remove_widget(lay)
        if lay_to is not None:
            layout.add_widget(lay_to)

    def questionnaire(self, dictionary, instance):

        # ============== questionnaire form ==============
        lay_quest = BoxLayout(orientation='horizontal')

        popup = Popup(title="Questionnaire", content=lay_quest, size=(400, 400), size_hint=(None, None))

        lay_quest_lbls = BoxLayout(orientation='vertical')
        lay_quest_lbls.add_widget(Label(text='First name:'))
        lay_quest_lbls.add_widget(Label(text='Last name:'))
        lay_quest_lbls.add_widget(Label(text='Date of birth:'))
        lay_quest_lbls.add_widget(Label(text='Phone number:'))
        lay_quest_lbls.add_widget(Label(text='Work place'))
        lay_quest_lbls.add_widget(Label(text='Family members:'))
        lay_quest_lbls.add_widget(Label(text='College:'))
        lay_quest_lbls.add_widget(Label(text='School:'))
        lay_quest_lbls.add_widget(Label(text='Email:'))

        lay_quest_fields = BoxLayout(orientation='vertical')

        self.qst_fname = TextInput(text='', size_hint=(.7, .05), multiline=False,
                              on_text_validate=partial(self.calc_dictionary, self.directory))
        self.qst_lname = TextInput(text='', size_hint=(.7, .05), multiline=False,
                              on_text_validate=partial(self.calc_dictionary, self.directory))
        self.qst_dateofbirth = TextInput(text='', size_hint=(.7, .05), multiline=False,
                              on_text_validate=partial(self.calc_dictionary, self.directory))
        self.qst_phone_number = TextInput(text='', size_hint=(.7, .05), multiline=False,
                              on_text_validate=partial(self.calc_dictionary, self.directory))
        self.qst_workplace = TextInput(text='', size_hint=(.7, .05), multiline=False,
                              on_text_validate=partial(self.calc_dictionary, self.directory))
        # add a button to add a member
        self.qst_family_members = TextInput(text='', size_hint=(.7, .05), multiline=False,
                              on_text_validate=partial(self.calc_dictionary, self.directory))
        self.qst_college = TextInput(text='', size_hint=(.7, .05), multiline=False,
                              on_text_validate=partial(self.calc_dictionary, self.directory))
        self.qst_school = TextInput(text='', size_hint=(.7, .05), multiline=False,
                              on_text_validate=partial(self.calc_dictionary, self.directory))
        self.qst_email = TextInput(text='', size_hint=(.7, .05), multiline=False,
                              on_text_validate=partial(self.calc_dictionary, self.directory))
        lay_quest_fields.add_widget(self.qst_fname)
        lay_quest_fields.add_widget(self.qst_lname)
        lay_quest_fields.add_widget(self.qst_dateofbirth)
        lay_quest_fields.add_widget(self.qst_phone_number)
        lay_quest_fields.add_widget(self.qst_workplace)
        lay_quest_fields.add_widget(self.qst_family_members)
        lay_quest_fields.add_widget(self.qst_college)
        lay_quest_fields.add_widget(self.qst_school)
        lay_quest_fields.add_widget(self.qst_email)

        lay_quest_btns = StackLayout(orientation='bt-lr', spacing=10)
        btn_ok_quest = Button(text='Submit',
                              size_hint=(.5, .1),
                              on_press=partial(self.on_dismiss_quest, dictionary))
        btn_cancel_quest = Button(text='Cancel',
                                  size_hint=(.5, .1),
                                  on_press=lambda *x: popup.dismiss())
        lay_quest_btns.add_widget(btn_cancel_quest)
        lay_quest_btns.add_widget(btn_ok_quest)

        lay_quest.add_widget(lay_quest_lbls)
        lay_quest.add_widget(lay_quest_fields)
        lay_quest.add_widget(lay_quest_btns)

        popup.open()

    def on_dismiss_quest(self, dictionary, instance):

        if self.qst_fname.text != '':
            dictionary.lists.words.append(self.qst_fname.text)
        if self.qst_lname.text != '':
            dictionary.lists.words.append(self.qst_lname.text)
        if self.qst_workplace.text != '':
            dictionary.lists.words.append(self.qst_workplace.text)
        if self.qst_family_members.text != '':
            dictionary.lists.words.append(self.qst_family_members.text)
        if self.qst_college.text != '':
            dictionary.lists.words.append(self.qst_college.text)
        if self.qst_school.text != '':
            dictionary.lists.words.append(self.qst_school.text)
        if self.qst_email.text != '':
            dictionary.lists.words.append(self.qst_email.text)

        if self.qst_dateofbirth.text != '':
            dictionary.lists.numbers.append(self.qst_dateofbirth.text)
        if self.qst_phone_number.text != '':
            dictionary.lists.numbers.append(self.qst_phone_number.text)
        print(dictionary.lists.numbers)
        print(dictionary.lists.words)


if __name__ == '__main__':
    MyDictionary().run()