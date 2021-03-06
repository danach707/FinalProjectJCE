from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from functools import partial
from kivy.clock import Clock


class DictionaryHandler:
    def submit_dictionary(self, dictionary, inp_wmin, inp_wmax, filename, progressbar, instance):

        wmin = inp_wmin.text
        wmax = inp_wmax.text

        if wmin == '':
            wmin = None
        if wmax == '':
            wmax = None

        dictionary.buildDictionary(wmin, wmax, filename.text, progressbar)

    def popup_dictionary(self, dictionary, instance):

        lay_minmax_words = BoxLayout(orientation='vertical', spacing=6)
        lay_center_minmaxbtn = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(1, .3))

        self.popup = Popup(title="Create my dictionary", content=lay_minmax_words, size=(400, 370), size_hint=(None, None))
        inp_min_len = TextInput(text='', hint_text='minimum length', size_hint=(1, .4))
        inp_max_len = TextInput(text='', hint_text='maximum length', size_hint=(1, .4))
        filename = TextInput(text='', hint_text='file name', size_hint=(1, .4))

        self.progressbar = ProgressBar(max=1100, size_hint=(1, .2))
        self.update_bar = Clock.create_trigger(self.update_bar_event)

        btn_minmax_submit = Button(text="Submit",
                                   size_hint=(.5, 1),
                                   on_press=partial(self.submit_dictionary,
                                                    dictionary,
                                                    inp_min_len,
                                                    inp_max_len,
                                                    filename,
                                                    self.update_bar_event
                                                    ))
        self.progressbar.value = 0
        lay_center_minmaxbtn.add_widget(btn_minmax_submit)

        lay_minmax_words.add_widget(Label(text='File Name:', size_hint=(1, .2), font_size='16sp'))
        lay_minmax_words.add_widget(Label(text='(For default length leave empty):', size_hint=(1, .2), font_size='14sp'))
        lay_minmax_words.add_widget(filename)
        lay_minmax_words.add_widget(Label(text='Words minimum length:', size_hint=(1, .2), font_size='16sp'))
        lay_minmax_words.add_widget(Label(text='(For default length leave empty):', size_hint=(1, .2), font_size='14sp'))
        lay_minmax_words.add_widget(inp_min_len)
        lay_minmax_words.add_widget(Label(text='Words maximum length:', size_hint=(1, .2), font_size='16sp'))
        lay_minmax_words.add_widget(Label(text='(For default length leave empty):', size_hint=(1, .2), font_size='14sp'))
        lay_minmax_words.add_widget(inp_max_len)
        lay_minmax_words.add_widget(self.progressbar)
        lay_minmax_words.add_widget(lay_center_minmaxbtn)

        self.popup.open()

    def update_bar_event(self):
        self.progressbar.value += 100
        if self.progressbar.value == 1100:
            self.popup.dismiss()
