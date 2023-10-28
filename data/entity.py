if __name__ == "__main__":
    pass

from .candidate import Candidate

class Entity:
    """
    Entity mention class
    """
    def __init__(self, surface_form :str, ner_class: str, position :(int,int)) -> None:
        self.surface_form :str = surface_form
        self.ner_class :str = ner_class
        self.position :(int,int) = position
        
        self.uri: str = "" 
        self.dbpedia_class :str = " "
        self.candidates = [Candidate] 

    def set_dbp_class(self,new_class):
        self.dbpedia_class = new_class

    def set_candidates(self, candidates):
        self.candidates = candidates