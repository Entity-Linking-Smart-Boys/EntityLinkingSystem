if __name__ == "__main__":
    pass

from file.io import FileIO
from ned.ned_component import NEDComponent
from ner.ner_component import NERComponent
from data.text import Text

from ner.test.ner_test import NERTest

from ned.test.ned_test import NEDTest

class EntityLinkingSystem:
    def __init__(self) -> None:

        self.IO : FileIO 
        """File Input/Output Component"""

        self.NER : NERComponent
        """Swappable Named Entity Recogniton Component"""
        self.NED : NEDComponent
        """Swappable Named Entity Disamiguation Component"""

        self.text: Text
        """Loaded Text"""

        self.IO = FileIO() 

    def select_ner(self,ner_id):
        match ner_id:
            case 1:
                self.NER = NERTest()
            case _:
                self.NER = NERTest()
        return


    def select_ned(self,ned_id):
        match ned_id:
            case 1:
                self.NED = NEDTest()
            case _:
                self.NED = NEDTest()
        return

    def load_text(self,path):
        self.text = self.IO.load(path)

    def load_text_string(self,text_string):
        self.text = self.IO.load_string(text_string)

    def ner(self):
        self.NER.NER(self.text)
        
    def ned(self):
        self.NED.NED(self.text)
        pass

    def save_text(self,path):
        self.IO.save_tagged(self.text,path)

    def show_text(self):
        return self.text

