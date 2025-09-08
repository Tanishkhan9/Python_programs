from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical")

        self.label = Label(text="Hello! Welcome to my app 😊", font_size=24)
        btn = Button(text="Click Me!", font_size=20)
        btn.bind(on_press=self.on_button_click)

        layout.add_widget(self.label)
        layout.add_widget(btn)
        return layout

    def on_button_click(self, instance):
        self.label.text = "You clicked the button 🎉"

if __name__ == "__main__":
    MyApp().run()