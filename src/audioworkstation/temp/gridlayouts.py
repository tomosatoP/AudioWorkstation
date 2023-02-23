from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

Builder.load_file("gridlayout1.kv")
Builder.load_file("gridlayout2.kv")
Builder.load_file("gridlayout3.kv")


class Screen1(BoxLayout):
    pass


class Screen2(BoxLayout):
    pass


class Screen3(BoxLayout):
    pass
