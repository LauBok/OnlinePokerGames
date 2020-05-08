import arcade

class Button(arcade.gui.TextButton):
    def __init__(self, view, x=0, y=0, width=100, height=40, text="New Game", theme=None, call_back = None):
        if theme is None:
            theme = view.window.theme
        super().__init__(x, y, width, height, text, theme=theme)
        self.hovered = False
        self.locked = False
        self.view = view
        self.visible = True

    @property
    def window(self):
        return self.view.window

    @property
    def client(self):
        return self.view.window.client
    
    def lock(self):
        self.locked = True
        self.pressed = False
        self.hovered = False
    
    def unlock(self):
        self.locked = False
    
    def draw_texture_theme(self):
        if self.locked:
            arcade.draw_texture_rectangle(self.center_x, self.center_y, self.width, self.height, self.locked_texture)
        elif self.pressed:
            arcade.draw_texture_rectangle(self.center_x, self.center_y, self.width, self.height, self.clicked_texture)
        elif self.hovered:
            arcade.draw_texture_rectangle(self.center_x, self.center_y, self.width, self.height, self.hover_texture)
        else:
            arcade.draw_texture_rectangle(self.center_x, self.center_y, self.width, self.height, self.normal_texture)

    def on_draw(self):
        if self.visible:
            super().draw()

    def on_press(self):
        pass

    def on_release(self):
        pass

    def check_mouse_press(self, x, y):
        if not self.visible or self.locked:
            return
        if self.check_mouse_inside(x, y):
            self.pressed = True
            self.hovered = False
            self.on_press()
    
    def check_mouse_release(self, x, y):
        if not self.visible or self.locked:
            return 
        if self.pressed:
            self.pressed = False
        if self.check_mouse_inside(x, y):
            self.on_release()
    
    def check_mouse_hover(self, x, y):
        if not self.visible or self.locked:
            return 
        if self.check_mouse_inside(x, y):
            if not self.pressed:
                self.hovered = True
        else:
            self.hovered = False
    
    def check_mouse_inside(self, x, y):
        if x > self.center_x + self.width / 2:
            return False
        if x < self.center_x - self.width / 2:
            return False
        if y > self.center_y + self.height / 2:
            return False
        if y < self.center_y - self.height / 2:
            return False
        return True