import sys

sys.path.append('../ned')

from data.candidate import Candidate


class CandidateLookup(Candidate):
    """
    This class saves candidate's information.
    Each candidate is assigned to specific entity (one-to-many).
    """

    def __init__(self, uri, label, type_names, ref_count, lookup_score, comment):
        super().__init__(uri, label, type_names, ref_count, lookup_score, comment)
