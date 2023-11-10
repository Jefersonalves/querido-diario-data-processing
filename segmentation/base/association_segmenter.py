import hashlib
from io import BytesIO

class AssociationSegmenter:
    def __init__(self, association_gazette: str):
        self.association_gazette = association_gazette
        self.association_source_text = self.association_gazette["source_text"]

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

    def get_segment(self, territory, segment_text):
        """
        Returns a GazetteSegment
        """
        raise NotImplementedError

    def get_checksum(self, source_text):
        """Calculate the md5 checksum of text
        by creating a file-like object without reading its
        whole content in memory.
        
        Example
        -------
        >>> extractor.get_checksum("A simple text")
            'ef313f200597d0a1749533ba6aeb002e'
        """
        file = BytesIO(source_text.encode(encoding='UTF-8'))

        m = hashlib.md5()
        while True:
            d = file.read(8096)
            if not d:
                break
            m.update(d)
        return m.hexdigest()