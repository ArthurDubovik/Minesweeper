import random
from PyQt6.QtWidgets import QPushButton, QApplication, QMainWindow, QWidget, QGridLayout, QToolBar, QLabel, QCheckBox, QStatusBar
from PyQt6.QtGui import QPalette, QColor, QAction
from PyQt6.QtCore import QSize, Qt, QCoreApplication
from PyQt6 import QtCore

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)
         
class MainWindow(QMainWindow):
    def __init__(self):
        #список с объктами кнопок
        self.cells = []
        
        #количество полей
        self.height = self.width = 12
        
        super(MainWindow, self).__init__()
    
        self.setWindowTitle("Minisweeper")
        self.layout = QGridLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        
        #панель меню
        toolbar = QToolBar("My main toolbar")

        button_action = QAction("New game", self)
        button_action.triggered.connect(self.ToolBarNewGame)
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        button_action2 = QAction("Difficult", self)
        #button_action2.triggered.connect()
        button_action2.setCheckable(True)
        toolbar.addAction(button_action2)

        button_action3 = QAction("Field size", self)
        #button_action3.triggered.connect()
        button_action3.setCheckable(True)
        toolbar.addAction(button_action3)

        button_action4 = QAction("Exit", self)
        button_action4.triggered.connect(QCoreApplication.instance().quit)
        toolbar.addAction(button_action4)

        menu = self.menuBar()

        file_menu = menu.addMenu("Menu")
        file_menu.addAction(button_action)
        file_menu.addSeparator()

        file_submenu = file_menu.addMenu("Difficult")
        file_submenu.addAction(button_action2)
        file_submenu = file_menu.addMenu("Field size")
        file_submenu.addAction(button_action3)
        
        file_menu.addSeparator()
        file_menu.addAction(button_action4)
        
    #заполнение поля кнопками
    def init(self):
        for i in range(self.height):
            for j in range(self.width):
                self.button = QPushButton()
                #размер полей
                self.button.setFixedSize(QSize(38, 38))
                #подгон размера игрового кона под количество полей
                self.setFixedSize(QSize(self.height * 38 + (self.height - 1) * 6, self.width * 38 + (self.width - 1) * 6))
                self.button.setStyleSheet("background-color: white")
                self.button.setCheckable(True)
                self.button.setText('')
                self.button.clicked.connect(self.open_cell)
                #флаг нажатой кнопки
                self.button.is_pressed = False
                #флаг отмеченной мины
                self.button.mine_note = False
                self.button.installEventFilter(self)
                self.layout.addWidget(self.button, i, j)
                self.button.x = i
                self.button.y = j
                self.cells.append(self.button)

    #событие NewGame
    def ToolBarNewGame(self, s):
        for i in self.cells:
            i.setText('')
            i.setStyleSheet("background-color: white")
        window.init()
        pole_game.pole = []
        pole_game.init()      
        
    #открытие поля по клику
    def open_cell(self):
        sender = self.sender()
        if sender.mine_note != True:
            #выключаем кнопку после нажалия ЛКМ
            sender.setDisabled(True)
            sender.is_pressed = True
            
            #нажатие на мину
            if pole_game.pole[sender.x][sender.y].mine == True:
                sender.setText('XX')
                for i in self.cells:
                    i.click() 
                    if i.mine_note == True:
                        i.mine_note = False
                        i.setCheckable(True)
                        i.setText('')
                    
            elif pole_game.pole[sender.x][sender.y].around_mines > 0:
                    sender.setText(str(pole_game.pole[sender.x][sender.y].around_mines))
            if pole_game.pole[sender.x][sender.y].around_mines == 0 and pole_game.pole[sender.x][sender.y].mine != True:
                self.rec_open(sender.x, sender.y)

    #открытие пустых ячеек вокруг выбранной пустой
    def rec_open(self, x, y):
        for i in self.cells:
            if i.x == x and i.y == y + 1:
                i.click()
            if i.x == x + 1 and i.y == y:
                i.click()
            if i.x == x - 1 and i.y == y:
                i.click()
            if i.x == x and i.y == y - 1:
                i.click()

    #обработка нажатия правой кнопоки мыши
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            #if event.button() == Qt.MouseButton.LeftButton:
            #    print(obj.objectName(), "Left click")
            if event.button() == Qt.MouseButton.RightButton:
                #print(obj.objectName(), "Right click")

                #отметка мин на поле
                if obj.is_pressed == False:
                    if obj.text() == '':
                        obj.setText("X")
                        obj.setStyleSheet("background-color: yellow")
                        obj.mine_note = True
                        obj.setCheckable(False)
                    else:
                        obj.setStyleSheet("background-color: white")
                        obj.setText('')
                        obj.mine_note = False
                        obj.setCheckable(True)

            #elif event.button() == Qt.MouseButton.MiddleButton:
            #    print(obj.objectName(), "Middle click")
        return QtCore.QObject.event(obj, event)

#описание игровой ячейки
class Cell:
    def __init__(self, around_mines, mine):
        self.around_mines = around_mines
        self.mine = mine
        self.fl_open = False

#описание игрового поля
class GamePole:
    def __init__(self):
        self.M = window.height
        self.N = window.width
        #self.pole = [[(Cell(0, False)) for i in range(self.N)] for i in range(self.N)]
    def init(self):
        self.pole = [[(Cell(0, False)) for i in range(self.N)] for i in range(self.N)]
        rij = []
        l = 0
        while l < self.N:
            r = [random.randrange(self.N), random.randrange(self.N)]
            if r not in rij:
                rij.append(r)
                self.pole[r[0]][r[1]].mine = True
                l += 1
        for i in range(self.N):
            for j in range(self.N):
                around_mines = 0
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        if (i + x) >= 0 and (j + y) >= 0 and (i + x) < self.N and (j + y) < self.N:
                            if self.pole[i + x][j + y].mine == True:
                                around_mines += 1
                if self.pole[i][j].mine == True and around_mines > 0:
                    around_mines -= 1
                self.pole[i][j].around_mines = around_mines
                around_mines = 0

app = QApplication([])
window = MainWindow()
pole_game = GamePole()
pole_game.init()
window.init()
window.show()
app.exec()
        
