from kivy.storage.jsonstore import JsonStore
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock, mainthread
import json

from androidstorage4kivy import SharedStorage, Chooser
from android import mActivity

from baza.create_baza_data import (
    select_all_auto,
    delete_auto_in_baza, or_table_in_baza,
)

primary_palette = [
    'Blue', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Red',
    'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime',
    'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray',
    'BlueGray'
]
color_hue = [
    '50', '100', '200', '300', '400', '500',
    '600', '700', '800', '900', 'A100', 'A200', 'A400', 'A700'
]


class ScreenSettings(MDScreen):
    index = 0
    index_hue = 0
    dialog = None
    menu = None
    click_language = True
    list_from_json_pl = []
    list_from_json_ukr = []
    app = MDApp.get_running_app()
    text_dialog = ''
    text_dialog1 = ''
    text_dialog2 = ''
    text_dialog3 = ''
    path = None
    shared = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chooser = Chooser(self.chooser_callback)


    def on_enter(self, *args):
        Clock.schedule_once(self.active_switch, 0)
        Clock.schedule_once(self.open_json, 0)

    def open_json(self, *args):
        with open('language.json', encoding='utf-8') as file:
            data = json.load(file)
        store = JsonStore('settings.json')
        res_language = store.store_get('language')['select_language']
        res_pl = data["screen_settings"]["pl"]
        res_ukr = data["screen_settings"]["ukr"]
        if res_language == 'pl':
            self.text_dialog = res_pl['t4']
            self.text_dialog1 = res_pl['t5']
            self.text_dialog2 = res_pl['t6']
            self.text_dialog3 = res_pl['t7']
            self.ids.btn_delete.text = res_pl['t3']
            self.ids.text_toolbar.title = res_pl['t1']
        else:
            self.text_dialog = res_ukr['t4']
            self.text_dialog1 = res_ukr['t5']
            self.text_dialog2 = res_ukr['t6']
            self.text_dialog3 = res_ukr['t7']
            self.ids.btn_delete.text = res_ukr['t3']
            self.ids.text_toolbar.title = res_ukr['t1']

    def active_switch(self, *args):
        store = JsonStore('settings.json')
        res_language = store.store_get('language')['select_language']
        res_theme = store.store_get('theme')['theme']
        res_primary_palette = store.store_get('palette')['primary_palette']
        res_primary_hue = store.store_get('hue')['primary_hue']
        self.ids.color_hue.text = res_primary_hue
        self.ids.color_primary.text = res_primary_palette
        if res_language == 'pl':
            self.ids.switch_language.active = False
            self.ids.label_pl.text_color = 'red'

        else:
            self.ids.switch_language.active = True
            self.ids.label_ukr.text_color = 'red'

        if res_theme == 'Light':
            self.ids.switch_theme.active = False
            self.ids.light.text_color = 'red'
        else:
            self.ids.switch_theme.active = True
            self.ids.dark.text_color = 'red'

    def back_screen_logo(self, obj):
        app = MDApp.get_running_app()
        app.sm.current = 'screen_logo'

    def click_plus(self):
        app = MDApp.get_running_app()
        store = JsonStore('settings.json', indent=True)
        if self.index < len(primary_palette) - 1:
            self.index += 1
        app.theme_cls.primary_palette = primary_palette[self.index]
        self.ids.color_primary.text = primary_palette[self.index]
        store.put('palette', primary_palette=primary_palette[self.index])

    def click_minus(self):
        app = MDApp.get_running_app()
        store = JsonStore('settings.json', indent=True)
        if self.index > 0:
            self.index -= 1
        app.theme_cls.primary_palette = primary_palette[self.index]
        self.ids.color_primary.text = primary_palette[self.index]
        store.put('palette', primary_palette=primary_palette[self.index])

    def click_plus_hue(self):
        app = MDApp.get_running_app()
        store = JsonStore('settings.json', indent=True)
        if self.index_hue < len(color_hue) - 1:
            self.index_hue += 1
        app.theme_cls.primary_hue = color_hue[self.index_hue]
        self.ids.color_hue.text = color_hue[self.index_hue]
        store.put('hue', primary_hue=color_hue[self.index_hue])

    def click_minus_hue(self):
        app = MDApp.get_running_app()
        store = JsonStore('settings.json', indent=True)
        if self.index_hue > 0:
            self.index_hue -= 1
        app.theme_cls.primary_hue = color_hue[self.index_hue]
        self.ids.color_hue.text = color_hue[self.index_hue]
        store.put('hue', primary_hue=color_hue[self.index_hue])

    def language_select(self, switch, value):
        store = JsonStore('settings.json', indent=True)

        with open('language.json', encoding='utf-8') as file:
            data = json.load(file)
        res_ukr = data["screen_settings"]["ukr"]
        res_pl = data["screen_settings"]["pl"]
        if value:
            store.put('language', select_language='ukr')
            self.ids.label_pl.text_color = 'black'
            self.ids.label_ukr.text_color = 'red'
            self.ids.text_toolbar.title = res_ukr['t1']
            self.ids.lab1.text = res_ukr['t2']
            self.ids.btn_delete.text = res_ukr['t3']
            self.text_dialog = res_ukr['t4']
            self.text_dialog1 = res_ukr['t5']
            self.text_dialog2 = res_ukr['t6']
            self.text_dialog3 = res_ukr['t7']

        else:
            store.put('language', select_language='pl')
            self.ids.label_ukr.text_color = 'black'
            self.ids.label_pl.text_color = 'red'
            self.ids.text_toolbar.title = res_pl['t1']
            self.ids.lab1.text = res_pl['t2']
            self.ids.btn_delete.text = res_pl['t3']
            self.text_dialog = res_pl['t4']
            self.text_dialog1 = res_pl['t5']
            self.text_dialog2 = res_pl['t6']
            self.text_dialog3 = res_pl['t7']


    def theme_select(self, switch, value):
        store = JsonStore('settings.json', indent=True)
        app = MDApp.get_running_app()
        if value:
            store.put('theme', theme='Dark')
            app.theme_cls.theme_style_switch_animation = True
            app.theme_cls.theme_style_switch_animation_duration = 0.8
            app.theme_cls.theme_style = 'Dark'
            self.ids.dark.text_color = 'red'
            self.ids.light.text_color = 'white'
        else:
            store.put('theme', theme='Light')
            app.theme_cls.theme_style_switch_animation = True
            app.theme_cls.theme_style_switch_animation_duration = 0.8
            app.theme_cls.theme_style = 'Light'
            self.ids.light.text_color = 'red'
            self.ids.dark.text_color = 'black'

    def click_delete_auto(self, item):
        if or_table_in_baza():
            list_auto = select_all_auto()
            if len(list_auto) > 0:
                menu_items = [
                    {
                        "text": f"{i[0]}  {i[1]}",
                        "viewclass": "OneLineListItem",
                        "on_release": lambda x=i: self.menu_list_auto(x),
                    } for i in list_auto
                ]
                self.menu = MDDropdownMenu(
                    caller=item,
                    items=menu_items,
                    width_mult=4,
                )
                self.menu.caller.pos = [10, 400]
                self.menu.open()
            else:
                MDDialog(title=f"{self.text_dialog}").open()
        else:
            MDDialog(title=f"{self.text_dialog}").open()

    def menu_list_auto(self, name_auto):
        self.select_auto_delete(name_auto)

    def cancel_dialog(self, obj):
        self.dialog.dismiss()
        self.menu.dismiss()

    def select_auto_delete(self, select_auto):
        marka = select_auto[0]
        model = select_auto[1]
        self.dialog = MDDialog(
            title=f'{self.text_dialog1} {marka} {model}  {self.text_dialog2}',
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.cancel_dialog
                ),
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    md_bg_color='red',
                    text_color='white',
                    on_release=lambda x: self.delete_auto(select_auto)
                ),
            ],
        )
        self.dialog.open()

    def delete_auto(self, name_auto):
        name_auto = f"{name_auto[0].lower()}{name_auto[1].lower()}"
        delete_auto_in_baza(name_auto)
        self.dialog.dismiss()
        self.menu.dismiss()
        toast(f"{self.text_dialog3}")
        store = JsonStore('main.json', indent=True)
        store.put('app', marka="", model="")

        store_del = JsonStore('main.json')
        res_marka = store_del.store_get('app')['marka']
        res_model = store_del.store_get('app')['model']
        key = res_marka.lower() + res_model.lower()
        store_del.put(key, name_photo='')
        

#################################################3
    def open_closer(self):
        self.chooser.choose_content("image/*")
        

    def chooser_callback(self,uri_list):
        try:
            ss = SharedStorage()
            for uri in uri_list:
                # copy to private
                self.path = ss.copy_from_shared(uri)
                if self.path:
                    self.shared = ss.copy_to_shared(self.path)
                    store_read = JsonStore('main.json')
                    res_marka = store_read.store_get('app')['marka']
                    res_model = store_read.store_get('app')['model']

                    
                    store = JsonStore('main.json', indent=True)
                    key = res_marka.lower() + res_model.lower()
                    store.put(key, name_photo=self.shared)
                    
                         
                    
            self.display()
        except Exception as e:
            pass
    @mainthread
    def display(self):
        pass
        
        


