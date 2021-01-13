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
from kivymd.uix.button import MDFlatButton, MDFloatingActionButtonSpeedDial, MDRoundFlatButton
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
import requests

class MainScreen(MDScreen):
    pass
class SearchScreen(MDScreen):
    pass
class WeatherPage(MDScreen):
    pass
class Settings(MDScreen):
    pass
class Manager(ScreenManager):
    pass

class NavDrawerItems(BoxLayout):
    pass
class SearchToolbar(RectangularElevationBehavior, ThemableBehavior, MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = [1, 1, 1, 1]


class WeatherApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Cyan"
        self.screen = Builder.load_file("weather.kv")
        self.apikey = 'bf527f2c0ece63f0e185788e4ea21be3'
        self.base_url = 'http://api.openweathermap.org/data/2.5'
        self.media = SoundLoader.load('Intentions.mp3')

    def build(self):
        return self.screen

    def test(self):
        print('Hello world!')

    def play(self):
        self.media.play()

    def clear(self):
        self.screen.ids.sec_layout.clear_widgets()

    def gomain(self):
        self.screen.ids.screen_manager.current = "main"
        self.screen.ids.screen_manager.transition.direction = "right"

    def changetheme(self):
        if self.screen.ids.weather_icon.icon == "weather-night":
            weather_icon.icon = "white-balance-sunny"
            self.theme_cls.theme_style = "Dark"
        elif self.screen.ids.weather_icon.icon == "white-balance-sunny":
            weather_icon.icon = "weather-night"
            self.theme_cls.theme_style = "Light"

    def find(self):
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
            self.screen.ids.main_weather.text = description
            self.screen.ids.temperature.text = f'{result}°'
            if main == "Clear":
                self.screen.ids.main_icon.icon = "weather-cloudy"
            elif main == "Sunny":
                self.screen.ids.main_icon.icon = "weather-sunny"
            elif main == "Clouds":
                self.screen.ids.main_icon.icon = "weather-cloudy"
            elif main == "Rainy":
                self.screen.ids.main_icon.icon = "weather-rainy"

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
            

WeatherApp().run()