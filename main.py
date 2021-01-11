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
    stars_texture = ObjectProperty(None)
    floor_texture = ObjectProperty(None)
    city_texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.stars_texture = Image(source="img/background/stars.png").texture
        self.stars_texture.wrap = "repeat"
        self.stars_texture.uvsize = (Window.width/ self.stars_texture.width, -1)

        self.city_texture = Image(source="img/background/city.png").texture
        self.city_texture.wrap = "repeat"
        self.city_texture.uvsize = (Window.width / self.city_texture.width, -1)

        self.floor_texture = Image(source="img/background/floor.png").texture
        self.floor_texture.wrap = "repeat"
        self.floor_texture.uvsize = (Window.width / self.floor_texture.width, -1)

    def scroll_texture(self, time_passed):
        self.stars_texture.uvpos = ((self.stars_texture.uvpos[0] + time_passed/1.5) % Window.width, self.stars_texture.uvpos[1])
        self.floor_texture.uvpos = ((self.floor_texture.uvpos[0] + time_passed/2.1) % Window.width, self.floor_texture.uvpos[1])
        self.city_texture.uvpos = ((self.city_texture.uvpos[0] + time_passed/1.3) % Window.width, self.city_texture.uvpos[1])
        
        texture = self.property("stars_texture")
        texture.dispatch(self)

        texture = self.property("city_texture")
        texture.dispatch(self)

        texture = self.property("floor_texture")
        texture.dispatch(self)


from random import randint
from kivy.properties import NumericProperty

class Player(Image):
    velocity = NumericProperty(0)
    def on_touch_down(self, touch):
        self.source = "img/body/body_fly.png"
        self.velocity = 225
        super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.source = "img/body/body_normal.png"
        super().on_touch_up(touch)


class MainApp(App):
    pipes = []
    GRAVITY = 500
    was_colliding = False

    def check_score_init(self):
        highscore = "0"
        with open("settings.txt", mode="r") as settingsFile:
            word = settingsFile.readline().split()
            if word[0] == "Highscore":
                highscore = word[2]
        return highscore

    def check_score(self):
        if int(self.root.ids.score.text) > int(self.root.ids.high_score.text):
            self.root.ids.high_score.text = self.root.ids.score.text
        with open("settings.txt", mode="w+") as settingsFile:
            settingsFile.writelines("Highscore = " + self.root.ids.high_score.text + "\n")


    def move_player(self, time_passed):
        player = self.root.ids.player
        player.y = player.y + player.velocity * time_passed
        player.velocity = player.velocity - self.GRAVITY * time_passed
        self.check_collision()

    def check_collision(self):
        player = self.root.ids.player
        is_colliding = False
        for pipe in self.pipes:
            if pipe.collide_widget(player):
                is_colliding = True
                if player.y < (pipe.pipe_center-pipe.GAP_SIZE/2.0):
                    self.game_over()
                if player.top > (pipe.pipe_center+pipe.GAP_SIZE/2.0):
                    self.game_over()
        if player.y < 114:
            self.game_over()
        if player.top > Window.height:
            self.game_over()

        if self.was_colliding and not is_colliding:
            self.root.ids.score.text = str(int(self.root.ids.score.text) + 1)
        self.was_colliding = is_colliding

    def game_over(self):
        self.check_score()
        self.root.ids.player.pos = 20, (self.root.height - 114) / 2.0
        for pipe in self.pipes:
            self.root.remove_widget(pipe)
        self.frame.cancel()
        self.root.ids.start_button.disabled = False
        self.root.ids.start_button.opacity = 1
        self.root.ids.high_score.opacity = 1
        self.root.ids.high_score_text.opacity = 1

    def next_frame(self, time_passed):
        self.move_player(time_passed)
        self.move_pipes(time_passed)
        self.root.ids.background.scroll_texture(time_passed)

    def start_game(self):
        self.root.ids.high_score.opacity = 0
        self.root.ids.high_score_text.opacity = 0
        self.root.ids.score.text = "0"
        self.was_colliding = False
        self.pipes = []
        self.frame = Clock.schedule_interval(self.next_frame, 1/60.)
        # Create the pipes
        num_pipes = 3
        distance_between_pipes = (Window.width / (num_pipes - 1)) + 50
        for i in range(num_pipes):
            pipe = Pipe()
            pipe.pipe_center = randint((114 + 120), (self.root.height - 120))
            pipe.size_hint = (None,None)
            pipe.pos = (i*distance_between_pipes + 500, 114)
            pipe.size = (64, self.root.height - 114)

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
            most_left_pipe.pipe_center = randint((114 + 120), (self.root.height - 120))

if __name__ == "__main__":
    MainApp().run()