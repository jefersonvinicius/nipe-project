from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import RiseInTransition

from kivy.properties import NumericProperty, StringProperty, ObjectProperty, BooleanProperty
from kivy.lang import Builder

Builder.load_string('''
#:import toRgb kivy.utils.get_color_from_hex

<PhotoContainer>:
    canvas.before:
        Color:
            rgb: (1, 1, 1)
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgb: (0, 0, 0)
        Line:
            rectangle: self.x, self.y, self.width, dp(1)

    padding: dp(5)
    Image:
        source: root.photopath
        size_hint_x: None
        width: "100dp"
    BoxLayout:
        orientation: "vertical"
        padding: dp(5)
        Label:
            text: "[b]" + root.name + "[/b]"
            markup: True
            color: (0, 0, 0, 1)
            text_size: self.size
            valign: "center"
            halign: "left"
            size_hint_y: None
            height: '16dp'
            font_size: "16sp"
        Label:
            text: str(root.lat) + ", " + str(root.lon)
            color: (.3, .3, .3, 1)
            text_size: self.size
            valign: "top"
            halign: "left"
            font_size: "12sp"

        Label:
            text: root.date
            color: (0, 0, 0, 1)
            text_size: self.size
            valign: "center"
            halign: "right"

<LabelTextWrap@Label>:
    shorten: True
	shorten_from: 'right'
	text_size: self.size
	valign: "center"
	halign: 'left'
	padding_x: dp(10)

<ModalLocationView>:
    canvas.before:
		Color:
			rgb: (.6, .6, .6)
		Rectangle:
			size: (self.width, dp(0.2))
			pos: self.pos
    LabelTextWrap:
        text: root.name
        color: [0, 0, 0, 1]
    Image:
		source: "assets/icons/selected.png" if root.selected else "assets/icons/noselected.png"
		center_y: root.center_y
		size_hint_x: None
		width: '50dp'
''')

class PhotoContainer(BoxLayout):
    id = NumericProperty()
    name = StringProperty()
    lat = NumericProperty()
    lon = NumericProperty()
    date = StringProperty()
    photopath = StringProperty()
    manager_root = ObjectProperty(None)

    def on_touch_up(self, touch):
        if not self.manager_root:
            self.manager_root = App.get_running_app().manager

        if self.collide_point(*touch.pos):
            self.manager_root.get_screen("photodetailscreen").pass_data(**self.get_data_packaged())
            self.manager_root.transition = RiseInTransition()
            self.manager_root.current = "photodetailscreen"

    def get_data_packaged(self):
        data = {
            "id": self.id,
            "name": self.name,
            "lat": self.lat,
            "lon": self.lon,
            "date": self.date,
            "photopath": self.photopath
        }
        return data

class ModalLocationView(BoxLayout):
    id = NumericProperty()
    name = StringProperty()
    lat = NumericProperty()
    lon = NumericProperty()
    date = StringProperty()
    photopath = StringProperty()
    selected = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(ModalLocationView, self).__init__(**kwargs)

    def on_touch_up(self, touch):
        modal_root = self.parent.parent.modal_root
        map_screen = modal_root.screen_root
        if self.collide_point(*touch.pos):

            self.selected = not self.selected

            if map_screen.location_selected is not None:
                map_screen.location_selected.selected = not map_screen.location_selected.selected

            if map_screen.location_selected == self:
                map_screen.localize()
            else:
                map_screen.location_selected = self

            modal_root.dismiss()

    def get_dict_location(self):
        return {"id": self.id, "name": self.name, "lat": self.lat, "lon": self.lon, "date": self.date, "photopath": self.photopath}
