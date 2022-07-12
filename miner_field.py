import random
from PyQt6.QtWidgets import QPushButton, QApplication, QMainWindow, QWidget, QGridLayout
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import QSize, Qt
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
        self.cells = []
        super(MainWindow, self).__init__()
    
        self.setWindowTitle("My App")
        self.layout = QGridLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        
        #количество полей
        self.height = self.width = 16

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
   
    #открытие поля по клику
    def open_cell(self):
        sender = self.sender()
        if sender.mine_note != True:
            #выключаем кнопку после нажалия ЛКМ
            sender.setDisabled(True)
            sender.is_pressed = True
            
            if pole_game.pole[sender.x][sender.y].mine == True:
                sender.setText('XX')
                for i in self.cells:
                    i.click()
                    if i.mine_note == True:
                        i.mine_note = False
                        i.setCheckable(True)
                        i.setStyleSheet("background-color: white")
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
            if event.button() == Qt.MouseButton.LeftButton:
                print(obj.objectName(), "Left click")
            elif event.button() == Qt.MouseButton.RightButton:
                print(obj.objectName(), "Right click")

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

            elif event.button() == Qt.MouseButton.MiddleButton:
                print(obj.objectName(), "Middle click")
        return QtCore.QObject.event(obj, event)

#описание игровой ячейки
class Cell:
    def __init__(self, around_mines, mine):
        self.around_mines = around_mines
        self.mine = mine
        self.fl_open = False

#описание игрового поля
class GamePole:
    def __init__(self, N, M):
        self.M = M
        self.N = N
        self.pole = [[(Cell(0, False)) for i in range(N)] for i in range(N)]
    def init(self):
        rij = []
        l = 0
        while l < self.M:
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
pole_game = GamePole(window.height, window.width)
pole_game.init()
window.init()
window.show()
app.exec()
        
