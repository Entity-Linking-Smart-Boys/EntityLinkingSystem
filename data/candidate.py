class Candidate:
    """
    This class saves candidate's information.
    Each candidate is assigned to specific entity (one-to-many).
    """

    def __init__(self, uri, label, ont_type, abstract=""):
        self.uri = uri  # from DBpedia - link to the page with details
        self.label = label  # from DBpedia - rdfs:label value
        self.ont_type = ont_type  # from DBpedia - ontology type
        self.abstract = abstract  # from DBpedia - entity abstract (optional)

    cand_dis_by_context_score = 0  # score from disambiguation by context
    cand_dis_by_levenshtein_score = 0  # score from disambiguation by levenshtein distance
    cand_dis_by_connectivity_score = 0  # score from disambiguation by similarity_in_dbpedia_graph
    cand_dis_current_score = 0  # score updated after each disambiguation step
