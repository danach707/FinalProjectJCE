import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

import ApplicationGUI


class FileExplorer(BoxLayout):
    def __init__(self, **kwargs):
        super(FileExplorer, self).__init__(**kwargs)

        self.orientation = 'vertical'
        self.fichoo = FileChooserListView(size_hint_y=0.8, path='./')
        self.fichoo.dirselect = True
        self.add_widget(self.fichoo)
        self.update_lbl_filename = ''

        control = GridLayout(cols=5, row_force_default=True, row_default_height=35, size_hint_y=0.14, padding=[10, 10])
        lbl_dir = Label(text='Folder', size_hint_x=None, width=150)
        self.tein_dir = TextInput(size_hint_x=None, width=400)
        bt_dir = Button(text='Select file', size_hint_x=None, width=80)
        bt_dir.bind(on_release=self.on_button_select)

        self.fichoo.bind(selection=self.on_mouse_select)

        control.add_widget(lbl_dir)
        control.add_widget(self.tein_dir)
        control.add_widget(bt_dir)

        self.add_widget(control)
        return

    def on_button_select(self, instance):
        self.update_lbl_filename = os.path.join(self.fichoo.path, self.fichoo.selection[0])
        self.parent.parent.parent.dismiss()
        return

    def on_mouse_select(self, obj, val):
        self.tein_dir.text = str(self.fichoo.path)
        return

    def on_touch_up(self, touch):
        if self.fichoo.selection:
            self.tein_dir.text = str(self.fichoo.selection[0])
        return super().on_touch_up(touch)
