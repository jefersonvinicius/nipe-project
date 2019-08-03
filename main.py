from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from screens.containerscreens import ContainerScreens
from screens.photodetailscreen import PhotoDetailScreen


class GeolocalizationApp(App):

    def build(self):
        self.manager = ScreenManager()
        self.manager.add_widget(ContainerScreens())
        self.manager.add_widget(PhotoDetailScreen())
        return self.manager


GeolocalizationApp().run()
