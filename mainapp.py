import os
import sys
from BlurWindow.blurWindow import GlobalBlur
from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QFrame, QApplication, QWidget, QVBoxLayout, QSizeGrip, \
    QHBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal, QObject, QThreadPool, QRunnable, QRect
from pyqt_frameless_window import FramelessMainWindow
from detailbox import DetailBox
from Api_Orders import orders
import time
import json

class Idk(QObject):
    result = pyqtSignal(dict, object)


class Worker(QRunnable):
    def __init__(self, item_name, frame):
        super().__init__()
        self.item_name = item_name
        self.frame = frame
        self.idk = Idk()

    def run(self):
        orders_dict: dict = orders(self.item_name)
        self.idk.result.emit(orders_dict, self.frame)


class MainWindow(FramelessMainWindow):
    def __init__(self):
        super().__init__()
        GlobalBlur(self.winId(), Dark=True)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setStyleSheet('background-color: rgba(0, 0, 0, 0)')
        self.setContentsMargins(0, 0, 0, 0)


        screens = app.primaryScreenChanged.connect(lambda: print("hmmmm"))
        #uhh
        # for i in screens:
        #     print(i.logicalDotsPerInch())
        # print(screens)


        with open("appsize.json", 'r') as f:
            appgeo = json.load(f)
        self.setGeometry(QRect(appgeo[0], appgeo[1], appgeo[2], appgeo[3]))

        self.buttons_css = """
            #close_btn:hover {
                background-color: rgb(232, 17, 35);
                border-radius: 5px;
            }
            #close_btn:pressed {
                background-color: rgba(232, 17, 35, 150);
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: rgba(135, 135, 135, 255);
                border-radius: 5px;
            }
            QPushButton:pressed {
                background-color: rgba(135, 135, 135, 170);
                border-radius: 5px;
            }
        """


        self.thread_pool = QThreadPool.globalInstance()
        self.tasks = []
        self.box_amount = 12
        self.frame_boxes = {f'{i}': DetailBox(6) for i in range(self.box_amount)}
        self.main_frame = QFrame()
        self.boxes_frame = QFrame()

        self.tbar_frame = QFrame()
        self.window_icon = QLabel()
        self.window_icon_pix = QPixmap('Resources\\Warframe market logo crop.png')
        self.window_icon.setPixmap(self.window_icon_pix)
        self.window_icon.setScaledContents(True)
        self.window_title = QLabel("WFM Prices")
        self.refresh_btn = QPushButton()
        self.refresh_btn.setIcon(QIcon("Resources\\refresh.png"))
        self.close_btn = QPushButton()
        self.close_btn.setObjectName("close_btn")
        self.close_btn.setIcon(QIcon("Resources\\icons8-close-100.png"))
        # self.maximize_btn = QPushButton()
        self.minimize_btn = QPushButton()
        self.minimize_btn.setIcon(QIcon("Resources\\icons8-minimize-100.png"))
        self.buttons = [self.refresh_btn, self.minimize_btn, self.close_btn]


        outer_vlay = QVBoxLayout()
        outer_vlay.setSpacing(0)
        outer_vlay.setContentsMargins(0, 0, 0, 0)

        main_grid = QGridLayout()
        main_grid.setContentsMargins(5, 0, 5, 5)

        tbar_hlay = QHBoxLayout()
        tbar_hlay.setSpacing(0)
        tbar_hlay.setContentsMargins(5, 0, 0, 0)
        tbar_spacer = QSpacerItem(100, 1, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)


        with open('items.json', 'r') as file:
            items = json.load(file)
            file.close()
        row: int = 0
        col: int = 0
        cols = 3
        for idi, i in enumerate(self.frame_boxes.items()):
            i[1].search.clicked.connect(self.start_thread)
            i[1].input.setText(items[f"{idi}"])
            i[1].search.click()

            if 9 <= self.box_amount <= 18:
                cols = self.box_amount/3
            if self.box_amount > 18:
                cols = 5
            if self.box_amount > 30:
                cols = 6
            if self.box_amount <= 6:
                cols = 2
            main_grid.addWidget(i[1], row, col)
            row += 1
            if row == cols:
                col += 1
                row = 0

        self.close_btn.clicked.connect(self.close_app)
        self.minimize_btn.clicked.connect(lambda: self.showMinimized())

        self.main_frame.setContentsMargins(0, 0, 0, 0)
        self.tbar_frame.setContentsMargins(0, 0, 0, 0)

        for i in self.buttons:
            i.setFixedSize(QSize(30, 30))
            i.setIconSize(QSize(30, 30))
            i.setStyleSheet(self.buttons_css)

        self.window_icon.setFixedSize(QSize(30, 30))
        self.refresh_btn.setFixedSize(QSize(27, 27))
        self.refresh_btn.setIconSize(QSize(27, 27))
        self.window_title.setContentsMargins(10, 0, 20, 0)


        tbar_hlay.addWidget(self.window_icon)
        tbar_hlay.addWidget(self.window_title)
        tbar_hlay.addWidget(self.refresh_btn)
        tbar_hlay.addItem(tbar_spacer)
        tbar_hlay.addWidget(self.minimize_btn)
        tbar_hlay.addWidget(self.close_btn)

        outer_vlay.addWidget(self.tbar_frame)
        outer_vlay.addWidget(self.boxes_frame)

        
        self.tbar_frame.setLayout(tbar_hlay)
        self.boxes_frame.setLayout(main_grid)
        self.main_frame.setLayout(outer_vlay)

        self.setCentralWidget(self.main_frame)

    def close_app(self):
        app_location = self.frameGeometry().getRect()
        with open("appsize.json", 'w') as f:
            json.dump(app_location, f)
            f.close()

        self.close()
        raise RuntimeError("QThreadPool wont let me out ); helpppp!")


    def search_item(self, orders_dict: dict, frame):
        orders_dict: dict = orders_dict
        try:
            list_range = range(0, self.frame_boxes['0'].number_listed)
            if len(orders_dict['sell']) < self.frame_boxes['0'].number_listed:
                list_range = range(0, len(orders_dict['sell']))

            for i in list_range:
                frame.names[i].setText(orders_dict['sell'][i]['ingame_name'])
                frame.prices[i].setText(str(orders_dict['sell'][i]['platinum']))
                frame.names[i].setAlignment(Qt.AlignmentFlag.AlignLeft)
                frame.names[i].setAlignment(Qt.AlignmentFlag.AlignVCenter)

        except Exception:
            for i in range(0, self.frame_boxes['0'].number_listed):
                frame.names[i].setText('')
                frame.names[i].setAlignment(Qt.AlignmentFlag.AlignCenter)
                frame.prices[i].setText('')
                frame.names[0].setText("Failed\nWrong item name\nor bad connection to WFM")


    def start_thread(self):
        sender = self.sender()
        frame = self.sender().parent().parent()
        item_name = frame.input.text()


        index = 0
        for i in self.frame_boxes.values():
            if i == frame:
                break
            else:
                index+=1

        with open('items.json', 'r') as raw:
            items: dict = json.load(raw)
            items[f'{index}'] = item_name
            raw.close()
        with open('items.json', 'w') as file:
            json.dump(items, file)
            file.close()

        task = Worker(item_name, frame)
        self.tasks.append(task)
        task.idk.result.connect(self.search_item)
        self.thread_pool.start(task)


if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())