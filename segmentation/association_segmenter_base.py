class AssociationSegmenter:
    def __init__(self, pdf_path: str, association_source_text: str):
        self.pdf_path = pdf_path
        self.association_source_text = association_source_text

    def get_gazette_segments(self):
        """
        Receives a source_text of a association
        and returns a list of GazetteSegment
        """
        city_segments = self.segment_by_city(self.association_source_text)
        gazette_segments = self.extract_gazette_segment_metadata(city_segments)
        return gazette_segments

    def segment_by_city(self, association_source_text):
        """
        Segment a source_text of a association by city
        and returns a list of text segments
        """
        raise NotImplementedError
    
    def extract_gazette_segment_metadata(self, city_segment_text):
        """
        Receives a text segment of a city
        and returns a dict with the gazette metadata
        """
        raise NotImplementedError