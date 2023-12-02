from ned.ned_math.cand_dis_by_context import disambiguate_by_context_sentence_and_abstract
from ned.ned_math.cand_dis_by_levenshtein import disambiguate_by_levenshtein_distance
import requests

if __name__ == "__main__":
    pass

import sys

sys.path.append('../.')

from ned.ned_component import NEDComponent
from data.text import Text
from data.entity import Entity
from dbp.repository import DBpediaRepository


class NEDMath(NEDComponent):
    """
    Named entity disambiguation component
    """

    def __init__(self) -> None:
        self.candidateType = "Math"

    def NED(self, text: Text):
        self.entities = []
        self.generate_candidates(text)

        self.disambiguate_candidates()

        [entity.set_uri_from_candidates() for entity in self.entities]

        text.set_entity_mentions(self.entities)
        
        return text

    def generate_candidates(self, text):
        for entity in text.get_entity_mentions():
            entity_with_candidates = self.query_dbpedia(entity)
            self.entities.append(entity_with_candidates)

    def query_dbpedia(self, entity: Entity, max_results: int = 10):
        """
        Query the DBpedia Lookup API to retrieve information about the given entity.
        DBpedia Lookup documentation: https://github.com/dbpedia/dbpedia-lookup

        Args:
            entity (Entity): The entity for which to query information.
            max_results (int): The maximum number of results to retrieve.

        Returns:
            dict: The JSON data containing information about the entity from DBpedia Lookup.
        """

        dbrep = DBpediaRepository()

        # entity_with_candidates
        entity_with_candidates = dbrep.get_candidates(entity, max_results, self.candidateType)
        return entity_with_candidates

    def disambiguate_candidates(self):
        """
        Disambiguate candidates for each entity.

        :return: entities with candidates ranked from the most probable to the least probable
        """
        self.entities = disambiguate_by_context_sentence_and_abstract(self.entities)
        self.sort_candidates_by_total_score()

        self.entities = disambiguate_by_levenshtein_distance(self.entities)
        self.sort_candidates_by_total_score()

        self.print_disambiguated_entities(top_n=5)
