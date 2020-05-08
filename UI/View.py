import arcade

class View(arcade.View):
    def __init__(self, window, background):
        super().__init__()
        self.window = window
        self.WIDTH, self.HEIGHT = window.get_size()
        if background is not None:
            self.Background = arcade.load_texture(background)
    
    @property
    def client(self):
        return self.window.client

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """
        Override this function to add mouse functionality.

        :param float x: x position of mouse
        :param float y: y position of mouse
        :param float dx: Change in x since the last time this method was called
        :param float dy: Change in y since the last time this method was called
        """
        try:
            if self.button_list:
                for button_widget in self.button_list:
                    button_widget.check_mouse_hover(x, y)
        except AttributeError:
            pass
    
    def on_draw(self, *args):
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.WIDTH, self.HEIGHT,
                                            self.Background)
        for a in args:
            a.draw()
        super().on_draw()