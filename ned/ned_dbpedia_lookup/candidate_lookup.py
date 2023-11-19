import sys

sys.path.append('../.')

from data.candidate import Candidate


class CandidateLookup(Candidate):
    """
    This class saves candidate's information.
    Each candidate is assigned to specific entity (one-to-many).
    """

    def __init__(self, uri, label, type_names, comment, ref_count, lookup_score):
        super().__init__(uri, label, type_names, comment)
        self.ref_count = int(ref_count)
        self.lookup_score = float(lookup_score)

    cand_dis_current_score = 0  # score updated after each disambiguation step
