import requests
import sys

from .candidate_lookup import CandidateLookup
from .cand_dis_by_dbpedia_lookup_score import disambiguate_by_dbpedia_lookup_score

sys.path.append('../.')

from ned.ned_component import NEDComponent
from data.text import Text
from data.entity import Entity


class NEDDBpediaLookup(NEDComponent):
    """
    Named entity disambiguation component
    """
    def __init__(self) -> None:
        pass

    def NED(self, text: Text):
        # Candidate generation
        for entity in text.get_entity_mentions():
            query_result = self.query_dbpedia(entity)
            entity = self.save_found_candidates(query_result, entity)
            self.entities.append(entity)

        self.disambiguate_candidates()

        [entity.set_uri_from_candidates() for entity in self.entities]

        text.set_entity_mentions(self.entities)

        return text

    def query_dbpedia(self, entity, max_results=10):
        """
        Docs: https://github.com/dbpedia/dbpedia-lookup
        """
        # DBpedia Lookup API endpoint
        api_url = "https://lookup.dbpedia.org/api/search"
        # type_name = 'Location'

        # Parameters for the GET request
        params = {'query': entity.surface_form, 'format': 'json', 'maxResults': max_results}

        # Make the GET request
        response = requests.get(api_url, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON data from the response
            data = response.json()
            return data
        else:
            # If the request was not successful, print an error message
            print(f"Error: {response.status_code}")
            return None

    def save_found_candidates(self, data, entity):
        # Check if the "docs" key is present in the data
        if "docs" in data:
            # Loop through each result
            for doc in data["docs"]:
                # Extract information for specific fields
                lookup_score = doc.get("score", [])[0] if doc.get("score") else None
                ref_count = doc.get("refCount", [])[0] if doc.get("refCount") else None
                resource = doc.get("resource", [])[0] if doc.get("resource") else None
                redirect_labels = doc.get("redirectlabel", [])
                type_names = doc.get("typeName", [])
                comment = doc.get("comment", [])[0].replace("<B>", "").replace("</B>", "") if doc.get("comment") else None
                label = doc.get("label", [])[0].replace("<B>", "").replace("</B>", "") if doc.get("label") else None
                types = doc.get("type", [])
                categories = doc.get("category", [])

                # # Print or save the extracted information (replace with your desired logic)
                # print(f"Score: {score}")
                # print(f"RefCount: {ref_count}")
                # print(f"Resource: {resource}")
                # print(f"Redirect Labels: {redirect_labels}")
                # print(f"Type Names: {type_names}")
                # print(f"Comment: {comment}")
                # print(f"Label: {label}")
                # print(f"Types: {types}")
                # print(f"Categories: {categories}")
                # print("\n")

                candidate = CandidateLookup(resource, label, type_names, comment, ref_count, lookup_score)
                entity.candidates.append(candidate)
        else:
            print("No 'docs' key found in the data.")
        return entity

    def disambiguate_candidates(self):
        """
        Disambiguate candidates for each entity.

        :param entities: list of entities found in the text and categorized into DBpedia ontology
        :return: entities with candidates ranked from the most probable to the least probable
        """
        self.entities = disambiguate_by_dbpedia_lookup_score(self.entities)
        self.sort_candidates_by_current_score()

        self.print_disambiguated_entities(top_n=5)
