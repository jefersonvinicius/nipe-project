from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_string('''
<CameraScreen>:
    name: "camerascreen"
    BoxLayout
        orientation: "vertical"
        AnchorLayout
            Label:
                anchor_y: "center"
                anchor_x: "center"
                text: "Camera Screen"
''')

class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)
