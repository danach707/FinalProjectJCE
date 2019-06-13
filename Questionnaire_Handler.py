from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from functools import partial

import StringOperations as sc
import Enums as e
import List_Box_Handler as lbh



class Questionnaire_Handler:

    def __init__(self):
        self.quest_lbl_list = []

    def questionnaire(self, dictionary, lbl, instance):

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

        self.qst_fname = TextInput(text='', size_hint=(1, .05), multiline=False,
                                   on_text_validate=partial(self.on_dismiss_quest, dictionary))
        self.qst_lname = TextInput(text='', size_hint=(1, .05), multiline=False,
                                   on_text_validate=partial(self.on_dismiss_quest, dictionary))
        self.qst_dateofbirth = TextInput(text='', size_hint=(1, .05), multiline=False,
                                         on_text_validate=partial(self.on_dismiss_quest, dictionary))
        self.qst_phone_number = TextInput(text='', size_hint=(1, .05), multiline=False,
                                          on_text_validate=partial(self.on_dismiss_quest, dictionary))
        self.qst_workplace = TextInput(text='', size_hint=(1, .05), multiline=False,
                                       on_text_validate=partial(self.on_dismiss_quest, dictionary))
        # add a button to add a member
        self.qst_family_members = TextInput(text='', size_hint=(1, .05), multiline=False,
                                            on_text_validate=partial(self.on_dismiss_quest, dictionary))
        self.qst_college = TextInput(text='', size_hint=(1, .05), multiline=False,
                                     on_text_validate=partial(self.on_dismiss_quest, dictionary))
        self.qst_school = TextInput(text='', size_hint=(1, .05), multiline=False,
                                    on_text_validate=partial(self.on_dismiss_quest, dictionary))
        self.qst_email = TextInput(text='', size_hint=(1, .05), multiline=False,
                                   on_text_validate=partial(self.on_dismiss_quest, dictionary))
        lay_quest_fields.add_widget(self.qst_fname)
        lay_quest_fields.add_widget(self.qst_lname)
        lay_quest_fields.add_widget(self.qst_dateofbirth)
        lay_quest_fields.add_widget(self.qst_phone_number)
        lay_quest_fields.add_widget(self.qst_workplace)
        lay_quest_fields.add_widget(self.qst_family_members)
        lay_quest_fields.add_widget(self.qst_college)
        lay_quest_fields.add_widget(self.qst_school)
        lay_quest_fields.add_widget(self.qst_email)

        lay_quest_btns = StackLayout(orientation='bt-lr', spacing=10, padding=[10, 10])
        btn_ok_quest = Button(text='Submit',
                              size_hint=(1, .1),
                              on_press=partial(self.on_dismiss_quest, dictionary, popup, lbl))
        btn_cancel_quest = Button(text='Cancel',
                                  size_hint=(1, .1),
                                  on_press=lambda *x: popup.dismiss())
        lay_quest_btns.add_widget(btn_cancel_quest)
        lay_quest_btns.add_widget(btn_ok_quest)

        lay_quest.add_widget(lay_quest_lbls)
        lay_quest.add_widget(lay_quest_fields)
        lay_quest.add_widget(lay_quest_btns)

        popup.open()

    def on_dismiss_quest(self, dictionary, popup, lbl, instance):

        if self.qst_fname.text != '':
            dictionary.extend_dictionary(sc.split_by_separator(self.qst_fname.text), e.Mode_Words)

        if self.qst_lname.text != '':
            dictionary.extend_dictionary(sc.split_by_separator(self.qst_lname.text), e.Mode_Words)

        if self.qst_workplace.text != '':
            dictionary.extend_dictionary(sc.split_by_separator(self.qst_workplace.text), e.Mode_Words)

        if self.qst_family_members.text != '':
            dictionary.extend_dictionary(sc.split_by_separator(self.qst_family_members.text), e.Mode_Words)

        if self.qst_college.text != '':
            dictionary.extend_dictionary(sc.split_by_separator(self.qst_college.text), e.Mode_Words)

        if self.qst_school.text != '':
            dictionary.extend_dictionary(sc.split_by_separator(self.qst_school.text), e.Mode_Words)

        if self.qst_email.text != '':
            dictionary.extend_dictionary(sc.parse_email(self.qst_email.text, e.Mode_Words), e.Mode_Words)
            dictionary.extend_dictionary(sc.parse_email(self.qst_email.text, e.Mode_Numbers), e.Mode_Numbers)

        if self.qst_dateofbirth.text != '':
            dob = sc.parse_dob(self.qst_dateofbirth.text)
            dictionary.extend_dictionary(dob, e.Mode_Numbers)

        if self.qst_phone_number.text != '':
            dictionary.extend_dictionary(sc.split_by_separator(self.qst_phone_number.text), e.Mode_Numbers)

        print(dictionary.lists.numbers)
        print(dictionary.lists.words)
        self.quest_lbl_list = dictionary.lists.words + dictionary.lists.numbers
        lbh.printto_lbllist(self.quest_lbl_list, lbl)

        popup.dismiss()