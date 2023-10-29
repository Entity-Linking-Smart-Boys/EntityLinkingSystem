if __name__ == "__main__":
    pass

class Candidate(object):
    """
    Class stores candidate information.
    Each candidate is assigned to specific entity.
    """
    def __init__(self, uri :str, label :str, dbpedia_class :str):
        self.uri :str = uri  # from DBpedia - link to the page with details
        self.label :str = label  # from DBpedia - rdfs:label value
        self.dbpedia_class :str = dbpedia_class  # from DBpedia - ontology type
