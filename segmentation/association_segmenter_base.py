class AssociationSegmenter:
    def __init__(self, association_source_text: str):
        self.association_source_text = association_source_text

    def get_gazette_segments(self):
        """
        Returns a list of GazetteSegment
        """
        territory_to_text_split = self.split_text_by_territory(self.association_source_text)
        gazette_segments = self.create_gazette_segments(territory_to_text_split)
        return gazette_segments

    def split_text_by_territory(self):
        """
        Segment a association text by territory
        and returns a list of text segments
        """
        raise NotImplementedError

    def create_gazette_segments(self, text_split):
        """
        Receives a text split of a association
        and returns a list of GazetteSegment
        """
        raise NotImplementedError
