import sys

from ned.ned_component import NEDComponent

sys.path.append('../.')
from data.entity import Entity

class TestEntity(Entity):
    def __init__(self):
        self.target_uri: str
        super().__init__()

    def __init__(self, surface_form: str, ner_class: str, position: (int, int), sentence_number: int, sentence_text: str, target_uri : str) -> None:
        self.target_uri = target_uri
        super().__init__(surface_form, ner_class, position, sentence_number, sentence_text)

    def accurate(self):
        return self.uri == self.target_uri
        #TODO: ? return self.wikipageID == get_wikipageID_from_uri(): ????

    def to_html(self) -> str:
        #TODO: comparing results html
        return super().to_html()
