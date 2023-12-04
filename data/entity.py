if __name__ == "__main__":
    pass

from .candidate import Candidate


class Entity(object):
    """
    Entity mention class
    """
    def __init__(self):
        self.surface_form: str 
        self.ner_class: str 
        self.position: (int, int) 
        self.uri: str
        self.dbpedia_class: str 
        self.candidates: list[Candidate] 

    def __init__(self, surface_form: str, ner_class: str, position: (int, int)) -> None:
        self.surface_form: str = surface_form
        self.ner_class: str = ner_class
        self.position: (int, int) = position
        self.uri: str = ""
        self.dbpedia_class: str = " "
        self.candidates: list[Candidate] = []

    def set_dbp_class(self, new_class):
        """Set dbpedia class for entity"""
        self.dbpedia_class = new_class

    def set_candidates(self, candidates):
        """Set candidates for entity"""
        self.candidates = candidates

    def set_uri_from_candidates(self):
        """Set uri from firts candidate in list for entity"""
        if len(self.candidates) > 0:
            self.uri = self.candidates[0].uri

    def to_html(self) -> str:
        """Serialize entity to html"""
        return f"<span><a href=\"{self.uri if hasattr(self,'uri') else ''}\">{self.surface_form}</a><sup>{self.ner_class if hasattr(self,'ner_class') else ''} | {self.dbpedia_class if hasattr(self,'dbpedia_class') else ''}</sup></span>"



class TestEntity(Entity):
    def __init__(self):
        self.target_uri = ""
        self.uri: str = ""
        super().__init__()

    def __init__(self, surface_form: str, ner_class: str, position: (int, int), sentence_number: int, sentence_text: str, target_uri : str) -> None:
        self.target_uri = target_uri
        self.uri: str = ""
        self.dbpedia_class: str = " "
        super().__init__(surface_form, ner_class, position)

    def accurate(self):
        return self.uri == self.target_uri
        #TODO: ? return self.wikipageID == get_wikipageID_from_uri(): ????

    def to_html(self) -> str:
        #TODO: comparing results html
        return super().to_html()