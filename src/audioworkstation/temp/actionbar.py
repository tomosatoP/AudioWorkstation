import kivy

from kivy.app import App
from kivy.uix.actionbar import ActionBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget


class ActionBar_main(Widget):
    pass


class ActionbarApp(App):
    def build(self):
        return ActionBar_main()


if __name__ == "__main__":
    ActionbarApp().run()
