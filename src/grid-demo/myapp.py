from textual.app import App
from textual.containers import Grid
from textual.widgets import Button, Static

class Foo( Static ):
    def compose(self):
        yield Button( self.id )

class GridApp(App):
    CSS_PATH = "myapp.tcss"

    def compose(self):
        with Grid(id="buttons"):
            for my in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLM":
                yield Foo(my+my+my, id=my)


if __name__ == "__main__":
    GridApp().run()
