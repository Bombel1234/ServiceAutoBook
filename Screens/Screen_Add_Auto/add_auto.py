import json
import os.path

from kivy.storage.jsonstore import JsonStore
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.toast import toast
from baza.create_baza_data import (
    or_ist_auto,
    add_marka_model_baza, or_table_in_baza,
    create_table_list_auto,
    create_table_name_auto
)


class AddAuto(MDScreen):
    dialog = None
    text_dialog1 = ''
    text_dialog2 = ''
    text_dialog3 = ''
    text_dialog4 = ''

    def on_enter(self, *args):
        Clock.schedule_once(self.start_screen, 0)
        Clock.schedule_once(self.open_json_language, 0)

    def back_screen_logo(self, obj):
        app = MDApp.get_running_app()
        app.sm.current = 'screen_logo'

    def open_json_language(self, *args):
        store = JsonStore('settings.json')
        res = store.store_get('language')['select_language']

        with open('language.json', encoding='utf-8') as file:
            data = json.load(file)

        if res == 'pl':
            self.select_language(data["screen_add_auto"]["pl"])
        else:
            self.select_language(data["screen_add_auto"]["ukr"])

    def select_language(self, data_json):
        self.ids.lab1.text = data_json['t1']
        self.ids.marka.hint_text = data_json['t2']
        self.ids.model.hint_text = data_json['t3']
        self.ids.btn_add.text = data_json['t4']
        self.text_dialog1 = data_json['t5']
        self.text_dialog2 = data_json['t6']
        self.ids.btn_back.title = data_json['t7']
        self.text_dialog3 = data_json['t8']
        self.text_dialog4 = data_json['t9']

    def start_screen(self, dt):
        if os.path.exists('main.json'):
            store = JsonStore('main.json', indent=True)
            marka = store.store_get('app')['marka']
            model = store.store_get('app')['model']
            self.ids.marka.text = marka
            self.ids.model.text = model

    def on_leave(self, *args):
        self.ids.marka.text = ''
        self.ids.model.text = ''

    def add_auto(self, marka, model):
        if marka != '' and model != '':
            if marka.isalnum() and model.isalnum():
                title = marka.lower() + model.lower()
                if or_table_in_baza():
                    if or_ist_auto(title):
                        dialog = MDDialog(title=f"{self.text_dialog1}")
                        dialog.open()
                    else:
                        create_table_list_auto()
                        create_table_name_auto(title)
                        add_marka_model_baza(marka, title, model)
                        toast(text=f"{self.text_dialog2}")
                        self.save_json(marka, model)
                        Clock.schedule_once(self.transition_screen_info, 2)

                else:
                    create_table_list_auto()
                    create_table_name_auto(title)
                    add_marka_model_baza(marka, title, model)
                    toast(text=f"{self.text_dialog2}")
                    self.save_json(marka, model)
                    Clock.schedule_once(self.transition_screen_info, 2)
            else:
                MDDialog(title=f"{self.text_dialog4}").open()
        else:
            MDDialog(title=f"{self.text_dialog3}").open()

    def transition_screen_info(self, dt):
        app = MDApp.get_running_app()
        app.sm.current = 'screen_info'

    def save_json(self, marka, model):
        store = JsonStore('main.json', indent=True)
        store.put('app', marka=marka, model=model)
