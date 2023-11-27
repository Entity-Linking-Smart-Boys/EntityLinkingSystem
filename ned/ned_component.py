if __name__ == "__main__":
    pass

import sys

sys.path.append('../.')

from dbp.repository import DBpediaRepository
from data.text import Text
from abc import ABC, abstractmethod
from data.entity import Entity


class NEDComponent(ABC):
    """
    Named entity disambiguation component
    """
    entities: [Entity] = []
    # def __init__(self) -> None:
    #     self.dbpedia :DBpediaRepository = DBpediaRepository() 
    #     pass

    @abstractmethod
    def NED(self, taggedText) -> Text:
        pass

    def sort_candidates_by_current_score(self):
        for entity in self.entities:
            if entity.candidates:
                entity.candidates.sort(key=lambda candidate: candidate.cand_dis_current_score, reverse=True)

    def print_disambiguated_entities(self, top_n):
        for entity in self.entities:
            # Print the entity label
            print("Entity Label:", entity.surface_form)

            # Iterate through the candidates for the current entity
            for candidate in entity.candidates[:top_n]:
                # Print the candidate's partial score and similarity score
                print("Candidate label:", candidate.label)
                print("Candidate uri:", candidate.uri)
                print("Candidate Current Score:", candidate.cand_dis_current_score)
                print("Candidate Context Score:", candidate.cand_dis_by_context_score)
                print("Candidate Levenshtein Score:", candidate.cand_dis_by_levenshtein_score)
                print("Candidate Connectivity Score:", candidate.cand_dis_by_connectivity_score)
                print('\n')
            print('\n\n')
