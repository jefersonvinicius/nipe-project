from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ListProperty

from screens.containerscreens import ContainerScreens
from screens.photodetailscreen import PhotoDetailScreen

from device.location import Location
from database.handlingdata import db


class GeolocalizationApp(App):

    locations = ListProperty()

    def build(self):

        self.locations = db.get_all_locations()

        self.location = Location()

        self.manager = ScreenManager()
        self.manager.add_widget(ContainerScreens())
        self.manager.add_widget(PhotoDetailScreen())

        return self.manager


GeolocalizationApp().run()
