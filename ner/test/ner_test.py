if __name__ == "__main__":
    pass

import spacy
from spacy import displacy

import sys
sys.path.append('../.')

from ner.ner_component import NERComponent
from dbp.repository import DBpediaRepository
from data.text import Text
from data.entity import Entity


class NERTest(NERComponent):
    """
    Named entity disambiguation component
    """
    def __init__(self) -> None:
        pass
    
    def NER(self, text:Text):
        text.set_entity_mentions(named_entity_recognition_using_spacy(text.get_plain_text()))
        for entity in text.entity_mentions:
            entity = map_entity_type_to_dbpedia_ontology(entity)

        return text
        
    def _map_ner_class_to_dbp():
        pass



def named_entity_recognition_using_spacy(text):
    """
    Perform Named Entity Recognition (NER) using spaCy (Docs: https://spacy.io/api/entityrecognizer).

    :param text: text to annotate
    :return: found entities with specific surface form and label.
    """
    nlp = spacy.load('en_core_web_lg') #trf

    doc = nlp(text)

    entities = [Entity(e.text, e.label_, (e.start_char, e.end_char)) for e in doc.ents]

    #displacy.render(doc, style='ent')

    # found_entities = []
    # for entity in list(entities):
    #     new_entity = Entity()
    #     new_entity.surface_form = entity[0]
    #     new_entity.ont_type_spacy = entity[1]

    #     found_entities.append(new_entity)

    return entities


def map_entity_type_to_dbpedia_ontology(entity: Entity):
    """
    Map the spaCy type of entity into the types of DBpedia ontology.
    This method allows to specify the type of entity in terms of DBpedia ontology and create effective SPARQL queries.

    :param entity: entity to map
    :return:
    """
    spacy_to_dbpedia_ontology_mapping = {
        "PERSON": "dbo:Species, dbo:Agent",  # People, including fictional.
        "NORP": "dbo:Agent, dbo:Species",  # Nationalities or religious or political groups.
        "FAC": "dbo:Building, dbo:ArchitecturalStructure, dbo:Infrastructure",  # Buildings, airports, highways, bridges, etc.
        "ORG": "dbo:Agent",  # Companies, agencies, institutions, etc.
        "GPE": "dbo:Place, dbo:Agent, dbo:Building",  # Countries, cities, states.
        "LOC": "dbo:Place",  # Non-GPE locations, mountain ranges, bodies of water.
        "PRODUCT": "dbo:MeanOfTransportation, dbo:Food, dbo:Device",  # Objects, vehicles, foods, etc. (Not services.)
        "EVENT": "dbo:Event",  # Named hurricanes, battles, wars, sports events, etc.
        "WORK_OF_ART": "dbo:Work",  # Titles of books, songs, etc.
        "LAW": "dbo:Work",  # Named documents made into laws.
        "LANGUAGE": "dbo:Language",  # Any named language.
        # DATE:       #  Absolute or relative dates or periods.
        # TIME:       # Times smaller than a day.
        # PERCENT:   #   Percentage, including ”%“.
        # MONEY:     #   Monetary values, including unit.
        # QUANTITY:  #   Measurements, as of weight or distance.
        # ORDINAL:   #   “first”, “second”, etc.
        "CARDINAL": "dbo:TopicalConcept"  # Numerals that do not fall under another type.
    }

    entity.dbpedia_class = spacy_to_dbpedia_ontology_mapping.get(entity.ner_class)

    return entity