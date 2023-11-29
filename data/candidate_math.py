import sys

sys.path.append('../ned')

from data.candidate import Candidate


class CandidateMath(Candidate):
    """
    This class saves candidate's information.
    Each candidate is assigned to specific entity (one-to-many).
    """

    def __init__(self, uri, label, ont_type, ref_count, lookup_score, comment):
        super().__init__(uri, label, ont_type, ref_count, lookup_score, comment)
        self.abstract = ""

    abstract = ""
