import random
from PyQt6.QtWidgets import QPushButton, QApplication, QMainWindow, QWidget, QGridLayout, QLabel
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QSize, Qt, QCoreApplication, QPoint, QPropertyAnimation, QUrl
from PyQt6 import QtCore

class MainWindow(QMainWindow):
    def __init__(self): 
        super(MainWindow, self).__init__()
        self.setWindowTitle("Minesweeper by Arthur Dubovik")
        self.setWindowIcon(QIcon("./img/mine.png"))

        #Sounds
        self.sound_click = QSoundEffect()
        self.sound_click.setSource(QUrl.fromLocalFile("./sound/click.wav"))
        self.sound_click.setVolume(0.5)
        self.sound_mine_check = QSoundEffect()
        self.sound_mine_check.setSource(QUrl.fromLocalFile("./sound/mine_check.wav"))
        self.sound_mine_check.setVolume(0.25)
        self.sound_mine_press = QSoundEffect()
        self.sound_mine_press.setSource(QUrl.fromLocalFile("./sound/mine_press.wav"))
        self.sound_mine_press.setVolume(0.25)
        self.sound_win = QSoundEffect()
        self.sound_win.setSource(QUrl.fromLocalFile("./sound/sound_win.wav"))
        self.sound_win.setVolume(0.5)
        
        #Button icons
        self.img_banner = QIcon("./img/banner.png")
        self.img_mine = QIcon("./img/mine.png")
        self.img_false_mine = QIcon("./img/false_mine.png")
        self.img_explode = QIcon("./img/explode_mine.png")
        
        #New game button
        button_action = QAction("New game", self)
        button_action.triggered.connect(self.new_game)

        #Difficult buttons
        self.button_action2_1 = QAction("10", self)
        self.button_action2_1.setCheckable(True)
        self.button_action2_1.setChecked(True)
        self.button_action2_1.triggered.connect(self.change_diff)

        self.button_action2_2 = QAction("25", self)
        self.button_action2_2.setCheckable(True)
        self.button_action2_2.triggered.connect(self.change_diff)

        self.button_action2_3 = QAction("40", self)
        self.button_action2_3.setCheckable(True)
        self.button_action2_3.triggered.connect(self.change_diff)
    
        #Field size buttons
        self.button_action3_1 = QAction("12 x 12", self)
        self.button_action3_1.setCheckable(True)
        self.button_action3_1.setChecked(True)
        self.button_action3_1.triggered.connect(self.change_size)

        self.button_action3_2 = QAction("16 x 16", self)
        self.button_action3_2.setCheckable(True)
        self.button_action3_2.triggered.connect(self.change_size)

        self.button_action3_3 = QAction("20 x 20", self)
        self.button_action3_3.setCheckable(True)
        self.button_action3_3.triggered.connect(self.change_size)
       
        #Exit button
        button_action4 = QAction("Exit", self)
        button_action4.triggered.connect(QCoreApplication.instance().quit)

        #Creating menu bar
        menu = self.menuBar()
        
        file_menu = menu.addMenu("Menu")
        file_menu.addAction(button_action)
        #_______________________
        file_menu.addSeparator()
        file_submenu = file_menu.addMenu("Difficult")
        file_submenu.addAction(self.button_action2_1)
        file_submenu.addAction(self.button_action2_2)
        file_submenu.addAction(self.button_action2_3)

        file_submenu = file_menu.addMenu("Field size")
        file_submenu.addAction(self.button_action3_1)
        file_submenu.addAction(self.button_action3_2)
        file_submenu.addAction(self.button_action3_3)
        #_______________________
        file_menu.addSeparator()
        file_menu.addAction(button_action4)
        
    #Filling the playing field with buttons
    def init(self, height=12, width=12, mines=10):
        #List of buttons
        self.CELLS = []
        #Field size (number of buttons)
        self.HEIGHT = height
        self.WIDTH = width
        #Number of buttons with mines
        self.MINES = mines
        #Number of buttons marked with a flag
        self.CHECK_BUTTONS = 0
        #List of coordinates with cells of correctly marked mines
        self.CHECKED_MINES = []
        #Button size
        self.BUTTON_HEIGHT = self.BUTTON_WIDTH = 38
        #Padding between buttons
        self.BUTTON_INDENT = 1
        
        #Arrangement of elements in the window
        self.layout = QGridLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        
        #Fixed size of the playing field for the number of buttons
        self.WIDTH_SIZE = self.HEIGHT * self.BUTTON_HEIGHT + (self.HEIGHT - 1) * self.BUTTON_INDENT 
        self.HEIGHT_SIZE = self.WIDTH * self.BUTTON_WIDTH + (self.WIDTH - 1) * self.BUTTON_INDENT
        self.setFixedSize(QSize(self.WIDTH_SIZE+30, self.HEIGHT_SIZE+40))

        #Creating a grid of buttons
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                self.button = QPushButton("Button ", self)

                #Setting the size of buttons
                self.button.setFixedSize(QSize(self.BUTTON_HEIGHT, self.BUTTON_WIDTH))
            
                self.button.setCheckable(True)
                self.button.setText('')
                self.button.clicked.connect(self.open_cell)
                
                #Flag of the pressed button
                self.button.is_pressed = False
                #Flag of a marked mine
                self.button.mine_note = False
                #Status of the buttons after the victory
                self.button.win = False
                
                #Redefining the right mouse button
                self.button.installEventFilter(self)
                self.layout.addWidget(self.button, i, j)
                
                #Setting coordinates to buttons
                self.button.x = i
                self.button.y = j
                
                #Adding buttons to the list
                self.CELLS.append(self.button)
        
        #Victory label
        self.btn = QLabel(self)
        self.btn.setText('You win!')
        self.btn.resize(200, 60)
        self.btn.setStyleSheet('QLabel {font: bold 44px;}')
        self.btn.hide()

    #Victory
    def victory(self):
        self.btn.show()
        animation = QPropertyAnimation(self.btn, b'pos', self)
        animation.setKeyValueAt(0, QPoint(20, 30))
        animation.setKeyValueAt(0.65, QPoint(self.HEIGHT_SIZE - 200, self.WIDTH_SIZE - 100))
        animation.setKeyValueAt(1, QPoint(int((self.HEIGHT_SIZE - 200) / 2), int((self.WIDTH_SIZE - 100) / 2)))
        animation.setDuration(20000)
        animation.start()
        self.sound_win.play()

    #New game event
    def new_game(self):
        self.sound_win.stop()
        self.btn.hide()
        self.new = False

        window.init(self.HEIGHT, self.WIDTH, self.MINES)
        pole_game.pole = []
        pole_game.init(self.HEIGHT, self.WIDTH, self.MINES)

    #Changing the difficulty
    def change_diff(self):
        sender = self.sender()
        sender.setChecked(True)
        if sender.text() == "10":
            self.MINES = 10
            self.button_action2_2.setChecked(False)
            self.button_action2_3.setChecked(False)
            self.new_game()
            
        if sender.text() == "25":
            self.MINES = 25
            self.button_action2_1.setChecked(False)
            self.button_action2_3.setChecked(False)
            self.new_game()
           
        if sender.text() == "40":
            self.MINES = 40
            self.button_action2_1.setChecked(False)
            self.button_action2_2.setChecked(False)
            self.new_game()
    
    #Field size selection
    def change_size(self):
        sender = self.sender()
        sender.setChecked(True)
        if sender.text() == "12 x 12":
            self.HEIGHT = self.WIDTH = 12
            self.button_action3_2.setChecked(False)
            self.button_action3_3.setChecked(False)
            self.new_game()
            
        if sender.text() == "16 x 16":
            self.HEIGHT = self.WIDTH = 16
            self.button_action3_1.setChecked(False)
            self.button_action3_3.setChecked(False)
            self.new_game()
           
        if sender.text() == "20 x 20":
            self.HEIGHT = self.WIDTH = 20
            self.button_action3_1.setChecked(False)
            self.button_action3_2.setChecked(False)
            self.new_game()
        
    #Opening a field by click
    def open_cell(self):
        
        #The object of the pressed button
        sender = self.sender()
        sender.setChecked(True)
        if sender.mine_note != True and sender.is_pressed == False:
            self.sound_click.play()
            sender.is_pressed = True
            
            #Number of buttons pressed
            self.PRESS_BUTTONS = len(list(filter(self.check_true, [i.is_pressed for i in self.CELLS])))
            
            #Checking the victory conditions (if the last closed cell opens)
            self.win_check()
            
            #Clicking on a mine
            if pole_game.pole[sender.x][sender.y].mine == True:
                self.sound_mine_press.play()
                self.mine_press(sender)
            #Counting the mines around the pressed button
            elif pole_game.pole[sender.x][sender.y].around_mines > 0:
                    sender.setText(str(pole_game.pole[sender.x][sender.y].around_mines))

                    #Number custom colors
                    if sender.text() == '1':
                        sender.setStyleSheet('QPushButton {color: #3F51B5; font: bold 20px;}')
                    if sender.text() == '2':
                        sender.setStyleSheet('QPushButton {color: #8B0000; font: bold 20px;}')
                    if sender.text() == '3':
                        sender.setStyleSheet('QPushButton {color: #FF0000; font: bold 20px;}')
                    if sender.text() == '4':
                        sender.setStyleSheet('QPushButton {color: #03A9F4; font: bold 20px;}')
                    if sender.text() == '5':
                        sender.setStyleSheet('QPushButton {color: #006400; font: bold 20px;}')

            #If you clicked on an empty cell
            if pole_game.pole[sender.x][sender.y].around_mines == 0 and pole_game.pole[sender.x][sender.y].mine != True:
                self.rec_open(sender.x, sender.y)
        
    #Clicking on a mine
    def mine_press(self, sender):
        for i in self.CELLS:
            if [i.x, i.y] in pole_game.rij and i.mine_note == False:
                i.setCheckable(True)
                i.setChecked(True)
                i.setIcon(QIcon(self.img_mine))
                i.setIconSize(QSize(35,35))
            if i.isChecked() == False:
                i.setCheckable(False)
            if i.mine_note == True and [i.x, i.y] not in pole_game.rij:
                i.setIcon(QIcon(self.img_false_mine))
                i.setIconSize(QSize(38,38))
            i.is_pressed = True
        sender.setIcon(QIcon(self.img_explode))
        sender.setIconSize(QSize(35,35))

    #Opening empty cells around the selected empty one
    def rec_open(self, x, y):
        for i in self.CELLS:
            if i.is_pressed == False:
                if i.x == x and i.y == y + 1:
                    i.click()
                if i.x == x + 1 and i.y == y:
                    i.click()
                if i.x == x - 1 and i.y == y:
                    i.click()
                if i.x == x and i.y == y - 1:
                    i.click()
    
    @staticmethod
    def check_true(x):
        if x == True:
            return x
    
    #Right-click processing
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            #if event.button() == Qt.MouseButton.LeftButton:
                #print(obj.objectName(), "Left click")

            if event.button() == Qt.MouseButton.RightButton:
                #print(obj.objectName(), "Right click")
                
                #Marking of mines on the field
                if obj.is_pressed == False and obj.win == False:
                    if obj.mine_note == False:
                        self.sound_mine_check.play()
                        obj.setIcon(QIcon(self.img_banner))
                        obj.setIconSize(QSize(34,34))
                        obj.mine_note = True
                        obj.setCheckable(False)

                        if pole_game.pole[obj.x][obj.y].mine == True:
                            if [obj.x, obj.y] not in self.CHECKED_MINES:
                                self.CHECKED_MINES.append([obj.x, obj.y])
                    
                    else:
                        self.sound_mine_check.play()
                        obj.mine_note = False
                        obj.setIcon(QIcon())
                        obj.setCheckable(True)
                        if [obj.x, obj.y] in self.CHECKED_MINES:
                                self.CHECKED_MINES.remove([obj.x, obj.y])

                #Number of buttons marked with a flag
                self.check_buttons = len(list(filter(self.check_true, [i.mine_note for i in self.CELLS])))

                self.win_check()
                #elif event.button() == Qt.MouseButton.MiddleButton:
                    #print(obj.objectName(), "Middle click")
        return QtCore.QObject.event(obj, event)

    #Win check
    def win_check(self):
        if sorted(self.CHECKED_MINES) == sorted(pole_game.rij) and self.check_buttons == self.MINES:
            if self.PRESS_BUTTONS == len(self.CELLS) - self.MINES:
                self.CHECKED_MINES = []
                for i in self.CELLS:
                    i.win = True
                self.victory()

#Game cell
class Cell:
    def __init__(self, around_mines, mine):
        self.around_mines = around_mines
        self.mine = mine
        self.fl_open = False

#Game field
class GameField:
    def init(self, height=12, width=12, mines=10):
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
            r = [random.randrange(self.N), random.randrange(self.M)]
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

app = QApplication([])
window = MainWindow()
pole_game = GameField()
window.init()
pole_game.init()
window.show()
app.exec()
        
