import kivy
kivy.require('1.7.0') 

from kivy.app import App
from kivy.uix.label import Label


class MyApp(App):

    def build(self):
        return Label(text='GUI TEST')


if __name__ == '__main__':
    MyApp().run()