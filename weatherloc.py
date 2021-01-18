from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.menu import  MDDropdownMenu, MDMenuItem
from kivy.clock import Clock
from kivy.uix.video import Video
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextFieldRound, MDTextField, MDTextFieldRect
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDFloatingActionButtonSpeedDial, MDRoundFlatButton, MDRaisedButton
from kivymd.uix.list import MDList, OneLineIconListItem, ILeftBodyTouch, OneLineListItem, ILeftBody, BaseListItem
from kivy.properties import StringProperty, NumericProperty
from kivymd.theming import ThemableBehavior
from kivy.uix.image import Image
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.bottomnavigation import MDBottomNavigation
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.audio import SoundLoader
from kivymd.uix.spinner import MDSpinner
import pandas as pd
import matplotlib.pyplot as plot
import requests

class SplashScreen(MDScreen):
    pass
class MainScreen(MDScreen):
    pass
class SearchScreen(MDScreen):
    pass
class WeatherPage(MDScreen):
    pass
class SettingsPage(MDScreen):
    pass
class AlternateScreen(MDScreen):
    pass
class AboutPage(MDScreen):
    pass
class Manager(ScreenManager):
    pass

class NavDrawerItems(BoxLayout):
    pass
class SearchToolbar(RectangularElevationBehavior, ThemableBehavior, MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass


class WeatherApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Cyan"
        self.screen = Builder.load_file("weather.kv")
        self.apikey = '804ec2a9beef39bfdc6f5d300b858502'
        self.base_url = 'http://api.openweathermap.org/data/2.5'
        self.csv_file = 'worldcities.csv'
        self.data = pd.read_csv(self.csv_file)
        self.cities = self.data["city"]
        self.info_dialog = MDDialog(
            text = "Successfully added to favourite cities!",
            buttons = [MDRaisedButton(
                text = "Done",
                text_color = [1, 1, 1, 1]
            )]
        )

    def build(self):
        return self.screen

    def clear(self):
        self.screen.ids.sec_layout.clear_widgets()

    def gomain(self):
        self.screen.ids.screen_manager.current = "main"
        self.screen.ids.nav_drawer.set_state('close')

    def settingspage(self):
        self.screen.ids.screen_manager.current = "settings"
        self.screen.ids.nav_drawer.set_state('close')
    
    def search(self):
        self.screen.ids.screen_manager.current = "alternate"
        self.screen.ids.nav_drawer.set_state('close')
        self.screen.ids.favorite_search.text = ""

    def show_dialog(self):
        self.info_dialog.open()

    def goabout(self):
        self.screen.ids.screen_manager.current = "about"
        self.screen.ids.nav_drawer.set_state('close')

    def settings(self):
        self.screen.ids.screen_manager.current = "settings"
        self.screen.ids.nav_drawer.set_state('close')

    def addcities(self):
        for city in list(self.cities):
            self.screen.ids.cities_list.add_widget(OneLineListItem(
                text = city,
            ))

    def find(self, *args):
        try:
            city = self.screen.ids.main_search.text
            full_url = f'{self.base_url}/weather?q={city}&appid={self.apikey}'
            weatherinfo = requests.get(full_url)
            result = weatherinfo.json()
            main = result.get('weather')[0].get('main')
            temp = result.get('main').get('temp')
            description = result.get('weather')[0].get('description')
            country = result.get('sys').get('country')
            cityname = result.get('name')
            real_temp = float(temp) - 273.15
            result = round(real_temp)
            self.screen.ids.main_weather.text = description.title()
            self.screen.ids.temperature.text = f'{result}°'
            self.screen.ids.city_banner.text = f'{city}, {country}'
            if main == "Clear":
                self.screen.ids.main_icon.icon = "weather-cloudy"
            elif main == "Sunny":
                self.screen.ids.main_icon.icon = "weather-sunny"
            elif main == "Clouds":
                self.screen.ids.main_icon.icon = "weather-cloudy"
            elif main == "Rainy":
                self.screen.ids.main_icon.icon = "weather-rainy"
            else:
                pass

        except Exception as e:
            self.clear()
            self.screen.ids.sec_layout.add_widget(Image(
                source = 'error_connection.png', 
                size = ["200dp", "200dp"],
                pos_hint = {"center_x": .5, "center_y": .65}
            ))
            self.screen.ids.sec_layout.add_widget(MDLabel(
                text = "Oops!",
                bold = True,
                font_size = 26,
                pos_hint = {"center_x": .5, "center_y": .41},
                halign = "center"
            ))

    def screen_main(self, *args):
        self.screen.ids.screen_manager.current = "main"

    def screen_search(self, *args):
        self.screen.ids.screen_manager.current = "search"

    def load_spinner(self):
        self.screen.ids.spinner.active = True
        Clock.schedule_once(self.screen_main, 6)

WeatherApp().run()