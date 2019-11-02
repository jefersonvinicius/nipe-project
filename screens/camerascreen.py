from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.utils import platform
from datetime import datetime

from database.handlingdata import db
from device.toast import Toast

if platform == 'android':
    from device.cameraandroid import CameraAndroid

Builder.load_string('''
<CameraScreen>:
    app: app
    image_preview: image_preview_id
    input_name_photo: input_name_photo_id
    name: "camerascreen"
    BoxLayout
        spacing: 10
        orientation: "vertical"
        AsyncImage:
            id: image_preview_id
        BoxLayout:
            orientation: 'vertical'
            spacing: 10
            padding: 10
            size_hint_y: None
            height: '100dp'
            TextInput:
                id: input_name_photo_id
                multline: False
            BoxLayout:
                spacing: 10
                padding: 10
                Button:
                    text: 'Salvar'
                    on_release:
                        root.save_location()
                        root.go_mapscreen()
                Button:
                    text: 'Cancelar'
''')

class CameraScreen(Screen):

    file_path = StringProperty()
    image_preview = ObjectProperty()
    input_name_photo = ObjectProperty()
    app = ObjectProperty()

    def __init__(self, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)
        
        if platform == 'android':
            self.camera = CameraAndroid()

    def access_camera(self):
        self.camera.take_picture(self.callback_camera)

    def callback_camera(self, file_path):
        self.file_path = file_path
        self.image_preview.source = file_path

    def save_location(self):
        location_data = {
            'name': self.input_name_photo.text,
            'lat' : self.app.location.get_lat(),
            'lon' : self.app.location.get_lon(),
            'date': datetime.now().strftime("%d/%m/%Y"),
            'photopath' : self.file_path
        }
        db.insert_location(location_data)
        self.input_name_photo.text = ''
        self.app.locations = db.get_all_locations()

        Toast.show('Salvo com sucesso!')

    def go_mapscreen(self):
        self.manager.current = 'mapscreen'

