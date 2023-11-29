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
        self.generate_candidates(text)

        self.disambiguate_candidates()

        [entity.set_uri_from_candidates() for entity in self.entities]

        text.set_entity_mentions(self.entities)
        
        return text

    def generate_candidates(self, text):
        for entity in text.get_entity_mentions():
            entity_with_candidates = self.query_dbpedia(entity)
            entity_with_candidates = self.get_abstract_of_candidates(entity_with_candidates)
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

    def get_abstract_of_candidates(self, entity_with_candidates):
        for cand in entity_with_candidates.candidates:
            abstract = self.get_abstract(cand.uri)
            if abstract is None:
                cand.abstract = cand.comment
            else:
                cand.abstract = abstract
        return entity_with_candidates

    def get_abstract(self, resource_uri):
        # Define the DBpedia endpoint and construct the SPARQL query
        dbpedia_endpoint = "http://dbpedia.org/sparql"
        query_template = """
            SELECT ?abstract
            WHERE {{
                <{resource_uri}> dbo:abstract ?abstract .
                FILTER (langMatches(lang(?abstract), "en"))
            }}
        """
        query = query_template.format(resource_uri=resource_uri)

        # Send the SPARQL query to the DBpedia endpoint
        headers = {'Accept': 'application/sparql-results+json'}
        params = {'query': query, 'format': 'json'}
        response = requests.get(dbpedia_endpoint, headers=headers, params=params)

        # Parse the JSON response
        results = response.json()
        bindings = results['results']['bindings']

        # Extract and print the abstract if available
        if bindings:
            abstract = bindings[0]['abstract']['value']
            # print(f"Abstract for {resource_uri}:\n{abstract}")
            return abstract
        else:
            # print(f"No abstract found for {resource_uri}")
            return None

    def disambiguate_candidates(self):
        """
        Disambiguate candidates for each entity.

        :param entities: list of entities found in the text and categorized into DBpedia ontology
        :return: entities with candidates ranked from the most probable to the least probable
        """
        self.entities = disambiguate_by_context_sentence_and_abstract(self.entities)
        self.sort_candidates_by_total_score()

        self.entities = disambiguate_by_levenshtein_distance(self.entities)
        self.sort_candidates_by_total_score()

        self.print_disambiguated_entities(top_n=5)
