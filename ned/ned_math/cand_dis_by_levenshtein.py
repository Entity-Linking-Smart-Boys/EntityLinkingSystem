"""
    Disambiguate candidate entities for each entity using Levenshtein distance-based similarity scores.
"""


def disambiguate_by_levenshtein_distance(entities):
    """
    Disambiguate candidate entities for each entity using Levenshtein distance-based similarity scores.
    This function compares two strings:
    - the entity label (surface form)
    - the candidate label of this entity (DBpedia label)
    This function calculates the Levenshtein distance-based similarity scores between
    the entity labels and candidate labels for each entity and its candidates.
    The calculated similarity scores are normalized and stored in the candidates
    and returned as the updated entity list.

    :param entities: A list of entity objects with associated candidates.
    :return: Updated entities with candidates containing normalized Levenshtein distance-based similarity scores.
    """

    for entity in entities:
        for candidate in entity.candidates:
            entity_label = entity.surface_form
            candidate_label = str(candidate.label).replace("_", " ")
            levenshtein_distance_score = calculate_levenshtein_distance_between_two_strings(entity_label,
                                                                                            candidate_label)
            candidate.cand_dis_by_levenshtein_score = levenshtein_distance_score

    entities = normalize_final_levenshtein_scores(entities)

    return entities


def calculate_levenshtein_distance_between_two_strings(entity_label, candidate_label):
    """
    Calculate the similarity score between an entity label and a candidate label using Levenshtein distance.

    :param entity_label: The label of the entity (e.g., the surface form).
    :param candidate_label: The label of the candidate.
    :return: The similarity score between 0 and 1, where higher values indicate greater similarity.

    This function uses Levenshtein distance to measure the similarity between two strings.
    It calculates the Levenshtein distance between the entity label and the candidate label,
    and then converts it into a similarity score.

    Note: A lower Levenshtein distance indicates higher similarity,
    so the similarity score is inversely proportional to the Levenshtein distance.
    """

    def levenshtein_distance(s1, s2):
        """
        Calculate the Levenshtein distance between two strings.

        :param s1: The first string.
        :param s2: The second string.
        :return: The Levenshtein distance between the two strings.
        """
        if len(s1) < len(s2):
            return levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    # Calculate Levenshtein distance
    levenshtein_distance_value = levenshtein_distance(entity_label, candidate_label)

    # Calculate similarity score using Levenshtein distance
    # The similarity score is inversely proportional to the Levenshtein distance
    similarity_score = 1 / (1 + levenshtein_distance_value)

    return similarity_score


def normalize_final_levenshtein_scores(entities):
    """
    Normalize Levenshtein distance scores for candidate entities.
    This function rescales Levenshtein distance scores
    within a list of entities and candidates to a range from 0 to 1.
    """
    # Calculate the minimum and maximum levenshtein distance scores
    min_score = min(candidate.cand_dis_by_levenshtein_score for entity in entities for candidate in entity.candidates)
    max_score = max(candidate.cand_dis_by_levenshtein_score for entity in entities for candidate in entity.candidates)
    # Normalize the context similarity scores
    for entity in entities:
        for candidate in entity.candidates:
            normalized_score = round((candidate.cand_dis_by_levenshtein_score - min_score) / (max_score - min_score), 3)
            candidate.cand_dis_by_levenshtein_score = normalized_score
            candidate.cand_dis_total_score += normalized_score

    return entities
