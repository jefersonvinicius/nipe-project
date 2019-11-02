from kivy.uix.screenmanager import Screen, FallOutTransition
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.modalview import ModalView
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.metrics import dp

import os

from database.handlingdata import db


Builder.load_string('''
<ButtonPopUpActions>:
    color: [0, 0, 0, 1]
    background_color: [1, 1, 1, 1]
    background_normal: ''
    background_down: ''
    text_size: self.size
    valign: 'center'
    halign: 'left'

<PopUpActions>:
    size_hint: .4, None
    BoxLayout:
        orientation: 'vertical'
        ButtonPopUpActions:
            text: "Localizar"
            size_hint_y: None
            height: '50dp'
            on_release:
                root.localize()
        ButtonPopUpActions:
            text: "Excluir"
            size_hint_y: None
            height: '50dp'
            on_release:
                root.exclude()

<PhotoDetailScreen>:
    app: app
    name: "photodetailscreen"
    btn_actions: btn_menu_actions
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
                    rgba: (0.3, 0.3, 0.3, 1)
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
            ButtonIcon:
                id: btn_menu_actions
                size_hint_x: None
                width: '50dp'
                path_icon: "assets/icons/menu.png"
                on_release:
                    root.open_popup(self)
        BoxLayout:
            padding: 20
            Image:
                source: root.photo_path
''')

class ButtonPopUpActions(Button):

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            Animation(background_color=(.9, .9, .9, 1), duration=0.1).start(self)
        super(ButtonPopUpActions, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        Animation(background_color=(1, 1, 1, 1), duration=0.1).start(self)
        if self.collide_point(*touch.pos):
            self.parent.parent.dismiss()
        super(ButtonPopUpActions, self).on_touch_up(touch)


class PopUpActions(ModalView):

    btn_target = ObjectProperty()

    def __init__(self, x=0, y=0, **kwargs):
        super(PopUpActions, self).__init__(**kwargs)

    def on_pre_open(self):
        self.pos_hint = {
            'x': (Window.width - (0.4 * Window.width) ) / Window.width,
            'y': (Window.height - dp(self.height)) / Window.height
        }

    def localize(self):
        pass

    def exclude(self):
        pass

class PhotoDetailScreen(Screen):

    app = ObjectProperty()

    photo_id = NumericProperty()
    photo_name = StringProperty()
    lat = NumericProperty()
    lon = NumericProperty()
    date = StringProperty()
    photo_path = StringProperty()

    # Widgets
    popup = ObjectProperty()
    btn_actions = ObjectProperty()

    def __init__(self, **kwargs):
        super(PhotoDetailScreen, self).__init__(**kwargs)
        self.popup = PopUpActions()
        self.popup.open()
        self.popup.dismiss()

    def on_enter(self, *args):
        self.popup = PopUpActions(self.btn_actions.x + self.btn_actions.width - self.popup.width, self.btn_actions.y - self.btn_actions.height/2)
        Window.bind(on_keyboard=self.back_screen)
        self.popup.localize = self.localize
        self.popup.exclude = self.exclude
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
        self.popup.dismiss()
        self.manager.get_screen("containerscreens").manager_screens.current = "mapscreen"
        self.manager.get_screen("containerscreens").manager_screens.current_screen.localize(id_location=self.photo_id)
        self.manager.get_screen("containerscreens").btn_mapscreen.state = "down"
        self.manager.get_screen("containerscreens").btn_galleryscreen.state = "normal"
        self.manager.current = "containerscreens"

    def exclude(self):
        try:
            db.delete_location(self.photo_id)
            os.remove(self.photo_path)
            self.app.locations = db.get_all_locations()
            self.manager.current = "containerscreens"
        except Exception as e:
            print(e)

    def open_popup(self, btn):
        self.popup.btn_target = btn
        self.popup.open()
