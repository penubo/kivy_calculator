from kivy.app import App
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, ListProperty
from kivy.graphics import Line, Rectangle, Bezier
from rbn import build, get_infix_notation, calculate
from math import sin, cos, tan, log, pi, pow, sqrt
import rbn
from pprint import pprint

def dist(a, b):
    return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

class MainInterface(BoxLayout):
    pass


class CalculatorScreen(Screen):
    pass


class GraphScreen(Screen):
    pass


class GraphWidget(Widget):
    def __init__(self, **kwargs):
        super(GraphWidget, self).__init__(**kwargs)
        self.t_point = []
        self.rbns = []
        self.scale = 2.0
        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
        self.update_canvas()

    @staticmethod
    def get_pivot(alist):
        result = list()
        for i in range(len(alist)-2,-1,-1):
            if dist(alist[i+1], alist[i]) > 500:
                result.append(i+1)
        return result

    @staticmethod
    def doubled_list(alist):
        result = list()
        for x in alist:
            result.append(x)
            result.append(x)
        return result

    @staticmethod
    def chunks(l, n):
        for i in range(0, len(l), n):
            yield l[i:i+n]

    def zoom(self, to):
        if to == 'default':
            self.scale = 2.0
        elif to == 'out':
            self.scale *= 0.5
        elif to == 'in':
            self.scale *= 2
        self.update_canvas()

    def update_canvas(self, *args):
        if(self.rbns):
            dots = list()

            for pixel_x in range(0, int(self.width)):
                try:
                    # press x value by multiplying 1/scale
                    x = (pixel_x-self.center_x)*1/self.scale
                    # stretch y value by multiplying scale
                    pixel_y = float(calculate(self.rbns, x))*self.scale + self.center_y
                    # get pixel position
                    dots.append([pixel_x, pixel_y])
                except ValueError: # ignore unexceptable values such as log(-1)
                    pass
                except OverflowError:
                    pass

            dots = [[x, y] for x, y in dots if y > -1000 and y < self.height+1000]
            pivots = self.get_pivot(dots)
            pivots.reverse()
            pivots = self.doubled_list(pivots)
            pivots.insert(0, 0)
            pivots.append(len(dots))
            point_sets = list()

            for pivot in self.chunks(pivots, 2):
                point_sets.append(dots[pivot[0]:pivot[1]])

            self.canvas.before.clear()

            with self.canvas.before:
                for points in point_sets:
                    Line(points=points)

    def on_touch_down(self, touch):
        print(str(dir(touch)))
        self.t_point = [touch.x, touch.y]

    def on_touch_move(self, touch):
        self.dist = [touch.x-self.t_point[0], touch.y-self.t_point[1]]
        self.center = self.add_point(self.center, self.dist)
        self.t_point = [touch.x, touch.y]

    def go_center(self):
        self.center = [self.width/2, self.height/2]

    def draw_it(self, expression):
        infix_tokens = get_infix_notation(expression)
        self.rbns = build(infix_tokens)
        self.scale = 2.0
        self.update_canvas()
        self.go_center()

    @staticmethod
    def add_point(p_a, p_b):
        return [p_a[0] + p_b[0], p_a[1] + p_b[1]]


class CLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(CLayout, self).__init__(**kwargs)
    text_label = ObjectProperty(None)
    rbn_tokens = ListProperty([])

    def evaluate(self, string):
        infix_tokens = get_infix_notation(string)
        self.rbn_tokens = build(infix_tokens)
        self.display.text = str(calculate(self.rbn_tokens))

    def delete(self, text):
        text_list = list(text)
        if(text_list):
            text_list.pop()
            self.display.text = ''.join(text_list)


class Calculator(App):
    def build(self):
        interface = MainInterface()
        return interface


if __name__ == '__main__':
    Window.fullscreen=False
    Config.set('graphics', 'fullscreen', 'auto')
    Config.set('graphics', 'width', '600')
    Config.set('graphics', 'height', '300')
    Config.write()
    Calculator().run()
