import sys

sys.path.append('../ned')

from data.candidate import Candidate


class CandidateGraph(Candidate):
    """
    This class saves candidate's information.
    Each candidate is assigned to specific entity (one-to-many).
    """

    def __init__(self, uri: str, label: str, type_names: [str], abstract: str, ref_count: int, lookup_score: float):
        super().__init__(uri, label, type_names, abstract, ref_count, lookup_score)
        self.cand_dis_by_connectivity_score = 0
        self.cand_dis_by_popularity_score = 0

    cand_dis_by_connectivity_score = 0  # score from disambiguation by connectivity
    cand_dis_by_popularity_score = 0
