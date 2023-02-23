import kivy  # noqa: F401

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget

from . import metronome
from . import player


class MainbarView(Widget):
    sm = ObjectProperty()
    mode = ObjectProperty()
    playback = ObjectProperty()
    volume = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm.add_widget(metronome.MetronomeView(name="m"))
        self.sm.add_widget(player.PlayerView(name="p"))

        self.set_mode(self.mode, "metronome")
        self.mode.bind(text=self.set_mode)

    def set_mode(self, widget, text) -> None:
        # default: "metronome", "main", "50"
        if text == "metronome":
            self.sm.current = "m"
            self.mode.text = "metronome"
            self.mode.values = "metronome", "player"
            self.playback.text = "main"
            self.playback.values = "main", "keyboard", "metronme"
            self.volume.value = 50
        elif text == "player":
            self.sm.current = "p"
            self.mode.text = "player"
            self.mode.values = "metronome", "player"
            self.playback.text = "main"
            self.playback.values = "main", "keyboard", "player"
            self.volume.value = 50


class MenubarApp(App):
    def build(self):
        self.title = "AudioWorkstation"
        return MainbarView()


if __name__ == "__main__":
    MenubarApp().run()
