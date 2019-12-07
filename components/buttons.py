from kivy.uix.button import Button
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.lang import Builder

Builder.load_string('''
<ButtonTransparent>
    background_normal: ""
    background_down: ""
    background_color: [0, 0, 0, 0]

<ButtonTextAndIcon>:
    icon: icon
    background_normal: ""
    background_down: ""
    background_color: [0, 0, 0, .56]
    text_size: self.size
    valign: "center"
    halign: "left"
    padding_x: dp(10)

    Image:
        id: icon
        source: root.path_icon
        x: root.width - self.width
        center_y: root.center_y
        size_hint_y: None
        height: '50dp'

<ButtonIcon>
    path_icon: ""
    background_normal: ""
    background_down: ""
    background_color: [1, 1, 1, 0]
    Image:
        source: root.path_icon
        center_x: self.parent.center_x
        center_y: self.parent.center_y
''')

class ButtonTransparent(Button):
    pass


class ButtonTextAndIcon(Button):
    path_icon = StringProperty()
    icon = ObjectProperty()
    height_icon = NumericProperty()


class ButtonIcon(Button):
    pass
