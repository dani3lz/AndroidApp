from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty, ListProperty
from kivy.uix.image import Image
from kivy.clock import Clock

class Pipe(Widget):

    high_pipe = 68.
    GAP_SIZE = NumericProperty(285)
    CAP_SIZE = NumericProperty(68)
    pipe_center = NumericProperty(0)
    bottom_body_position = NumericProperty(0)
    bottom_cap_position = NumericProperty(0)
    top_body_position = NumericProperty(0)
    top_cap_position = NumericProperty(0)
    big_pipe = NumericProperty(0)

    pipe_body_texture = ObjectProperty(None)
    lower_tex_coords = ListProperty((0, 0, 1, 0, 1, 1, 0, 1))
    top_tex_coords = ListProperty((0, 0, 1, 0, 1, 1, 0, 1))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pipe_body_texture = Image(source="img/pipe/pipe.png").texture
        self.pipe_body_texture.wrap = "repeat"

    def on_size(self, *args):
        lower_body_size = self.bottom_cap_position - self.bottom_body_position
        top_body_size = self.top - self.top_body_position

        self.lower_tex_coords[5] = lower_body_size / self.high_pipe
        self.lower_tex_coords[7] = lower_body_size / self.high_pipe

        self.top_tex_coords[5] = top_body_size / self.high_pipe
        self.top_tex_coords[7] = top_body_size / self.high_pipe

    def on_pipe_center(self, *args):
        Clock.schedule_once(self.on_size, 0)


