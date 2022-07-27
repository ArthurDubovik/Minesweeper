import random
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.core.window import Window

class LongpressButton(Factory.Button):
    __events__ = ('on_long_press', )
    long_press_time = Factory.NumericProperty(0.3)
    def on_state(self, instance, value):
        if value == 'down':
            lpt = self.long_press_time
            self._clockev = Clock.schedule_once(self._do_long_press, lpt)
        else:
            self._clockev.cancel()
    def _do_long_press(self, dt):
        self.dispatch('on_long_press')
    def on_long_press(self, *largs):
        pass
    def on_release(self, *largs):
        pass

class SoundButtonSettings(ToggleButton):
    def on_state(self, instance, value):
        if instance.state == 'normal':
            GameScreen.sound_click.play()

class SoundButtonMenu(Button):
    def on_state(self, instance, value):
        if instance.state == 'down':
            GameScreen.sound_click.play()

class MenuScreen(Screen):
    def __init__(self, **kw):
        super(MenuScreen, self).__init__(**kw)
        box = BoxLayout(orientation='vertical', size=(Window.width, Window.height/3), spacing=30, pos_hint = {'center_x': 0.5, 'center_y': 0.5}, size_hint = (None, None)) 
        new_game = SoundButtonMenu(text='New game', font_size = Window.width/15, on_press=lambda x: set_screen('game_field'), size_hint=(.9, .1), pos_hint = {'center_x': 0.5, 'center_y': 0.75}, background_color = '#005454' )
        box.add_widget(new_game)
        settings = SoundButtonMenu(text='Settings', font_size = Window.width/15, on_press=lambda x: set_screen('settings'), size_hint=(.9, .1), pos_hint = {'center_x': 0.5, 'center_y': 0.5}, background_color = '#005454' )
        box.add_widget(settings)
        exit = SoundButtonMenu(text='Exit', font_size = Window.width/15, on_press=lambda x: MineSweeperApp().stop(), size_hint=(.9, .1), pos_hint = {'center_x': 0.5, 'center_y': 0.25}, background_color = '#005454')
        box.add_widget(exit)
        self.add_widget(box)

class SettingsScreen(Screen):
    def __init__(self, **kw):
        super(SettingsScreen, self).__init__(**kw)
        box = BoxLayout(orientation='vertical', size=(Window.width, Window.height/2.3), spacing=40, pos_hint = {'center_x': 0.5, 'center_y': 0.5}, size_hint = (None, None)) 
        self.level_1 = SoundButtonSettings(text='5 x 11, 5 mines', on_press=self.change_diff_1, font_size = Window.width/15, size_hint=(.9, .1), pos_hint = {'center_x': 0.5}, background_color = '#005454' )
        box.add_widget(self.level_1)
        self.level_2 = SoundButtonSettings(text='6 x 13, 10 mines', on_press=self.change_diff_2, state = 'down', font_size = Window.width/15, size_hint=(.9, .1), pos_hint = {'center_x': 0.5}, background_color = '#005454' )
        box.add_widget(self.level_2)
        self.level_3 = SoundButtonSettings(text='8 x 17, 15 mines', on_press=self.change_diff_3, font_size = Window.width/15, size_hint=(.9, .1), pos_hint = {'center_x': 0.5}, background_color = '#005454')
        box.add_widget(self.level_3)
        box.add_widget(SoundButtonMenu(text='Back', on_press=lambda x: set_screen('menu'), font_size = Window.width/15, size_hint=(.9, .05), pos_hint = {'center_x': 0.5}, background_color = '#005454'))
        self.add_widget(box)
    
    def change_diff_1(self, sender, height=11, width=5, mines=5):
        self.level_1.state = 'down'
        self.level_2.state = 'normal'
        self.level_3.state = 'normal'
        pole_game.pole = []
        pole_game.init(height, width, mines)

    def change_diff_2(self, sender, height=13, width=6, mines=10):
        self.level_1.state = 'normal'
        self.level_2.state = 'down'
        self.level_3.state = 'normal'
        pole_game.pole = []
        pole_game.init(height, width, mines)
    
    def change_diff_3(self, sender, height=17, width=8, mines=15):
        self.level_1.state = 'normal'
        self.level_2.state = 'normal'
        self.level_3.state = 'down'
        pole_game.pole = []
        pole_game.init(height, width, mines)

