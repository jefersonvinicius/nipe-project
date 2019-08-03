from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from kivy.lang import Builder

Builder.load_string('''
#:import toRgb kivy.utils.get_color_from_hex
#:set BACK_NAVIGATION_COLOR '#282828'

<NavigationButton>:
    icon: icon
    background_down: ""
    background_normal: ""
    background_color: (0, 0, 0, 0)

    Image:
        id: icon
        source: root.path_icon_normal if root.state  == "normal" else root.path_icon_active
        center_x: root.center_x
        center_y: root.center_y
        size_hint: None, None
        size: (dp(50), dp(50))

<NavigationBar>:
    canvas.before:
        Color:
            rgba: toRgb(BACK_NAVIGATION_COLOR)
        Rectangle:
            pos: self.pos
            size: self.size
    size_hint_y: None
    height: '75dp'
''')

class NavigationButton(ToggleButton):
    path_icon_normal = StringProperty()
    path_icon_active = StringProperty()
    icon = ObjectProperty()

    def on_state(self, *args):
        if self.state == "down":
            self.icon.source = self.path_icon_active
        else:
            self.icon.source = self.path_icon_normal


class NavigationBar(BoxLayout):

    navigation_buttons = ListProperty()
    button_active = ObjectProperty()

    def __init__(self, **kwargs):
        super(NavigationBar, self).__init__(**kwargs)

    def on_button_active(self, *args):
        for button in self.navigation_buttons:
            if button != self.button_active:
                button.icon.source = button.path_icon_normal
