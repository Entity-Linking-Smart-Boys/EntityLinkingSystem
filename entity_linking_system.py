if __name__ == "__main__":
    pass

import os

from file.io import FileIO
from ned.ned_component import NEDComponent
from ner.ner_component import NERComponent
from data.text import Text

from ner.ner_spacy.ner_spacy import NERSpacy

from ned.ned_math.ned_math import NEDMath
from ned.ned_graph.ned_graph import NEDGraph
from ned.ned_dbpedia_lookup.ned_dbpedia_lookup import NEDDBpediaLookup
from tests.evaluation_component import EvaluationComponent

from ner.ner_conll.ner_conll import NERConll
from ner.ner_multinerd.ner_multinerd import NERMultinerd

class EntityLinkingSystem:
    def __init__(self) -> None:

        self.IO: FileIO
        """File Input/Output Component"""

        self.NER: NERComponent
        """Swappable Named Entity Recogniton Component"""
        self.NED: NEDComponent
        """Swappable Named Entity Disamiguation Component"""
        self.test = EvaluationComponent()


        self.text: Text
        """Loaded Text"""

        self._ners = {"Spacy": NERSpacy(), "NERDBERT": NERMultinerd(), "CONLLBERT": NERConll()}

        self._neds = {
            "LookupNed": NEDDBpediaLookup(),
            "Graph": NEDGraph(),
            "Math": NEDMath()
        }
        
        self.IO = FileIO()

    
    def get_neds(self):
        """Returns list of ned algorithms' names for display"""
        return list(self._neds.keys())
    
    def get_ners(self):    
        """Returns list of ner algorithms' names for display"""
        return list(self._ners.keys())

    def select_ner(self, ner_id):
        """Change used ner algorithm"""
        self.NER  = list(self._ners.values())[ner_id]
        return 

    def select_ned(self, ned_id):
        """Change used ned algorithm"""
        self.NED  = list(self._neds.values())[ned_id]
        return

    def ned_use_ner_class(self, use_NER_class):
        self.NED.use_NER_class = use_NER_class
        return

    def load_text_string(self, text_string):
        """Load text into the system via string"""
        self.text = self.IO.load_string(text_string)
        return
    
    def load_text(self, path: str):
        """Load text into the system via file"""
        ext = os.path.splitext(path)[1]
        match ext:
            case ".txt":
                self.text = self.IO.load(path)
            case ".json":
                self.text = self.IO.load_tagged(path)
        return
    
    def load_dataset(self, path: str):
        """Load dataset into the system via file"""
        ext = os.path.splitext(path)[1]
        match ext:
            case ".json":
                self.test.load_dataset(self.IO.load_dataset(path))
        return



    def ned_tests(self):
        """Do ned algorithm tests"""
        self.test.test_ned(self.NED)

    def get_accuracy(self):
        """Get accuracies of last ran ned test"""
        return (self.test.get_ned_micro_accuracy(),self.test.get_ned_macro_accuracy())

    def ner(self):
        """Do NER on currently loaded text"""
        self.text.clear_entities()
        self.text = self.NER.NER(self.text)

    def ned(self):
        """Do NED on currently loaded text"""
        self.text.clear_candidates()
        self.text = self.NED.NED(self.text)

    def save_text(self, path):
        """Save currently loaded text to a json file"""
        self.IO.save_tagged(self.text, path)

    def save_html(self, path):
        """Save currently loaded text to a html file"""
        self.IO.save_html(self.text, path)

    def get_text(self):
        """Get current text"""
        return self.text
    
    def show_text(self):
        """Get current text"""
        return self.text.get_html_text()

    def show_test_text(self,index):
        """Get text from loaded dataset in test component"""
        if index < self.test.get_dataset_length():
            return self.test.get_text(index).get_html_text()
        
    def get_test_text_accuracy(self,index):
        """accuracy of text from loaded dataset in test component"""
        if index < self.test.get_dataset_length():
            txt = self.test.get_text(index)
            return (txt.get_ned_accuracy(), txt.get_accurate_count(), txt.get_entities_count())
        

