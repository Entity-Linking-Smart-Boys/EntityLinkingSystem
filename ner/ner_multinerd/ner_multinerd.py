if __name__ == "__main__":
    pass

import spacy
import sys

import datasets
import numpy as np
import torch
from sklearn.model_selection import train_test_split
from transformers import BertTokenizerFast
from transformers import DataCollatorForTokenClassification
from transformers import AutoModelForTokenClassification
from transformers import pipeline
from transformers import TrainingArguments, Trainer
import json
import os

sys.path.append('../.')

from ner.ner_component import NERComponent
from dbp.repository import DBpediaRepository
from data.text import Text
from data.entity import Entity


class NERMultinerd(NERComponent):
    """
    Named entity recognition component
    """

    def __init__(self) -> None:
        pass

    def NER(self, text: Text):
        # NER
        entities = named_entity_recognition_using_multinerd(text.get_plain_text())

        # map entities to dbpedia ontology classes
        for i in range(len(entities)):
            entities[i] = map_entity_type_to_dbpedia_ontology(entities[i])

        # remove entities, that were not mapped into dbpedia ontology classes
        entities = remove_unmapped_entities(entities)

        text.set_entity_mentions(entities)

        return text

    def _map_ner_class_to_dbp(self):
        pass


def remove_unmapped_entities(entities):
    entities = list(filter(lambda entity: entity.dbpedia_class is not None, entities))

    return entities


def use_multinerd_model(input_sentence):

    tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")

    model_fine_tuned = AutoModelForTokenClassification.from_pretrained("ner/ner_multinerd/model")
    nlp = pipeline("ner", model=model_fine_tuned, tokenizer=tokenizer)
    ner_results = nlp(input_sentence)

    return ner_results


def named_entity_recognition_using_multinerd(text):
    """
    Perform Named Entity Recognition (NER) using fine-tuned BERT model

    :param text: text to annotate
    :return: found entities with specific surface form, label, and sentence number.
    """
    ner_results = use_multinerd_model(text)
    # maps ner_results into expected format

    # list of entities to be returned
    entity_list = []
    curr_entity_class = ""
    # string containing a sum of same entity's tokens resulting in a full word
    curr_word = ""
    curr_word_start_idx = -1
    curr_word_last_idx = -1

    for r in ner_results:
        # check if its continuation of entity therefore
        # if previous entity "B-XYX" or "I-XYX" is followed by "I-XYX"
        if "I" + curr_entity_class[1:] == r['entity']:
            # optionally add space between words
            if r['start'] > curr_word_last_idx:
                curr_word += " "
            # remove '##' added by tokenizer
            #TODO: fix if 1 letter token
            if r['word'].startswith("##"):
                curr_word += r['word'][2:]
            else:
                curr_word += r['word']
            curr_word_last_idx = r['end']
        else:
            # return previous entity if one exists
            if curr_entity_class != "":
                entity_list.append(Entity(curr_word, curr_entity_class, (curr_word_start_idx, curr_word_last_idx)))
            # and start building new one
            curr_entity_class = r['entity']
            curr_word = r['word']
            curr_word_start_idx = r['start']
            curr_word_last_idx = r['end']

    # loop skips adding last entity if one exists
    if curr_entity_class != "":
        entity_list.append(Entity(curr_word, curr_entity_class, (curr_word_start_idx, curr_word_last_idx)))

    return entity_list


def map_entity_type_to_dbpedia_ontology(entity: Entity):
    """
    Map the multinerd type of entity into the types of DBpedia ontology.
    This method allows to specify the type of entity in terms of DBpedia ontology and create effective SPARQL queries.

    :param entity: entity to map
    :return:
    """
    spacy_to_dbpedia_ontology_mapping = {
        # "O": 0,
        "B-PER": "Agent",
        "B-LOC": "Place",
        "B-ORG": "Agent",
        "B-ANIM": "Species",
        "B-BIO": "Species",
        "B-CEL": "CelestialBody,Place",
        "B-DIS": "Disease",
        "B-EVE": "Event",
        "B-FOOD": "Food",
        "B-INST": "Instrument,Device",
        "B-MEDIA": "Media",
        "B-PLANT": "Species,Plant,Eukaryote",
        "B-MYTH": "TopicalConcept,Organisation",
        "B-TIME": "Event",
        "B-VEHI": "MeanOfTransportation",
        # "B-SUPER": 31,
        # "B-PHY": 33,
    }

    entity.dbpedia_class = spacy_to_dbpedia_ontology_mapping.get(entity.ner_class)

    return entity
