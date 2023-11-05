"""
    Disambiguate candidates for each entity based on context similarity.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


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
    # TODO: add normalization of magnitude:
    #   Normalization is an optional step in the TF-IDF calculation,
    #   and it's often used to ensure that the vectors
    #   have a unit length (a magnitude of 1).
    #   Normalization can be achieved using various techniques,
    #   with the most common one being L2 normalization (also known as Euclidean normalization).

    # TODO: add normalization of the final scores (from 0 - min score, to 1 - max score)

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

    # Iterate through entities and calculate similarity
    for entity in entities:
        if entity.candidates:
            entity_sentence = entity.sentence_text  # Sentence of the entity
            if entity_sentence:
                tfidf_entity = tfidf_vectorizer.transform([entity_sentence])

                for candidate in entity.candidates:
                    candidate_sentence = abstracts.get(candidate.uri, '')  # Get the abstract of the candidate
                    tfidf_candidate = tfidf_vectorizer.transform([candidate_sentence])
                    similarity_score = linear_kernel(tfidf_entity, tfidf_candidate).flatten()[0]

                    # Store the score in the candidate instance
                    candidate.cand_dis_by_context_score = similarity_score
                    candidate.cand_dis_current_score += similarity_score

    return entities
