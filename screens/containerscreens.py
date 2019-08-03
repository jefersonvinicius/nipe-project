from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder

from screens.camerascreen import CameraScreen
from screens.mapscreen import MapScreen
from screens.galleryscreen import GalleryScreen
from components.navigation import NavigationBar, NavigationButton

Builder.load_string('''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition

<ContainerScreens>:
    name: "containerscreens"
    manager_screens: manager
    btn_mapscreen: btn_mapscreen
    btn_galleryscreen: btn_galleryscreen
    BoxLayout:
        orientation: "vertical"
        ScreenManager:
            id: manager
            transition: FadeTransition(duration=0.01)
            CameraScreen:
            MapScreen:
            GalleryScreen:
        NavigationBar:
            pos_hint: {"top": 0}
            NavigationButton:
                group: "navbtns"
                state: "down"
                allow_no_selection: False
                path_icon_normal: "assets/icons/camera-normal.png"
                path_icon_active: "assets/icons/camera-active.png"
                on_release:
                    manager.current = "camerascreen"

            NavigationButton:
                id: btn_mapscreen
                group: "navbtns"
                allow_no_selection: False
                path_icon_normal: "assets/icons/map-normal.png"
                path_icon_active: "assets/icons/map-active.png"
                on_release:
                    manager.current = "mapscreen"

            NavigationButton:
                id: btn_galleryscreen
                group: "navbtns"
                allow_no_selection: False
                path_icon_normal: "assets/icons/gallery-normal.png"
                path_icon_active: "assets/icons/gallery-active.png"
                on_release:
                    manager.current = "galleryscreen"
''')

class ContainerScreens(Screen):
    manager_screens = ObjectProperty()
