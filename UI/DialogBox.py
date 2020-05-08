import arcade

class DialogBox(arcade.DialogueBox):
    def __init__(self, view, x, y, width, height, color=None, theme=None):
        if theme is None:
            theme = view.window.theme
        super().__init__(x, y, width, height, color, theme)