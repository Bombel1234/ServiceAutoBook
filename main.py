import os.path
from os.path import exists, join

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.lang.builder import Builder
from baza.create_baza_data import create_baza
from kivy.storage.jsonstore import JsonStore
from kivy.core.window import Window
from shutil import rmtree
from Screens.ScreenLogo.screen_logo import ScreenLogo
from Screens.Screen_Add_Auto.add_auto import AddAuto
from Screens.ScreenInfo.screen_info import ScreenInfo
from Screens.AddInfoAuto.add_info import AddInfo

from Screens.ScreenSettings.screen_settings import ScreenSettings
from Screens.ScreenUpdate.screen_update import ScreenUpdate

from kivy.core.window import Window
from android_permissions import AndroidPermissions
from androidstorage4kivy import SharedStorage


Window.softinput_mode = 'below_target'



class ServiceBookAuto(MDApp):
    sm = None
    select_language = None

    def build(self):
        Window.bind(on_keyboard=self.quit_app)
        create_baza()
        self.save_json_settings()
        temp = SharedStorage().get_cache_dir()
        if temp and exists(temp):
            rmtree(temp)

        self.sm = ScreenManager(transition=NoTransition())

        self.sm.add_widget(ScreenLogo(name='screen_logo'))
        self.sm.add_widget(AddAuto(name='add_auto'))
        self.sm.add_widget(ScreenInfo(name='screen_info'))
        self.sm.add_widget(AddInfo(name='adding_info'))

        self.sm.add_widget(ScreenSettings(name='screen_settings'))
        self.sm.add_widget(ScreenUpdate(name='screen_update'))
        return self.sm
    
    def on_start(self):
        self.dont_gc = AndroidPermissions(self.start_app)

    def start_app(self):
        self.dont_gc = None
    

    def load_kv(self, filename=None):
        Builder.load_file('Screens/ScreenLogo/screen_logo.kv')
        Builder.load_file('Screens/Screen_Add_Auto/add_auto.kv')
        Builder.load_file('Screens/ScreenInfo/screen_info.kv')
        Builder.load_file('Screens/AddInfoAuto/add_info.kv')

        Builder.load_file('Screens/ScreenSettings/screen_settings.kv')
        Builder.load_file('Screens/ScreenUpdate/screen_update.kv')

    def save_json_settings(self):
        if os.path.exists('settings.json'):
            store = JsonStore('settings.json')
            theme = store.store_get('theme')['theme']
            primary_color = store.store_get('palette')['primary_palette']
            primary_hue = store.store_get('hue')['primary_hue']
            self.theme_cls.theme_style = theme
            self.theme_cls.primary_palette = primary_color
            self.theme_cls.primary_hue = primary_hue
        else:
            store = JsonStore('settings.json', indent=True)
            store.put('language', select_language='pl')
            store.put('theme', theme='Light')
            store.put('palette', primary_palette='Blue')
            store.put('hue', primary_hue='500')
            store.put('count_App', count=0)

    def quit_app(self, window, key, *args):

        if key == 27:
            mActivity.finishAndRemoveTask()
            return True
        else:
            return False


if __name__ == "__main__":
    ServiceBookAuto().run()
