import sys
from PyQt5.QtWidgets import QApplication, QCheckBox, QVBoxLayout, QWidget

class CheckBoxExample(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        check_box = QCheckBox("Check me", self)

        # Apply styles using CSS
        check_box.setStyleSheet("""
            QCheckBox {
    spacing: 5px;
}

QCheckBox::indicator {
    width: 13px;
    height: 13px;
}

QCheckBox::indicator:unchecked {
    image: url(:/images/checkbox_unchecked.png);
}

        """)

        layout.addWidget(check_box)

        self.setLayout(layout)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Styled QCheckBox')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CheckBoxExample()
    sys.exit(app.exec_())