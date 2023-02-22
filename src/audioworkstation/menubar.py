import kivy

from kivy.app import App
from kivy.uix.widget import Widget


class MainbarView(Widget):
    pass


class MenubarApp(App):
    def build(self):
        return MainbarView()


if __name__ == "__main__":
    MenubarApp().run()
