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
    Named entity disambiguation component.
    """

    entities: [Entity] = []
    candidateType = "Lookup"

    @abstractmethod
    def NED(self, taggedText) -> Text:
        """
        Perform Named Entity Disambiguation (NED) on the given tagged text.

        Args:
            taggedText (Text): The tagged text with identified entities.

        Returns:
            Text: The disambiguated text.
        """
        pass

    def sort_candidates_by_total_score(self):
        """
        Sort candidates for each entity by their total disambiguation score in descending order.
        """
        for entity in self.entities:
            if entity.candidates:
                entity.candidates.sort(key=lambda candidate: candidate.cand_dis_total_score, reverse=True)

    def print_disambiguated_entities(self, top_n):
        """
        Print disambiguated entities and their top candidates with scores.

        Args:
            top_n (int): The number of top candidates to display.
        """
        for entity in self.entities:
            # Print the entity label
            print("Entity Label:", entity.surface_form)

            # Iterate through the top candidates for the current entity
            for candidate in entity.candidates[:top_n]:
                # Print candidate information
                print("Candidate label:", candidate.label)
                print("Candidate uri:", candidate.uri)
                print("Candidate Total Score:", round(candidate.cand_dis_total_score, 3))  # 3 decimal points
                if hasattr(candidate, 'cand_dis_by_lookup_score'):
                    print("Candidate Lookup Score:", candidate.cand_dis_by_lookup_score)
                if hasattr(candidate, 'cand_dis_by_context_score'):
                    print("Candidate Context Score:", candidate.cand_dis_by_context_score)
                if hasattr(candidate, 'cand_dis_by_levenshtein_score'):
                    print("Candidate Levenshtein Score:", candidate.cand_dis_by_levenshtein_score)
                if hasattr(candidate, 'cand_dis_by_connectivity_score'):
                    print("Candidate Connectivity Score:", candidate.cand_dis_by_connectivity_score)
                if hasattr(candidate, 'cand_dis_by_popularity_score'):
                    print("Candidate Popularity Score:", candidate.cand_dis_by_popularity_score)
                print('\n')
            print('\n\n')

    def query_dbpedia(self, entity: Entity, max_results: int = 10):
        """
        Query the DBpedia Lookup API to retrieve information about the given entity.

        Args:
            entity (Entity): The entity for which to query information.
            max_results (int): The maximum number of results to retrieve.

        Returns:
            dict: The JSON data containing information about the entity from DBpedia Lookup.
        """
        dbrep = DBpediaRepository()

        # Make the GET request
        response = dbrep.get_candidates(entity, max_results)
        return response
