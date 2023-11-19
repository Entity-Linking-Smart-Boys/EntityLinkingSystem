from ned.ned_math.cand_dis_by_levenshtein import disambiguate_by_levenshtein_distance
from ned.ned_graph.cand_dis_by_connectivity import disambiguate_by_dbpedia_graph_connectivity
from ned.ned_graph.cand_dis_by_popularity import normalize_popularity_in_dbpedia_scores

if __name__ == "__main__":
    pass

from SPARQLWrapper import SPARQLWrapper, JSON
import ssl
import time
import sys

sys.path.append('../.')

from ned.ned_component import NEDComponent
from data.text import Text
from data.entity import Entity
from data.candidate import Candidate


class NEDGraph(NEDComponent):
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
            entity = sort_candidates_of_entity_by_pop_score(entity)
            self.entities.append(entity)

        entities = disambiguate_candidates(self.entities)

        for entity in entities:
            entity.set_uri_from_candidates()

        text.set_entity_mentions(entities)

        return text


# CANDIDATE GENERATION BEGIN
# CANDIDATE GENERATION BEGIN
def query_dbpedia(entity, max_retries=3, retry_delay=2):
    """
    Create SPARQL query and send it via SPARQLWrapper with retry mechanism.

    :param entity: entity containing details used during the creation of the query
    :param max_retries: maximum number of retry attempts
    :param retry_delay: delay (in seconds) between retry attempts
    :return: query result
    """

    ssl._create_default_https_context = ssl._create_unverified_context  # set the SSL Certificate

    for attempt in range(1, 4):  # 3 attempts
        sparql = None  # Set to None before recreating
        sparql = SPARQLWrapper('https://dbpedia.org/sparql')  # initialize SPARQL Wrapper
        # Set the timeout to 3000 milliseconds
        timeout = 45  # seconds
        sparql.timeout = timeout * 1000  # milliseconds

        try:
            query_result = query_dbpedia_for_surfaceform(entity, sparql)
            del sparql

            if "results" in query_result and "bindings" in query_result["results"]:
                if len(query_result["results"]["bindings"]) > 0:
                    print("success")
                    return query_result
                else:
                    print(f"No results found for the SPARQL query (attempt {attempt}/3). Retrying...")
                    time.sleep(1)  # 1 second delay between retries

            else:
                print(f"Unexpected response format for the SPARQL query (attempt {attempt}/3). Retrying...")

        except Exception as e:
            print(f"Error executing SPARQL query (attempt {attempt}/3): {str(e)}")
            time.sleep(1)  # 1 second delay between retries

    print("Reached the maximum number of retries. Unable to execute SPARQL query.")
    results_empty = {
        "head": {
            "link": [],
            "vars": ["entity", "label", "linkCount"]
        },
        "results": {
            "distinct": False,
            "ordered": True,
            "bindings": []
        }
    }
    return results_empty


def query_dbpedia_for_surfaceform(entity, sparql):
    # query the whole dbpedia (do not use NER type or ontology class)
    query = '''
                    PREFIX owl: <http://www.w3.org/2002/07/owl#>
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    PREFIX dc: <http://purl.org/dc/elements/1.1/>
                    PREFIX : <http://dbpedia.org/resource/>
                    PREFIX dbpedia2: <http://dbpedia.org/property/>
                    PREFIX dbpedia: <http://dbpedia.org/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

                    SELECT ?entity ?label (COUNT(?link) as ?linkCount) ?disambiguates
                    WHERE {
                      ?entity rdfs:label ?label 
                      OPTIONAL {
                        ?entity dbo:wikiPageDisambiguates ?disambiguates .
                      }
                      OPTIONAL {
                        ?entity dbo:wikiPageWikiLink ?link .
                      }
                      FILTER (langMatches(lang(?label), "en") && regex(?label, "''' + entity.surface_form + '''", "i"))
                    }
                '''
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    query_result = sparql.query().convert()
    return query_result


def save_found_candidates(query_results, entity):
    """
    Extract data from SPARQL query results and save it into candidate instances.
    The list of candidates is saved into the entity.

    :param query_results: results of SPARQL query
    :param entity: entity in which the candidates are saved into
    :return: updated entity with a list of candidates
    """
    if query_results is None:
        # Handle the case where the query failed after retries
        print("Error: SPARQL query failed. Unable to save candidates.")
        return entity

    # print("Query results:", query_results)  # Add this line for debugging

    entity.candidates = []
    for result in query_results["results"]["bindings"]:
        candidate_uri = result["entity"]["value"]
        candidate_label = result["label"]["value"]
        popularity_score = int(result["linkCount"]["value"]) if "linkCount" in result else 0

        # Check if there are disambiguates links - get only the links from disambiguation
        if "disambiguates" in result:
            disambiguates_links = result["disambiguates"]["value"].split()

            # Create Candidate instances for each disambiguates link
            for disambiguates_link in disambiguates_links:
                disambiguates_candidate_uri = disambiguates_link
                disambiguates_candidate_label = disambiguates_link.split('/')[-1].replace("_", " ")  # Use label as link name
                disambiguates_candidate = Candidate(disambiguates_candidate_uri, disambiguates_candidate_label, "")
                disambiguates_candidate.cand_dis_by_popularity_score = popularity_score
                entity.candidates.append(disambiguates_candidate)
        else:
            # Add the main candidate - the entity is not a "disambiguate" entity (it is a page about a specific object)
            main_candidate = Candidate(candidate_uri, candidate_label, "")
            main_candidate.cand_dis_by_popularity_score = popularity_score
            entity.candidates.append(main_candidate)

    return entity


# CANDIDATE GENERATION END
# CANDIDATE DISAMBIGUATION BEGIN

def disambiguate_candidates(entities):
    """
    Disambiguate candidates for each entity.

    :param entities: list of entities found in the text and categorized into DBpedia ontology
    :return: entities with candidates ranked from the most probable to the least probable
    """

    entities = normalize_popularity_in_dbpedia_scores(entities)
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


def sort_candidates_of_entity_by_pop_score(entity):
    if entity.candidates:
        entity.candidates.sort(key=lambda candidate: candidate.cand_dis_by_popularity_score, reverse=True)

    return entity


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
            print("Candidate Popularity Score:", candidate.cand_dis_by_popularity_score)
            print("Candidate Levenshtein Score:", candidate.cand_dis_by_levenshtein_score)
            print('\n')
        print('\n\n')

# CANDIDATE DISAMBIGUATION END
