"""

"""

from SPARQLWrapper import SPARQLWrapper, JSON
import ssl
from urllib.parse import quote
import math


def disambiguate_by_dbpedia_graph_connectivity(entities):
    """
    Disambiguate candidate entities for each entity based on connectivity in the DBpedia graph.

    This function compares the connectivity of the central entity candidate with candidates from
    entities on both sides, left and right. The connectivity is determined using SPARQL queries
    to DBpedia to find common connections between entities.

    :param entities: List of entities found in the text, each with associated candidates.
    :return: List of entities with candidates ranked based on connectivity in the DBpedia graph.
    """
    for i, entity in enumerate(entities):
        closest_left_entity, closest_right_entity = find_two_closest_entities(entities, i)

        # Get the top candidates for the centre entity, left entity, and right entity
        top_candidates_count = 5
        current_entity_candidates = entity.candidates[:top_candidates_count]
        left_entity_candidates = closest_left_entity.candidates[:top_candidates_count] if closest_left_entity else []
        right_entity_candidates = closest_right_entity.candidates[:top_candidates_count] if closest_right_entity else []

        # Calculate the connectivity in the DBpedia graph for the selected candidates
        for candidate in current_entity_candidates:
            # Calculate connectivity with candidates from the left entity and the right entity
            candidate_total_connectivity_score = calculate_connectivity_for_candidate(candidate,
                                                                                      left_entity_candidates,
                                                                                      right_entity_candidates)

            candidate.cand_dis_by_connectivity_score = candidate_total_connectivity_score

    entities = normalize_connectivity_in_dbpedia_scores(entities)

    return entities


def find_two_closest_entities(entities, n):
    """
    Find the two closest entities to a given entity in the list of entities.

    This function searches for the closest entity on the left and right sides of the provided entity.
    It calculates the distance based on the 'position' attribute.

    :param entities: List of entities.
    :param n: Index of the target entity in the list.
    :return: Closest left and right entities, if found.
    """
    if n < 0 or n >= len(entities):
        return None, None

    n_entity = entities[n]

    closest_left_entity = None
    closest_right_entity = None

    min_left_distance = float("inf")
    min_right_distance = float("inf")

    for i, entity in enumerate(entities):
        if i == n:
            continue

        # Calculate the distance between the n-th entity and the current entity using self.position
        if entity.position[1] < n_entity.position[0]:  # Assuming position is a tuple (start, end)
            left_distance = n_entity.position[0] - entity.position[1]
            if left_distance < min_left_distance:
                min_left_distance = left_distance
                closest_left_entity = entity
        elif entity.position[0] > n_entity.position[1]:
            right_distance = entity.position[0] - n_entity.position[1]
            if right_distance < min_right_distance:
                min_right_distance = right_distance
                closest_right_entity = entity

    return closest_left_entity, closest_right_entity


def calculate_connectivity_for_candidate(center_entity_candidate, left_entity_candidates, right_entity_candidates):
    """
    Calculate the connectivity score for a central entity candidate with side entity candidates.

    This function calculates the connectivity score for a central entity candidate with side entity candidates.
    It uses SPARQL queries to DBpedia to find common connections between the central entity and side entities.

    :param center_entity_candidate: Central entity candidate.
    :param left_entity_candidates: List of left-side entity candidates.
    :param right_entity_candidates: List of right-side entity candidates.
    :return: Total connectivity score.
    """
    # Initialize the total connectivity score
    total_connectivity_score = 0

    # Set up the SPARQL endpoint
    ssl._create_default_https_context = ssl._create_unverified_context  # set the SSL Certificate
    sparql = SPARQLWrapper('https://dbpedia.org/sparql')  # initialize SPARQL Wrapper

    connectivity_score_with_right_candidates = query_side_entity_candidates(center_entity_candidate,
                                                                            left_entity_candidates,
                                                                            sparql,
                                                                            total_connectivity_score)
    connectivity_score_with_left_candidates = query_side_entity_candidates(center_entity_candidate,
                                                                           right_entity_candidates,
                                                                           sparql,
                                                                           total_connectivity_score)

    total_connectivity_score = connectivity_score_with_right_candidates + connectivity_score_with_left_candidates

    return total_connectivity_score


def query_side_entity_candidates(center_entity_candidate, side_entity_candidates, sparql, total_connectivity_score):
    """
    Query DBpedia for connectivity between a central entity and side entities.

    This function constructs a SPARQL query and sends it to DBpedia to find connectivity
    between a central entity and side entities.

    :param center_entity_candidate: Central entity candidate.
    :param side_entity_candidates: List of side entity candidates.
    :param sparql: SPARQLWrapper instance.
    :param total_connectivity_score: Total connectivity score.
    :return: Updated total connectivity score.
    """
    for i in range(0, len(side_entity_candidates)):
        # Encode the entity labels
        center_entity_label = quote(str(center_entity_candidate.label).replace(' ', '_'))
        side_entity_label = quote(str(side_entity_candidates[i].label).replace(' ', '_'))

        query = """
            PREFIX dbo: <http://dbpedia.org/ontology/> 
            PREFIX dbr: <http://dbpedia.org/resource/> 

            SELECT ?connection (count(?connection) as ?count) 

            WHERE { 

              dbr:""" + center_entity_label + """ ?connection ?x . 

              ?x ?y dbr:""" + side_entity_label + """ . 

              FILTER (?connection = dbo:wikiPageWikiLink) 
            } 
        """
        # print(query)

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)

        try:
            # Execute the query
            results = sparql.query().convert()
            # Check if there are results
            if "results" in results and "bindings" in results["results"]:
                count = int(results["results"]["bindings"][0]["count"]["value"])
                total_connectivity_score += count
                print("count:" + str(count))
        except IndexError:
            # Handle the case where no results are found
            print(f"No results found for the SPARQL query.")
        except Exception as e:
            print(f"Error executing SPARQL query: {str(e)}")
    return total_connectivity_score


def normalize_connectivity_in_dbpedia_scores(entities):
    """
    Normalize the connectivity scores of entity candidates.

    This function normalizes the connectivity scores of entity candidates using a logarithmic transformation.
    It calculates the minimum and maximum scores in each entity and applies a logarithmic transformation
    to emphasize score differences and compress the range.

    :param entities: List of entities with associated candidates.
    :return: List of entities with normalized connectivity scores.
    """
    for entity in entities:
        if entity.candidates:
            # Get the minimum and maximum connectivity scores in the entity
            min_score = min(candidate.cand_dis_by_connectivity_score for candidate in entity.candidates)
            max_score = max(candidate.cand_dis_by_connectivity_score for candidate in entity.candidates)
            print(min_score, max_score)
            # Normalize the scores for each candidate using a logarithmic transformation
            for candidate in entity.candidates:
                if max_score == min_score:
                    normalized_connectivity_score = 0  # All scores are the same
                else:
                    # Apply a logarithmic transformation
                    normalized_connectivity_score = round(
                        math.log(candidate.cand_dis_by_connectivity_score - min_score + 1) / (
                            math.log(max_score - min_score + 1)), 3)
                candidate.cand_dis_by_connectivity_score = normalized_connectivity_score
                candidate.cand_dis_current_score += normalized_connectivity_score

    return entities
