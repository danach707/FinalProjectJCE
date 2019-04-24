import os
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from functools import partial
import DictionaryBuilder as db
import Search
import re
import Enums


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

        lay_dict = BoxLayout(orientation='vertical')
        btn_calc_dict = Button(text='Make me a dictionary!', size_hint=(0.8, 0.1))
        lbl_calc = Label(text='', size_hint=(1, .9))
        btn_calc_dict.bind(on_press=partial(self.calc_dictionary, dictionary, lbl_calc))

        lay_dict.add_widget(btn_calc_dict)
        lay_dict.add_widget(lbl_calc)

        # bind nav bar functions
        btn_nav_search.bind(on_press=partial(self.navigate, lay_container, lay_dict, lay_search))
        btn_nav_create_dict.bind(on_press=partial(self.navigate, lay_container, lay_search, lay_dict))

        # add widgets to the root layout
        root.add_widget(lay_nav)
        root.add_widget(lay_container)
        return root

    def handleSearch(self, lbl_res, etr_pass, dict, instance):
        s = Search.Search()
        if os.path.isfile(dict.fileName):
            result = s.search(etr_pass.text, dict.fileName)
            lbl_res.text = result
        else:
            lbl_res.text = 'Dictionary file not found. You can create one with the application!'
        etr_pass.text = ''

    def calc_dictionary(self, dictionary, lbl_calc, instance):
        dictionary.buildDictionary()
        dictionary.lists.cleanLists()
        lbl_calc.text = 'Finished!'

    # nav function
    def navigate(self, layout, lay_from, lay_to, instance):
        layout.remove_widget(lay_from)
        layout.add_widget(lay_to)


    # # save dictionary popup
    #
    # def dismiss_popup(self):
    #     self._popup.dismiss()
    #
    # def show_save(self):
    #     content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
    #     self._popup = Popup(title="Save file", content=content,
    #                         size_hint=(0.9, 0.9))
    #     self._popup.open()
    #
    # def save(self, path, filename):
    #     with open(os.path.join(path, filename), 'w') as stream:
    #         stream.write(';')
    #
    #     self.dismiss_popup()


if __name__ == '__main__':
    MyDictionary().run()