class GameScreen(Screen):
    sound_click = SoundLoader.load('./sound/click.wav')
    sound_mine_press = SoundLoader.load('./sound/mine_press.wav')
    sound_mine_check = SoundLoader.load('./sound/mine_check.wav')
    sound_win = SoundLoader.load('./sound/sound_win.wav')
    
    def __init__(self, **kw):
        super(GameScreen, self).__init__(**kw)
        Window.bind(on_keyboard=self.onBackBtn)

    def onBackBtn(self, window, key, *args):
        if key == 27:
            set_screen('menu')
            return True
        return False

    def on_enter(self):
        pole_game.pole = []
        pole_game.init(pole_game.HEIGHT, pole_game.WIDTH, pole_game.MINES)
        
        #Button icons
        self.img_banner = './img/banner_2.png'
        self.img_mine = './img/mine_2.png'
        self.img_false_mine = './img/false_mine_2.png'
        self.img_explode = './img/explode_mine_2.png'

        self.CELLS = []
        self.HEIGHT = pole_game.HEIGHT
        self.WIDTH = pole_game.WIDTH
        
        #List of coordinates with cells of correctly marked mines
        self.CHECKED_MINES = []
        self.MINES = pole_game.MINES

        #List with cells that have been unchecked
        self.non_check_mines = []

        self.open_cells = []

        #Button sizes      
        space = 10
        win_x = int((Window.width  - space * (self.WIDTH + 1)) / self.WIDTH)
        win_y = int((Window.height - space * (self.HEIGHT + 1)) / self.HEIGHT)
        but_size_x = but_size_y = min(win_x, win_y)
        
        #Setting the padding
        pad_x = Window.width - (but_size_x * self.WIDTH + space * (self.WIDTH - 1))
        pad_y = Window.height - (but_size_y * self.HEIGHT + space * (self.HEIGHT - 1))
        
        self.layout = GridLayout(cols=self.WIDTH, rows=self.HEIGHT, padding=[pad_x/2, pad_y/2], spacing=[space])
        
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                self.button = LongpressButton()
                self.button.bind(on_release=self.open_cell)
                self.button.bind(on_long_press=self.mine_check)
                self.button.bind(on_press=self.flag)
                self.button.background_color = '#005454'
                self.button.win = False
                self.button.font_size = Window.width/15
                self.button.coord_x = i
                self.button.coord_y = j
                self.button.long = False
                self.button.is_pressed = False
                self.button.mine_note = False
                self.CELLS.append(self.button)
                self.layout.add_widget(self.button)

        root = BoxLayout(size=(Window.width, Window.height))
        root.add_widget(self.layout)
        self.add_widget(root)

    def on_leave(self): 
        self.layout.clear_widgets()

    #Victory
    def victory(self):
        self.sound_win.play()

    #Win check
    def win_check(self):
        if sorted(self.CHECKED_MINES) == sorted(pole_game.rij):
            if self.PRESS_BUTTONS == len(self.CELLS) - self.MINES:
                self.CHECKED_MINES = []
                for i in self.CELLS:
                    i.win = True
                self.victory()

    #Opening a field by click
    def open_cell(self, sender):
        #The object of the pressed button
        if sender.mine_note != True and sender.is_pressed == False and sender.long == False:
            self.sound_click.play()

            sender.is_pressed = True
            sender.background_color = 180, 40, 100, 0.8
            
            #Number of buttons pressed
            self.PRESS_BUTTONS = len(list(filter(self.check_true, [i.is_pressed for i in self.CELLS])))
            
            #Checking the victory conditions (if the last closed cell opens)
            self.win_check()
            
            #Clicking on a mine
            if pole_game.pole[sender.coord_x][sender.coord_y].mine == True:
                self.mine_press(sender)
            #Counting the mines around the pressed button
            elif pole_game.pole[sender.coord_x][sender.coord_y].around_mines > 0:
                    sender.text = str(pole_game.pole[sender.coord_x][sender.coord_y].around_mines)
                    
                    #Number custom colors
                    if sender.text == '1':
                        sender.background_color = '#20B2AA'
                    if sender.text == '2':
                        sender.background_color = '#ff0000' #255, 0.5, 0.6, 1
                    if sender.text == '3':
                        sender.background_color = '#DA70D6'   
                    if sender.text == '4':
                        sender.background_color = '#DAA520'
                    if sender.text == '5':
                        sender.background_color = '#00FF00'

            #If you clicked on an empty cell
            if pole_game.pole[sender.coord_x][sender.coord_y].around_mines == 0 and pole_game.pole[sender.coord_x][sender.coord_y].mine != True:
                self.rec_open(sender.coord_x, sender.coord_y)  
                
    def flag(self, sender):
        if sender.mine_note == False:
            sender.long = False
        for i in self.non_check_mines:
            i.long = False

    #Marking of mines on the field
    def mine_check(self, sender):    
        
        if sender.is_pressed == False and sender.win == False:
            if sender.mine_note == False:
                sender.background_color = 180, 40, 100, 0.8
                sender.background_normal = self.img_banner
                sender.background_down = self.img_banner
                
                self.sound_mine_check.play()
                sender.mine_note = True
                if sender in self.non_check_mines:
                    self.non_check_mines.remove(sender)
                if pole_game.pole[sender.coord_x][sender.coord_y].mine == True:
                    if [sender.coord_x, sender.coord_y] not in self.CHECKED_MINES:
                        self.CHECKED_MINES.append([sender.coord_x, sender.coord_y])
            
            else:
                sender.is_pressed = False
                self.sound_mine_check.play()
                sender.mine_note = False
                sender.long = True
                if sender not in self.non_check_mines:
                    self.non_check_mines.append(sender)
                sender.background_color = '#005454'
                sender.background_normal = 'atlas://data/images/defaulttheme/button'
                sender.background_down = 'atlas://data/images/defaulttheme/button_pressed'
                if [sender.coord_x, sender.coord_y] in self.CHECKED_MINES:
                    self.CHECKED_MINES.remove([sender.coord_x, sender.coord_y])
        self.win_check()

    #Clicking on a mine
    def mine_press(self, sender):
        self.sound_click.stop()
        self.sound_mine_press.play()
        for i in self.CELLS:
            i.is_pressed = True
            if [i.coord_x, i.coord_y] in pole_game.rij and i.mine_note == False:
                i.state = 'normal'
                i.background_color = 180, 40, 100, 0.8
                i.background_normal = self.img_mine
            if i.mine_note == True and [i.coord_x, i.coord_y] not in pole_game.rij:
                i.background_normal = self.img_false_mine

        sender.background_color = 1, 0, 0, 1
        #sender.background_color = 180, 40, 100, 0
        sender.background_normal = self.img_explode
        

    #Opening empty cells around the selected empty one
    def rec_open(self, x, y):
        for i in self.CELLS:
            if i.is_pressed == False:
                if i.coord_x == x + 1 and i.coord_y == y + 1:
                        self.open_cell(i)
                elif i.coord_x == x - 1 and i.coord_y == y - 1:
                        self.open_cell(i)
                elif i.coord_x == x + 1 and i.coord_y == y - 1:
                        self.open_cell(i)
                elif i.coord_x == x - 1 and i.coord_y == y + 1:
                        self.open_cell(i)
                elif i.coord_x == x and i.coord_y == y + 1:
                        self.open_cell(i)
                elif i.coord_x == x + 1 and i.coord_y == y:
                        self.open_cell(i)
                elif i.coord_x == x - 1 and i.coord_y == y:
                        self.open_cell(i)
                elif i.coord_x == x and i.coord_y == y - 1:
                        self.open_cell(i)
    
    @staticmethod
    def check_true(x):
        if x == True:
            return x

