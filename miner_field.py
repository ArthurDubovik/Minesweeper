import random
from PyQt6.QtWidgets import QPushButton, QApplication, QMainWindow, QWidget, QGridLayout, QLabel
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QSize, Qt, QCoreApplication, QPoint, QPropertyAnimation, QUrl
from PyQt6 import QtCore

class MainWindow(QMainWindow):
    def __init__(self): 
        super(MainWindow, self).__init__()
        self.setWindowTitle("Minisweeper")
        self.setWindowIcon(QIcon("./img/window_icon.png"))

        #звуки
        self.sound_click = QSoundEffect()
        self.sound_click.setSource(QUrl.fromLocalFile("./sound/click.wav"))
        self.sound_click.setVolume(0.5)
        self.mine_check = QSoundEffect()
        self.mine_check.setSource(QUrl.fromLocalFile("./sound/mine_check.wav"))
        self.mine_check.setVolume(0.25)
        self.mine_press = QSoundEffect()
        self.mine_press.setSource(QUrl.fromLocalFile("./sound/mine_press.wav"))
        self.mine_press.setVolume(0.25)
        self.sound_win = QSoundEffect()
        self.sound_win.setSource(QUrl.fromLocalFile("./sound/sound_win.wav"))
        self.sound_win.setVolume(0.5)
        

        #button icons
        self.IMG_BANNER = QIcon("./img/banner.png")
        self.IMG_MINE = QIcon("./img/mine.png")
        self.IMG_FALSE_MINE = QIcon("./img/false_mine.png")
        self.IMG_EXPLODE = QIcon("./img/explode_mine.png")
        
        #кнопка New game (новая игра)
        button_action = QAction("New game", self)
        button_action.triggered.connect(self.NewGame)

        #кнопки выбора сложности
        self.button_action2_1 = QAction("2", self)
        #button_action2.triggered.connect()
        self.button_action2_1.setCheckable(True)
        self.button_action2_1.setChecked(True)
        self.button_action2_1.triggered.connect(self.ChangeDiff)

        self.button_action2_2 = QAction("25", self)
        #button_action2.triggered.connect()
        self.button_action2_2.setCheckable(True)
        self.button_action2_2.triggered.connect(self.ChangeDiff)

        self.button_action2_3 = QAction("40", self)
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
        #список с объктами игровых кнопок
        self.cells = []
        #количество кнопок
        self.height = height
        self.width = width
        #количество кнопок с минами
        self.mines = mines
        #число кнопок отмеченных флажком
        self.check_buttons = 0
        #список координат с клетками верно отмеченных мин
        self.checked_mines = []
        #размер кнопок
        self.button_height = self.button_width = 38
        #отступ между кнопками
        self.button_indent = 3
        #расположение элементов в окне
        self.layout = QGridLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        
        #размер игрового поля под количество кнопок
        self.width_size = self.height * self.button_height + (self.height - 1) * self.button_indent 
        self.height_size = self.width * self.button_width + (self.width - 1) * self.button_indent
        self.setFixedSize(QSize(self.width_size, self.height_size))
        
        #создание сетки из кнопок
        for i in range(self.height):
            for j in range(self.width):
                self.button = QPushButton("Button ", self)

                #размер кнопок
                self.button.setFixedSize(QSize(self.button_height, self.button_width))
            
                self.button.setCheckable(True)
                self.button.setText('')
                self.button.clicked.connect(self.open_cell)
                
                #флаг нажатой кнопки
                self.button.is_pressed = False
                #флаг отмеченной мины
                self.button.mine_note = False
                #состояние кнопок после победы
                self.button.win = False
                
                #переопределение для правой кнопки мыши
                self.button.installEventFilter(self)
                self.layout.addWidget(self.button, i, j)
                
                #задание координат кнопкам
                self.button.x = i
                self.button.y = j
                self.cells.append(self.button)
        
        #win button
        self.btn = QLabel(self)
        self.btn.setText('You win!')
        self.btn.resize(200, 60)
        self.btn.setStyleSheet('QLabel {font: bold 44px;}')
        self.btn.hide()

    #Win
    def win_ui(self):
        #включаем Win button
        self.btn.show()

        animation = QPropertyAnimation(self.btn, b'pos', self)
        animation.setKeyValueAt(0, QPoint(20, 30))
        animation.setKeyValueAt(0.65, QPoint(self.height_size - 200, self.width_size - 100))
        animation.setKeyValueAt(1, QPoint(int((self.height_size - 200) / 2), int((self.width_size - 100) / 2)))
        #длительность анимации
        animation.setDuration(20000)
        #запускаем
        animation.start()
        self.sound_win.play()

    #событие NewGame
    def NewGame(self):
        self.sound_win.stop()
        self.btn.hide()
        self.new = False
        
        for i in self.cells:
            i.setText('')

        window.init(self.height, self.width, self.mines)
        pole_game.pole = []
        pole_game.init(self.height, self.width, self.mines)

    #событие выбор уровня сложности
    def ChangeDiff(self):
        sender = self.sender()
        sender.setChecked(True)
        if sender.text() == "2":
            self.mines = 2
            self.button_action2_2.setChecked(False)
            self.button_action2_3.setChecked(False)
            self.NewGame()
            
        if sender.text() == "25":
            self.mines = 25
            self.button_action2_1.setChecked(False)
            self.button_action2_3.setChecked(False)
            self.NewGame()
           
        if sender.text() == "40":
            self.mines = 40
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
        sender.setChecked(True)
        if sender.mine_note != True and sender.is_pressed == False:
            self.sound_click.play()
            sender.is_pressed = True
            
            #число нажатых кнопок
            self.press_buttons = len(list(filter(self.Check_true, [i.is_pressed for i in self.cells])))
            
            #проверка условий победы (если открывается последняя закрытая клетка)
            self.win_check()
            
            #нажатие на мину
            if pole_game.pole[sender.x][sender.y].mine == True:
                self.mine_press.play()
                self.Mine_press(sender)
            #подсчет мин вокруг нажатой кнопки
            elif pole_game.pole[sender.x][sender.y].around_mines > 0:
                    sender.setText(str(pole_game.pole[sender.x][sender.y].around_mines))

                    #number custom colors
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

            #если нажали на пустую ячейку
            if pole_game.pole[sender.x][sender.y].around_mines == 0 and pole_game.pole[sender.x][sender.y].mine != True:
                self.rec_open(sender.x, sender.y)
        
        
    #нажатие на мину
    def Mine_press(self, sender):
        for i in self.cells:
            if [i.x, i.y] in pole_game.rij and i.mine_note == False:
                i.setCheckable(True)
                i.setChecked(True)
                i.setIcon(QIcon(self.IMG_MINE))
                i.setIconSize(QSize(35,35))
            if i.isChecked() == False:
                i.setCheckable(False)
            if i.mine_note == True and [i.x, i.y] not in pole_game.rij:
                i.setIcon(QIcon(self.IMG_FALSE_MINE))
                i.setIconSize(QSize(38,38))
            i.is_pressed = True
        sender.setIcon(QIcon(self.IMG_EXPLODE))
        sender.setIconSize(QSize(35,35))

    #открытие пустых ячеек вокруг выбранной пустой
    def rec_open(self, x, y):
        for i in self.cells:
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
    def Check_true(x):
        if x == True:
            return x
    
    #обработка нажатия правой кнопоки мыши
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            #if event.button() == Qt.MouseButton.LeftButton:
                #print(obj.objectName(), "Left click")

            
            if event.button() == Qt.MouseButton.RightButton:
                #print(obj.objectName(), "Right click")
                
                #отметка мин на поле
                if obj.is_pressed == False and obj.win == False:
                    if obj.mine_note == False:
                        self.mine_check.play()
                        obj.setIcon(QIcon(self.IMG_BANNER))
                        obj.setIconSize(QSize(34,34))
                        
                        obj.mine_note = True
                        obj.setCheckable(False)
                        if pole_game.pole[obj.x][obj.y].mine == True:
                            if [obj.x, obj.y] not in self.checked_mines:
                                self.checked_mines.append([obj.x, obj.y])
                    
                    else:
                        obj.mine_note = False
                        obj.setIcon(QIcon())
                        obj.setCheckable(True)
                        if [obj.x, obj.y] in self.checked_mines:
                                self.checked_mines.remove([obj.x, obj.y])

                #число кнопок отмеченных флажком
                self.check_buttons = len(list(filter(self.Check_true, [i.mine_note for i in self.cells])))

                self.win_check()
                #elif event.button() == Qt.MouseButton.MiddleButton:
                    #print(obj.objectName(), "Middle click")
        return QtCore.QObject.event(obj, event)

    #проверка победных условий
    def win_check(self):
        if sorted(self.checked_mines) == sorted(pole_game.rij) and self.check_buttons == self.mines:
            if self.press_buttons == len(self.cells) - self.mines:
                self.checked_mines = []
                for i in self.cells:
                    i.win = True
                self.win_ui()

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
        self.rij = []
        
        #заполение поля минами
        mine_count = 0
        while mine_count < self.mines:
            r = [random.randrange(self.N), random.randrange(self.M)]
            if r not in self.rij:
                self.rij.append(r)
                self.pole[r[0]][r[1]].mine = True
                mine_count += 1
        
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
        
