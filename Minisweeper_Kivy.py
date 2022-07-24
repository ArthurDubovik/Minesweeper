import random
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.uix.recycleview import RecycleView
from kivy.core.window import Window

class LongpressButton(Factory.Button):
    __events__ = ('on_long_press', )
    long_press_time = Factory.NumericProperty(0.2)
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
    

class MenuScreen(Screen):
    def __init__(self, **kw):
        super(MenuScreen, self).__init__(**kw)
        
        box = BoxLayout(orientation='vertical')
        box.add_widget(Button(text='New game', on_release=lambda x: set_screen('game_field')))
        box.add_widget(Button(text='Exit', on_release=lambda x: MineSweeperApp().stop()))
        self.add_widget(box)


class GameScreen(Screen):
    def __init__(self, **kw):
        super(GameScreen, self).__init__(**kw)
        Window.bind(on_keyboard=self.onBackBtn)

    def onBackBtn(self, window, key, *args):
        if key == 27:
            set_screen('menu')
            pole_game.pole = []
            pole_game.init(13, 6, 6)
            return True
        return False

    def on_enter(self):
  
        self.sound_click = SoundLoader.load('./sound/click.wav')
        self.sound_mine_press = SoundLoader.load('./sound/mine_press.wav')
        self.sound_mine_check = SoundLoader.load('./sound/mine_check.wav')
        self.sound_win = SoundLoader.load('./sound/sound_win.wav')

        #Button icons
        #self.img_banner = Icon("./img/banner.png")
        #self.img_mine = QIcon("./img/mine.png")
        #self.img_false_mine = QIcon("./img/false_mine.png")
        #self.img_explode = QIcon("./img/explode_mine.png")

        self.CELLS = []
        self.HEIGHT = 13
        self.WIDTH = 6
        #List of coordinates with cells of correctly marked mines
        self.CHECKED_MINES = []
        self.MINES = 6

        #список с клетками с которых сняли флажок
        self.non_check_mines = []

        self.open_cells = []

        
        self.layout = GridLayout(cols=6, rows=13)
        self.layout.col_default_width = self.layout.row_default_height = 40

        root = RecycleView(size_hint=(1, None), size=(Window.width, Window.height))
        root.add_widget(self.layout)
        self.add_widget(root)

        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):

                self.button = LongpressButton(height=38, width=38, font_size=30)
                #self.button.background_color = 23,67,88,0.5
                self.button.bind(on_release=self.open_cell)
                self.button.bind(on_long_press=self.mine_check)
                self.button.bind(on_press=self.flag)
                self.button.win = False
                #self.button.size = 40, 40
                #self.button.border = 0, 0, 0, 0
                self.button.coord_x = i
                self.button.coord_y = j
                self.button.long = False
                self.button.is_pressed = False
                self.button.mine_note = False
                self.CELLS.append(self.button)
                self.layout.add_widget(self.button)
        return self.layout

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
            #self.sound_click.stop()
            self.sound_click.play()
            #time.sleep(0.005)
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
                        sender.font_size = 70
                        sender.background_color = 0.1, 0.5, 0.6, 1
                    if sender.text == '2':
                        sender.font_size = 70
                        sender.background_color = 255, 0.5, 0.6, 1
                    if sender.text == '3':
                        sender.font_size = 70
                        sender.background_color = 0.1, 0.5, 0.6, 1
                    if sender.text == '4':
                        sender.font_size = 70
                        sender.background_color = 0.1, 0.5, 0.6, 1
                    if sender.text == '5':
                        sender.font_size = 70
                        sender.background_color = 0.1, 0.5, 0.6, 1

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
                sender.background_normal = './img/banner_2.png'
                sender.background_down = './img/banner_2.png'
                
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
                i.background_normal = "./img/mine_2.png"
            if i.mine_note == True and [i.coord_x, i.coord_y] not in pole_game.rij:
                i.background_normal = "./img/false_mine_2.png"

        sender.background_color = 1, 0, 0, 1
        #sender.background_color = 180, 40, 100, 0
        sender.background_normal = "./img/explode_mine_2.png"
        
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
    def init(self, height=13, width=6, mines=6):
        #List size
        self.M = height
        self.N = width
        #Number of mines
        self.mines = mines

        #Filling the list of cells with zeros
        self.pole = [[(Cell(0, False)) for i in range(self.N)] for i in range(self.M)]

        #List with mines
        self.rij = []
        
        #Filling the field with mines
        mine_count = 0
        while mine_count < self.mines:
            r = [random.randrange(self.M), random.randrange(self.N)]
            if r not in self.rij:
                self.rij.append(r)
                self.pole[r[0]][r[1]].mine = True
                mine_count += 1
        
        #Counting the number of mines around each cell
        for i in range(self.M):
            for j in range(self.N):
                around_mines = 0
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        if (i + x) >= 0 and (j + y) >= 0 and (i + x) < self.M and (j + y) < self.N:
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
sm.add_widget(GameScreen(name='game_field'))

class MineSweeperApp(App):
    def __init__(self, **kvargs):
        super(MineSweeperApp, self).__init__(**kvargs)

    def build(self):
        return sm

if __name__ == '__main__':
    pole_game = GameField()
    pole_game.init()
    MineSweeperApp().run()