class Candidate:
    """
    This class saves candidate's information.
    Each candidate is assigned to specific entity (one-to-many).
    """

    def __init__(self, uri, label, ont_type, ref_count, lookup_score, comment):
        self.uri = uri  # from DBpedia - link to the page with details
        self.label = label  # from DBpedia - rdfs:label value
        self.ont_type = ont_type  # from DBpedia - ontology type
        self.ref_count = int(ref_count)
        self.lookup_score = float(lookup_score)
        self.comment = str(comment)
        self.cand_dis_total_score = 0
        self.cand_dis_by_lookup_score = 0
