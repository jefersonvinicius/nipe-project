from kivy.app import App
from kivy.uix.recycleview import RecycleView
from kivy.properties import ObjectProperty
from kivy.lang import Builder

from database.handlingdata import db

Builder.load_string('''
<RecycleGallery>:
    viewclass: "PhotoContainer"
    RecycleBoxLayout:
        default_size: None, dp(90)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'

<RecycleModalSelectLocation>:
    viewclass: "ModalLocationView"
    RecycleBoxLayout:
        default_size: None, dp(40)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
''')

class RecycleGallery(RecycleView):

    def __init__(self, **kwargs):
        super(RecycleGallery, self).__init__(**kwargs)

class RecycleModalSelectLocation(RecycleView):

    modal_root = ObjectProperty()

    def __init__(self, **kwargs):
        super(RecycleModalSelectLocation, self).__init__(**kwargs)
