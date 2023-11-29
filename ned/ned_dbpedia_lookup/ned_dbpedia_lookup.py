import sys

from .cand_dis_by_dbpedia_lookup_score import disambiguate_by_dbpedia_lookup_score

sys.path.append('../.')

from ned.ned_component import NEDComponent
from data.text import Text
from data.entity import Entity
from dbp.repository import DBpediaRepository


class NEDDBpediaLookup(NEDComponent):
    """
    Named entity disambiguation component
    """

    def __init__(self) -> None:
        self.candidateType = "Lookup"

    def NED(self, text: Text):
        self.entities = []
        self.generate_candidates(text)

        self.disambiguate_candidates()

        [entity.set_uri_from_candidates() for entity in self.entities]

        text.set_entity_mentions(self.entities)

        return text

    def generate_candidates(self, text):
        for entity in text.get_entity_mentions():
            entity = self.query_dbpedia(entity)
            self.entities.append(entity)

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

        # Make the GET request
        response = dbrep.get_candidates(entity, max_results, self.candidateType)
        return response

    def disambiguate_candidates(self):
        """
        Disambiguate candidates for each entity.

        :return: entities with candidates ranked from the most probable to the least probable
        """
        self.entities = disambiguate_by_dbpedia_lookup_score(self.entities)
        self.sort_candidates_by_total_score()

        self.print_disambiguated_entities(top_n=5)
