import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
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

        self.is_ner_used = False
        '''Check if ner is used'''

        self.is_ned_used = False
        '''Check if ned is used'''

        self.text_from_file = None
        '''Check if the txt for nerd is inside a variable or inside a file'''

        self.textbox_text = None
        '''Text from the texbox component'''


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
            QCheckBox {
                color: #ffffff;
            }
        ''')

        

        self.setWindowTitle("NERD")
        self.setGeometry(constant.APP_POS_X, constant.APP_POS_Y, constant.APP_WIDTH, constant.APP_HEIGHT)  # Set initial position (x, y) and size (width, height)

        # Create the main widget and set it as the central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create horizontal layout
        layout = QHBoxLayout(central_widget)
        

        #--------------MANAGING LEFT PANEL--------------#
        label1 = QLabel("", self)
        label1.setFixedSize(300, self.height())

        # EKSERYMENT
        left_layout_widget = QWidget(self)
        left_layout = QVBoxLayout(left_layout_widget)
        left_layout.addWidget(label1)
        left_layout.setContentsMargins(0,0,0,0)
        #left_layout.addWidget(label1)
        left_layout_widget.setFixedSize(300, self.height())


        # TEXTBOX
        self.textbox = QPlainTextEdit(self)
        self.textbox.move(50, 20)
        self.textbox.resize(constant.ELM_WIDTH, constant.ELM_HEIGHT * 4)

        # LOAD TEXBOX TEXT BUTTON
        self.button_texbox = QPushButton('Load text', self)
        self.button_texbox.move(50,140)
        self.button_texbox.resize(constant.ELM_WIDTH, constant.ELM_HEIGHT)
        self.button_texbox.clicked.connect(self.on_load_textbox)

        # Load button
        self.button_load = QPushButton('Load file:', self)
        self.button_load.setToolTip('laod file to perform nerd on')
        self.button_load.move(50,180)
        self.button_load.resize(constant.ELM_WIDTH, constant.ELM_HEIGHT)
        self.button_load.clicked.connect(self.on_load_file)
        '''Load text button'''

        self.button_select_ner = QComboBox(self)
        self.button_select_ner.addItems(self.nerAlgorithms)
        self.button_select_ner.move(50,240)
        self.button_select_ner.resize(120, constant.ELM_HEIGHT)
        self.button_select_ner.currentIndexChanged.connect(self.on_select_ner)

        self.checkbox_ner = QCheckBox('Use NER', self)
        self.checkbox_ner.move(180,240)
        self.checkbox_ner.resize(60, constant.ELM_HEIGHT)
        self.checkbox_ner.stateChanged.connect(self.set_ner)


        self.button_select_ned = QComboBox(self)
        self.button_select_ned.addItems(self.nedAlgorithms)
        self.button_select_ned.move(50,280)
        self.button_select_ned.resize(120, constant.ELM_HEIGHT)
        self.button_select_ned.currentIndexChanged.connect(self.on_select_ned)

        self.checkbox_ned = QCheckBox('Use NED', self)
        self.checkbox_ned.move(180,280)
        self.checkbox_ned.resize(60, constant.ELM_HEIGHT)
        self.checkbox_ned.stateChanged.connect(self.set_ned)
        '''Choice component (ner and ned choice)'''

        self.button_start = QPushButton('Start', self)
        self.button_start.setToolTip('start algorithms')
        self.button_start.move(50,320)
        self.button_start.resize(constant.ELM_WIDTH, constant.ELM_HEIGHT)
        self.button_start.clicked.connect(self.on_start)
        '''Start button'''

        self.button_dataset = QPushButton('Load Dataset', self)
        self.button_dataset.setToolTip('')
        self.button_dataset.move(50,640)
        self.button_dataset.resize(constant.ELM_WIDTH, constant.ELM_HEIGHT)
        self.button_dataset.clicked.connect(self.on_load_dataset)
        '''Load Dataset button'''

        self.button_ned_test = QPushButton('Start NED Test', self)
        self.button_ned_test.setToolTip('')
        self.button_ned_test.move(50,680)
        self.button_ned_test.resize(constant.ELM_WIDTH, constant.ELM_HEIGHT)
        self.button_ned_test.clicked.connect(self.on_start_ned_test)
        '''Start Ned Test button'''

        #--------------MANAGING MIDDLE PANEL--------------#

        # HTML section
        # self.app_html_section = HTMLWindow(int(self.width()/2), self.height())
        # self.app_html_section.setContentsMargins(0,0,0,0)
        
        #self.app_html_section = QWebEnginePage(self)
        self.app_html_section = QWebEngineView(self)
        self.app_html_section.setFixedSize(470, self.height())
        self.app_html_section.setHtml(template)
        
        # self.setCentralWidget(self.app_html_section)
        # self.setFixedSize(width, height)
    
    


        #--------------MANAGING RIGHT PANEL--------------#
        # DBPedia section
        self.dbpedia = QWebEngineView(self)
        self.dbpedia.setFixedSize(470, self.height())
        self.app_html_section.setPage(CustomWebEnginePage(self.dbpedia, self))
        # self.dbpedia.setHtml(template)
        # self.setCentralWidget(self.dbpedia)
        # self.setFixedSize(380, self.height())
        # self.dbpedia.page().
        #label3 = QLabel("", self)
        #label3.setFixedSize(380, self.height())
        

        
        
        layout.addWidget(left_layout_widget)
        layout.addWidget(self.app_html_section)
        #layout.addWidget(label3)
        layout.addWidget(self.dbpedia)
    
        self.setLayout(layout)
      


    @pyqtSlot()
    def on_load_textbox(self):
        self.textbox_text = self.textbox.toPlainText()
        self.EL.load_text_string(self.textbox_text)
        self.text_from_file = False
        self.display_html_content()

    @pyqtSlot()
    def on_load_file(self):
        self.getFile()

    def on_select_ner(self, index):
        self.selectedNER = index

    def on_select_ned(self, index):
        self.selectedNED = index

    def set_ner(self):
        self.is_ner_used = not self.is_ner_used

    def set_ned(self):
        self.is_ned_used = not self.is_ned_used

    @pyqtSlot()
    def on_start(self):
        self.EL.select_ner(self.selectedNER)
        self.EL.select_ned(self.selectedNED)

        if self.text_from_file:
            self.EL.load_text(self.path)
        else:
            self.EL.load_text_string(self.textbox_text)
        
        if self.is_ner_used:
            self.EL.ner()
        if self.is_ned_used:
            self.EL.ned()
        
        self.display_html_content()

    @pyqtSlot()
    def on_load_dataset(self):
        print('Load Dataset')

    @pyqtSlot()
    def on_start_ned_test(self):
        print('Start Ned test')

    
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
        self.text_from_file = True
        self.textbox_text = None
        self.display_html_content()
    

    def display_html_content(self):
        self.dom.find("div[id=content]").text(self.EL.text.get_html_text())
        self.html_content = "<!DOCTYPE html>"+self.dom.referenceToRootElement.html() # = file.read()
        # self.app_html_section.setHtml(self.html_content)
        self.update_html_text(self.html_content)

    def update_html_text(self, content):
        self.app_html_section.setHtml(content)


class CustomWebEnginePage(QWebEnginePage):
    """ Custom WebEnginePage to customize how we handle link navigation """
    def __init__(self, destination, parent=None):
        super().__init__(parent)

        self.destination = destination


    def acceptNavigationRequest(self, url,  _type, isMainFrame):
        if _type == QWebEnginePage.NavigationTypeLinkClicked:
            self.destination.setUrl(url)

            return False
        return super().acceptNavigationRequest(url,  _type, isMainFrame)
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DesktopApplication()
    window.show()
    sys.exit(app.exec_())