#Game cell
class Cell:
    def __init__(self, around_mines, mine):
        self.around_mines = around_mines
        self.mine = mine
        self.fl_open = False

#Game field
class GameField:
    def init(self, height=13, width=6, mines=10):
        #List size
        self.HEIGHT = height
        self.WIDTH = width
        #Number of mines
        self.MINES = mines
        #print(self.HEIGHT, self.WIDTH, self.MINES)

        #Filling the list of cells with zeros
        self.pole = [[(Cell(0, False)) for i in range(self.WIDTH)] for i in range(self.HEIGHT)]

        #List with mines
        self.rij = []
        
        #Filling the field with mines
        mine_count = 0
        while mine_count < self.MINES:
            r = [random.randrange(self.HEIGHT), random.randrange(self.WIDTH)]
            #print(r)
            if r not in self.rij:
                self.rij.append(r)
                self.pole[r[0]][r[1]].mine = True
                mine_count += 1
        
        #Counting the number of mines around each cell
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                around_mines = 0
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        if (i + x) >= 0 and (j + y) >= 0 and (i + x) < self.HEIGHT and (j + y) < self.WIDTH:
                            if self.pole[i + x][j + y].mine == True:
                                around_mines += 1
                if self.pole[i][j].mine == True and around_mines > 0:
                    around_mines -= 1
                self.pole[i][j].around_mines = around_mines
                around_mines = 0


def set_screen(name_screen):
    sm.current = name_screen

sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(SettingsScreen(name='settings'))
sm.add_widget(GameScreen(name='game_field'))

class MineSweeperApp(App):
    def __init__(self, **kvargs):
        super(MineSweeperApp, self).__init__(**kvargs)

    def build(self):
        return sm

pole_game = GameField()
pole_game.init()
MineSweeperApp().run()