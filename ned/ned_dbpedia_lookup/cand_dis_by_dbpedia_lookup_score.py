

def disambiguate_by_dbpedia_lookup_score(entities):

    entities = normalize_scores_within_entity(entities)

    return entities


def normalize_scores_within_entity(entities):
    """
    Normalize DBpedia Lookup scores for candidate entities.
    This function rescales DBpedia Lookup scores distance scores
    within a list of entities and candidates to a range from 0 to 1.
    """
    for entity in entities:
        # Calculate the minimum and maximum levenshtein distance scores for the current entity
        min_score = min(candidate.lookup_score for candidate in entity.candidates)
        max_score = max(candidate.lookup_score for candidate in entity.candidates)

        # Normalize the context similarity scores within the current entity
        for candidate in entity.candidates:
            if max_score != min_score:  # Avoid division by zero
                normalized_score = round((candidate.lookup_score - min_score) / (max_score - min_score), 3)
                candidate.cand_dis_current_score += normalized_score

    return entities
