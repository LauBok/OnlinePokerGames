import socket
import arcade
from UI.Button import Button
from UI.View import View
from UI.InputBox import InputBox
from message import Message
from collections import deque
from coolname import generate_slug
from util.func import Case

class NewGameButton(Button):
    def __init__(self, view, x=0, y=0, width=100, height=40, text="New Game", theme=None):
        super().__init__(view, x, y, width, height, text, theme=theme)
    
    def on_release(self):
        self.window.show_view(self.client.loginview)
                  
class QuitGameButton(Button):
    def __init__(self, view, x=0, y=0, width=100, height=40, text="Quit", theme=None):
        super().__init__(view, x, y, width, height, text, theme=theme)

    def on_release(self):
        self.view.window.close()

class LoginButton(Button):
    def __init__(self, view, x=0, y=0, width=100, height=40, text="Login", theme=None):
        super().__init__(view, x, y, width, height, text, theme=theme)

    def on_release(self):
        self.lock()
        result, msg = self.client.connect('127.0.0.1', 28888)
        print("login", msg)
        self.unlock()
        if result == False:
            pass
        else:
            print(msg)
            self.client.roomview.host = msg['HOST']
            self.client.send_data({"NAME": self.view.name})
            self.window.show_view(self.client.roomview)

class BackGameButton(Button):
    def __init__(self, view, x=0, y=0, width=100, height=40, text="Back", theme=None, backview = None):
        super().__init__(view, x, y, width, height, text, theme=theme)
        self.backview = backview

    def on_release(self):
        self.window.show_view(self.backview)

class SeatButton(Button):
    def __init__(self, view, x=0, y=0, width=40, height=40, text="", theme=None, id = None):
        super().__init__(view, x, y, width, height, text, theme=theme)
        self.id = id
    def on_release(self):
        print(SeatButton)
        result = self.client.send_data({
            "TYPE": "SEATREQUEST",
            "ID": self.id
        })

class StartRoomButton(Button):
    def __init__(self, view, x=0, y=0, width=100, height=80, text="Start", theme=None):
        super().__init__(view, x, y, width, height, text, theme=theme)
    def on_release(self):
        result = self.client.send_data({
            "TYPE": "STARTREQUEST"
        })        

class MenuView(View):
    def __init__(self, window, background = None):
        super().__init__(window, background)
        self.Menulist = arcade.SpriteList()
        self.setup()     

    def setup(self):
        self.MenuSprite = arcade.Sprite("image/GUI/Menu.png")
        self.MenuSprite.center_x = self.WIDTH / 2
        self.MenuSprite.center_y = 370
        self.MenuSprite._set_height(400)
        self.MenuSprite._set_width(300)
        self.Menulist.append(self.MenuSprite)

        btn_new_local_game = NewGameButton(self, self.WIDTH / 2, 450, 180, 50, text = "Local Game")
        btn_new_online_game = NewGameButton(self, self.WIDTH / 2, 370, 180, 50, text = "Online Game")
        btn_quit_game = QuitGameButton(self, self.WIDTH / 2, 290, 180, 50, text = "Quit")
        self.button_list = [btn_new_local_game, btn_new_online_game, btn_quit_game]
        
    def on_show(self):
        arcade.set_background_color(arcade.color.BLUE_GREEN)
    
    def on_draw(self):
        arcade.start_render()
        super().on_draw(self.Menulist)

