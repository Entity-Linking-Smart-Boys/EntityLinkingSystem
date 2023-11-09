"""
Disambiguation by DBpedia Graph Popularity

This module provides methods for disambiguating candidate entities for each entity based on popularity in the DBpedia graph.

"""

from SPARQLWrapper import SPARQLWrapper, JSON
import ssl
from urllib.parse import quote


def disambiguate_by_dbpedia_graph_popularity(entities):
    """
    Disambiguate candidate entities for each entity based on popularity in the DBpedia graph.

    :param entities: List of entities found in the text, each with associated candidates.
    :return: List of entities with candidates ranked based on popularity in the DBpedia graph.
    """
    for i, entity in enumerate(entities):
        entity = calculate_popularity_for_entity_candidates(entity)

    entities = normalize_popularity_in_dbpedia_scores(entities)

    return entities


def calculate_popularity_for_entity_candidates(entity):
    """
    Calculate the popularity score for all candidates of one entity.

    :param entity: An entity object with associated candidates.
    :return: The updated entity object with popularity scores for each candidate.
    """
    # Set up the SPARQL endpoint
    ssl._create_default_https_context = ssl._create_unverified_context  # set the SSL Certificate
    sparql = SPARQLWrapper('https://dbpedia.org/sparql')  # initialize SPARQL Wrapper

    for cand in entity.candidates:
        candidate_label = quote(str(cand.label).replace(' ', '_'))

        query = """
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX dbr: <http://dbpedia.org/resource/>

            SELECT (COUNT(?link) as ?linkCount)
            WHERE {
              dbr:""" + candidate_label + """ dbo:wikiPageWikiLink ?link.
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
                if results["results"]["bindings"]:
                    link_count = int(results["results"]["bindings"][0]["linkCount"]["value"])
                    cand.cand_dis_by_popularity_score = link_count
                    print("count:" + str(link_count))
                else:
                    print(f"No results found for the SPARQL query for candidate {candidate_label}.")
        except Exception as e:
            print(f"Error executing SPARQL query: {str(e)}")

    return entity


def normalize_popularity_in_dbpedia_scores(entities):
    """
    Normalize the popularity scores of entity candidates using linear normalization.

    :param entities: List of entities with associated candidates.
    :return: List of entities with normalized popularity scores for each candidate.
    """
    for entity in entities:
        if entity.candidates:
            # Get the minimum and maximum popularity scores in the entity
            min_score = min(candidate.cand_dis_by_popularity_score for candidate in entity.candidates)
            max_score = max(candidate.cand_dis_by_popularity_score for candidate in entity.candidates)

            # Normalize the scores for each candidate using linear normalization
            for candidate in entity.candidates:
                if max_score == min_score:
                    normalized_popularity_score = 0  # All scores are the same
                else:
                    # Linear normalization
                    normalized_popularity_score = (candidate.cand_dis_by_popularity_score - min_score)/ (max_score - min_score)

                # Update the candidate's normalized popularity score
                candidate.cand_dis_by_popularity_score = round(normalized_popularity_score, 3)
                candidate.cand_dis_current_score += normalized_popularity_score

    return entities
