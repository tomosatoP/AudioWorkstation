import kivy  # noqa: F401

from kivy.app import App
from kivy.uix.gridlayout import GridLayout

from .temp import gridlayouts  # noqa: F401


class main_kv(GridLayout):
    pass


class Gridlayout_mainApp(App):
    def build(self):
        self.x = 800 / 4
        self.y = 400 * 0.8
        return main_kv()


if __name__ == "__main__":
    Gridlayout_mainApp().run()
