import requests

from data.candidate import Candidate
from data.candidate_graph import CandidateGraph
from data.candidate_lookup import CandidateLookup
from data.candidate_math import CandidateMath
from data.entity import Entity


class DBpediaRepository:
    """
    Repository for fetching candidates from DBpedia
    """

    api_url = "https://lookup.dbpedia.org/api/search"

    def __init__(self) -> None:
        """
        Initialize the DBpediaRepository instance with the default API URL.
        """
        self.api_url = "https://lookup.dbpedia.org/api/search"

    def get_candidates(self, entity, max_results, candidateType="", params=None):
        """
        Get candidates for the specified entity from DBpedia.

        Args:
            entity (Entity): The entity for which to fetch candidates.
            max_results (int): The maximum number of results to fetch.
            candidateType (str): Type of candidate (one of the previously defined types).
            params (dict): Additional parameters for the API request.

        Returns:
            Entity: The entity with added candidates.
        """
        if params is None:
            params = {}
        params['query'] = entity.surface_form
        params['format'] = 'JSON_FULL'
        params['maxResults'] = max_results

        result = self.search_candidates_in_DBpedia(params)
        entity = self.save_found_candidates(result, entity, candidateType)
        return entity

    def search_candidates_in_DBpedia(self, params):
        """
        Search for candidates in DBpedia using the specified parameters.

        Args:
            params (dict): Parameters for the DBpedia Lookup API request.

        Returns:
            dict: JSON data containing DBpedia Lookup results.
        """
        # Make the GET request
        response = requests.get(self.api_url, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON data from the response
            data = response.json()
            return data
        else:
            # If the request was not successful, print an error message
            print(f"Error: {response.status_code}")
            return None

    def save_found_candidates(self, data: dict, entity: Entity, candidateType=""):
        """
        Save the found candidates for the entity based on the DBpedia Lookup results.

        Args:
            data (dict): The JSON data containing DBpedia Lookup results.
            entity (Entity): The entity to associate with the candidates.
            candidateType (str): Type of candidate (one of previously defined)

        Returns:
            Entity: The entity with added candidates.
        """
        # Check if the "docs" key is present in the data
        if "docs" in data:
            # Loop through each result
            for doc in data["docs"]:
                # Extract information for specific fields
                lookup_score = doc.get("score", [])[0] if doc.get("score") else None
                ref_count = doc.get("refCount", [])[0]["value"] if doc.get("refCount") else None
                uri = doc.get("resource", [])[0]["value"] if doc.get("resource") else None
                redirect_labels = [label["value"] for label in doc.get("redirectlabel", [])]
                type_names = [type["value"] for type in doc.get("typeName", [])]
                abstract = doc.get("comment", [])[0]["value"].replace("<B>", "").replace("</B>", "") if doc.get(
                    "comment") else None
                label = doc.get("label", [])[0]["value"].replace("<B>", "").replace("</B>", "") if doc.get(
                    "label") else None
                types = [type["value"] for type in doc.get("type", [])]
                categories = [category["value"] for category in doc.get("category", [])]

                if candidateType == "Graph":
                    candidate = CandidateGraph(uri, label, type_names, abstract, ref_count, lookup_score)
                elif candidateType == "Math":
                    candidate = CandidateMath(uri, label, type_names, abstract, ref_count, lookup_score)
                elif candidateType == "Lookup":
                    candidate = CandidateLookup(uri, label, type_names, abstract, ref_count, lookup_score)
                else:
                    candidate = Candidate(uri, label, type_names, abstract, ref_count, lookup_score)
                entity.candidates.append(candidate)

            entity = self.normalize_lookup_scores_within_entity(entity)
        else:
            print("No 'docs' key found in the data.")
        return entity

    def normalize_lookup_scores_within_entity(self, entity):
        """
        Normalize DBpedia Lookup scores for candidate entities.

        This method performs linear normalization, rescaling DBpedia Lookup scores
        (distance scores) within a list of entities and candidates to a range from 0 to 1.

        Args:
            entity (Entity): The entity whose candidates' scores need to be normalized.

        Returns:
            Entity: The entity with normalized candidate scores.
        """
        # Calculate the minimum and maximum DBpedia Lookup scores for the current entity
        min_score = min(candidate.lookup_score for candidate in entity.candidates)
        max_score = max(candidate.lookup_score for candidate in entity.candidates)

        # Normalize the DBpedia Lookup scores within the current entity
        for candidate in entity.candidates:
            if max_score != min_score:  # Avoid division by zero
                normalized_score = round((candidate.lookup_score - min_score) / (max_score - min_score), 3)
                candidate.cand_dis_by_lookup_score = normalized_score
                candidate.cand_dis_total_score += normalized_score

        return entity

