from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ObjectProperty, BooleanProperty, NumericProperty, \
     ReferenceListProperty, StringProperty
from kivy.vector import Vector
from kivy.graphics import Ellipse
import random


endGame = False

class Board(Widget):
    ledge = ObjectProperty(None)
    redge = ObjectProperty(None)
    tedge = ObjectProperty(None)
    bedge = ObjectProperty(None)
    snake = ObjectProperty(None)
    egg = ObjectProperty(None)
    speed = NumericProperty(7.5)
    score = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self._keyboard.bind(on_key_down = self.keyPressed)

    def keyboard_closed(self):
        self._keyboard.unbind(on_key_down = self.keyPressed)
        self._keyboard = None

    def keyPressed(self, keyboard, keycode, text, modifiers):
        if self.snake.velocity_x == 0 and self.snake.velocity_y == 0:
            self.score = 0
        if keycode[1] == 'numpad8':
            self.snake.velocity_x = 0
            self.snake.velocity_y = self.speed
            self.snake.src = 'creature_up.png'
        elif keycode[1] == 'numpad2':
            self.snake.velocity_x = 0
            self.snake.velocity_y = -1 * self.speed
            self.snake.src = 'creature_down.png'
        elif keycode[1] == 'numpad4':
            self.snake.velocity_x = -1 * self.speed
            self.snake.velocity_y = 0
            self.snake.src = 'creature_left.png'
        elif keycode[1] == 'numpad6':
            self.snake.velocity_x = self.speed
            self.snake.velocity_y = 0
            self.snake.src = 'creature_right.png'
        elif keycode[1] == 'numpad9':
            self.snake.velocity_x = self.speed / pow(2, 0.5)
            self.snake.velocity_y = self.speed / pow(2, 0.5)
        elif keycode[1] == 'numpad7':
            self.snake.velocity_x = -1 * self.speed / pow(2, 0.5)
            self.snake.velocity_y = self.speed / pow(2, 0.5)
        elif keycode[1] == 'numpad1':
            self.snake.velocity_x = -1 * self.speed / pow(2, 0.5)
            self.snake.velocity_y = -1 * self.speed / pow(2, 0.5)
        elif keycode[1] == 'numpad3':
            self.snake.velocity_x = self.speed / pow(2, 0.5)
            self.snake.velocity_y = -1 * self.speed / pow(2, 0.5)

    def update(self, dt):
        global endGame
        if endGame == True:
            self.startGame()
            endGame = False
        else:            
            self.snake.move()
            self.ledge.collide(self.snake)
            self.redge.collide(self.snake)
            self.tedge.collide(self.snake)
            self.bedge.collide(self.snake)
            self.barr.collide(self.snake)
            snegg = self.snake.collide(self.egg)
            if snegg == 1:
                self.score += 1
                self.speed *= 1.05
                self.egg.place(self.center, self.pos, self.size)

    def startGame(self):
        self.speed = 7.5
        self.egg.place(self.center, self.pos, self.size)
        self.snake.pos = 200, 100
        self.snake.velocity_x = 0
        self.snake.velocity_y = 0
        self.snake.src = 'creature_right.png'


class LongEdge(Widget):
    def __init__(self, **kwargs):
        super(LongEdge, self).__init__(**kwargs)
    def collide(self, snake):
        if self.collide_widget(snake):
            global endGame
            endGame = True


class WideEdge(Widget):
    def collide(self, snake):
        if self.collide_widget(snake):
            global endGame
            endGame = True


class Barrier(Widget):
    def collide(self, snake):
        if self.collide_widget(snake):
            global endGame
            endGame = True


class Snake(Widget):
    src = StringProperty('')
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos    
    
    def collide(self, egg):
        if self.collide_widget(egg):
            return 1


class Egg(Widget):
    def place(self, pctr, ppos, psize):
        rnd_x = list(range(int(ppos[0]) + 50, int(pctr[0]) - 100 - self.width)
        ) + list(range(int(pctr[0]) + 100, int(psize[0]) - self.width - 50))
        rnd_y = list(range(int(psize[1]) - self.height - 50, int(pctr[1]) + 38, -1)
        ) + list(range(int(ppos[1]) + 50, int(pctr[1]) - 68))
        
        self.x = random.choice(rnd_x)
        self.y = random.choice(rnd_y)


class xenzApp(App):
    def build(self):
        game = Board()
        game.startGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    xenzApp().run()
