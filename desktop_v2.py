import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import constant

from entity_linking_system import EntityLinkingSystem

import ntpath
from htmldom import htmldom


class DesktopApplication(QMainWindow):
    def __init__(self, ):
        super().__init__()

        self.path = None
        '''A path to the file to perform nerd on'''

        self.text = None
        '''Text'''

        self.selectedNER = 0
        '''Selected NER Algorithm, default is 0'''

        self.selectedNED = 0
        '''Selected NED Algorithm, default is 0'''

        self.nerAlgorithms = ['one', 'two', 'threeeeee']
        '''NER Algorithms'''

        self.nedAlgorithms = ['four', 'five', 'six']
        '''NED Algorithms'''

        tfile = open(f"./file/template.xhtml", mode= "r" , encoding="utf-8")
        template = tfile.read()
        tfile.close()
        self.dom = htmldom.HtmlDom().createDom(template)
        '''Template'''

        self.html_content = None
        '''HTML text'''

        self.EL = EntityLinkingSystem()
        '''System creation'''

        self.nerAlgorithms = self.EL.get_ners()
        '''NER Algorithms'''

        self.nedAlgorithms = self.EL.get_neds()
        '''NED Algorithms'''


        self.setStyleSheet('''
            QMainWindow {
                background-color: #2b2b2b;  /* Dark background color */
                color: #ffffff;  /* Text color */
            }
            
            QPushButton {
                background-color: #4c4c4c;  /* Dark button color */
                color: #ffffff;  /* Button text color */
                border: 1px solid #333333;  /* Button border color */
            }

            QPushButton:hover {
                background-color: #5a5a5a;  /* Darker button color on hover */
            }
                           
            QLabel {
                background-color: #424242;
                color: #ffffff;
            }
        ''')



        
        

        self.setWindowTitle("HTML Viewer")
        # self.setWindowFlag(Qt.FramelessWindowHint)
        self.setGeometry(constant.APP_POS_X, constant.APP_POS_Y, constant.APP_WIDTH, constant.APP_HEIGHT)  # Set initial position (x, y) and size (width, height)

        # Create the main widget and set it as the central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        # Create horizontal layout
        layout = QHBoxLayout(central_widget)
        self.setLayout(layout)
        

        #--------------MANAGING LEFT PANEL--------------#
        label1 = QLabel("", self)
        label1.setFixedSize(380, self.height())

        # TEXTBOX
        self.textbox = QPlainTextEdit(self)
        self.textbox.move(100, 20)
        self.textbox.resize(constant.ELM_WIDTH, constant.ELM_HEIGHT * 4)

        # LOAD TEXBOX TEXT BUTTON
        self.button_texbox = QPushButton('Load text', self)
        self.button_texbox.move(100,140)
        self.button_texbox.resize(constant.ELM_WIDTH, constant.ELM_HEIGHT)

        # Load button
        self.button_load = QPushButton('Load file:', self)
        self.button_load.setToolTip('laod file to perform nerd on')
        self.button_load.move(100,180)
        self.button_load.resize(constant.ELM_WIDTH, constant.ELM_HEIGHT)
        self.button_load.clicked.connect(self.on_load)
        '''Load text button'''

        # NER button
        self.button_select_ner = QPushButton('Select NER:', self)
        self.button_select_ner.setToolTip('Select NER algorithm')
        self.button_select_ner.move(100,240)
        self.button_select_ner.resize(constant.ELM_WIDTH, constant.ELM_HEIGHT)
        self.button_select_ner.clicked.connect(self.on_select_ner)

        self.ner_menu = QMenu(self)
        i = 0
        for ner_alg in self.nerAlgorithms:
            option = QAction(ner_alg, self)
            option.triggered.connect(lambda: self.on_select_ner(i))
            self.ner_menu.addAction(option)
            i = i + 1

        self.button_select_ner.setMenu(self.ner_menu)


        self.button_select_ned = QPushButton('Select NED:', self)
        self.button_select_ned.setToolTip('Select NED algorithm')
        self.button_select_ned.move(100,280)
        self.button_select_ned.resize(constant.ELM_WIDTH, constant.ELM_HEIGHT)
        self.button_select_ned.clicked.connect(self.on_select_ned)

        self.ned_menu = QMenu(self)
        j = 0
        for ned_alg in self.nedAlgorithms:
            option = QAction(ned_alg, self)
            # option.
            option.triggered.connect(lambda: self.on_select_ned(ned_alg))
            self.ned_menu.addAction(option)
            j = j + 1

        self.button_select_ned.setMenu(self.ned_menu)
        '''Choice component (ner and ned choice)'''

        self.button_start = QPushButton('Start', self)
        self.button_start.setToolTip('start algorithms')
        self.button_start.move(100,320)
        self.button_start.resize(constant.ELM_WIDTH, constant.ELM_HEIGHT)
        self.button_start.clicked.connect(self.on_start)
        '''Start button'''

        self.button_save = QPushButton('Save HTML', self)
        self.button_save.setToolTip('Save HTML file')
        self.button_save.move(100,640)
        self.button_save.resize(constant.ELM_WIDTH, constant.ELM_HEIGHT)
        self.button_save.clicked.connect(self.on_save)
        '''Save button'''

        #--------------MANAGING MIDDLE PANEL--------------#
        


        # HTML section
        self.app_html_section = HTMLWindow(int(self.width()/2), self.height())


        # DBPedia section
        label3 = QLabel("", self)
        label3.setFixedSize(380, self.height())
        


        # Add sections to layout
        layout.addWidget(label1)
        layout.addWidget(self.app_html_section)
        layout.addWidget(label3)
        

    def show_menu(self):
        # Show the menu at the button's position
        self.menu.exec_(self.button.mapToGlobal(self.button.rect().bottomLeft()))

    def menu_action(self, option):
        print(f'Chose: {option}')


    @pyqtSlot()
    def on_load(self):
        self.getFile()

    @pyqtSlot()
    def on_select_ner(self, index):
        self.selectedNER = index
        print('bloblbloblblRRRRRRRRRRRR', index)

    @pyqtSlot()
    def on_select_ned(self, index):
        self.selectedNED = index
        print('bloblbloblblDDDDDDDDDDDD', index)

    @pyqtSlot()
    def on_start(self):
        self.EL.select_ner(self.selectedNER)
        self.EL.select_ned(self.selectedNED)
        self.EL.load_text(self.path)
        
        fileName = ntpath.basename(self.path)
        self.EL.ner()
        self.EL.ned()
        self.display_html_content()

    @pyqtSlot()
    def on_save(self):
        print('PyQt5 button click')

    
    def getFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        path_to_file, _ = QFileDialog.getOpenFileName(self,"Load file", None,"TXT|JSON (*.txt *.json);;HTML Files (*.html)", options=options)
        if path_to_file:
            print(path_to_file)
            self.path = path_to_file
            self.select_file()


    def select_file(self):
        fileName = ntpath.basename(self.path)
        self.button_load.setText(fileName)
        self.button_load.update()

        '''Displaying unedited text'''
        self.EL.load_text(self.path)
        self.display_html_content()
    

    def display_html_content(self):
        self.dom.find("div[id=content]").text(self.EL.text.get_html_text())
        self.html_content = "<!DOCTYPE html>"+self.dom.referenceToRootElement.html() # = file.read()
        # self.app_html_section.setHtml(self.html_content)
        self.app_html_section.update_html_text(self.html_content)


class HTMLWindow(QMainWindow):
    def __init__(self, width, height):
        super().__init__()

        tfile = open("siem.html", mode= "r" , encoding="utf-8")
        template = tfile.read()
        tfile.close()

        self.web_engine_view = QWebEngineView(self)
        self.web_engine_view.setHtml(template)
        self.setCentralWidget(self.web_engine_view)
        self.setFixedSize(width, height)
    
    def update_html_text(self, content):
        self.web_engine_view.setHtml(content)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DesktopApplication()
    window.show()
    sys.exit(app.exec_())