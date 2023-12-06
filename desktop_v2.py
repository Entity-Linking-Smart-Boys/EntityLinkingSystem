import sys
import ctypes
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

        self.use_ner_class = False
        '''Check if ner class is taken into consideration'''

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
            QPlainTextEdit {
                background-color: #202020;
                color: #ffffff;
                border: 1px solid #333333;
            }
            QComboBox {
                background-color: #424242;
                color: #ffffff;
                border: 1px solid #333333;
            }
            checkbox {
                background-color: #424242;
            }
            QComboBox:indicator {
                background-color:red;
            }
        ''')


        self.setWindowTitle("NERD")
        self.setWindowIcon(QIcon("file/icon.png"))
        self.setGeometry(constant.APP_POS_X, constant.APP_POS_Y, constant.APP_WIDTH, constant.APP_HEIGHT)  # Set initial position (x, y) and size (width, height)
        self.setFixedSize(constant.APP_WIDTH, constant.APP_HEIGHT + 20)
        # self.setWindowFlags(Qt.FramelessWindowHint)

        # Create the main widget and set it as the central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create horizontal layout
        layout = QHBoxLayout(central_widget)
        

        #--------------MANAGING LEFT PANEL--------------#
        label1 = QLabel("", self)
        label1.setFixedSize(220, self.height())

        # EXPERIMENT
        left_layout_widget = QWidget(self)
        left_layout = QVBoxLayout(left_layout_widget)
        left_layout.addWidget(label1)
        left_layout.setContentsMargins(0,0,0,0)
        #left_layout.addWidget(label1)
        left_layout_widget.setFixedSize(220, constant.APP_HEIGHT)


        # TEXTBOX
        self.textbox = QPlainTextEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(constant.ELM_WIDTH, constant.ELM_HEIGHT * 4)

        # LOAD TEXBOX TEXT BUTTON
        self.button_texbox = QPushButton('Load text', self)
        self.button_texbox.move(20,140)
        self.button_texbox.resize(constant.ELM_WIDTH, constant.ELM_HEIGHT)
        self.button_texbox.clicked.connect(self.on_load_textbox)

        # Load button
        self.button_load = QPushButton('Load file:', self)
        self.button_load.setToolTip('laod file to perform nerd on')
        self.button_load.move(20,180)
        self.button_load.resize(constant.ELM_WIDTH, constant.ELM_HEIGHT)
        self.button_load.clicked.connect(self.on_load_file)
        '''Load text button'''

        self.button_select_ner = QComboBox(self)
        self.button_select_ner.addItems(self.nerAlgorithms)
        self.button_select_ner.move(20,240)
        self.button_select_ner.resize(120, constant.ELM_HEIGHT)
        self.button_select_ner.currentIndexChanged.connect(self.on_select_ner)

        self.checkbox_ner = QCheckBox('Use NER', self)
        self.checkbox_ner.move(150,240)
        self.checkbox_ner.resize(60, constant.ELM_HEIGHT)
        self.checkbox_ner.stateChanged.connect(self.set_ner)


        self.button_select_ned = QComboBox(self)
        self.button_select_ned.addItems(self.nedAlgorithms)
        self.button_select_ned.move(20,280)
        self.button_select_ned.resize(120, constant.ELM_HEIGHT)
        self.button_select_ned.currentIndexChanged.connect(self.on_select_ned)

        self.checkbox_ned = QCheckBox('Use NED', self)
        self.checkbox_ned.move(150,280)
        self.checkbox_ned.resize(60, constant.ELM_HEIGHT)
        self.checkbox_ned.stateChanged.connect(self.set_ned)
        '''Choice component (ner and ned choice)'''

        self.checkbox_ner_classes = QCheckBox('Use NER classes', self)
        self.checkbox_ner_classes.move(20,320)
        self.checkbox_ner_classes.resize(constant.ELM_WIDTH, constant.ELM_HEIGHT)
        self.checkbox_ner_classes.setDisabled(True)
        self.checkbox_ner_classes.stateChanged.connect(self.set_ner_classes)

        self.button_start = QPushButton('Start', self)
        self.button_start.setToolTip('start algorithms')
        self.button_start.move(20,360)
        self.button_start.resize(constant.ELM_WIDTH, constant.ELM_HEIGHT)
        self.button_start.clicked.connect(self.on_start)
        '''Start button'''

        self.button_dataset = QPushButton('Load Dataset', self)
        self.button_dataset.setToolTip('Load a dataset to perform test on')
        self.button_dataset.move(20,560)
        self.button_dataset.resize(constant.ELM_WIDTH, constant.ELM_HEIGHT)
        self.button_dataset.clicked.connect(self.on_load_dataset)
        '''Load Dataset button'''

        self.button_ned_test = QPushButton('Start NED Test', self)
        self.button_ned_test.setToolTip('Start tests')
        self.button_ned_test.move(20,600)
        self.button_ned_test.resize(constant.ELM_WIDTH, constant.ELM_HEIGHT)
        self.button_ned_test.clicked.connect(self.on_start_ned_test)
        '''Start Ned Test button'''

        self.micro_accuracy = QLabel('Micro accuracy: ', self)
        self.micro_accuracy.move(20,640)
        self.micro_accuracy.resize(constant.ELM_WIDTH, constant.ELM_HEIGHT)

        self.macro_accuracy = QLabel('Macro accuracy: ', self)
        self.macro_accuracy.move(20,680)
        self.macro_accuracy.resize(constant.ELM_WIDTH, constant.ELM_HEIGHT)

        

        #--------------MANAGING MIDDLE PANEL--------------#

        # HTML section
        # self.app_html_section = HTMLWindow(int(self.width()/2), self.height())
        # self.app_html_section.setContentsMargins(0,0,0,0)
        
        #self.app_html_section = QWebEnginePage(self)
        self.app_html_section = QWebEngineView(self)
        self.app_html_section.setFixedSize(510, constant.APP_HEIGHT)
        
        # self.setCentralWidget(self.app_html_section)
        # self.setFixedSize(width, height)
    
    


        #--------------MANAGING RIGHT PANEL--------------#
        # DBPedia section
        self.dbpedia = QWebEngineView(self)
        self.dbpedia.setFixedSize(510, constant.APP_HEIGHT)
        self.app_html_section.setPage(CustomWebEnginePage(self.dbpedia, self))
        

        #--------------CHANGING BACKGROUND OF HTML ELEMENTS--------------#
        self.dbpedia.setHtml("<!DOCTYPE html>"+self.dom.referenceToRootElement.html())
        self.app_html_section.setHtml("<!DOCTYPE html>"+self.dom.referenceToRootElement.html())


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
        self.getFile(False)

    def on_select_ner(self, index):
        self.selectedNER = index
        # self.EL.select_ner(self.selectedNER)

    def on_select_ned(self, index):
        self.selectedNED = index
        self.unckeck_ner_classes()
        # self.EL.select_ned(self.selectedNED)

    def set_ner(self):
        self.is_ner_used = not self.is_ner_used

    def set_ned(self):
        self.is_ned_used = not self.is_ned_used
        if self.is_ned_used:
            self.checkbox_ner_classes.setEnabled(True)
        else:
            self.checkbox_ner_classes.setDisabled(True)
            self.unckeck_ner_classes()
            # self.use_ner_class = False
            # self.checkbox_ner_classes.setChecked(False)
            # print(self.use_ner_class)
            # self.checkbox_ner_classes.update()
    
    def set_ner_classes(self):
        self.use_ner_class = not self.use_ner_class
        print('tutaj jest w fukcnji zmiana', self.use_ner_class)

    def unckeck_ner_classes(self):
        self.checkbox_ner_classes.setChecked(False)
        #print(self.use_ner_class)
        self.checkbox_ner_classes.update()

    @pyqtSlot()
    def on_start(self):
        if not self.EL.text:
            return

        self.EL.select_ner(self.selectedNER)
        self.EL.select_ned(self.selectedNED)
        self.EL.ned_use_ner_class(self.use_ner_class)

        # if self.use_ner_class:
        #     self.EL.select_ned(self.selectedNED, True)
        # else:
        #     self.EL.select_ned(self.selectedNED, False)

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
        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        # path_to_file, _ = QFileDialog.getOpenFileName(self,"Load dataset", None,"JSON (*.json)", options=options)
        # if path_to_file:
        #     print(path_to_file)
        #     self.EL.load_dataset(path_to_file)
        self.getFile(True)
        print('Load Dataset')

    @pyqtSlot()
    def on_start_ned_test(self):
        # if not self.EL.NED:
        #     return
        if not hasattr(self.EL.test, "dataset"):
            return
        self.EL.select_ned(self.selectedNED)


        #self.unckeck_ner_classes()
        #self.use_ner_class = False
        class_status = self.EL.ned_use_ner_class
        self.EL.ned_use_ner_class(False)
        self.EL.ned_tests()
        self.EL.ned_use_ner_class = class_status

        accuracies = self.EL.get_accuracy()

        self.micro_accuracy.setText('Micro accuracy: ' + str(accuracies[0]))
        self.micro_accuracy.update()
        self.macro_accuracy.setText('Macro accuracy: ' + str(accuracies[1]))
        self.macro_accuracy.update()
        print('Start Ned test')

    
    def getFile(self, is_dataset: bool):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        if is_dataset:
            title = "Load dataset"
            extensions = "JSON (*.json)"
            initial_dir = "test_datasets"
        else:
            title = "Load file"
            extensions = "TXT|JSON (*.txt *.json);;HTML Files (*.html)"
            initial_dir = "examples"

        # path_to_file, _ = QFileDialog.getOpenFileName(self,"Load file", None,"TXT|JSON (*.txt *.json);;HTML Files (*.html)", options=options)
        path_to_file, _ = QFileDialog.getOpenFileName(self, title, initial_dir, extensions, options=options)

        if not path_to_file:
            return
        
        if is_dataset:
            self.EL.load_dataset(path_to_file)
        
        else:
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
        self.dom.find("div[id=content]").text(self.EL.show_text())
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
    myappid = u'mycompany.myproduct.subproduct.version' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app = QApplication(sys.argv)
    window = DesktopApplication()
    window.show()
    sys.exit(app.exec_())