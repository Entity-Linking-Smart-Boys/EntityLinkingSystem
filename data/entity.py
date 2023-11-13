if __name__ == "__main__":
    pass

from .candidate import Candidate


class Entity(object):
    """
    Entity mention class
    """

    def __init__(self, surface_form: str, ner_class: str, position: (int, int), sentence_number: int, sentence_text: str) -> None:
        self.surface_form: str = surface_form
        self.ner_class: str = ner_class
        self.position: (int, int) = position
        self.sentence_number = sentence_number
        self.sentence_text = sentence_text
        self.uri: str = ""
        self.dbpedia_class: str = " "
        self.candidates: [Candidate] = []

    def set_dbp_class(self, new_class):
        self.dbpedia_class = new_class

    def set_candidates(self, candidates):
        self.candidates = candidates

    def set_uri_from_candidates(self):
        if len(self.candidates) > 0:
            self.uri = self.candidates[0].uri

    def to_html(self) -> str:
        return f"<span><a href=\"{self.uri}\">{self.surface_form}</a><sup>{self.ner_class} | {self.dbpedia_class}</sup></span>"
