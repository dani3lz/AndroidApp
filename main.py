from kivy.app import App
from kivy.config import Config

Config.set("graphics", "resizable", 0)
Config.set("graphics", "width", 500)
Config.set("graphics", "height", 800)

from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.widget import Widget
from pipe import Pipe

class Background(Widget):
    cloud_texture = ObjectProperty(None)
    floor_texture = ObjectProperty(None)
    city_texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cloud_texture = Image(source="cloud.png").texture
        self.cloud_texture.wrap = "repeat"
        self.cloud_texture.uvsize = (Window.width/ self.cloud_texture.width, -1)

        self.city_texture = Image(source="city.png").texture
        self.city_texture.wrap = "repeat"
        self.city_texture.uvsize = (Window.width / self.city_texture.width, -1)

        self.floor_texture = Image(source="floor.png").texture
        self.floor_texture.wrap = "repeat"
        self.floor_texture.uvsize = (Window.width / self.floor_texture.width, -1)

    def scroll_texture(self, time_passed):
        self.cloud_texture.uvpos = ((self.cloud_texture.uvpos[0] + time_passed/1.5) % Window.width, self.cloud_texture.uvpos[1])
        self.floor_texture.uvpos = ((self.floor_texture.uvpos[0] + time_passed/2.1) % Window.width, self.floor_texture.uvpos[1])
        self.city_texture.uvpos = ((self.city_texture.uvpos[0] + time_passed/1.3) % Window.width, self.city_texture.uvpos[1])
        
        texture = self.property("cloud_texture")
        texture.dispatch(self)

        texture = self.property("city_texture")
        texture.dispatch(self)

        texture = self.property("floor_texture")
        texture.dispatch(self)

from random import randint
from kivy.properties import NumericProperty

class Bison(Image):
    velocity = NumericProperty(0)
    def on_touch_down(self, touch):
        self.source = "bison2.png"
        self.velocity = 225
        super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.source = "bison1.png"
        super().on_touch_up(touch)

class MainApp(App):
    pipes = []
    GRAVITY = 500
    was_colliding = False


    def move_bison(self, time_passed):
        bison = self.root.ids.bison
        bison.y = bison.y + bison.velocity * time_passed
        bison.velocity = bison.velocity - self.GRAVITY * time_passed
        self.check_collision()

    def check_collision(self):
        bison = self.root.ids.bison
        is_colliding = False
        for pipe in self.pipes:
            if pipe.collide_widget(bison):
                is_colliding = True
                if bison.y < (pipe.pipe_center-pipe.GAP_SIZE/2.0):
                    self.game_over()
                if bison.top > (pipe.pipe_center+pipe.GAP_SIZE/2.0):
                    self.game_over()
        if bison.y < 38:
            self.game_over()
        if bison.top > Window.height:
            self.game_over()

        if self.was_colliding and not is_colliding:
            self.root.ids.score.text = str(int(self.root.ids.score.text) + 1)
        self.was_colliding = is_colliding

    def game_over(self):
        self.root.ids.bison.pos = 20, (self.root.height - 38) / 2.0
        for pipe in self.pipes:
            self.root.remove_widget(pipe)
        self.frame.cancel()
        self.root.ids.start_button.disabled = False
        self.root.ids.start_button.opacity = 1

    def next_frame(self, time_passed):
        self.move_bison(time_passed)
        self.move_pipes(time_passed)
        self.root.ids.background.scroll_texture(time_passed)

    def start_game(self):
        self.root.ids.score.text = "0"
        self.was_colliding = False
        self.pipes = []
        self.frame = Clock.schedule_interval(self.next_frame, 1/60.)
        # Create the pipes
        num_pipes = 3
        distance_between_pipes = (Window.width / (num_pipes - 1)) + 50
        for i in range(num_pipes):
            pipe = Pipe()
            pipe.pipe_center = randint((38 + 100), (self.root.height - 100))
            pipe.size_hint = (None,None)
            pipe.pos = (i*distance_between_pipes + 500, 38)
            pipe.size = (100, self.root.height - 38)

            self.pipes.append(pipe)
            self.root.add_widget(pipe, -1)

    def move_pipes(self, time_passed):
        # Move pipes
        for pipe in self.pipes:
            pipe.x -= time_passed * 100

        # Check
        num_pipes = 3
        distance_between_pipes = (Window.width / (num_pipes - 1)) + 50
        pipe_xs = list(map(lambda pipe: pipe.x, self.pipes))
        right_most_x = max(pipe_xs)
        if right_most_x <= Window.width - distance_between_pipes:
            most_left_pipe = self.pipes[pipe_xs.index(min(pipe_xs))]
            most_left_pipe.x = Window.width
            most_left_pipe.pipe_center = randint((38 + 100), (self.root.height - 100))






if __name__ == "__main__":
    MainApp().run()