import sys
from BlurWindow.blurWindow import GlobalBlur
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QFrame, QApplication, QWidget
from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal, QObject, QThreadPool, QRunnable
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        GlobalBlur(self.winId(), Dark=True)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setWindowFlag(Qt.FramelessWindowHint)
        self.setStyleSheet('background-color: rgba(0, 0, 0, 0)')
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle('WF Prices')
        self.setWindowIcon(QIcon('Resources\\Warframe market logo crop (1).png'))

        self.thread_pool = QThreadPool.globalInstance()
        self.box_amount = 12
        self.frame_boxes = {f'{i}': DetailBox(6) for i in range(self.box_amount)}


        with open('items.json', 'r') as file:
            items = json.load(file)
            file.close()



        main_grid = QGridLayout()
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


        self.threads = []


        main_frame = QFrame(self)
        main_frame.setLayout(main_grid)
        self.setCentralWidget(main_frame)


    def search_item(self, orders_dict: dict, frame):
        orders_dict: dict = orders_dict
        try:
            for i in range(0, self.frame_boxes['0'].number_listed):
                frame.names[i].setText(orders_dict['sell'][i]['ingame_name'])
                frame.names[i].setAlignment(Qt.AlignmentFlag.AlignLeft)
                frame.names[i].setAlignment(Qt.AlignmentFlag.AlignVCenter)
                frame.prices[i].setText(str(orders_dict['sell'][i]['platinum']))
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
        task.idk.result.connect(self.search_item)
        self.thread_pool.start(task)


if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())