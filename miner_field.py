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
        super(MainWindow, self).__init__()
    
        self.setWindowTitle("Minisweeper")
        
        #кнопка New game (новая игра)
        button_action = QAction("New game", self)
        button_action.triggered.connect(self.NewGame)

        #кнопки выбора сложности
        self.button_action2_1 = QAction("10", self)
        #button_action2.triggered.connect()
        self.button_action2_1.setCheckable(True)
        self.button_action2_1.setChecked(True)
        self.button_action2_1.triggered.connect(self.ChangeDiff)

        self.button_action2_2 = QAction("20", self)
        #button_action2.triggered.connect()
        self.button_action2_2.setCheckable(True)
        self.button_action2_2.triggered.connect(self.ChangeDiff)

        self.button_action2_3 = QAction("30", self)
        #button_action2.triggered.connect()
        self.button_action2_3.setCheckable(True)
        self.button_action2_3.triggered.connect(self.ChangeDiff)
    
        #кнопки выбора размера игрового поля
        self.button_action3_1 = QAction("12 x 12", self)
        #button_action3.triggered.connect()
        self.button_action3_1.setCheckable(True)
        self.button_action3_1.setChecked(True)
        self.button_action3_1.triggered.connect(self.ChangeSize)

        self.button_action3_2 = QAction("16 x 16", self)
        #button_action3.triggered.connect()
        self.button_action3_2.setCheckable(True)
        self.button_action3_2.triggered.connect(self.ChangeSize)

        self.button_action3_3 = QAction("20 x 20", self)
        #button_action3.triggered.connect()
        self.button_action3_3.setCheckable(True)
        self.button_action3_3.triggered.connect(self.ChangeSize)
       
        #Кнопка и событие Exit (закрытие приложения)
        button_action4 = QAction("Exit", self)
        button_action4.triggered.connect(QCoreApplication.instance().quit)

        menu = self.menuBar()

        file_menu = menu.addMenu("Menu")
        file_menu.addAction(button_action)
        file_menu.addSeparator()

        file_submenu = file_menu.addMenu("Difficult")
        file_submenu.addAction(self.button_action2_1)
        file_submenu.addAction(self.button_action2_2)
        file_submenu.addAction(self.button_action2_3)
        file_submenu = file_menu.addMenu("Field size")
        file_submenu.addAction(self.button_action3_1)
        file_submenu.addAction(self.button_action3_2)
        file_submenu.addAction(self.button_action3_3)
        
        file_menu.addSeparator()
        file_menu.addAction(button_action4)
        
    #заполнение игрового поля кнопками
    def init(self, height=12, width=12, mines=10):
        #список с объктами кнопок
        self.cells = []
        
        #количество кнопок
        self.height = height
        self.width = width

        #количество кнопок с минами
        self.mines = mines

        #размер кнопок
        self.button_height = self.button_width = 38

        #отступ между кнопками
        self.button_indent = 3
        
        #расположение элементов в окне
        self.layout = QGridLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        
        #размера игрового поля под количество кнопок
        self.setFixedSize(QSize(self.height * self.button_height + (self.height - 1) * self.button_indent , self.width * self.button_width + (self.width - 1) * self.button_indent ))
        
        for i in range(self.height):
            for j in range(self.width):
                self.button = QPushButton("Button ", self)

                #шрифт кнопок
                self.button.setStyleSheet("QPushButton"
                             "{"
                             "font: bold 18px;"
                             "}"
                             )
                
                #размер кнопок
                self.button.setFixedSize(QSize(self.button_height, self.button_width))
            
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
    def NewGame(self):
        for i in self.cells:
            i.setText('')

        window.init(self.height, self.width, self.mines)
        pole_game.pole = []
        pole_game.init(self.height, self.width, self.mines)

    #событие выбор уровня сложности
    def ChangeDiff(self):
        sender = self.sender()
        sender.setChecked(True)
        if sender.text() == "10":
            self.mines = 10
            self.button_action2_2.setChecked(False)
            self.button_action2_3.setChecked(False)
            self.NewGame()
            
        if sender.text() == "20":
            self.mines = 20
            self.button_action2_1.setChecked(False)
            self.button_action2_3.setChecked(False)
            self.NewGame()
           
        if sender.text() == "30":
            self.mines = 30
            self.button_action2_1.setChecked(False)
            self.button_action2_2.setChecked(False)
            self.NewGame()
    
    #событие выбор размера поля
    def ChangeSize(self):
        sender = self.sender()
        sender.setChecked(True)
        if sender.text() == "12 x 12":
            self.height = self.width = 12
            self.button_action3_2.setChecked(False)
            self.button_action3_3.setChecked(False)
            self.NewGame()
            
        if sender.text() == "16 x 16":
            self.height = self.width = 16
            self.button_action3_1.setChecked(False)
            self.button_action3_3.setChecked(False)
            self.NewGame()
           
        if sender.text() == "20 x 20":
            self.height = self.width = 20
            self.button_action3_1.setChecked(False)
            self.button_action3_2.setChecked(False)
            self.NewGame()
        
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
                        #obj.setStyleSheet("background-color: yellow")
                        obj.mine_note = True
                        obj.setCheckable(False)
                    else:
                        #obj.setStyleSheet("background-color: white")
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

#описание внутреннего игрового поля
class GamePole:
    def init(self, height=12, width=12, mines=10):
        #число ячеек
        self.M = height
        self.N = width
        #количество мин
        self.mines = mines

        #заполнение списка ячеек нулями
        self.pole = [[(Cell(0, False)) for i in range(self.N)] for i in range(self.M)]
        
        #список с минами
        rij = []
        
        #заполение поля минами
        mine_count = 0
        while mine_count < self.mines:
            r = [random.randrange(self.N), random.randrange(self.M)]
            if r not in rij:
                rij.append(r)
                self.pole[r[0]][r[1]].mine = True
                mine_count += 1
        print(mine_count)
        print(len(rij))
        
        #подчет количества мин вокруг каждой ячейки
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
pole_game = GamePole()
window.init()
pole_game.init()

window.show()
app.exec()
        
