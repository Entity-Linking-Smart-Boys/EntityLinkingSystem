from ned.ned_basic.cand_dis_by_connectivity import disambiguate_by_dbpedia_graph_connectivity
from ned.ned_basic.cand_dis_by_context import disambiguate_by_context_sentence_and_abstract
from ned.ned_basic.cand_dis_by_levenshtein import disambiguate_by_levenshtein_distance

if __name__ == "__main__":
    pass

from SPARQLWrapper import SPARQLWrapper, JSON
import ssl

import sys

sys.path.append('../.')

from ned.ned_component import NEDComponent
from dbp.repository import DBpediaRepository
from data.text import Text
from data.entity import Entity
from data.candidate import Candidate


class NEDBasic(NEDComponent):
    """
    Named entity disambiguation component
    """
    entities: [Entity] = []

    def __init__(self) -> None:
        pass

    def NED(self, text: Text):
        # Candidate generation
        for entity in text.get_entity_mentions():
            query_result = query_dbpedia(entity)
            entity = save_found_candidates(query_result, entity)
            self.entities.append(entity)

        entities = disambiguate_candidates(self.entities)

        for entity in entities:
            entity.set_uri_from_candidates()
            
        text.set_entity_mentions(entities)
        
        return text


# CANDIDATE GENERATION BEGIN
def merge_results(new_results, main_results):
    """
    Merge two dictionaries containing results from SPARQL query.

    :param new_results: results with entities of new ontology type
    :param main_results: results with entities of old ontology types
    :return: merged results as dictionary
    """
    # Merge the 'bindings' lists from both dictionaries
    main_results['results']['bindings'].extend(new_results['results']['bindings'])
    return main_results


def query_dbpedia(entity):
    """
    Create SPARQL query and send it via SPARQLWrapper.

    :param entity: entity containing details used during creation of query
    :return: query result
    """

    ssl._create_default_https_context = ssl._create_unverified_context  # set the SSL Certificate

    sparql = SPARQLWrapper('https://dbpedia.org/sparql')  # initialize SPARQL Wrapper

    dbpedia_ont_types = entity.dbpedia_class.split(',')

    results = {
        "head": {
            "link": [],
            "vars": ["entity", "typeValue", "name", "abstract"]
        },
        "results": {
            "distinct": False,
            "ordered": True,
            "bindings": []
        }
    }

    for ontology_type in dbpedia_ont_types:


        query = '''
            PREFIX dbo: <http://dbpedia.org/ontology/>

            SELECT ?entity ?typeValue ?name ?abstract
            WHERE {
              {
                ?entity a/rdfs:subClassOf* ''' + ontology_type + ''';
                        rdfs:label ?name ;
                        a ?type ;
                        dbo:abstract ?abstract.
                BIND ("''' + ontology_type + '''" as ?typeValue)
                FILTER (langMatches(lang(?name), "en") && CONTAINS(?name, "''' + entity.surface_form + '''") && STRSTARTS(STR(?type), "http://dbpedia.org/ontology") && langMatches(lang(?abstract), "en"))
              }
            }
            group by ?entity  # this lowers the number of results
        '''

        sparql.setQuery(query)

        sparql.setReturnFormat(JSON)

        sparql.verify = False
        query_result = sparql.query().convert()
        results = merge_results(query_result, results)
    return results


def save_found_candidates(query_results, entity):
    """
    Extract data from SPARQL query results and save it into candidate instances.
    The list of candidates is saved into the entity.

    :param query_results: results of SPARQL query
    :param entity: entity in which the candidates are saved into
    :return: updated entity with list of candidates
    """
    entity.candidates = []
    for result in query_results["results"]["bindings"]:
        candidate_uri = result["entity"]["value"]
        candidate_label = result["name"]["value"]
        candidate_type = result["typeValue"]["value"]

        # if abstract exists:
        if result["abstract"]["value"]:
            abstract = result["abstract"]["value"]
            candidate = Candidate(candidate_uri, candidate_label, candidate_type, abstract)
        else:
            candidate = Candidate(candidate_uri, candidate_label, candidate_type)
        entity.candidates.append(candidate)
    return entity


# CANDIDATE GENERATION END

# CANDIDATE DISAMBIGUATION BEGIN

def disambiguate_candidates(entities):
    """
    Disambiguate candidates for each entity.

    :param entities: list of entities found in the text and categorized into DBpedia ontology
    :return: entities with candidates ranked from the most probable to the least probable
    """
    entities = disambiguate_by_context_sentence_and_abstract(entities)
    entities = sort_candidates_by_current_score(entities)

    entities = disambiguate_by_levenshtein_distance(entities)
    entities = sort_candidates_by_current_score(entities)

    entities = disambiguate_by_dbpedia_graph_connectivity(entities)
    entities = sort_candidates_by_current_score(entities)

    print_disambiguated_entities(entities, top_n=5)

    return entities


def sort_candidates_by_current_score(entities):
    for entity in entities:
        if entity.candidates:
            entity.candidates.sort(key=lambda candidate: candidate.cand_dis_current_score, reverse=True)

    return entities


def print_disambiguated_entities(entities, top_n):
    for entity in entities:
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

# CANDIDATE DISAMBIGUATION END