class LoginView(View):
    def __init__(self, window, background = None):
        super().__init__(window, background)
        self.Menulist = arcade.SpriteList()
        self.setup()     

    def setup(self):
        self.MenuSprite = arcade.Sprite("image/GUI/Menu.png")
        self.MenuSprite.center_x = self.WIDTH / 2
        self.MenuSprite.center_y = self.HEIGHT / 2
        self.MenuSprite._set_height(300)
        self.MenuSprite._set_width(400)
        self.Menulist.append(self.MenuSprite)

        btn_back = BackGameButton(self, self.WIDTH / 2 - 80, self.HEIGHT / 2 - 80, 70, 50, 
            text = "Back", backview = self.client.menuview)
        btn_enter = LoginButton(self, self.WIDTH / 2 + 80, self.HEIGHT / 2 - 80, 70, 50, text = "Enter")
        self.button_list = [btn_back, btn_enter]

        self.name = generate_slug(2)
        
    def on_show(self):
        arcade.set_background_color(arcade.color.BLUE_GREEN)
    
    def on_draw(self):
        arcade.start_render()
        super().on_draw(self.Menulist)
        arcade.draw_text("Welcome!",
                         self.WIDTH / 2, self.HEIGHT / 2 + 40, arcade.color.BLACK_OLIVE, 14, width=200, align="center",
                         anchor_x="center", anchor_y="center")
        arcade.draw_text(self.name,
                         self.WIDTH / 2, self.HEIGHT / 2, arcade.color.BLUE_VIOLET, 18, width=200, align="center",
                         anchor_x="center", anchor_y="center")
        
class RoomView(View):
    def __init__(self, window, background = None):
        super().__init__(window, background)
        self.Menulist = arcade.SpriteList()
        self.setup()    
        self.host = False 

    def setup(self):
        center_W = 800 / 2
        center_H = self.HEIGHT / 2
        shift_W = 200
        shift_H = 140
        self.button_list = [None] * 4
        self.button_list[0] = SeatButton(self, center_W, center_H - shift_H, 60, 60, '0', theme = None, id = 0)
        self.button_list[1] = SeatButton(self, center_W + shift_W, center_H, 60, 60, '1', theme = None, id = 1)
        self.button_list[2] = SeatButton(self, center_W, center_H + shift_H, 60, 60, '2', theme = None, id = 2)
        self.button_list[3] = SeatButton(self, center_W - shift_W, center_H, 60, 60, '3', theme = None, id = 3)
        self.button_list.append(StartRoomButton(self, 1000, 210, 180, 60))

        self.MenuSprite = arcade.Sprite("image/GUI/Menu.png")
        self.MenuSprite.center_x = 1000
        self.MenuSprite.center_y = self.HEIGHT / 2
        self.MenuSprite._set_height(600)
        self.MenuSprite._set_width(400)
        self.Menulist.append(self.MenuSprite)

        self.seatnames = []
        for i in range(4):
            self.seatnames.append(arcade.TextLabel(
                "", self.button_list[i].center_x, self.button_list[i].center_y - 40, font_size = 12, font_name = 'Calibri'
            ))
        self.onlinenames = []
        
    def on_show(self):
        arcade.set_background_color(arcade.color.BLUE_GREEN)
        if not self.host:
            self.button_list.remove(self.button_list[-1])
    
    def on_update(self, time):
        res = self.client.send_data({"TYPE": "ROOMINFO"})
        if res["TYPE"] == "RESPONSE":
            for id, seat in enumerate(res["SEAT"]):
                if seat is None:
                    self.button_list[id].unlock()
                    self.seatnames[id].text = ""
                else:
                    self.button_list[id].lock()
                    self.seatnames[id].text = seat
            self.onlinenames = res["ONLINE"]
        elif res["TYPE"] == "INFORM" and res["MESSAGE"] == "STARTGAME":
            self.window.show_view(self.client.dispatchview)
    
    def on_mouse_release(self, x, y, button, modifiers):
        super().on_mouse_release(x, y, button, modifiers)
        print("mouse", x, y)
        if self.MenuSprite.collides_with_point(arcade.Point(x, y)):
            if len(self.button_list) == 5:
                if self.button_list[-1].check_mouse_inside(x, y):
                    return
            res = self.client.send_data({"TYPE": "SEATCANCELREQUEST"})

    
    def on_draw(self):
        arcade.start_render()
        super().on_draw(self.Menulist)
        for seatname in self.seatnames:
            seatname.draw()
        arcade.draw_text("ONLINE", 1000, 665, arcade.color.BLUEBERRY, 28, bold = True, anchor_x="center",
            anchor_y= "center", align = "center", font_name = 'calibri')
        for id, name in enumerate(self.onlinenames):
            arcade.draw_text(name, 1000, 560 - 40 * id, arcade.color.BLACK, 16, anchor_x="center",
            anchor_y= "center", align = "left")

