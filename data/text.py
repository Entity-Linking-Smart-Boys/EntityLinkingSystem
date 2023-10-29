if __name__ == "__main__":
    pass

from .entity import Entity

class Text(object):
    """
    Text class for processing
    """
    def __init__(self, text :str) -> None:
        self.text :str = text
        self.entity_mentions: [Entity] = []

    def set_entity_mentions(self,entities: [Entity]):
        self.entity_mentions = entities

    def get_entity_mentions(self):
        return self.entity_mentions

    def get_plain_text(self):
        return self.text
    
    def get_tagged_text(self):
        """Get text with named entity mentions tagged with classes"""
        tagged_text = self.text

        for entity in self.entity_mentions[::-1]:
            entity: Entity
            tagged_text = tagged_text[:entity.position[0]] + f"[{entity.surface_form}<{entity.ner_class}>]" + tagged_text[entity.position[1]:]
        return tagged_text
    
    def get_html_text(self):
        """Get text with named entity mentions linked in html"""
        tagged_text = self.text

        for entity in self.entity_mentions[::-1]:
            entity: Entity
            tagged_text = tagged_text[:entity.position[0]] + entity.to_html() + tagged_text[entity.position[1]:]
        return tagged_text
    
