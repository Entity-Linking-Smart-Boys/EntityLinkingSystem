if __name__ == "__main__":
    pass

from .entity import Entity, TestEntity


class Text(object):
    """
    Text class for processing
    """

    def __init__(self, text: str) -> None:
        self.text: str = text
        self.entity_mentions: [Entity] = []

    def set_entity_mentions(self, entities: [Entity]):
        self.entity_mentions = entities

    def clear_entities(self):
        self.entity_mentions = []

    def clear_candidates(self):
        for entity in self.entity_mentions:
            # if hasattr(entity,"candidates"):
            #     entity.candidates.clear() 
            # else:
            entity.candidates = []

    def get_entity_mentions(self):
        return self.entity_mentions

    def get_plain_text(self):
        return self.text

    def get_tagged_text(self):
        """Get text with named entity mentions tagged with classes"""
        tagged_text = self.text

        for entity in self.entity_mentions[::-1]:
            entity: Entity
            tagged_text = tagged_text[
                          :entity.position[0]] + f"[{entity.surface_form}<{entity.ner_class}>]" + tagged_text[
                                                                                                  entity.position[1]:]
        return tagged_text

    def get_html_text(self):
        """Get text with named entity mentions linked in html"""
        tagged_text = self.text

        for entity in self.entity_mentions[::-1]:
            entity: Entity
            tagged_text = tagged_text[:entity.position[0]] + entity.to_html() + tagged_text[entity.position[1]:]
        return tagged_text


class TestText(Text):
    def __init__(self, text: str) -> None:
        self.entity_mentions: list[TestEntity]
        super().__init__(text)


    def get_accurate_count(self):
        """Get count of accurate enitites"""
        accurate_count = 0
        for entity in self.entity_mentions:
            entity : TestEntity
            if entity.accurate():
                accurate_count += 1
        return accurate_count
        
    def get_entities_count(self):
        """Get count of enitites"""
        return len(self.entity_mentions)
    
    def get_ned_accuracy(self):
        """Get accuracy for this text"""
        return self.get_accurate_count()/self.get_entities_count()

    # def get_document_f_score(self):
    #     return 2 * self.get_precision() * self.get_recall() / (self.get_recall() + self.get_precision())

    def get_precision(self):
        pass
    def get_recall(self):
        pass