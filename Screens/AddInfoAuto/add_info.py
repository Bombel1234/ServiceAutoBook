
import json

from kivy.storage.jsonstore import JsonStore
from kivymd.uix.dialog import MDDialog
from datepicker.datepicker import MDDatePicker
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivymd.uix.fitimage import FitImage

from kivymd.app import MDApp
from kivymd.toast import toast

from datetime import datetime
from baza.create_baza_data import (
    create_table_name_auto,
    save_info_auto,
    is_km,
    digit_end_km
)
from androidstorage4kivy import SharedStorage
from android import mActivity, autoclass
from os.path import join,exists
from kivy.logger import Logger

Environment = autoclass('android.os.Environment')


class AddInfo(MDScreen):
    my_data = ''
    my_data_c = ''
    text_dialog1 = ''
    text_dialog2 = ''
    text_dialog3 = ''
    text_dialog4 = ''
    text_dialog5 = ''
    img = None
    
    
    def add_image_auto(self, *args):
        store_read = JsonStore('main.json')
        res_marka = store_read.store_get('app')['marka']
        res_model = store_read.store_get('app')['model']
        key = res_marka + res_model

        context = mActivity.getApplicationContext()
        result = context.getExternalFilesDir(None)
        storage_path =  str(result.toString())

        if exists(f'{storage_path}/img.json'):
            store = JsonStore(f'{storage_path}/img.json')
            if store.exists(key.lower()):
                name_file = store.store_get(key)['name_file']
                Logger.warning(name_file)
                ss = SharedStorage()
                app_title = str(ss.get_app_title())

            
                path2 = ss.copy_from_shared(join(Environment.DIRECTORY_PICTURES,
                                                app_title, name_file))
                self.img = FitImage()
                self.img.source = path2
                self.ids.box_photo.add_widget(self.img)

    def on_enter(self, *args):
        Clock.schedule_once(self.start_screen, 0)
        Clock.schedule_once(self.open_json_language, 0)
        Clock.schedule_once(self.add_image_auto, 1)

    def on_leave(self, *args):
        sp = []
        self.my_data = ''
        self.my_data_c = ''
        self.ids.km.text = ''
        self.ids.work.text = ''
        self.ids.cena.text = ''
        self.ids.value_day.text = ''
       
        root = self.ids.box_photo
        for child in root.children:
            sp.append(child)
        if len(sp) > 0:   
            self.ids.box_photo.remove_widget(self.img)

    def start_screen(self, dt):
        self.ids.value_day.text = str(datetime.now().strftime('%d-%m-%Y'))

    def open_json_language(self, *args):
        store = JsonStore('settings.json')
        res = store.store_get('language')['select_language']

        with open('language.json', encoding='utf-8') as file:
            data = json.load(file)

        if res == 'pl':
            self.select_language(data["screen_add_info"]["pl"])
        else:
            self.select_language(data["screen_add_info"]["ukr"])

    def select_language(self, data_json):
        self.ids.back.title = data_json['t1']
        self.ids.km.hint_text = data_json['t2']
        self.ids.work.hint_text = data_json['t3']
        self.ids.cena.hint_text = data_json['t4']
        self.ids.btn_save.text = data_json['t5']
        self.text_dialog1 = data_json['t6']
        self.text_dialog2 = data_json['t7']
        self.text_dialog3 = data_json['t8']
        self.text_dialog4 = data_json['t9']
        self.text_dialog5 = data_json['t10']

    def open_calendar(self):
        date_dialog = MDDatePicker(title=f"{self.text_dialog4}", selector_color="red",
                                   text_toolbar_color="lightgrey")
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        self.ids.value_day.text = value.strftime('%d-%m-%Y')
        self.my_data_c = str(value.strftime('%d-%m-%Y'))

    def on_cancel(self, instance, value):
        pass

    def save_data_in_baza(self, km, work, cena):
        store = JsonStore('main.json')
        marka = store.store_get('app')['marka']
        model = store.store_get('app')['model']
        marka_model = f"{marka.lower()}{model.lower()}"
        create_table_name_auto(marka_model)
        if self.my_data_c == '':
            self.my_data = str(datetime.now().strftime('%d-%m-%Y'))
        else:
            self.my_data = self.my_data_c

        if km != '' and work != '' and cena != '':
            if is_km(marka_model):
                last_km = digit_end_km(marka_model)[0]
                if int(km) > int(last_km):
                    save_info_auto(km, work, cena, self.my_data, marka_model)
                    toast(f"{self.text_dialog1}")
                    Clock.schedule_once(self.back_screen_info, 2)
                else:
                    dialog = MDDialog(title=f'{self.text_dialog2} {str(last_km)}, {self.text_dialog3}')
                    dialog.open()

            else:
                save_info_auto(km, work, cena, self.my_data, marka_model)
                toast(f"{self.text_dialog1}")
                Clock.schedule_once(self.back_screen_info, 2)
            
        else:
            MDDialog(title=f"{self.text_dialog5}").open()

    def back_screen_info(self, *args):
        app = MDApp.get_running_app()
        app.sm.transition.direction = 'right'
        app.sm.current = 'screen_info'