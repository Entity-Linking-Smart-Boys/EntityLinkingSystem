class Candidate:
    """
    This class saves candidate's information.
    Each candidate is assigned to specific entity (one-to-many).
    """

    def __init__(self, uri: str, label: str, type_names: [str], abstract: str, ref_count: int, lookup_score: float):
        self.uri = uri  # from DBpedia - link to the page with details
        self.label = label  # from DBpedia - rdfs:label value
        self.ont_type = type_names  # from DBpedia - ontology type
        self.ref_count = int(ref_count if ref_count is not None else 0)
        self.lookup_score = float(lookup_score)
        self.abstract = str(abstract)
        self.cand_dis_total_score = 0
        self.cand_dis_by_lookup_score = 0
