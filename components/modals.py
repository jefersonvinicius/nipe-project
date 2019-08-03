from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder

Builder.load_string('''
<ModalShowPhoto>:
    size_hint: .9, .6
    BoxLayout:
        padding: '10dp'
        BoxLayout:
            canvas.before:
                Color:
                    rgb: (1, 1, 1)
                Rectangle:
                    source: root.photo_path
                    size: self.size
                    pos: self.pos
            orientation: "vertical"

<ModalSelectLocation>:
    recycleview: rv
    size_hint: .90, .75
    BoxLayout:
        orientation: "vertical"
        canvas.before:
			Color:
				rgb: [1, 1, 1]
			Rectangle:
				pos: self.pos
				size: self.size
        Label:
            size_hint_y: None
            height: "40dp"
            canvas.before:
                Color:
                    rgba: toRgb('#6C6B6B')
                Rectangle:
                    pos: self.pos
                    size: self.size
            text: "Localizações:"
        RecycleModalSelectLocation:
            id: rv
            modal_root: root
''')

class ModalSelectLocation(ModalView):

    recycleview = ObjectProperty()

    def __init__(self, screen_root, **kwargs):
        super(ModalSelectLocation, self).__init__(**kwargs)
        self.screen_root = screen_root

class ModalShowPhoto(ModalView):

    photo_path = StringProperty()

    def __init__(self, photo_path, **kwargs):
        super(ModalShowPhoto, self).__init__(**kwargs)
        self.photo_path = photo_path
