from kivy.uix.screenmanager import Screen, FallOutTransition
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.metrics import dp

import os

from database.handlingdata import db
from components.buttons import ButtonTransparent


Builder.load_string('''
#:import toRgb kivy.utils.get_color_from_hex

<ToolsBar>:
    size_hint_y: None
    height: '50dp'

    canvas.before:
        Color:
            rgb: toRgb('#282828')
        Rectangle:
            size: self.size
            pos: self.pos

    ButtonTransparent:
        text: 'EXCLUIR'
        on_release:
            root.exclude_button_event()

    ButtonTransparent:
        text: 'LOCALIZAR'
        on_release:
            root.localize_button_event()

<PhotoDetailScreen>:
    app: app
    name: "photodetailscreen"
    BoxLayout:
        canvas.before:
            Color:
                rgba: (0, 0, 0, .56)
            Rectangle:
                pos: self.pos
                size: self.size
        orientation: "vertical"
        BoxLayout:
            canvas.before:
                Color:
                    rgb: toRgb('#282828')
                Rectangle:
                    pos: self.pos
                    size: self.size
            size_hint_y: None
            height: "60dp"
            ButtonIcon:
                size_hint_x: None
                width: '50dp'
                path_icon: "assets/icons/arrow-left.png"
                on_release:
                    root.manager.current = "containerscreens"
            Label:
                text: root.photo_name

        BoxLayout:
            padding: 20

            canvas.before:
                Color:
                    rgb: toRgb('#fefefe')
                Rectangle:
                    size: self.size
                    pos: self.pos
            Image:
                source: root.photo_path
        ToolsBar:
            exclude_button_event: root.exclude
            localize_button_event: root.localize
''')


class ToolsBar(BoxLayout):
    
    exclude_button_event = ObjectProperty()
    localize_button_event = ObjectProperty()

class PhotoDetailScreen(Screen):

    app = ObjectProperty()

    photo_id = NumericProperty()
    photo_name = StringProperty()
    lat = NumericProperty()
    lon = NumericProperty()
    date = StringProperty()
    photo_path = StringProperty()

    def __init__(self, **kwargs):
        super(PhotoDetailScreen, self).__init__(**kwargs)

    def on_enter(self, *args):
        Window.bind(on_keyboard=self.back_screen)
        self.manager.transition = FallOutTransition(duration=0.2)

    def on_pre_leave(self, *args):
        Window.unbind(on_keyboard=self.back_screen)

    def back_screen(self, window, key, *args):
        if key == 27:
            self.manager.current = "containerscreens"
        return True

    def pass_data(self, **data):
        self.photo_id = data.get("id")
        self.photo_name = data.get("name")
        self.lat = data.get("lat")
        self.lon = data.get("lon")
        self.date = data.get("date")
        self.photo_path = data.get("photopath")

    def localize(self):
        self.manager.get_screen("containerscreens").manager_screens.current = "mapscreen"
        self.manager.get_screen("containerscreens").manager_screens.current_screen.localize(id_location=self.photo_id)
        self.manager.get_screen("containerscreens").btn_mapscreen.state = "down"
        self.manager.get_screen("containerscreens").btn_galleryscreen.state = "normal"
        self.manager.current = "containerscreens"

    def exclude(self):
        db.delete_location(self.photo_id)
        self.app.locations = db.get_all_locations()
        self.manager.current = "containerscreens"
        
        try:  
            os.remove(self.photo_path)
        except Exception as e:
            print(e)
