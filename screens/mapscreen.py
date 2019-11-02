from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.garden.mapview import MapMarker
from kivy.lang import Builder

from components.recycleview.views import ModalLocationView
from components.recycleview.recyclers import RecycleModalSelectLocation
from components.modals import ModalSelectLocation, ModalShowPhoto
from components.buttons import ButtonTextAndIcon

Builder.load_string('''
<MapScreen>:
    name: "mapscreen"
    map_view: map_view
    btn_open_modal: btn
    FloatLayout
        MapView:
            id: map_view
            zoom: 11
            pause_on_action: False
            double_tap_zoom: True
        ButtonTextAndIcon:
            id: btn
            path_icon: "assets/icons/arrow-down.png"
            font_size: "18sp"
            text: "Selecione um local:"
            size_hint_y: None
            height: '50dp'
            pos_hint: {"top": 1}
            on_release: root.open_modal()

''')


class MapScreen(Screen):

    app = ObjectProperty()

    map_view = ObjectProperty()
    btn_open_modal = ObjectProperty()
    modal_select_location = ObjectProperty()
    location_selected = ObjectProperty()
    marker = ObjectProperty(MapMarker())
    recycle_view_select_location = ObjectProperty()

    def __init__(self, **kwargs):
        super(MapScreen, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.modal_select_location = ModalSelectLocation(self)
        self.recycle_view_select_location = self.modal_select_location.recycleview
        self.marker.bind(on_release=self.marker_action)

    def on_enter(self, *args):
        self.recycle_view_select_location.data = self.app.locations
        
    def open_modal(self):
        self.modal_select_location.open()

    def on_location_selected(self, *args):
        self.localize()

    def localize(self, id_location=None):
        if id_location is None:
            pos = (self.location_selected.lat, self.location_selected.lon)
            self.btn_open_modal.text = self.location_selected.name
            self.map_view.center_on(*pos)
            self.set_marker(*pos)
        else:
            dict_location = list(filter(lambda element: element["id"] == id_location,
                                        self.modal_select_location.recycleview.data))[0]
            location_selected_aux = ModalLocationView()
            location_selected_aux.id = dict_location["id"]
            location_selected_aux.name = dict_location["name"]
            location_selected_aux.lat = dict_location["lat"]
            location_selected_aux.lon = dict_location["lon"]
            location_selected_aux.date = dict_location["date"]
            location_selected_aux.photopath = dict_location["photopath"]
            location_selected_aux.selected = True

            self.location_selected = location_selected_aux

    def set_marker(self, lat, lon):
        self.map_view.remove_marker(self.marker)
        self.marker.lat, self.marker.lon = (lat, lon)
        self.map_view.add_marker(self.marker)

    def marker_action(self, *args):
        ModalShowPhoto(self.location_selected.photopath).open()
