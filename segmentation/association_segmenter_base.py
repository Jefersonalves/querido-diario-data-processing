class AssociationSegmenter:
    def __init__(self, association_source_text: str):
        self.association_source_text = association_source_text

    def get_gazette_segments(self):
        """
        Returns a list of GazetteSegment
        """
        city_to_text_split = self.split_text_by_city(self.association_source_text)
        gazette_segments = self.create_gazette_segments(city_to_text_split)
        return gazette_segments

    def split_text_by_city(self):
        """
        Segment a association text by city
        and returns a list of text segments
        """
        raise NotImplementedError

    def create_gazette_segments(self, text_split):
        """
        Receives a text split of a association
        and returns a list of GazetteSegment
        """
        raise NotImplementedError
