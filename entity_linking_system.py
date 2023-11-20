if __name__ == "__main__":
    pass

import os

from file.io import FileIO
from ned.ned_component import NEDComponent
from ner.ner_component import NERComponent
from data.text import Text

from ner.ner_spacy.ner_spacy import NERSpacy

from ned.ned_basic.ned_basic import NEDBasic
from ned.ned_popularity.ned_popularity import NEDPopularity


class EntityLinkingSystem:
    def __init__(self) -> None:

        self.IO: FileIO
        """File Input/Output Component"""

        self.NER: NERComponent
        """Swappable Named Entity Recogniton Component"""
        self.NED: NEDComponent
        """Swappable Named Entity Disamiguation Component"""

        self.text: Text
        """Loaded Text"""

        self._ners = { "Spacy": NERSpacy() }

        self._neds = {
            "Basic": NEDBasic(),
            "Popularity": NEDPopularity()          
            }



        self.IO = FileIO()

    def get_neds(self):
        return list(self._neds.keys())
    def get_ners(self):
        return list(self._ners.keys())

    def select_ner(self, ner_id):
        self.NER  = list(self._ners.values())[ner_id]
        return 


    def select_ned(self, ned_id):
        self.NED  = list(self._neds.values())[ned_id]
        return
    

    def load_text(self, path: str):
        ext = os.path.splitext(path)[1]
        match ext:
            case ".txt":
                self.text = self.IO.load(path)
            case ".json":
                self.text = self.IO.load_tagged(path)
        return

    def load_text_string(self, text_string):
        self.text = self.IO.load_string(text_string)

    def ner(self):
        self.text.clear_entities()
        self.NER.NER(self.text)

    def ned(self):
        self.text.clear_candidates()
        self.NED.NED(self.text)

    def save_text(self, path):
        self.IO.save_tagged(self.text, path)

    def save_html(self, path):
        self.IO.save_html(self.text, path)

    def show_text(self):
        return self.text
