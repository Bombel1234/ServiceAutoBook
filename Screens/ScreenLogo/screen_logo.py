import json
import os.path
from os.path import exists, join
from shutil import rmtree
from kivymd.app import MDApp
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock


from baza.create_baza_data import (
    or_ist_auto,
    or_table_in_baza,
    select_all_auto
)


class ScreenLogo(MDScreen):
    data = []
    text_dialog1 = ''
    text_dialog2 = ''
    text_dialog3 = ''
    menu = None

    def on_leave(self, *args):
        marka = self.ids.marka.text
        model = self.ids.model.text
        if marka != '' and model != '':
            self.save_json(marka, model)


    def on_enter(self, *args):
        Clock.schedule_once(self.start_screen, 0)
        Clock.schedule_once(self.open_json_language, 0)

    def open_json_language(self, *args):
        store = JsonStore('settings.json')
        res = store.store_get('language')['select_language']

        with open('language.json', encoding='utf-8') as file:
            data = json.load(file)
        if res == 'pl':
            self.select_language(data["screen_logo"]["pl"])
        else:
            self.select_language(data["screen_logo"]["ukr"])

    def select_language(self, dict_json):
        self.ids.lab_mark_model.text = dict_json['t1']
        self.ids.marka.hint_text = dict_json['t2']
        self.ids.model.hint_text = dict_json['t3']
        self.ids.btn1.text = dict_json['t4']
        self.ids.btn2.text = dict_json['t5']
        self.ids.drop.text = dict_json['t6']
        self.text_dialog1 = dict_json['t7']
        self.text_dialog2 = dict_json['t8']
        self.text_dialog3 = dict_json['t9']

    def start_screen(self, dt):
        if os.path.exists('main.json'):
            store = JsonStore('main.json', indent=True)
            marka = store.store_get('app')['marka']
            model = store.store_get('app')['model']
            self.ids.marka.text = marka
            self.ids.model.text = model

    def open_menu(self):
        if or_table_in_baza():
            list_auto = select_all_auto()
            if len(list_auto) > 0:
                menu_items = [
                    {
                        "text": f"{i[0]}  {i[1]}",
                        "viewclass": "OneLineListItem",
                        "on_release": lambda x=i: self.menu_callback(x),
                    } for i in list_auto
                ]
                self.menu = MDDropdownMenu(
                    caller=self.ids.drop,
                    items=menu_items,
                    width_mult=4,
                )
                self.menu.caller.pos = [10, 24.5]
                self.menu.open()
            else:
                MDDialog(title=f"{self.text_dialog1}").open()
        else:
            MDDialog(title=f"{self.text_dialog1}").open()

    def menu_callback(self, obj):
        self.ids.marka.text = obj[0]
        self.ids.model.text = obj[1]

    def open_screen_result(self):
        app = MDApp.get_running_app()
        marka = self.ids.marka.text
        model = self.ids.model.text
        if marka != '' and model != '':
            title = marka.lower() + model.lower()
            if or_table_in_baza():
                res = or_ist_auto(title)
                if res:
                    app.sm.current = 'screen_info'
                    self.save_json(marka, model)
                else:
                    dialog = MDDialog(title=f'{self.text_dialog2}')
                    dialog.open()
            else:
                dialog = MDDialog(title=f'{self.text_dialog2}')
                dialog.open()
                self.save_json(marka, model)
        else:
            dialog = MDDialog(title=f"{self.text_dialog3}")
            dialog.open()

    def save_json(self, marka, model):
        store = JsonStore('main.json', indent=True)
        store.put('app', marka=marka.lower(), model=model.lower())
