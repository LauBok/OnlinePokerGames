import arcade

class TextDisplay(arcade.TextDisplay):
    def draw_text(self):
        if self.highlighted:
            arcade.draw_text(self.text[:self.cursor_index] + self.symbol + self.text[self.cursor_index:],
                             self.x-self.width/2.1, self.y, self.font_color, font_size=self.font_size,
                             align = "center", 
                             anchor_y="center", font_name=self.font_name)
        else:
            arcade.draw_text(self.text, self.x - self.width/2.1, self.y, self.font_color, font_size=self.font_size,
                             align = "center", anchor_x="center",
                             anchor_y="center", font_name=self.font_name)
    def draw(self):
        if self.texture is None:
            self.color_theme_draw()
        else:
            self.texture_theme_draw()

class InputBox(arcade.TextBox):
    def __init__(self, view, x=0, y=0, width=100, height=40, text="New Game", theme=None, outline_color=arcade.color.BLACK, font_size=24,
                 shadow_color=arcade.color.WHITE_SMOKE, highlight_color=arcade.color.WHITE):
        if theme is None:
            theme = view.window.theme
        self.theme = theme
        self.theme.set_font(18, arcade.color.WHITE)
        if self.theme:
            self.text_display = TextDisplay(x, y, width, height, theme=self.theme)
            self.text_storage = arcade.TextStorage(width * 1.5, theme=self.theme)
        else:
            self.text_display = TextDisplay(x, y, width, height, outline_color, shadow_color, highlight_color)
            self.text_storage = arcade.TextStorage(width * 1.5, font_size)
        self.text = ""
    
    def update(self, delta_time, key):
        if self.text_display.highlighted:
            self.text, symbol, cursor_index = self.text_storage.update(delta_time, key)
            self.text_display.update(delta_time, self.text, symbol, cursor_index)