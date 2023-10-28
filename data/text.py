if __name__ == "__main__":
    pass

from .entity import Entity

class Text:
    """
    Text class for processing
    """
    def __init__(self, text :str) -> None:
        self.text :str = text
        self.entity_mentions = [Entity]

    def set_entity_mentions(self,entities: [Entity]):
        self.entity_mentions = entities

    def get_entity_mentions(self):
        return self.entity_mentions

    def get_plain_text(self):
        return self.text
    
    def get_tagged_text(self):
        tagged_text = self.text

        for entity in self.entity_mentions[::-1]:
            entity: Entity
            tagged_text = tagged_text[:entity.position[0]] + "["+entity.surface_form+"<"+entity.ner_class+">]" + tagged_text[entity.position[1]:]
        return tagged_text