class DispatchView(View):
    CARD_WIDTH = 100
    CARD_OVERLAP_WIDTH = 18
    CARD_OVERLAP_HEIGHT = 15
    CARD_WIDTH_SMALL = 75
    CARD_OVERLAP_WIDTH_SMALL = 13.5
    SUIT_SIZE = 27
    def __init__(self, window, background = None):
        super().__init__(window, background)
        self.textureList = arcade.load_spritesheet('image/cardsheet_style2.png',180,250,15,60)
        self.HandLists = [arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList()]
        self.FrontLists = [arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList()]
        self.panel = arcade.SpriteList()
        self.SuitList = arcade.SpriteList()
        self.TimerList = arcade.SpriteList()
        self.LevelList = arcade.SpriteList()
        self.ScoreList = arcade.SpriteList()
        self.cursuit = None
        self.currank = None
        self.ranklevel = [6, 3]
        self.suits = [False, False, False, False, False]
        self.timer = [0, 0, 0, 0]
        self.score = 0
        self.cards = []
        self.cardcount = []
        self.front = []
        self.names = ['Goodman', 'Goodman', 'Goodman', 'Goodman']
        self.setup()
    def setup(self):
        self.BoardSprite = arcade.Sprite("image/GUI/Menu.png")
        self.BoardSprite.center_x = self.WIDTH - 90
        self.BoardSprite.center_y = self.HEIGHT - 80
        self.BoardSprite._set_height(150)
        self.BoardSprite._set_width(180)
        self.panel.append(self.BoardSprite)
        self.SuitPanelSprite = arcade.Sprite("image/GUI/bar.png")
        self.SuitPanelSprite._set_alpha(120)
        self.SuitPanelSprite.center_x = 870
        self.SuitPanelSprite.center_y = 285
        self.SuitPanelSprite._set_height(120)
        self.SuitPanelSprite._set_width(280)
        self.panel.append(self.SuitPanelSprite)
        
        suit_textures = [[None] * 5, [None] * 5]
        # NT, Spade, Heart, Club, Diamond
        tmp = arcade.load_spritesheet('image/card-suits-blank.png', 256,256,2,4)
        suit_textures[0][1:] = [tmp[i] for i in [0, 2, 3, 1]]
        tmp = arcade.load_spritesheet('image/card-suits-color.png', 256,256,2,4)
        suit_textures[1][1:] = [tmp[i] for i in [0, 2, 3, 1]]
        suit_textures[0][0] = arcade.load_texture('image/NT-blank.png')
        suit_textures[1][0] = arcade.load_texture('image/NT-color.png')
        for i in range(5):
            sprite = arcade.Sprite()
            sprite.append_texture(suit_textures[0][i])
            sprite.append_texture(suit_textures[1][i])
            sprite._set_center_x(self.SuitPanelSprite.center_x - 10 + (i - 2) * (self.SUIT_SIZE + 3))
            sprite._set_center_y(self.SuitPanelSprite.center_y + 5)
            sprite._set_scale(self.SUIT_SIZE / 256)
            sprite.set_texture(0)
            self.SuitList.append(sprite)
        
        num_textures = arcade.load_spritesheet('image/numbersheet_style1.png', 30, 45, 10, 10)
        x = self.BoardSprite.center_x
        y = self.BoardSprite.center_y - 5
        for i in range(3):
            sprite = arcade.Sprite()
            for j in range(10):
                sprite.append_texture(num_textures[j])
            sprite.set_texture(0)
            sprite._set_scale(0.6)
            sprite._set_center_x(x + 18 * (i - 1))
            sprite._set_center_y(y)
            self.ScoreList.append(sprite)
        
        level_textures = arcade.load_spritesheet('image/levelsheet.png', 100, 128, 13, 13)
        for i in range(4):
            sprite = arcade.Sprite()
            for j in range(13):
                sprite.append_texture(level_textures[j])
            sprite._set_scale(0.2)
            sprite.set_texture(0)
            self.LevelList.append(sprite)
        self.LevelList[0]._set_center_x(x)
        self.LevelList[0]._set_center_y(y - 40)
        self.LevelList[1]._set_center_x(x + 50)
        self.LevelList[1]._set_center_y(y)
        self.LevelList[2]._set_center_x(x)
        self.LevelList[2]._set_center_y(y + 40)
        self.LevelList[3]._set_center_x(x - 50)
        self.LevelList[3]._set_center_y(y)
        
        timer_textures = arcade.load_spritesheet('image/timersheet.png', 120, 160, 10, 10)
        for i in range(4):
            sprite = arcade.Sprite()
            for j in range(10):
                sprite.append_texture(timer_textures[j])
            sprite._set_scale(0.25)
            sprite.set_texture(0)
            self.TimerList.append(sprite)
        self.TimerList[0]._set_center_x(self.WIDTH / 2)
        self.TimerList[0]._set_center_y(300)
        self.TimerList[1]._set_center_x(340)
        self.TimerList[1]._set_center_y(self.HEIGHT / 2 + 10)
        self.TimerList[2]._set_center_x(self.WIDTH / 2)
        self.TimerList[2]._set_center_y(self.HEIGHT - 280)
        self.TimerList[3]._set_center_x(self.WIDTH - 340)
        self.TimerList[3]._set_center_y(self.HEIGHT / 2 + 10)
        
    def on_draw(self):
        arcade.start_render()
        super().on_draw(self.panel)
        for handlist in self.HandLists:
            handlist.draw()
        for frontlist in self.FrontLists:
            frontlist.draw()
        self.TimerList.draw()
        self.SuitList.draw()
        self.ScoreList.draw()
        self.LevelList.draw()
        arcade.draw_text(self.names[0], self.WIDTH / 2, 95, arcade.color.PURPLE_NAVY, align = 'center',
        anchor_x = 'center', anchor_y='center')
        arcade.draw_text(self.names[1], self.WIDTH - 230, 665, arcade.color.PURPLE_NAVY, align = 'center',
        anchor_x = 'center', anchor_y='center')
        arcade.draw_text(self.names[2], self.WIDTH / 2, self.HEIGHT - 75, arcade.color.PURPLE_NAVY, align = 'center',
        anchor_x = 'center', anchor_y='center')
        arcade.draw_text(self.names[3], 230, 665, arcade.color.PURPLE_NAVY, align = 'center',
        anchor_x = 'center', anchor_y='center')
        
    
    def on_update(self, time):
        self.cardcount = [25, 25, 25]
        self.cards = list(range(33))
        res = self.client.send_data({"TYPE": "DISPATCHINFO"})
        print(res)
        if res['TYPE'] == 'RESPONSE':
            self.cards = res['CARDS']
            self.cardcount = res['COUNT']
            self.front = res['FRONT']
            self.cursuit = res['SUIT']
            self.currank = res['RANK']
            self.suits = res['SUITABLE']
            self.ranklevel = res['LEVEL']
            self.timer = res['TIMER']
            self.names = res['NAME']
            self._update_all()
        elif res['TYPE'] == 'INFORM':
            self.window.show_view(self.client.gameview)
    
    def _update_all(self):
        self._update_score()
        self._update_suits()
        self._update_cards()
        self._update_cardcount()
        self._update_front()
        self._update_timer()
        self._update_level()

    def _update_level(self):
        for id, level in enumerate(self.ranklevel):
            self.LevelList[id].set_texture(level % 13)
            self.LevelList[id + 2].set_texture(level % 13)
    
    def _update_score(self):
        for id, card in enumerate(self.ScoreList):
            num = (self.score // 10 ** (2 - id)) % 10
            card.set_texture(num)

    def _update_suits(self):
        for id, suit in enumerate(self.suits):
            self.SuitList[id].set_texture(1 if suit else 0)
    
    def _update_timer(self):
        for id, timer in enumerate(self.timer):
            self.TimerList[id].set_texture(timer)

    def _update_cards(self):
        self.HandLists[0] = arcade.SpriteList()
        length = len(self.cards)
        for id, card in enumerate(self.cards):
            sprite = arcade.Sprite()
            sprite._set_scale(self.CARD_WIDTH / 180)
            total_width = self.CARD_OVERLAP_WIDTH * (length - 1) + self.CARD_WIDTH
            sprite.center_x = self.WIDTH / 2 - total_width / 2 + self.CARD_WIDTH / 2 + self.CARD_OVERLAP_WIDTH * id
            sprite.center_y = 180
            sprite._set_texture2(self.textureList[card])
            self.HandLists[0].append(sprite)
    
    def _update_cardcount(self):
        for idcount, count in enumerate(self.cardcount):
            self.HandLists[idcount + 1] = arcade.SpriteList()
            for i in range(count):
                sprite = arcade.Sprite()
                sprite._set_scale(self.CARD_WIDTH / 180)
                if idcount == 0 or idcount == 2:
                    CARD_HEIGHT = self.CARD_WIDTH * 25 / 18
                    total_height = self.CARD_OVERLAP_HEIGHT * (count - 1) + CARD_HEIGHT
                    sprite.center_x = 230 if idcount == 2 else self.WIDTH - 230
                    sprite.center_y = self.HEIGHT / 2 + total_height / 2 - CARD_HEIGHT / 2 - self.CARD_OVERLAP_HEIGHT * i
                    sprite._set_texture2(self.textureList[59])
                elif idcount == 1:
                    total_width = self.CARD_OVERLAP_WIDTH * (count - 1) + self.CARD_WIDTH
                    sprite.center_x = self.WIDTH / 2 - total_width / 2 + self.CARD_WIDTH / 2 + self.CARD_OVERLAP_WIDTH * i
                    sprite.center_y = self.HEIGHT - 160
                    sprite._set_texture2(self.textureList[59])
                    
                self.HandLists[idcount].append(sprite)
    
    def _update_front(self):
        for idcount, cards in enumerate(self.front):
            self.FrontLists[idcount] = arcade.SpriteList()
            length = len(cards)
            for id, card in enumerate(cards):
                sprite = arcade.Sprite()
                sprite._set_scale(self.CARD_WIDTH_SMALL / 180)
                total_width = self.CARD_OVERLAP_WIDTH_SMALL * (length - 1) + self.CARD_WIDTH_SMALL
                group_center_x = self.WIDTH / 2 - total_width / 2 + self.CARD_WIDTH / 2
                group_center_y = self.HEIGHT / 2 + 10
                case = Case(idcount)
                if case(0):     group_center_y = 320
                elif case(1):   group_center_x = 360
                elif case(2):   group_center_y = self.HEIGHT - 300
                elif case(3):   group_center_x = self.WIDTH - 360 - self.CARD_OVERLAP_WIDTH_SMALL * (length - 1)
                sprite.center_x = group_center_x + self.CARD_OVERLAP_WIDTH * id
                sprite.center_y = group_center_y
                sprite._set_texture2(self.textureList[card])
                    
                self.FrontLists[idcount].append(sprite)
        
    def on_mouse_release(self, x, y, button, modifiers):
        super().on_mouse_release(x, y, button, modifiers)
        print("mouse", x, y)
        for id, suit in enumerate(self.SuitList):
            inside = suit.center_x - 13.5 < x < suit.center_x + 13.5 and suit.center_y - 13.5 < y < suit.center_y + 13.5
            print(id, self.suits[id], inside)
            if self.suits[id] and inside:
                res = self.client.send_data({
                    "TYPE": "SUITREQUEST",
                    "SUIT": id
                })

class GameView(View):
    CARD_WIDTH = 100
    CARD_OVERLAP_WIDTH = 18
    CARD_OVERLAP_HEIGHT = 15
    CARD_WIDTH_SMALL = 75
    CARD_OVERLAP_WIDTH_SMALL = 13.5
    def __init__(self, window, background = None):
        super().__init__(window, background)
        self.textureList = arcade.load_spritesheet('image/cardsheet_style2.png',180,250,15,60)
        self.HandLists = [arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList()]
        self.FrontLists = [arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList()]
        self.panel = arcade.SpriteList()
        self.TimerList = arcade.SpriteList()
        self.LevelList = arcade.SpriteList()
        self.ScoreList = arcade.SpriteList()
        self.cursuit = None
        self.currank = None
        self.ranklevel = [9, 12]
        self.timer = [0, 0, 0, 0]
        self.score = 0
        self.cards = []
        self.selected = []
        self.cardcount = []
        self.front = []
        self.names = ['','','','']
        self.press = None
        self.setup()
    def setup(self):
        self.BoardSprite = arcade.Sprite("image/GUI/Menu.png")
        self.BoardSprite.center_x = self.WIDTH - 90
        self.BoardSprite.center_y = self.HEIGHT - 80
        self.BoardSprite._set_height(150)
        self.BoardSprite._set_width(180)
        self.panel.append(self.BoardSprite)
        
        num_textures = arcade.load_spritesheet('image/numbersheet_style1.png', 30, 45, 10, 10)
        x = self.BoardSprite.center_x
        y = self.BoardSprite.center_y - 5
        for i in range(3):
            sprite = arcade.Sprite()
            for j in range(10):
                sprite.append_texture(num_textures[j])
            sprite.set_texture(0)
            sprite._set_scale(0.6)
            sprite._set_center_x(x + 18 * (i - 1))
            sprite._set_center_y(y)
            self.ScoreList.append(sprite)
        
        level_textures = arcade.load_spritesheet('image/levelsheet.png', 100, 128, 13, 13)
        for i in range(4):
            sprite = arcade.Sprite()
            for j in range(13):
                sprite.append_texture(level_textures[j])
            sprite._set_scale(0.2)
            sprite.set_texture(0)
            self.LevelList.append(sprite)
        self.LevelList[0]._set_center_x(x)
        self.LevelList[0]._set_center_y(y - 40)
        self.LevelList[1]._set_center_x(x + 50)
        self.LevelList[1]._set_center_y(y)
        self.LevelList[2]._set_center_x(x)
        self.LevelList[2]._set_center_y(y + 40)
        self.LevelList[3]._set_center_x(x - 50)
        self.LevelList[3]._set_center_y(y)
            
        timer_textures = arcade.load_spritesheet('image/timersheet.png', 120, 160, 10, 10)
        for i in range(4):
            sprite = arcade.Sprite()
            for j in range(10):
                sprite.append_texture(timer_textures[j])
            sprite._set_scale(0.25)
            sprite.set_texture(0)
            self.TimerList.append(sprite)
        self.TimerList[0]._set_center_x(self.WIDTH / 2)
        self.TimerList[0]._set_center_y(300)
        self.TimerList[1]._set_center_x(340)
        self.TimerList[1]._set_center_y(self.HEIGHT / 2 + 10)
        self.TimerList[2]._set_center_x(self.WIDTH / 2)
        self.TimerList[2]._set_center_y(self.HEIGHT - 280)
        self.TimerList[3]._set_center_x(self.WIDTH - 340)
        self.TimerList[3]._set_center_y(self.HEIGHT / 2 + 10)


        
    def on_draw(self):
        arcade.start_render()
        super().on_draw(self.panel)
        for handlist in self.HandLists:
            handlist.draw()
        for frontlist in self.FrontLists:
            frontlist.draw()
        self.TimerList.draw()
        self.ScoreList.draw()
        self.LevelList.draw()

        arcade.draw_text(self.names[0], self.WIDTH / 2, 95, arcade.color.PURPLE_NAVY, align = 'center',
        anchor_x = 'center', anchor_y='center')
        arcade.draw_text(self.names[1], self.WIDTH - 230, 665, arcade.color.PURPLE_NAVY, align = 'center',
        anchor_x = 'center', anchor_y='center')
        arcade.draw_text(self.names[2], self.WIDTH / 2, self.HEIGHT - 75, arcade.color.PURPLE_NAVY, align = 'center',
        anchor_x = 'center', anchor_y='center')
        arcade.draw_text(self.names[3], 230, 665, arcade.color.PURPLE_NAVY, align = 'center',
        anchor_x = 'center', anchor_y='center')

    def on_update(self, time):
        res = self.client.send_data({"TYPE": "GAMEINFO"})
        print (res)
        if res['TYPE'] == 'RESPONSE':
            self.cards = res['CARDS']
            self.cardcount = res['COUNT']
            self.front = res['FRONT']
            self.cursuit = res['SUIT']
            self.currank = res['RANK']
            self.ranklevel = res['LEVEL']
            self.timer = res['TIMER']
        self._update_all()
    
    def _update_all(self):
        self._update_score()
        self._update_cards()
        self._update_cardcount()
        self._update_front()
        self._update_timer()
        self._update_level()

    def _update_score(self):
        for id, card in enumerate(self.ScoreList):
            num = (self.score // 10 ** (2 - id)) % 10
            card.set_texture(num)
    
    def _update_timer(self):
        for id, timer in enumerate(self.timer):
            self.TimerList[id].set_texture(timer)
    
    def _update_level(self):
        for id, level in enumerate(self.ranklevel):
            self.LevelList[id].set_texture(level % 13)
            self.LevelList[id + 2].set_texture(level % 13)

    def _update_cards(self):
        self.HandLists[0] = arcade.SpriteList()
        length = len(self.cards)
        for id, card in enumerate(self.cards):
            sprite = arcade.Sprite()
            sprite._set_scale(self.CARD_WIDTH / 180)
            total_width = self.CARD_OVERLAP_WIDTH * (length - 1) + self.CARD_WIDTH
            sprite.center_x = self.WIDTH / 2 - total_width / 2 + self.CARD_WIDTH / 2 + self.CARD_OVERLAP_WIDTH * id
            sprite.center_y = 200 if id in self.selected else 180
            sprite._set_texture2(self.textureList[card])
            self.HandLists[0].append(sprite)
    
    def _update_cardcount(self):
        for idcount, count in enumerate(self.cardcount):
            self.HandLists[idcount + 1] = arcade.SpriteList()
            for i in range(count):
                sprite = arcade.Sprite()
                sprite._set_scale(self.CARD_WIDTH / 180)
                if idcount == 0 or idcount == 2:
                    CARD_HEIGHT = self.CARD_WIDTH * 25 / 18
                    total_height = self.CARD_OVERLAP_HEIGHT * (count - 1) + CARD_HEIGHT
                    sprite.center_x = 230 if idcount == 2 else self.WIDTH - 230
                    sprite.center_y = self.HEIGHT / 2 + total_height / 2 - CARD_HEIGHT / 2 - self.CARD_OVERLAP_HEIGHT * i
                    sprite._set_texture2(self.textureList[59])
                elif idcount == 1:
                    total_width = self.CARD_OVERLAP_WIDTH * (count - 1) + self.CARD_WIDTH
                    sprite.center_x = self.WIDTH / 2 - total_width / 2 + self.CARD_WIDTH / 2 + self.CARD_OVERLAP_WIDTH * i
                    sprite.center_y = self.HEIGHT - 160
                    sprite._set_texture2(self.textureList[59])
                    
                self.HandLists[idcount].append(sprite)
    
    def _update_front(self):
        for idcount, cards in enumerate(self.front):
            self.FrontLists[idcount] = arcade.SpriteList()
            length = len(cards)
            for id, card in enumerate(cards):
                sprite = arcade.Sprite()
                sprite._set_scale(self.CARD_WIDTH_SMALL / 180)
                total_width = self.CARD_OVERLAP_WIDTH_SMALL * (length - 1) + self.CARD_WIDTH_SMALL
                group_center_x = self.WIDTH / 2 - total_width / 2 + self.CARD_WIDTH / 2
                group_center_y = self.HEIGHT / 2 + 10
                case = Case(idcount)
                if case(0):     group_center_y = 320
                elif case(1):   group_center_x = 360
                elif case(2):   group_center_y = self.HEIGHT - 300
                elif case(3):   group_center_x = self.WIDTH - 360 - self.CARD_OVERLAP_WIDTH_SMALL * (length - 1)
                sprite.center_x = group_center_x + self.CARD_OVERLAP_WIDTH * id
                sprite.center_y = group_center_y
                sprite._set_texture2(self.textureList[card])
                    
                self.FrontLists[idcount].append(sprite)
        
    def on_mouse_release(self, x, y, button, modifiers):
        super().on_mouse_release(x, y, button, modifiers)
        print("mouse", x, y)
        pos = self.get_mouse_on(x, y)
        if pos is None:
            return 
        if self.press is None:
            self.press = pos
        p = min(self.press, pos)
        while p <= max(self.press, pos):
            if p in self.selected:
                self.selected.remove(p)
            else:
                self.selected.append(p)
            p += 1
        self.press = None

    def on_mouse_press(self, x, y, button, modifiers):
        self.press = self.get_mouse_on(x, y)
    
    def get_mouse_on(self, x, y):
        pos = None
        CARD_HEIGHT = self.CARD_WIDTH * 25 / 18
        for id, card in enumerate(self.HandLists[0]):
            if card.center_x - self.CARD_WIDTH / 2 < x < card.center_x + self.CARD_WIDTH / 2 and \
                card.center_y - CARD_HEIGHT / 2 < y < card.center_y + CARD_HEIGHT / 2:
                pos = id
        return pos


class GameWindow(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.AMAZON)
        self.theme = None
        self.client = None
        self.qmessage = deque()
        # State of Game

        # If you have sprite lists, you should create them here,
        # and set them to None

    def set_button_textures(self):
        normal = "image/GUI/Buttons/Normal.png"
        hover = "image/GUI/Buttons/Hover.png"
        clicked = "image/GUI/Buttons/Clicked.png"
        locked = "image/GUI/Buttons/Locked.png"
        self.theme.add_button_textures(normal, hover, clicked, locked)
    
    def setup_theme(self):
        self.theme = arcade.gui.Theme()
        self.theme.set_font(18, arcade.color.BLACK_OLIVE)
        self.set_button_textures()
        self.theme.add_text_box_texture("image/GUI/Brown.png")
        self.theme.add_window_texture("image/GUI/Window.png")

    def setup(self, client):
        # Create your sprites and sprite lists here
        self.client = client
        self.setup_theme()
    

class Client:
    def __init__(self):
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 800
        self.SCREEN_TITLE = "Game Center"
        self.game = GameWindow(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.SCREEN_TITLE)
        self.game.setup(self)
        self.socket = None
        self.menuview = None
        self.roomview = None
    def connect(self, addr: str = '127.0.0.1', port: int = 8888):
        try:
            self.socket = socket.create_connection((addr, port), timeout = 10)
        except ConnectionRefusedError as e:
            return False, e
        data = self.socket.recv(128)
        return True, Message.decode(data)
    def send_data(self, message: dict):
        self.socket.sendall(Message.encode(message))
        data = self.socket.recv(2048)
        return Message.decode(data)
    def run(self):
        self.menuview = MenuView(self.game, "image/GUI/background1.jpg")
        self.loginview = LoginView(self.game, "image/GUI/background1.jpg")
        self.roomview = RoomView(self.game, "image/GUI/background1.jpg")
        self.dispatchview = DispatchView(self.game, "image/GUI/Window.png")
        self.gameview = GameView(self.game, "image/GUI/Window.png")
        self.game.show_view(self.menuview)
        arcade.run()

Client().run()