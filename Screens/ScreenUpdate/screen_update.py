import json

from kivy.storage.jsonstore import JsonStore
from datepicker.datepicker import MDDatePicker
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.uix.screenmanager import NoTransition
from kivy.clock import Clock
from kivymd.toast import toast
from baza.create_baza_data import (
    update_baza_info,
    select_rowid_for_update,
)


class ScreenUpdate(MDScreen):
    my_data = ''
    text_toast = ''

    def on_enter(self, *args):
        Clock.schedule_once(self.add_textinput, 0)
        Clock.schedule_once(self.open_json_language, 0)

    def open_json_language(self, *args):
        store = JsonStore('settings.json')
        res = store.store_get('language')['select_language']

        with open('language.json', encoding='utf-8') as file:
            data = json.load(file)

        if res == 'pl':
            self.select_language(data["screen_update"]["pl"])
            self.text_toast = data["screen_update"]["pl"]["t7"]
        else:
            self.select_language(data["screen_update"]["ukr"])
            self.text_toast = data["screen_update"]["ukr"]["t7"]

    def select_language(self, data_json):
        self.ids.text_toolbar.title = data_json["t1"]
        self.ids.lab1.text = data_json["t2"]
        self.ids.lab2.text = data_json["t3"]
        self.ids.lab3.text = data_json["t4"]
        self.ids.lab4.text = data_json["t5"]
        self.ids.lab5.text = data_json["t6"]

    def add_textinput(self, dt):
        store = JsonStore('main.json')
        info = store.store_get('info')
        self.ids.km.text = info['km']
        self.ids.work.text = info['work']
        self.ids.cena.text = info['cena']
        self.ids.value_day.text = info['data']

    def open_calendar(self):
        date_dialog = MDDatePicker(title="SELECT DATE", selector_color="red",
                                   text_toolbar_color="lightgrey")
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        self.ids.value_day.text = value.strftime('%d-%m-%Y')

    def on_cancel(self, instance, value):
        pass

    def update_baza(self, km, work, cena):
        store = JsonStore('main.json')
        marka = store.store_get('app')['marka']
        model = store.store_get('app')['model']
        marka_model = marka.lower() + model.lower()
        store = JsonStore('main.json')
        km_json = store.store_get('info')['km']

        if km != '' and work != '' and cena != '':
            self.my_data = self.ids.value_day.text
            rowid = select_rowid_for_update(marka_model, km_json)
            update_baza_info(int(km), work, int(cena), self.my_data, marka_model, rowid)
            toast(f"{self.text_toast}")
            Clock.schedule_once(self.back_screen_info, 2.5)

    def back_screen_info(self, dt):
        app = MDApp.get_running_app()
        app.sm.transition = NoTransition()
        app.sm.current = 'screen_info'
