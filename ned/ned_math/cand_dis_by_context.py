"""
    Disambiguate candidates for each entity based on context similarity.
"""


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.preprocessing import normalize


def disambiguate_by_context_sentence_and_abstract(entities):
    """
    Disambiguate candidates for each entity based on context similarity.
    Two strings are compared:
    - the sentence in which the entity was recognized
    - the abstract of the candidate of the recognized entity
    The similarity between the two strings is calculated using TF-IDF and cosine similarity.

    :param entities: List of entities found in the text, each with associated candidates.
    :return: List of entities with candidates ranked from the most probable to least probable, based on context.
    """

    # Create a dictionary to store the first sentence of each abstract by URI
    abstracts = {}

    # Iterate through entities and extract the first sentence of the abstract for each candidate
    for entity in entities:
        if entity.candidates:
            for candidate in entity.candidates:
                abstract = candidate.abstract
                if abstract:
                    abstracts[candidate.uri] = candidate.abstract.split('.')[0]  # Extract the first sentence

    # Calculate TF-IDF for the extracted sentences
    all_sentences = list(abstracts.values()) + [entity.sentence_text for entity in entities if
                                                entity.sentence_text]  # Combine abstract sentences and entity sentences
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(all_sentences)

    tfidf_matrix_normalized = normalize_tfidf_vectors_magnitude(tfidf_matrix)

    # Iterate through entities and calculate similarity
    for i, entity in enumerate(entities):
        if entity.candidates:
            entity_sentence = entity.sentence_text  # Sentence of the entity
            if entity_sentence:
                tfidf_entity = tfidf_matrix_normalized[i]  # Retrieve the normalized vector for the entity

                for candidate in entity.candidates:
                    candidate_sentence = abstracts.get(candidate.uri, '')  # Get the abstract of the candidate
                    tfidf_candidate = tfidf_matrix_normalized[all_sentences.index(candidate_sentence)]  # Retrieve the normalized vector for the candidate

                    similarity_score = linear_kernel(tfidf_entity, tfidf_candidate).flatten()[0]

                    # Store the score in the candidate instance
                    candidate.cand_dis_by_context_score = similarity_score

    normalize_final_context_scores(entities)

    return entities


def normalize_tfidf_vectors_magnitude(tfidf_matrix):
    """
    Normalize TF-IDF vectors using L2 normalization (Euclidean normalization).

    Normalization ensures that the TF-IDF vectors
    have a consistent unit length (a magnitude of 1) regardless of the text length.

    By normalizing TF-IDF vectors, we ensure that the vectors are directly comparable
    and that the results of similarity measurements are more robust and reliable.

    :param tfidf_matrix: The TF-IDF matrix containing TF-IDF vectors for documents.
    :return: Normalized TF-IDF matrix with unit-length vectors.
    """
    # L2 normalization (Euclidean normalization) scales the vectors to have a unit length (magnitude of 1)
    tfidf_matrix_normalized = normalize(tfidf_matrix, norm='l2', axis=1)
    return tfidf_matrix_normalized


def normalize_final_context_scores(entities):
    """
    Normalize context similarity scores for candidate entities.
    This function rescales context similarity scores
    within a list of entities and candidates to a range from 0 to 1.
    """
    # Calculate the minimum and maximum context similarity scores
    min_score = min(candidate.cand_dis_by_context_score for entity in entities for candidate in entity.candidates)
    max_score = max(candidate.cand_dis_by_context_score for entity in entities for candidate in entity.candidates)
    # Normalize the context similarity scores
    for entity in entities:
        for candidate in entity.candidates:
            normalized_score = round((candidate.cand_dis_by_context_score - min_score) / (max_score - min_score), 3)
            candidate.cand_dis_by_context_score = normalized_score
            candidate.cand_dis_current_score += normalized_score

    return entities
