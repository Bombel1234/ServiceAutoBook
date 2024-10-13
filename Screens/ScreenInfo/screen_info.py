import json

from kivy.storage.jsonstore import JsonStore
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivy.uix.screenmanager import RiseInTransition
from baza.create_baza_data import is_km, select_info_auto, or_table_in_baza


class MyCard(MDCard):
    data = StringProperty()
    km = StringProperty()
    work = StringProperty()
    cena = StringProperty()


class ScreenInfo(MDScreen):
    res = ''
    text_from_card_pl = []
    text_from_card_ukr = []

    def on_enter(self, *args):
        Clock.schedule_once(self.start_screen, 0.5)
        Clock.schedule_once(self.open_json_language, 0)

    def open_json_language(self, *args):
        store = JsonStore('settings.json')
        self.res = store.store_get('language')['select_language']

        with open('language.json', encoding='utf-8') as file:
            data = json.load(file)
            a = data["screen_info"]["pl"]["t3"]
            b = data["screen_info"]["pl"]["t4"]
            c = data["screen_info"]["pl"]["t5"]
            d = data["screen_info"]["pl"]["t6"]

            a1 = data["screen_info"]["ukr"]["t3"]
            b1 = data["screen_info"]["ukr"]["t4"]
            c1 = data["screen_info"]["ukr"]["t5"]
            d1 = data["screen_info"]["ukr"]["t6"]
        if self.res == 'pl':
            self.select_language(data["screen_info"]["pl"])
            self.text_from_card_pl.append(a)
            self.text_from_card_pl.append(b)
            self.text_from_card_pl.append(c)
            self.text_from_card_pl.append(d)
        else:
            self.select_language(data["screen_info"]["ukr"])
            self.text_from_card_ukr.append(a1)
            self.text_from_card_ukr.append(b1)
            self.text_from_card_ukr.append(c1)
            self.text_from_card_ukr.append(d1)

    def select_language(self, data_json):
        self.ids.text_toolbar.title = data_json["t1"]
        self.ids.btn_add_info.text = data_json["t2"]

    def on_leave(self, *args):
        self.ids.container_card.clear_widgets()

    def click_btn_card(self, cena, km, work, data):
        app = MDApp.get_running_app()
        store = JsonStore('main.json', indent=True)
        store.put('info', km=km, work=work, cena=cena, data=data)
        app.sm.transition = RiseInTransition(duration=0.5)
        app.sm.current = 'screen_update'

    def back_screen_logo(self, obj):
        app = MDApp.get_running_app()
        app.sm.current = 'screen_logo'

    def start_screen(self, dt):
        store = JsonStore('main.json')
        marka = store.store_get('app')['marka']
        model = store.store_get('app')['model']
        marka_model = marka.lower() + model.lower()
        self.ids.name_auto.text = f"{marka.upper()}  {model.upper()}"
        if or_table_in_baza():
            if is_km(marka_model):
                all_data = select_info_auto(marka_model)
                if not all_data == "":
                    keys = ['km', 'work', 'cena', 'data']
                    result = [dict(zip(keys, values)) for values in all_data]
                    for item in result:
                        obj = MyCard()
                        if self.res == 'pl':
                            obj.ids.lab1.text = self.text_from_card_pl[0]
                            obj.ids.lab2.text = self.text_from_card_pl[1]
                            obj.ids.lab3.text = self.text_from_card_pl[2]
                            obj.ids.button.text = self.text_from_card_pl[3]
                        else:
                            obj.ids.lab1.text = self.text_from_card_ukr[0]
                            obj.ids.lab2.text = self.text_from_card_ukr[1]
                            obj.ids.lab3.text = self.text_from_card_ukr[2]
                            obj.ids.button.text = self.text_from_card_ukr[3]
                        obj.data = f'{item["data"]}'
                        obj.km = f"{item['km']}"
                        obj.work = f'{item["work"]}'
                        obj.cena = f'{item["cena"]}'
                        self.ids.container_card.add_widget(obj)
