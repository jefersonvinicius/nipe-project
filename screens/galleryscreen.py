from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty, ObjectProperty
from kivy.lang import Builder

from database.handlingdata import db

Builder.load_string('''
<GalleryScreen>:
    app: app
    name: "galleryscreen"
    recycle_gallery: recycle_gallery
    BoxLayout
        canvas.before:
            Color:
                rgba: (0.8, 0.8, 0.8, 1)
            Rectangle:
                pos: self.pos
                size: self.size
        orientation: "vertical"
        RecycleGallery:
            id: recycle_gallery
''')

class GalleryScreen(Screen):

    gallery_data = ListProperty()
    recycle_gallery = ObjectProperty(None)
    app = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(GalleryScreen, self).__init__(**kwargs)

    def on_enter(self, *args):
        self.update_data()

    def update_data(self):
        self.recycle_gallery.data = self.app.locations
