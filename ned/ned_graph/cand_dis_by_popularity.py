"""
Disambiguation by DBpedia Graph Popularity

This module provides methods for disambiguating candidate entities for each entity based on popularity in the DBpedia graph.

"""

from SPARQLWrapper import SPARQLWrapper, JSON
import ssl
from urllib.parse import quote
import math


def disambiguate_by_dbpedia_graph_popularity(entities):
    """
    Disambiguate candidate entities for each entity based on popularity in the DBpedia graph.

    :param entities: List of entities found in the text, each with associated candidates.
    :return: List of entities with candidates ranked based on popularity in the DBpedia graph.
    """

    entities = normalize_popularity_in_dbpedia_scores(entities)

    return entities


def normalize_popularity_in_dbpedia_scores(entities):
    """
    Normalize the popularity scores of entity candidates using linear normalization.

    :param entities: List of entities with associated candidates.
    :return: List of entities with normalized popularity scores for each candidate.
    """
    for entity in entities:
        if entity.candidates:
            # Get the minimum and maximum popularity scores in the entity
            min_score = min(candidate.ref_count for candidate in entity.candidates)
            max_score = max(candidate.ref_count for candidate in entity.candidates)

            # Normalize the scores for each candidate using linear normalization
            for candidate in entity.candidates:
                if max_score == min_score:
                    normalized_popularity_score = 0  # All scores are the same
                else:
                    # Logarithmic normalization
                    normalized_popularity_score = (math.log(candidate.ref_count + 1) - math.log(
                        min_score + 1)) / (math.log(max_score + 1) - math.log(min_score + 1))
                # Update the candidate's normalized popularity score
                candidate.cand_dis_by_popularity_score = round(normalized_popularity_score, 3)
                candidate.cand_dis_total_score += round(normalized_popularity_score, 3)

    return entities
