from PyQt5.QtGui import QPixmap, QColor, QIcon
from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, QLineEdit, QSpacerItem, \
    QGraphicsDropShadowEffect, QPushButton, QWidget
from PyQt5.QtCore import Qt, pyqtSignal, QSize


class DetailBox(QFrame):
    def __init__(self, number_listed):
        super().__init__()
        self.setContentsMargins(0, 0, 5, 0)

        self.setObjectName("outerFrame")
        self.frame_css = """
            QFrame#outerFrame {
                border-radius: 10px 10px 5px 5px;
                background-color: rgba(7, 16, 19, 15);
                border: 1px solid rgba(120, 120, 120, 55);
            }
            QFrame#outerFrame:hover {
                border-radius: 10px 10px 5px 5px;
                background-color: rgba(7, 16, 19, 50);
            }
        """
        self.setStyleSheet(self.frame_css)

        self.interaction_buttons_frame_css = """
            QFrame {
                background-color: rgba(0, 0, 0, 0);
                border-radius: 5px;
            }
        """

        self.details_text_css = """
            QLabel {
                background-color: rgba(0, 0, 0, 0);
                border-radius: 0px;
                font: 87 12pt "Lato Black";
                color: rgb(255, 255, 255);                    
            }
            """

        self.names_css = """
            QLabel {
                color: rgba(60, 135, 156, 1);
            }
        """
        self.prices_css = """
            QLabel {
                color: rgba(203, 74, 158, 1);
            }
        """
        self.input_background_css = """
            QLineEdit {
                background-color: rgba(7, 16, 19, 0);
                border: none;
                color: rgb(255, 255, 255);
                font: 81 16pt "Lato ExtraBold";
                
            }
        """

        self.buttons_css = """
            QPushButton {
                background-color: rgba(0, 0, 0, 0);
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
        self.input_frame_css = """
            QFrame#inputFrame {
                background-color: rgba(7, 16, 19, 80);
                border-radius: 10px;
                
            }
        """

        shadow_main = QGraphicsDropShadowEffect(self)
        shadow_main.setColor(QColor(0, 0, 0, 105))
        shadow_main.setBlurRadius(10)
        shadow_main.setXOffset(0)
        shadow_main.setYOffset(0)
        self.setGraphicsEffect(shadow_main)

        self.number_listed: int = number_listed
        self.prices = [QLabel("default price") for i in range(0, self.number_listed)]
        self.names = [QLabel("Default name") for i in range(0, self.number_listed)]
        self.plat_icons = [QLabel("") for i in range(0, self.number_listed)]
        self.plat_icon = QPixmap('Resources\\PlatIcon.png')
        self.input = QLineEdit()
        self.search = QPushButton()
        self.search.setIcon(QIcon('Resources\\Search.png'))
        self.gotolink = QPushButton()
        self.gotolink.setIcon(QIcon('Resources\\gotolink.png'))
        self.purchase = QPushButton()
        self.purchase.setIcon(QIcon('Resources\\New\\coins.png'))
        self.buttons = [self.search, self.gotolink, self.purchase]

        name_frame = QFrame()
        name_frame.setContentsMargins(0, 0, 0, 0)
        name_frame.setStyleSheet(self.details_text_css)
        name_vbox = QVBoxLayout()
        name_vbox.setContentsMargins(5, 2, 5, 2)
        name_vbox.setSpacing(0)

        price_frame = QFrame()
        price_frame.setContentsMargins(0, 0, 0, 0)
        price_frame.setStyleSheet(self.details_text_css)
        price_vbox = QVBoxLayout()
        price_vbox.setContentsMargins(0, 2, 2, 2)
        price_vbox.setSpacing(0)

        plat_frame = QFrame()
        plat_frame.setMaximumWidth(28)
        plat_frame.setContentsMargins(0, 0, 0, 0)
        plat_frame.setStyleSheet(self.details_text_css)
        plat_vbox = QVBoxLayout()
        plat_vbox.setContentsMargins(0, 3, 0, 0)
        plat_vbox.setSpacing(0)

        detail_frame = QFrame()
        detail_frame.setContentsMargins(0, 0, 0, 0)
        detail_frame_hbox = QHBoxLayout()
        detail_frame_hbox.setContentsMargins(0, 0, 0, 0)
        detail_frame_hbox.setSpacing(0)

        interaction_buttons_frame = QFrame()
        interaction_buttons_frame.setMaximumWidth(22)
        interaction_buttons_frame.setContentsMargins(0, 0, 0, 0)
        interaction_buttons_frame.setStyleSheet(self.interaction_buttons_frame_css)
        interaction_buttons_vbox = QVBoxLayout()
        interaction_buttons_vbox.setContentsMargins(0, 5, 0, 0)
        interaction_buttons_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.interaction_buttons_top_spacer = QSpacerItem(0, 0)

        detail_interaction_frame = QFrame()
        interaction_buttons_frame.setContentsMargins(0, 0, 0, 0)
        detail_interaction_hbox = QHBoxLayout()
        detail_interaction_hbox.setContentsMargins(0, 0, 0, 0)
        detail_interaction_hbox.setSpacing(0)

        input_frame = QFrame()
        input_frame.setObjectName('inputFrame')
        input_frame.setStyleSheet(self.input_frame_css)
        input_frame.setContentsMargins(27, 0, 5, 0)
        input_frame_hbox = QHBoxLayout()
        input_frame_hbox.setContentsMargins(0, 0, 0, 0)
        input_frame_hbox.setSpacing(0)

        outer_vbox = QVBoxLayout()
        outer_vbox.setContentsMargins(5, 5, 0, 5)
        outer_vbox.setSpacing(0)


        for i in self.names:
            i.setStyleSheet(self.names_css)
            name_vbox.addWidget(i)
            i.setAlignment(Qt.AlignmentFlag.AlignLeft)
            i.setAlignment(Qt.AlignmentFlag.AlignVCenter)
            i.setContentsMargins(0, 0, 0, 0)

        for i in self.prices:
            i.setStyleSheet(self.prices_css)
            price_vbox.addWidget(i, alignment=Qt.AlignRight)
            i.setAlignment(Qt.AlignmentFlag.AlignVCenter)
            i.setContentsMargins(0, 0, 0, 0)

        for i in self.plat_icons:
            i.setPixmap(self.plat_icon)
            i.setScaledContents(True)
            i.setFixedSize(28, 28)
            plat_vbox.addWidget(i, alignment=Qt.AlignCenter)
            i.setAlignment(Qt.AlignmentFlag.AlignCenter)
            i.setContentsMargins(0, 0, 0, 0)

        self.input.setStyleSheet(self.input_background_css)
        self.input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input.setContentsMargins(5, 5, 5, 5)
        self.input.setText('')

        for i in self.buttons:
            i.setFixedSize(22, 22)
            i.setIconSize(QSize(22, 22))
            i.setContentsMargins(0, 0, 0, 0)
            i.setStyleSheet(self.buttons_css)

        shadow_input = QGraphicsDropShadowEffect(self)
        shadow_input.setColor(QColor(0, 0, 0, 205))
        shadow_input.setBlurRadius(20)
        shadow_input.setXOffset(0)
        shadow_input.setYOffset(0)
        input_frame.setGraphicsEffect(shadow_input)

        self.input.textEdited.connect(lambda: print("text"))
        self.input.selectionChanged.connect(lambda: print("text"))


        # Add widgets
        detail_frame_hbox.addWidget(name_frame)
        detail_frame_hbox.addWidget(price_frame)
        detail_frame_hbox.addWidget(plat_frame)

        interaction_buttons_vbox.addWidget(self.gotolink)
        interaction_buttons_vbox.addWidget(self.purchase)
        interaction_buttons_vbox.addItem(interaction_buttons_spacer)

        detail_interaction_hbox.addWidget(detail_frame)
        detail_interaction_hbox.addWidget(interaction_buttons_frame)

        input_frame_hbox.addWidget(self.input)
        input_frame_hbox.addWidget(self.search)

        outer_vbox.addWidget(input_frame)
        outer_vbox.addWidget(detail_interaction_frame)

        # Set layouts
        name_frame.setLayout(name_vbox)
        price_frame.setLayout(price_vbox)
        plat_frame.setLayout(plat_vbox)
        detail_frame.setLayout(detail_frame_hbox)

        interaction_buttons_frame.setLayout(interaction_buttons_vbox)

        detail_interaction_frame.setLayout(detail_interaction_hbox)

        input_frame.setLayout(input_frame_hbox)

        self.setLayout(outer_vbox)